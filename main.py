from datetime import datetime
from random import randint
from secrets import token_hex
from typing import Optional


from fastapi import FastAPI, status, HTTPException, Body, Path
from fastapi.responses import JSONResponse

from models.user_model import ResponseModel, UserData, SupportData, UserCreateRequest, \
    UserCreateResponse, TokenResponse, UpdateUserRequest, UpdatedUserResponse
from users_data import mock_users

app = FastAPI()


@app.get("/api/users/{user_id}", response_model=ResponseModel)
def get_user(user_id: int):
    users_db = [UserData(
        id=2,
        email="janet.weaver@reqres.in",
        first_name="Janet",
        last_name="Weaver",
        avatar="https://reqres.in/img/faces/2-image.jpg"
    )]

    support_info = SupportData(
        url="https://contentcaddy.io?utm_source=reqres&utm_medium=json&utm_campaign=referral",
        text="Tired of writing endless social media content? Let Content Caddy generate it for you."
    )
    user_data = next((user for user in users_db if user.id == user_id), None)

    if not user_data:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={})

    return ResponseModel(data=user_data, support=support_info)


@app.post("/api/users", response_model=UserCreateResponse, status_code=status.HTTP_201_CREATED)
def post_user(user_in: UserCreateRequest):
    new_id = str(randint(1000, 9999))

    user_out = UserCreateResponse(
        id=new_id,
        name=user_in.name,
        job=user_in.job,
        created_at=datetime.now().isoformat(timespec='milliseconds') + 'Z'
    )

    return user_out.model_dump(by_alias=True)


@app.delete("/api/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    return {}


@app.exception_handler(HTTPException)
def custom_http_exception_handler(request, exc):
    if exc.status_code == 400:
        return JSONResponse({"error": "Missing password"}, status_code=exc.status_code)
    return JSONResponse({"detail": exc.detail}, status_code=exc.status_code)


@app.post("/api/login")
def login(email: str = Body(...), password: Optional[str] = Body(None)):
    if not password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")

    random_token = token_hex(16)
    return TokenResponse(token=random_token)


@app.patch("/api/users/{user_id}")
async def patch_user(user_id: str = Path(..., title="The ID of the user to get"), user_update: UpdateUserRequest = Body(...)):
    user = next((user for user in mock_users if user["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    update_data = user_update.dict(exclude_unset=True)

    for field, value in update_data.items():
        user[field] = value

    user["updatedAt"] = datetime.utcnow().isoformat() + "Z"

    return UpdatedUserResponse(name=user["name"], job=user["job"], updatedAt=user["updatedAt"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
