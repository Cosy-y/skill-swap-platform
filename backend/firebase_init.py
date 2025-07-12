
import os
import logging

try:
    import firebase_admin
    from firebase_admin import credentials, firestore, auth

    # Path to firebase.json (should be in the same directory as this file)
    cred_path = "firebase.json"

    if os.path.exists(cred_path):
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        print("✅ Firebase connected successfully!")
        print(f"📂 Using credentials from: {cred_path}")
    else:
        print(f"[WARNING] Firebase credentials not found at {cred_path}")
        print("Running without database connection.")
        db = None

except ImportError as e:
    print(f"[ERROR] Firebase dependencies not installed: {e}")
    print("Install with: pip install firebase-admin")
    db = None

except Exception as e:
    print(f"[ERROR] Firebase setup failed: {e}")
    print("Running in offline mode...")
    db = None
