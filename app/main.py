from fastapi import FastAPI
from app.config.database import engine, Base
from app.routes.items import router as items_router
import uvicorn

app = FastAPI(title="FastAPI CRUD App")

# Create database tables
Base.metadata.create_all(bind=engine)

app.include_router(items_router)

# Sample Health Check Endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "FastAPI app is running!"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)