import firebase_admin
from firebase_admin import credentials, firestore

credential = credentials.ApplicationDefault()

firebase_admin.initialize_app(credential)

db = firestore.client()

def get_users():
    return db.collection('users').get()

def get_todos(user_id):
    return db.collection('users').document(user_id).collection('todos').get()