import uvicorn
from fastapi import FastAPI
from models import User, UserCreate, NewColumn, DelColumn
from database import collection
from database_mongodb_api import DatabaseManager

app = FastAPI()
db = DatabaseManager()
# print(db.fetch_all_records())

@app.post("/user")
async def create_user(user: User):
    result = await collection.insert_one(user.dict())
    return {"id": str(result.inserted_id)}


@app.get("/users")
async def get_users():
    users = []
    async for user in db.fetch_all_records():
        # del user["_id"]
        user['_id'] = str(user['_id'])
        users.append(user)
    return users
@app.post("/create", status_code=201, responses={404: {"description": "Not found"}})
async def create_user(user: UserCreate):
    try:
     db.add_record(dict(user))
     return user.model_dump()
    except Exception as e:
        print(f"{e}, got error in creating new users")

@app.delete("/delete/{user_id}", status_code=204, responses={204: {"description": "items has beed delete"}})
async def delete_user(user_id: str):
    cnt=db.delete_records([user_id])
    return {"deleted": cnt}


@app.put("/user/{user_id}",status_code=204,responses={404: {"description": "Not found"}})
async def update_user(user_id: str, user: UserCreate):
    cnt=db.update_record(user_id, user.model_dump())
    return {"updated": cnt}
@app.get("/user/{user_id}",status_code=200,responses={404: {"description": "Not found"}})
async def get_user(user_id: str):
    search_users=[]
    async for user in db.search_records(user_id):
        user['_id'] = str(user['_id'])
        del user['_id']
        search_users.append(user)
    return search_users

@app.post("/NewColumn", status_code=201, responses={404: {"description": "Not found", 201:{"description": "Column has been created"}}})
async def create_new_column(column: NewColumn):
    hname=column.ColumnName
    hId=column.ColumnID
    db.add_new_column(hname, hId)

@app.delete("/ColDelete/{Col_ID}",status_code=204, responses={404: {"description": "Not found"}})
async def delete_column(col: DelColumn):
    await db.del_sel_column(col.ColumnName)

@app.get("/Auth" ,status_code=200,responses={404: {"description": "Not found"}})
async def get_auth(user:str, password:str):
    user= await db.authenticate_user(user, password)
    # users.append(user)
    return user


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)