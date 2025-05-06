import pyrebase
import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore
from firebase_admin.exceptions import FirebaseError

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
}

try:
    # Initialize Firebase Admin
    cred = credentials.Certificate(".venv/serviceAccountKey.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    
    # Test document data
    test_data = {
        "name": "Test User",
        "email": "test@example.com",
        "timestamp": firestore.SERVER_TIMESTAMP
    }
    
    # Add a document to the 'users' collection
    doc_ref = db.collection('users').add(test_data)
    
    print(f"Successfully added document with ID: {doc_ref[1].id}")
    print("Connection to Firestore is working correctly!")

except FileNotFoundError:
    print("Error: serviceAccountKey.json file not found. Please ensure it's in the correct directory.")
except FirebaseError as e:
    print(f"Firebase Error: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")