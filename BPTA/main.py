from fastapi import FastAPI
from typing import Optional
from uuid import UUID, uuid4
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, Field, constr
from enum import StrEnum, auto
import datetime

Base = declarative_base()

app = FastAPI()

class Role(StrEnum):
    ADMIN = auto()
    MANAGER = auto()
    OWNER = auto()
    REPORTER = auto()
    TESTER = auto()
    VIEWER = auto()

class Result(StrEnum):
    PASS = auto()
    FAIL = auto()
    WARN = auto()

# class AddressOrm(Base):
#     __tablename__ = 'address'
#     uid = Column(UUID, primary_key=True, nullable=False)
#     updated = Column(datetime.date, nullable=False)
#     building = Column(String(16), nullable=False)
#     suite = Column(String(16), nullable=True)
#     street1 = Column(String(256), nullable=False)
#     street2 = Column(String(256), nullable=True)
#     street3 = Column(String(256), nullable=True)
#     street4 = Column(String(256), nullable=True)
#     city = Column(String(128), nullable=False)
#     state = Column(String(2), nullable=True)
#     region = Column(String(128), nullable=True)
#     county = Column(String(128), nullable=False)
#     postal_code = Column(String(10), nullable=False)
#     country = Column(String(64), nullable=False)

# class AddressModel(BaseModel):
#     uid: UUID = Field(default_factory=uuid4)
#     updated: datetime = Field(default_factory=datetime.utcnow)
#     building: constr(max_length=16)
#     suite: Optional[constr(max_length=16)]
#     street1: constr(max_length=256)
#     street2: Optional[constr(max_length=256)]
#     street3: Optional[constr(max_length=256)]
#     street4: Optional[constr(max_length=256)]
#     city: constr(max_length=128)
#     state: Optional[constr(max_length=2)]
#     region: Optional[constr(max_length=128)]
#     county: Optional[constr(max_length=128)]
#     postal_code: constr(max_length=10)
#     country: constr(max_length=64)

#     class Config:
#         orm_mode = True

# class UserModel(BaseModel):
#     uid: UUID = Field(default_factory=uuid4)
#     updated: datetime = Field(default_factory=datetime.utcnow)
#     first_name: str
#     middle_name: str
#     last_name: str
#     email: str
#     phone: str
#     cell: str
#     address: AddressModel.uid
#     roles: list[Role]

#     class Config:
#         orm_mode = True

# class ProjectModel(BaseModel):
#     uid: UUID = Field(default_factory=uuid4)
#     updated: datetime = Field(default_factory=datetime.utcnow)
#     name: str
#     description: Optional[str]
#     planned_start_date: Optional[datetime.date]
#     planned_finish_date: Optional[datetime.date]
#     actual_start_date: Optional[datetime.date]
#     actual_finish_date: Optional[datetime.date]
#     project_managers: Optional[list[UserModel.uid]]
#     process_owners: Optional[list[UserModel.uid]]
#     technical_owners: Optional[list[UserModel.uid]]
#     testers: Optional[list[UserModel.uid]]

#     class Config:
#         orm_mode = True

# class CaseModel(BaseModel):
#     def default_date_format() -> str:
#         return "%m/%d/%Y"
    
#     def default_explicit_wait() -> float:
#         return 0.25
    
#     def default_system() -> str:
#         return ""
    
    # uid: UUID = Field(default_factory=uuid4)
    # created_on: datetime = Field(default_factory=datetime.utcnow)
    # updated_on: datetime = Field(default_factory=datetime.utcnow)
    # created_by: UserModel.uid
    # updated_by: UserModel.uid
    # name: str
    # project: ProjectModel.uid
    # description: Optional[str]
    # process_owners: list[UserModel.uid]
    # technical_owners: list[UserModel.uid]
    # testers: list[UserModel.uid]
    # documentation_link: str
    # date_format: Optional[str] = Field(default_factory=default_date_format)
    # explicit_wait: float = Field(default_factory=default_explicit_wait)
    # screenshot_on_pass: bool = Field(default=False)
    # screenshot_on_fail: bool = Field(default=False)
    # fail_on_error: bool = Field(default=True)
    # close_on_cleanup: bool = Field(default=True)
    # system: str = Field(default_factory=default_system)     

    # class Config:
    #     orm_mode = True

# class StepModel(BaseModel):
#     uid: UUID = Field(default_factory=uuid4)
#     created_on: datetime = Field(default_factory=datetime.utcnow)
#     updated_on: datetime = Field(default_factory=datetime.utcnow)
#     created_by: UserModel.uid
#     updated_by: UserModel.uid
#     case: CaseModel.uid
#     action: str
#     element_id: Optional[str]
#     args: Optional[list]
#     kwargs: Optional[dict]
#     name: str
#     description: Optional[str]
#     code: Optional[str]
    
#     class Config:
#         orm_mode = True

# class StatusModel(BaseModel):
#     uid: UUID = Field(default_factory=uuid4)
#     created_on: datetime = Field(default_factory=datetime.utcnow)
#     created_by: UserModel.uid
#     parent: StepModel.uid|CaseModel.uid
#     result: Result
#     screenshot: Optional[str]
#     error: Optional[str]

#     class Config:
#         orm_mode = True

class Project(BaseModel):
    id = int
    name: str
    description: Optional[str]
    project_manager: Optional[str]

class Case(BaseModel):
    id = int
    name: str
    project: Project
    tester: str
    system: str
    status: Optional[Result]

class Step(BaseModel):
    id: int
    name: str
    case: Case
    action: str
    element_id: Optional[str]
    args: Optional[list[str]]
    kwargs: Optional[dict]
    status: Optional[Result]

cases = {
    0: Case(id=0, name="case1", project=Project(id=0, name="project1"), tester="Jason", system="1.2 ERP - RQ2"),
    1: Case(id=1, name="case2", project=Project(id=0, name="project1"), tester="Ann", system="1.2 ERP - RQ2", status=Result.FAIL)
}

@app.get("/")
def index() -> dict[str, dict[int, Case]]:
    return {"cases": cases}

@app.get("/case/{case_id}")
def query_case_by_id(case_id: int) -> Case:
    if case_id not in cases:
        raise HTTPException(status_code=404, detail=f"Case with (case_id=) does not exist.")
    return cases[case_id]
