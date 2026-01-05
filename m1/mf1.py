from fastapi import APIRouter  # Use APIRouter, NOT FastAPI!

router = APIRouter(
    prefix="/m1",     # All routes start with /m1
    tags=["m1"]       # Groups in docs
)


@router.get("/")
def root():
    return {"message": "Hello World from m1"}


