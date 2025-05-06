import pyrebase
import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore

def configure():
    load_dotenv()

# Load environment variables
load_dotenv()

# Pyrebase config (for auth, storage, etc.)
firebaseConfig = {
    "apiKey": os.getenv('api_key'),
    "authDomain": os.getenv('auth_domain'),
    "projectId": os.getenv('project_id'),
    "storageBucket": os.getenv('storage_bucket'),
    "messagingSenderId": os.getenv('messaging_sender_id'),
    "appId": os.getenv('app_id'),
    "measurementId": os.getenv('measurement_id'),
    "databaseURL": os.getenv('database_url')  # Optional if you use Realtime DB
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

# Initialize Firebase Admin SDK (for Firestore access)
if not firebase_admin._apps:
    cred_path = os.getenv('firebase_admin_sdk_path')  # Path to your service account key JSON
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)

db = firestore.client()
