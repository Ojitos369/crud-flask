from flask_login import UserMixin

from .firestore_service import get_user

class UserData:
    def __init__(self, username, password):
        self.username = username
        self.password = password

class User(UserMixin):
    
    def __init__(self, UserData):
        """
        UserData: UserData object
        """
        
        self.id = UserData.username
        self.password = UserData.password
        
    @staticmethod
    def query(user_id):
        user_doc = get_user(user_id)
        user_data = UserData(
            username = user_doc.id,
            password = user_doc.to_dict()['password']
        )
        
        return User(user_data)