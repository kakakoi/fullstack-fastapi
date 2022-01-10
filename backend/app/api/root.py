from fastapi import APIRouter

root_router = APIRouter()


@root_router.get("/")
async def root():
    return {"message": root_router.state_message}
