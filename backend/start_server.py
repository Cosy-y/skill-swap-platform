#!/usr/bin/env python3
"""
Startup script for the SkillSwap backend
This will test Firebase connection and start the FastAPI server
"""

import os
import sys

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_firebase_connection():
    """Test Firebase connection before starting the server"""
    print("🔥 Testing Firebase connection...")
    try:
        from firebase_init import db
        if db is not None:
            print("✅ Firebase connection successful!")
            
            # Test basic database operations
            test_collection = db.collection("test")
            test_doc = test_collection.document("connection_test")
            test_doc.set({"timestamp": "connection_test", "status": "ok"})
            print("✅ Database write test successful!")
            
            # Clean up test document
            test_doc.delete()
            print("✅ Database cleanup successful!")
            
            return True
        else:
            print("❌ Firebase connection failed!")
            return False
    except Exception as e:
        print(f"❌ Firebase test failed: {e}")
        return False

def start_server():
    """Start the FastAPI development server"""
    print("🚀 Starting SkillSwap API server...")
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    print("🎯 SkillSwap Backend Starting...")
    print("=" * 50)
    
    # Test Firebase connection
    if test_firebase_connection():
        print("=" * 50)
        print("✅ All systems ready!")
        print("📡 API will be available at: http://localhost:8000")
        print("📚 API docs will be available at: http://localhost:8000/docs")
        print("=" * 50)
        
        # Start the server
        start_server()
    else:
        print("=" * 50)
        print("❌ Firebase connection failed. Please check your configuration.")
        print("💡 Make sure firebase.json is in the backend directory")
        print("🔧 You can still start the server, but database features won't work")
        
        # Ask if user wants to continue anyway
        response = input("\nDo you want to start the server anyway? (y/N): ")
        if response.lower() in ['y', 'yes']:
            print("🚀 Starting server without database...")
            start_server()
        else:
            print("👋 Exiting. Fix Firebase connection and try again.")
            sys.exit(1)
