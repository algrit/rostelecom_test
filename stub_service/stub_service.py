import asyncio

import uvicorn
from fastapi import FastAPI, HTTPException

app = FastAPI()

from pydantic import BaseModel, Field, ValidationError


class Parameters(BaseModel):
    username: str
    password: str
    vlan: int | None = None
    interfaces: list[int]


class ParamsInput(BaseModel):
    timeoutInSeconds: int
    parameters: Parameters


class ParamsBase(ParamsInput):
    id: str = Field(pattern="^[a-zA-Z0-9]{6,}$")


@app.post("/api/v1/equipment/cpe/{id}", summary="Сервис заглушка, ничего не делает")
async def params_input(id: str, cpe_data: ParamsInput):
    try:
        task_data = ParamsBase(id=id, **cpe_data.model_dump())
    except ValidationError:
        raise HTTPException(404, "The requested equipment is not found")
    except Exception:
        raise HTTPException(500, "Internal provisioning exception")
    await asyncio.sleep(60)
    return {"message": "success"}


if __name__ == "__main__":
    uvicorn.run("stub_service:app", host="localhost", port=6999, reload=True)
