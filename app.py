from fastapi import FastAPI
import uvicorn
import os

app = FastAPI()

# MongoDB will be added here
mongodb_available = False

@app.get("/")
def root():
    return {
        "message": "ROG Pool Service v2.0 on Render!", 
        "status": "success", 
        "platform": "render",
        "mongodb": "ready_to_add" if not mongodb_available else "connected"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy", 
        "port": os.environ.get("PORT", "8000"),
        "platform": "render",
        "mongodb": mongodb_available
    }

@app.get("/api/")
def api_root():
    return {
        "message": "ROG Pool Service API",
        "version": "2.0",
        "platform": "render", 
        "endpoints": ["/", "/health", "/api/"]
    }

# Start server directly
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting ROG Pool Service on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)

# Auto-start in production
try:
    port = int(os.environ.get("PORT", 8000))
    if port != 8000:  # Production environment
        print(f"Auto-starting on Render port {port}")
        uvicorn.run(app, host="0.0.0.0", port=port)
except:
    pass