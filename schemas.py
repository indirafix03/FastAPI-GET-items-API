from pydantic import BaseModel
from pydantic import BaseModel, ConfigDict

class ItemBase(BaseModel):
    name: str
    description: str

class Item(ItemBase):
    id: int
    model_config = ConfigDict(from_attributes=True)