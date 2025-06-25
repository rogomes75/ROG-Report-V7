from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Simple MongoDB connection
mongo_url = os.environ.get('DATABASE_URL', 'mongodb://localhost:27017')
db_name = os.environ.get('DB_NAME', 'pool_maintenance_db')

try:
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    logger.info("MongoDB connection initialized")
except Exception as e:
    logger.error(f"MongoDB connection error: {e}")
    client = None
    db = None

# Create the main app
app = FastAPI(title="ROG Pool Service API")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

@api_router.get("/")
async def root():
    return {"message": "ROG Pool Service API is running", "status": "OK"}

@api_router.get("/health")
async def health_check():
    db_status = "connected" if db else "disconnected"
    return {"status": "healthy", "database": db_status}

# Include the router
app.include_router(api_router)

# Mount static files for production
static_dir = Path(__file__).parent.parent / "frontend" / "build"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=static_dir / "static"), name="static")
    
    @app.get("/{catchall:path}")
    async def serve_spa(catchall: str):
        # Serve API routes normally
        if catchall.startswith("api/"):
            return {"error": "API endpoint not found"}
        
        # For all other routes, serve the React app
        index_file = static_dir / "index.html"
        if index_file.exists():
            return FileResponse(index_file)
        else:
            return {"error": "Frontend not available"}
    
    @app.get("/")
    async def serve_root():
        index_file = static_dir / "index.html"
        if index_file.exists():
            return FileResponse(index_file)
        else:
            return {"message": "ROG Pool Service API", "status": "Frontend not available"}

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)