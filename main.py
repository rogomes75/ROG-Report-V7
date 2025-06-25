from fastapi import FastAPI
import os

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "ROG Pool Service is running!", "status": "OK"}

@app.get("/api/")
def api_root():
    return {"message": "ROG Pool Service API", "status": "healthy"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "rog-pool-service"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)