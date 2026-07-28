from fastapi import APIRouter,Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.database import get_db
from sqlalchemy.orm import Session

from fastapi.security import OAuth2PasswordRequestForm

from app.auth.auth import verify_access_token,create_access_token,hash_password,verify_password
from app.models.model import User,Notes
from app.schemas.schemes import UserCreate,UserLogin,NoteCreate
router = APIRouter()

@router.get("/")
async def root(db: Session = Depends(get_db),user_id: int = Depends(verify_access_token)):
    return db.query(User).filter(User.id == user_id).first()


@router.post("/create_user")
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = hash_password(user.password)
    new_user = User(
        name = user.name,
        email=user.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user     
     

@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(User.email == form_data.username).first()

    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    if not verify_password(form_data.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    access_token = create_access_token({"user_id": db_user.id})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.post("/create_note")
async def create_note(note: NoteCreate, db: Session = Depends(get_db),User_id: int = Depends(verify_access_token)):
    if not User_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    db_user = db.query(User).filter(User.id == User_id).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="User not found")
    new_note = Notes(
        title=note.title,
        content=note.content,
        user_id=User_id
    )
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note


@router.get("/view_note")
async def view_note( db: Session = Depends(get_db), User_id: int = Depends(verify_access_token)):
    if not User_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    db_user = db.query(User).filter(User.id == User_id).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="User not found")
    return db.query(Notes).filter(Notes.user_id == User_id).all()


@router.delete("/delete_note")
async def delete_note(id : int, db: Session = Depends(get_db), User_id: int = Depends(verify_access_token)):
    if not User_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    note = db.query(Notes).filter(Notes.id == id, Notes.user_id == User_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(note)
    db.commit()
    return {"message": "Note deleted successfully"}