from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    broadcasts = db.relationship('Broadcast', backref='creator', lazy=True, foreign_keys='Broadcast.creator_id')
    notifications = db.relationship('Notification', backref='user', lazy=True)
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if password matches hash"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Broadcast(db.Model):
    __tablename__ = 'broadcasts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(20), default='draft')  # draft, published, sent
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    sent_at = db.Column(db.DateTime)
    
    # Relationships
    notifications = db.relationship('Notification', backref='broadcast', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self, include_notifications=False):
        data = {
            'id': self.id,
            'title': self.title,
            'message': self.message,
            'creator_id': self.creator_id,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'sent_at': self.sent_at.isoformat() if self.sent_at else None
        }
        if include_notifications:
            data['notifications'] = [n.to_dict() for n in self.notifications]
        return data

class Notification(db.Model):
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    broadcast_id = db.Column(db.Integer, db.ForeignKey('broadcasts.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, sent, failed, delivered
    fcm_token = db.Column(db.Text)  # Firebase Cloud Messaging token
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    sent_at = db.Column(db.DateTime)
    error_message = db.Column(db.Text)
    
    def to_dict(self):
        return {
            'id': self.id,
            'broadcast_id': self.broadcast_id,
            'user_id': self.user_id,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'sent_at': self.sent_at.isoformat() if self.sent_at else None,
            'error_message': self.error_message
        }
