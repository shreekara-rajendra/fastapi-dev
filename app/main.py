from fastapi import FastAPI
from . import models
from .database import SessionLocal, engine
from .routers import posts,users,auth,vote
from fastapi.middleware.cors import CORSMiddleware
from .config import settings

#models.Base.metadata.create_all(bind=engine)



app = FastAPI()

origins = [
    'www.google.com'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
'''
while(True):
    try:
        conn = psycopg2.connect(host = 'localhost',database = 'fastapi',user = 'postgres',
                                password = 'FITJEEALLEN',cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("database connected")
        break
    except Exception as error:
        print("connection failed")
        print(f"error is {error}")
        time.sleep(2)
        
'''
'''
myposts = [{"id":1,"title":"csk","content":"dhoni"},{"id":2,"title":"rcb","content":"kohli"}]
'''
@app.get("/")
async def root():
    return {'data':'hi bro'}

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)


    


    



    


