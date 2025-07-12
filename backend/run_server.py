import uvicorn

if __name__ == "__main__":
    print("🚀 Starting SkillSwap API Server...")
    print("✅ Firebase connected and ready!")
    print("📡 Server will be available at: http://127.0.0.1:8000")
    print("📚 API docs will be available at: http://127.0.0.1:8000/docs")
    
    uvicorn.run(
        "main:app", 
        host="127.0.0.1", 
        port=8000, 
        reload=True
    )
