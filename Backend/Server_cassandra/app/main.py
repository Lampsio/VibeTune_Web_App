from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import router

app = FastAPI()

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rejestracja endpointów
app.include_router(router, prefix="/api", tags=["Subtitles"])

@app.get("/")
def root():
    return {"message": "Welcome to the FastAPI Cassandra API"}
