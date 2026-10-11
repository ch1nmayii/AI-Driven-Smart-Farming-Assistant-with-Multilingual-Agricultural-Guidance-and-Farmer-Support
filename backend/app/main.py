from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api.chat import router as chat_router
from app.api.audio import router as audio_router
from app.api.advisory import router as advisory_router
from app.api.admin import router as admin_router

app = FastAPI(
    title=settings.APP_NAME,
    description="Multilingual Agricultural Advisory & Voice Assistant Platform for Indian Farmers",
    version="1.0.0"
)

# CORS middleware to allow Next.js PWA running on port 3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat_router)
app.include_router(audio_router)
app.include_router(advisory_router)
app.include_router(admin_router)

@app.get("/")
async def root():
    return {
        "status": "online",
        "service": settings.APP_NAME,
        "port": settings.PORT,
        "docs": f"http://localhost:{settings.PORT}/docs",
        "languages_supported": ["Hindi (hi)", "Kannada (kn)", "English (en)"]
    }

@app.get("/health")
@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "service": "agri-backend", "port": settings.PORT}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=True)
