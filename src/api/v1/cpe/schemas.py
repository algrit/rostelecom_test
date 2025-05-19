from pydantic import BaseModel, Field


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
