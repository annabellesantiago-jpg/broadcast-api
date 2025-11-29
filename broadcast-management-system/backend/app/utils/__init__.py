import firebase_admin
from firebase_admin import credentials, messaging
import os
from datetime import datetime

# Initialize Firebase (only if credentials file exists)
firebase_creds_path = os.getenv('FIREBASE_CREDENTIALS_PATH', './firebase-service-account.json')
firebase_initialized = False

try:
    if os.path.exists(firebase_creds_path):
        cred = credentials.Certificate(firebase_creds_path)
        firebase_admin.initialize_app(cred)
        firebase_initialized = True
except Exception as e:
    print(f"Warning: Firebase not initialized. Using mock notifications. Error: {e}")

def send_push_notification(fcm_token, title, message, data=None):
    """
    Send push notification via Firebase Cloud Messaging
    
    Args:
        fcm_token: Firebase Cloud Messaging token
        title: Notification title
        message: Notification message
        data: Additional data to send with notification
    
    Returns:
        dict with status and message_id or error
    """
    if not firebase_initialized:
        return {
            'status': 'mock',
            'message': f'Mock notification sent to {fcm_token}',
            'title': title,
            'message': message
        }
    
    try:
        notification = messaging.Notification(
            title=title,
            body=message
        )
        
        msg = messaging.Message(
            notification=notification,
            data=data or {},
            token=fcm_token
        )
        
        response = messaging.send(msg)
        return {
            'status': 'success',
            'message_id': response
        }
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e)
        }

def send_multicast_notification(fcm_tokens, title, message, data=None):
    """
    Send push notification to multiple devices
    
    Args:
        fcm_tokens: List of Firebase Cloud Messaging tokens
        title: Notification title
        message: Notification message
        data: Additional data to send with notification
    
    Returns:
        dict with results
    """
    if not firebase_initialized:
        return {
            'status': 'mock',
            'success_count': len(fcm_tokens),
            'failure_count': 0,
            'message': f'Mock broadcast notification sent to {len(fcm_tokens)} devices'
        }
    
    try:
        notification = messaging.Notification(
            title=title,
            body=message
        )
        
        msg = messaging.MulticastMessage(
            notification=notification,
            data=data or {},
            tokens=fcm_tokens
        )
        
        response = messaging.send_multicast(msg)
        return {
            'status': 'success',
            'success_count': response.success_count,
            'failure_count': response.failure_count
        }
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e)
        }
