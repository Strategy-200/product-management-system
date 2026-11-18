from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from database.database import SessionLocal
from models.user import User as UserModel
from schemas.user import User, UserResponse, MessageResponse, UserRegister, UserLogin
from utils.security import (
    hash_password,
    verify_password,
    create_access_token,
    verify_access_token
)
from models.revoked_token import RevokedToken
from fastapi.middleware.cors import CORSMiddleware
from routes.products import router as product_router

app = FastAPI()
app.include_router(product_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5174",
        "http://127.0.0.1:5174"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
security = HTTPBearer()

# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Authentication Dependency
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials

    # Check whether token is revoked
    revoked_token = db.query(RevokedToken).filter(
        RevokedToken.token == token
    ).first()

    if revoked_token is not None:
        raise HTTPException(
            status_code=401,
            detail="Token has been revoked. Please login again."
        )

    # Verify JWT
    payload = verify_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    user_id = payload.get("sub")

    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid token payload"
        )

    return user_id

# REGISTER USER
@app.post("/register", response_model=UserResponse)
def register_user(user: UserRegister, db: Session = Depends(get_db)):

    existing_user = db.query(UserModel).filter(
        UserModel.email == user.email
    ).first()

    if existing_user is not None:
        raise HTTPException(
            status_code=409,
            detail="Email already registered"
        )

    hashed_password = hash_password(user.password)

    new_user = UserModel(
        name=user.name,
        email=user.email,
        age=user.age,
        hashed_password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

# LOGIN USER
@app.post("/login")
def login_user(user: UserLogin, db: Session = Depends(get_db)):

    existing_user = db.query(UserModel).filter(
        UserModel.email == user.email
    ).first()

    if existing_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not existing_user.hashed_password or not verify_password(
        user.password,
        existing_user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        data={
            "sub": str(existing_user.id),
            "email": existing_user.email
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

# UPDATE PROFILE
@app.put("/profile", response_model=UserResponse)
def update_profile(
    user: User,
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    existing_user = db.query(UserModel).filter(
        UserModel.id == int(user_id)
    ).first()

    if existing_user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    duplicate_email = db.query(UserModel).filter(
        UserModel.email == user.email,
        UserModel.id != int(user_id)
    ).first()

    if duplicate_email is not None:
        raise HTTPException(
            status_code=409,
            detail="Email already registered"
        )

    existing_user.name = user.name
    existing_user.email = user.email
    existing_user.age = user.age

    db.commit()
    db.refresh(existing_user)

    return existing_user

# DELETE ACCOUNT
@app.delete("/account", response_model=MessageResponse)
def delete_account(
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user = db.query(UserModel).filter(
        UserModel.id == int(user_id)
    ).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    db.delete(user)
    db.commit()

    return {
        "message": "Account deleted successfully"
    }

# LOGOUT USER
@app.post("/logout", response_model=MessageResponse)
def logout_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials

    # Check whether token is already revoked
    existing_token = db.query(RevokedToken).filter(
        RevokedToken.token == token
    ).first()

    if existing_token is None:
        revoked_token = RevokedToken(token=token)
        db.add(revoked_token)
        db.commit()

    return {
        "message": "Logout successful. Token revoked."
    }

# GET ALL USERS
@app.get("/users", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):

    users = db.query(UserModel).all()

    return users


# GET USER BY ID
@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):

    user = db.query(UserModel).filter(
        UserModel.id == user_id
    ).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user

# GET PROFILE
@app.get("/profile", response_model=UserResponse)
def get_profile(
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    user = db.query(UserModel).filter(
        UserModel.id == int(user_id)
    ).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user

# UPDATE USER
@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user: User,
    db: Session = Depends(get_db)
):

    duplicate_email = db.query(UserModel).filter(
        UserModel.email == user.email,
        UserModel.id != user_id
    ).first()

    if duplicate_email is not None:
        raise HTTPException(
            status_code=409,
            detail="Email already registered"
        )

    existing_user = db.query(UserModel).filter(
        UserModel.id == user_id
    ).first()

    if existing_user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    existing_user.name = user.name
    existing_user.email = user.email
    existing_user.age = user.age

    db.commit()
    db.refresh(existing_user)

    return existing_user

# DELETE USER
@app.delete("/users/{user_id}", response_model=MessageResponse)
def delete_user(user_id: int, db: Session = Depends(get_db)):

    user = db.query(UserModel).filter(
        UserModel.id == user_id
    ).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    db.delete(user)
    db.commit()

    return {"message": "User deleted successfully"}
