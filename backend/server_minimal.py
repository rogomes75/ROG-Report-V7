from fastapi import FastAPI
from fastapi.responses import JSONResponse
import os

# Create the app
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "ROG Pool Service is running!", "status": "OK"}

@app.get("/api/")
async def api_root():
    return {"message": "ROG Pool Service API", "status": "healthy"}

@app.get("/api/health")
async def health():
    return {"status": "healthy", "service": "rog-pool-service"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)