from fastapi import FastAPI
from backend.routers import users, swaps

app = FastAPI()

# Attach route files
app.include_router(users.router)
app.include_router(swaps.router)

@app.get("/")
def read_root():
    return {"message": "Skill Swap API is running!"}
