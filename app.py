from fastapi import FastAPI
import uvicorn
import os

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Railway working!", "status": "success", "method": "direct_uvicorn"}

@app.get("/health")
def health():
    return {"status": "healthy", "port": os.environ.get("PORT", "8000")}

# Start server directly
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)

# Also try starting automatically when imported
try:
    port = int(os.environ.get("PORT", 8000))
    if port != 8000:  # Only auto-start in production
        print(f"Auto-starting on port {port}")
        uvicorn.run(app, host="0.0.0.0", port=port)
except Exception as e:
    print(f"Auto-start failed: {e}")
    pass