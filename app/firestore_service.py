import firebase_admin
from firebase_admin import credentials, firestore

credential = credentials.ApplicationDefault()

firebase_admin.initialize_app(credential)

db = firestore.client()

def get_users():
    return db.collection('users').get()

def get_user(user_id):
    return db.collection('users').document(user_id).get()

def get_todos(user_id):
    return db.collection('users').document(user_id).collection('todos').get()

def create_user(user_data):
    user_ref = db.collection('users').document(user_data.username)
    user_ref.set({
        'password': user_data.password
    })
    
def create_todo(user_id, description):
    todo_collection_ref = db.collection('users').document(user_id).collection('todos')
    
    todo_collection_ref.add({
        'description': description,
        'done': False
    })
    
def delete_todo(user_id, todo_id):
    todo_collection_ref = db.collection('users').document(user_id).collection('todos')
    todo_ref = todo_collection_ref.document(todo_id)
    todo_ref.delete()
    
def todo_toggle(user_id, todo_id):
    todo_collection_ref = db.collection('users').document(user_id).collection('todos')
    todo_ref = todo_collection_ref.document(todo_id)
    state = todo_ref.get().to_dict()['done']
    if state:
        todo_ref.update({
            'done': False
        })
    else:
        todo_ref.update({
            'done': True
        })
    
def update_todo(user_id, todo_id, description):
    todo_collection_ref = db.collection('users').document(user_id).collection('todos')
    todo_ref = todo_collection_ref.document(todo_id)
    todo_ref.update({
        'description': description
    })