
import os

try:
    import firebase_admin
    from firebase_admin import credentials, firestore

    cred_path = "backend/firebase_key.json"

    if os.path.exists(cred_path):
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        print("Firebase connected successfully!")
    else:
        print("[WARNING] Firebase key not found. Running without database.")
        db = None

except Exception as e:
    print(f"[ERROR] Firebase setup failed: {e}")
    print("Running in offline mode...")
    db = None
