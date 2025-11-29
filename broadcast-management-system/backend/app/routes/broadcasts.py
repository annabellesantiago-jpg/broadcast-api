from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from app import db
from app.models import User, Broadcast, Notification
from app.utils import send_push_notification, send_multicast_notification

broadcasts_bp = Blueprint('broadcasts', __name__, url_prefix='/api/broadcasts')

@broadcasts_bp.route('', methods=['GET'])
@jwt_required()
def list_broadcasts():
    """List all broadcasts created by the current user"""
    user_id = get_jwt_identity()
    
    try:
        # Get pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        status = request.args.get('status', None)
        
        # Build query
        query = Broadcast.query.filter_by(creator_id=user_id)
        
        if status:
            query = query.filter_by(status=status)
        
        # Paginate results
        paginated = query.order_by(Broadcast.created_at.desc()).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        return jsonify({
            'broadcasts': [b.to_dict() for b in paginated.items],
            'total': paginated.total,
            'pages': paginated.pages,
            'current_page': page
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@broadcasts_bp.route('/<int:broadcast_id>', methods=['GET'])
@jwt_required()
def get_broadcast(broadcast_id):
    """Get a specific broadcast"""
    user_id = get_jwt_identity()
    
    try:
        broadcast = Broadcast.query.filter_by(
            id=broadcast_id,
            creator_id=user_id
        ).first()
        
        if not broadcast:
            return jsonify({'error': 'Broadcast not found'}), 404
        
        return jsonify(broadcast.to_dict(include_notifications=True)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@broadcasts_bp.route('', methods=['POST'])
@jwt_required()
def create_broadcast():
    """Create a new broadcast"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # Validate input
    if not data or not data.get('title') or not data.get('message'):
        return jsonify({'error': 'Missing required fields: title, message'}), 400
    
    try:
        # Create broadcast
        broadcast = Broadcast(
            title=data['title'],
            message=data['message'],
            creator_id=user_id,
            status='draft'
        )
        
        db.session.add(broadcast)
        db.session.commit()
        
        return jsonify({
            'message': 'Broadcast created successfully',
            'broadcast': broadcast.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@broadcasts_bp.route('/<int:broadcast_id>', methods=['PUT'])
@jwt_required()
def update_broadcast(broadcast_id):
    """Update a broadcast (only draft status)"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    try:
        broadcast = Broadcast.query.filter_by(
            id=broadcast_id,
            creator_id=user_id
        ).first()
        
        if not broadcast:
            return jsonify({'error': 'Broadcast not found'}), 404
        
        if broadcast.status != 'draft':
            return jsonify({'error': 'Can only update draft broadcasts'}), 400
        
        # Update fields
        if 'title' in data:
            broadcast.title = data['title']
        if 'message' in data:
            broadcast.message = data['message']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Broadcast updated successfully',
            'broadcast': broadcast.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@broadcasts_bp.route('/<int:broadcast_id>', methods=['DELETE'])
@jwt_required()
def delete_broadcast(broadcast_id):
    """Delete a broadcast (only draft status)"""
    user_id = get_jwt_identity()
    
    try:
        broadcast = Broadcast.query.filter_by(
            id=broadcast_id,
            creator_id=user_id
        ).first()
        
        if not broadcast:
            return jsonify({'error': 'Broadcast not found'}), 404
        
        if broadcast.status != 'draft':
            return jsonify({'error': 'Can only delete draft broadcasts'}), 400
        
        db.session.delete(broadcast)
        db.session.commit()
        
        return jsonify({'message': 'Broadcast deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@broadcasts_bp.route('/<int:broadcast_id>/send', methods=['POST'])
@jwt_required()
def send_broadcast(broadcast_id):
    """Send a broadcast (trigger push notifications)"""
    user_id = get_jwt_identity()
    data = request.get_json() or {}
    
    try:
        broadcast = Broadcast.query.filter_by(
            id=broadcast_id,
            creator_id=user_id
        ).first()
        
        if not broadcast:
            return jsonify({'error': 'Broadcast not found'}), 404
        
        if broadcast.status == 'sent':
            return jsonify({'error': 'Broadcast already sent'}), 400
        
        # Get all users to send notifications to
        target_users = data.get('target_users', [])
        if not target_users:
            # Send to all users except creator
            all_users = User.query.filter(User.id != user_id).all()
            target_users = [u.id for u in all_users]
        
        if not target_users:
            return jsonify({'error': 'No target users specified'}), 400
        
        # Create notifications for each target user
        fcm_tokens = []
        results = []
        
        for target_user_id in target_users:
            user = User.query.get(target_user_id)
            if user:
                notification = Notification(
                    broadcast_id=broadcast_id,
                    user_id=target_user_id,
                    status='pending'
                )
                db.session.add(notification)
                results.append({
                    'user_id': target_user_id,
                    'username': user.username,
                    'status': 'pending'
                })
        
        # Update broadcast status
        broadcast.status = 'sent'
        broadcast.sent_at = datetime.utcnow()
        
        db.session.commit()
        
        # Send mock notifications (in production, would send actual push notifications)
        send_result = {
            'status': 'success',
            'message': f'Broadcast sent to {len(target_users)} user(s)',
            'sent_count': len(target_users)
        }
        
        return jsonify({
            'message': 'Broadcast sent successfully',
            'broadcast': broadcast.to_dict(),
            'notifications': results,
            'send_result': send_result
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@broadcasts_bp.route('/notifications/all', methods=['GET'])
@jwt_required()
def get_user_notifications():
    """Get all notifications for current user"""
    user_id = get_jwt_identity()
    
    try:
        # Get pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Get notifications
        paginated = Notification.query.filter_by(user_id=user_id).order_by(
            Notification.created_at.desc()
        ).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        notifications = []
        for notif in paginated.items:
            notif_data = notif.to_dict()
            # Add broadcast details
            broadcast = Broadcast.query.get(notif.broadcast_id)
            if broadcast:
                notif_data['broadcast'] = broadcast.to_dict()
            notifications.append(notif_data)
        
        return jsonify({
            'notifications': notifications,
            'total': paginated.total,
            'pages': paginated.pages,
            'current_page': page
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
