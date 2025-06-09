from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import auth, mood, thoughts, feedback, reports, testing, interpretations, users

app = FastAPI(
    title="Psychological Service API",
    description="API for psychological self-monitoring and assessment service",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(mood.router)
app.include_router(thoughts.router)
app.include_router(testing.router)
app.include_router(feedback.router)
app.include_router(reports.router)
app.include_router(interpretations.router)
app.include_router(users.router)

@app.get("/")
async def root():
    return {
        "message": "Welcome to Psychological Service API",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 