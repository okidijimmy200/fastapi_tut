from fastapi import FastAPI, Depends, status, Response
from . import schemas, models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
# import uvicorn

app = FastAPI()


models.Base.metadata.create_all(engine)

# get db func 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/blog', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get('/blog')
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

# get blog with particular id
@app.get('/blog/{id}', status_code=200)
def detail(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'detail': f'Blog with the id {id} is not available'}

    return blog




# if __name__ == "__main__":
#     uvicorn.run(app, host='127.0.0.1', port=8000)