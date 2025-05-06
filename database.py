import requests
from firebase_config import auth
from firebase_config import db

def test_fetch_users():
    try:
        users_ref = db.collection('users')
        docs = users_ref.stream()

        for doc in docs:
            data = doc.to_dict()
            print(f"Document ID: {doc.id}")
            print(f"Username: {data.get('username')}")
            print(f"Highscore: {data.get('highscore')}")
            print("-" * 30)

    except Exception as e:
        print("Error fetching users:", e)

if __name__ == "__main__":
    test_fetch_users()


class LoginRegister:
    pass

class HighScores:
    pass

