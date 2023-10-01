from fastapi import FastAPI
from pydantic import BaseModel
from pprint import pprint


class GetModel(BaseModel):
    data: dict

app = FastAPI()

@app.post('/orders')
def test(data: dict):
    pprint(data)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=1234)