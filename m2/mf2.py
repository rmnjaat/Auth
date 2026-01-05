from fastapi import APIRouter  # Use APIRouter, NOT FastAPI!

router = APIRouter(
    prefix="/m2",     # All routes start with /m2
    tags=["m2"]       # Groups in docs
)

# Use @router.get, NOT @app.get!
@router.get("/")
def root():
    return {"message": "Hello World from m2"}