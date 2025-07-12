from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import users, swaps, reviews, admin, auth

# just making a basic API for my skill swap idea
app = FastAPI()

# need this so my html pages can talk to the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # probably should fix this later but works for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# adding all my route files
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(swaps.router)
app.include_router(reviews.router)
app.include_router(admin.router)

@app.get("/")
def read_root():
    # basic home endpoint
    return {"message": "Hey! My skill swap app is working!"}

@app.get("/health")
def health_check():
    # simple health check endpoint
    return {"status": "healthy", "service": "skill-swap-api"}
