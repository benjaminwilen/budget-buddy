from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str


@app.post("/data")
async def get_data(item: Item):
    return {"message": f"Hello, {item.name}"}
