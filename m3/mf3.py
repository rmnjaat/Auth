from fastapi import APIRouter

router = APIRouter(
    prefix="/m3",
    tags=["m3"]
)

@router.get("/")
def root():
    return {"message": "Hello World from m3 which is session based"}