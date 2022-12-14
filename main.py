import strawberry
from fastapi import FastAPI
from strawberry.asgi import GraphQL
import mysql.connector
from dotenv import load_dotenv
from pathlib import Path
import os

#-----------------------
# ENVIRONMENTAL VARIABLES
#-----------------------
app = FastAPI()
load_dotenv()
env_path = Path('.env')
load_dotenv(dotenv_path=env_path)

#-----------------------
# DB CONNECTION
#-----------------------
mydb = mysql.connector.connect(
  host = os.getenv('HOST'),
  username = os.getenv('USERNAME'),
  password = os.getenv('PASSWORD'),
  database = os.getenv('DATABASE'),
)
mycursor = mydb.cursor()



msg = {
    'msg': 'Welcome to FastAPI + Graph QL Template',
    'info':'visit http://localhost:<port>/graphql for GraphiQL UI.',
    'link':'https://et-dev.firstam.com'
    }



@strawberry.type
class User:
    name: str
    age: int    
    title: str

@strawberry.type
class Query:
    @strawberry.field
    def user(self) -> User:
        return User(name="Tony Stark", age=48, title='Iron Man')

schema = strawberry.Schema(query=Query)
graphql_app = GraphQL(schema)



@app.get("/")
async def root():
    return msg

@app.get("/assets")
async def getAssets():
    mycursor.execute("SELECT * FROM crypto.assets")
    res = mycursor.fetchall()
    return res

app.add_route("/graphql", graphql_app)
app.add_websocket_route("/graphql", graphql_app)
