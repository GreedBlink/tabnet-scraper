
from pydantic import BaseModel, Field
from typing import List

class TabnetComponent(BaseModel):
    id: str
    column: List[str] = Field(description='')
    row: List[str] = Field(description='')
    mesure: List[str] = Field(description='')
    period: List[str] = Field(description='')
    custom_filters: List[dict] = Field(description='', options=True)


class TabnetComponents(BaseModel):
    components: List[TabnetComponent] = Field(description='')