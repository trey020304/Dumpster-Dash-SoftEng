import pyrebase
import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore
from firebase_admin.exceptions import FirebaseError
import json

# Load environment variables
load_dotenv()

# Pyrebase config (for auth, storage, etc.)
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

# Initialize Firebase Firestore and Pyrebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

class LoginRegister:
    def register(self):
        email = input("Enter email: ")
        password = input("Enter password: ")
        confirm_password = input("Confirm password: ")
        username = input("Enter username: ")

        if password != confirm_password:
            print("Passwords do not match.")
            return

        try:
            user = auth.create_user_with_email_and_password(email, password)
            uid = user['localId']  # Firebase Auth UID

            # Add user to Firestore 'users' collection
            db.collection('users').document(uid).set({
                'email': email,
                'username': username,
                'highscore': 0
            })

            print("Successfully Registered and stored user info in Firestore.")
        except Exception as e:
            error_str = str(e)
            if "EMAIL_EXISTS" in error_str:
                print("This email is already registered.")
            else:
                print(f"Registration failed: {error_str}")

    def login(self):
        email = input("Enter email: ")
        password = input("Enter password: ")

        try:
            user = auth.sign_in_with_email_and_password(email, password)
            uid = user['localId']
            print("Successfully logged in.")
            return uid
        except Exception as e:
            try:
                error_json = json.loads(e.args[1])  # e.args[1] contains the JSON error
                error_message = error_json['error']['message']

                if error_message == "EMAIL_NOT_FOUND":
                    print("Error: Email not found.")
                elif error_message == "INVALID_PASSWORD":
                    print("Error: Incorrect password.")
                elif error_message == "USER_DISABLED":
                    print("Error: This user account has been disabled.")
                else:
                    print(f"Login failed: {error_message}")
            except:
                # Fallback if parsing fails
                print("An unknown error occurred during login.")


class HighScores:
    pass


if __name__ == "__main__":
    loginregister = LoginRegister()
    loginregister.register()
