from fastapi import APIRouter,Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy.orm import aliased
from fastapi.security import OAuth2PasswordRequestForm

from app.auth.auth import verify_access_token,create_access_token,hash_password,verify_password
from app.models.model import User,Notes,Like
from app.schemas.schemes import UserCreate,UserLogin,NoteCreate
router = APIRouter()

@router.get("/health")
async def health_check():
    return {"status": "ok"}


@router.get("/userdetails")
async def get_user_details(db: Session = Depends(get_db),user_id: int = Depends(verify_access_token)):
    return db.query(User).filter(User.id == user_id).first()


@router.post("/create_user")
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    if db.query(User).filter(User.display_name == user.display_name).first():
        raise HTTPException(status_code=400, detail="Display name already taken")
    hashed_password = hash_password(user.password)
    new_user = User(
        display_name = user.display_name,
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

@router.post("/create_thought")
async def create_note(note: NoteCreate, db: Session = Depends(get_db),User_id: int = Depends(verify_access_token)):
    db_user = db.query(User).filter(User.id == User_id).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="User not found")
    if not note.title or not note.content:
        raise HTTPException(status_code=400, detail="Title and content are required")
    new_note = Notes(
        title=note.title,
        content=note.content,
        user_id=User_id
    )
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

# @router.get("/view_thoughts")
# async def view_note(
#     all: bool = False,
#     db: Session = Depends(get_db),
#     User_id: int = Depends(verify_access_token)
# ):
#     if not User_id:
#         raise HTTPException(status_code=401, detail="Invalid token")

#     db_user = db.query(User).filter(User.id == User_id).first()
#     if not db_user:
#         raise HTTPException(status_code=400, detail="User not found")

#     query = db.query(Notes)
#     if not all:
#         query = query.filter(Notes.user_id == User_id)

#     notes = query.all()

#     result = []
#     for note in notes:
#         likes = db.query(Like).filter(Like.note_id == note.id).count()
#         liked_by_me = db.query(Like).filter(
#             Like.note_id == note.id, Like.user_id == User_id
#         ).first() is not None
#         author = db.query(User).filter(User.id == note.user_id).first()

#         result.append({
#             "id": note.id,
#             "title": note.title,
#             "content": note.content,
#             "likes": likes,
#             "liked_by_me": liked_by_me,
#             "author": author.display_name if author else "Unknown",
#             "user_id": note.user_id
#         })

#     return result



@router.get("/view_thoughts")
async def view_note(
    all: bool = False,
    db: Session = Depends(get_db),
    user_id: int = Depends(verify_access_token),
):
    Author = aliased(User)

    query = (
        db.query(
            Notes.id,
            Notes.title,
            Notes.content,
            Notes.user_id,
            Author.display_name.label("author"),
            func.count(Like.id).label("likes"),
        )
        .join(Author, Notes.user_id == Author.id)
        .outerjoin(Like, Like.note_id == Notes.id)
        .group_by(
            Notes.id,
            Notes.title,
            Notes.content,
            Notes.user_id,
            Author.display_name,
        )
    )

    if not all:
        query = query.filter(Notes.user_id == user_id)

    notes = query.all()

    # Get all notes liked by the current user in one query
    liked_notes = {
        row.note_id
        for row in db.query(Like.note_id)
        .filter(Like.user_id == user_id)
        .all()
    }

    return [
        {
            "id": note.id,
            "title": note.title,
            "content": note.content,
            "likes": note.likes,
            "liked_by_me": note.id in liked_notes,
            "author": note.author,
            "user_id": note.user_id,
        }
        for note in notes
    ]

@router.delete("/delete_thought")
async def delete_note(id : int, db: Session = Depends(get_db), User_id: int = Depends(verify_access_token)):
    note = db.query(Notes).filter(Notes.id == id, Notes.user_id == User_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(note)
    db.commit()
    return {"message": "Note deleted successfully"}

@router.put("/update_thought")
async def update_note(id: int, note: NoteCreate, db: Session = Depends(get_db), User_id: int = Depends(verify_access_token)):
    db_note = db.query(Notes).filter(Notes.id == id, Notes.user_id == User_id).first()
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
    db_note.title = note.title
    db_note.content = note.content
    db.commit()
    db.refresh(db_note)
    return db_note

@router.post("/like_thought/{id}")
async def like_note(
    id: int,
    db: Session = Depends(get_db),
    User_id: int = Depends(verify_access_token)
):
    note = db.query(Notes).filter(
        Notes.id == id
    ).first()

    if not note:
        raise HTTPException(
            status_code=404,
            detail="Thought not found"
        )

    like = db.query(Like).filter(
        Like.user_id == User_id,
        Like.note_id == id
    ).first()

    if like:
        db.delete(like)
        db.commit()

        return {
            "liked": False,
            "message": "Like removed"
        }

    new_like = Like(
        user_id=User_id,
        note_id=id
    )

    db.add(new_like)
    db.commit()

    return {
        "liked": True,
        "message": "Thought liked"
    }

