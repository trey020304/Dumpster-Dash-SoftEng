import pyrebase
import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore
import json
import re


# Load environment variables
load_dotenv()

firebaseConfig = {
    "apiKey": os.getenv('api_key'),
    "authDomain": os.getenv('auth_domain'),
    "databaseURL": os.getenv('databaseURL'),
    "projectId": os.getenv('project_id'),
    "storageBucket": os.getenv('storage_bucket'),
    "messagingSenderId": os.getenv('messaging_sender_id'),
    "appId": os.getenv('app_id'),
    "measurementId": os.getenv('measurement_id'),
}

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

SESSION_FILE = "session.json"

# ------------------ Session Management ------------------ #

def save_session(user):
        with open(SESSION_FILE, "w") as f:
            json.dump({
                "idToken": user['idToken'],
                "refreshToken": user['refreshToken'],
                "localId": user['localId']
            }, f)

def load_session():
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, "r") as f:
            session = json.load(f)
        try:
            user = auth.refresh(session['refreshToken'])  # Refresh token
            session['idToken'] = user['idToken']  # Update session with new idToken
            save_session(session)
            print("Auto-login successful. Logged in: " + session['localId'])
            return session['localId']
        except:
            print("Session expired or invalid.")
    return None
    

# ------------------ Authorization ------------------ #
class Authorization:

    
    def register(email, password, confirm_password, username):
        # Email format validation
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            print("Invalid email format.")
            return ''

        if password != confirm_password:
            print("Passwords do not match.")
            return ''

        try:
            user = auth.create_user_with_email_and_password(email, password)
            uid = user['localId']
            db.collection('users').document(uid).set({
                'email': email,
                'username': username,
                'highscore': 0
            })
            return 'success'
        except Exception as e:
            error_str = str(e)
            if "EMAIL_EXISTS" in error_str:
                return 'already_registered'
            else:
                return 'registration_failed'


    def login(email, password):
        if not email or not password:
            return 'invalid_credentials'
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            uid = user['localId']
            save_session(user)
            print(uid + ' is the user.')
            return uid
        except Exception as e:
            try:
                error_json = json.loads(e.args[1])
                error_message = error_json['error']['message']
                if error_message in ["EMAIL_NOT_FOUND", "INVALID_PASSWORD", "INVALID_EMAIL"]:
                    return 'invalid_credentials'
            except:
                return 'unknown_error'
            return 'unknown_error'
    
    def logout():
        if os.path.exists(SESSION_FILE):
            os.remove(SESSION_FILE)
        print("Logged out successfully.")

    def reset_password(email):
        try:
            auth.send_password_reset_email(email)
            return 'reset_email_sent'
        except:
            return 'reset_failed'

# ------------------ High Score Handling ------------------ #
class HighScoreDB:
    @staticmethod
    def updateCurrentPlayerHighScore(uid, score):
        db.collection('users').document(uid).set({
            'highscore': score,
            'highscore_timestamp': firestore.SERVER_TIMESTAMP
        }, merge=True)
        
    @staticmethod
    def getCurrentPlayerHighScore(uid):
        try:
            doc = db.collection('users').document(uid).get()
            if doc.exists:
                data = doc.to_dict()
                return data.get('highscore', 0)
            else:
                print("User document not found.")
                return None
        except Exception as e:
            print(f"Failed to get highscore: {e}")
            return None

# ------------------ Leaderboard ------------------ #
class LeaderBoardDB:
    @staticmethod
    def get_leaderboard_from_DB():
        try:
            users_ref = db.collection('users')
            top_users = users_ref.order_by('highscore', direction=firestore.Query.DESCENDING).limit(10).stream()

            leaderboard = []
            for user in top_users:
                data = user.to_dict()
                leaderboard.append({
                    'username': data.get('username', 'Unknown'),
                    'highscore': data.get('highscore', 0),
                })

            return leaderboard
        except Exception as e:
            print(f"Error fetching leaderboard: {e}")
            return []
        