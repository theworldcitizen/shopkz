from typing import Optional

from pydantic import BaseModel


class Ad(BaseModel):
    name: str
    articul: str
    price: Optional[str] = None
    memory_size: str
    link: str
