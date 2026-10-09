from pydantic import BaseModel, Field, computed_field, field_validator
from typing import Annotated, Literal
from config.city_tier import tier_1_cities, tier_2_cities

#pydantic model to validate incoming data
class UserInput(BaseModel):
    age:Annotated[int, Field(gt=0,lt=100,decription='age of the user')]
    weight:Annotated[float, Field(gt=0,decription='weight of the user')]
    height:Annotated[float, Field(gt=0,decription='height of the user')]
    income_lpa:Annotated[float, Field(gt=0,decription='annual salary of the user')]
    smoker:Annotated[bool,Field(decription='Is user a smoker')]
    city:Annotated[str, Field(max_length=100)]
    occupation:Annotated[Literal['student','teacher','admin','retired','unemployed','business_owner'], Field(max_length=100)]

    @field_validator('city')
    @classmethod
    def normalize_city(cls,v:str)->str:
        v=v.strip().title()
        return v

    @computed_field
    @property
    def bmi(self)->float:
        return self.weight/(self.height**2)
    @computed_field
    @property
    def lifestyle_risk(self)->str:
        if self.smoker and self.bmi > 30:
            return 'high'
        elif self.smoker and self.bmi > 27:
            return 'medium'
        else:
            return 'low'
    @computed_field
    @property
    def  age_group(self)->str:
        if self.age<18:
            return 'teen'
        elif self.age<35:
            return 'young'
        else:
            return 'old'
    @computed_field
    @property
    def city_tier(self) -> int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3