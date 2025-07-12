
import os

try:
    import firebase_admin
    from firebase_admin import credentials, firestore

    cred_path = "backend/firebase_key.json"

    if os.path.exists(cred_path):
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
        db = firestore.client()
    else:
        print("[WARNING] Firebase key not found. Running in mock mode.")
        db = None

except Exception as e:
    print(f"[ERROR] Firebase failed to initialize: {e}")
    db = None
