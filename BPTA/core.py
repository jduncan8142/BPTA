from sqlalchemy import Column, Integer, String, Float, Text, BLOB, Boolean
from sqlalchemy import ForeignKey, Table, Date, DateTime, create_engine
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, backref, declarative_base
from sqlalchemy.schema import ForeignKeyConstraint

engine = create_engine('sqlite:///bpta.db', echo=True)
Base = declarative_base()


user_company = Table(
    "user_company",
    Base.metadata,
    Column("user_id", String(128), ForeignKey("user.email")),
    Column("company_id", String(8), ForeignKey("company.company_id")),
    Column("created", DateTime(timezone=True), server_default=func.now()),
    Column("updated", DateTime(timezone=True), onupdate=func.now()),
)

user_area = Table(
    "user_area",
    Base.metadata,
    Column("user_id", String(128), ForeignKey("user.email")),
    Column("area_id", String(32), ForeignKey("area.area_id")),
    Column("created", DateTime(timezone=True), server_default=func.now()),
    Column("updated", DateTime(timezone=True), onupdate=func.now()),
)

user_key_user_group = Table(
    "user_key_user_group", 
    Base.metadata, 
    Column("user_id", String(128), ForeignKey("user.email")),
    Column("key_user_group", String(32), ForeignKey("key_user_group.kug_id")),
    Column("created", DateTime(timezone=True), server_default=func.now()),
    Column("updated", DateTime(timezone=True), onupdate=func.now()),
)


user_role = Table(
    "user_role", 
    Base.metadata, 
    Column("user_id", String(128), ForeignKey("user.email")),
    Column("role", String(32), ForeignKey("role.role_id")),
    Column("created", DateTime(timezone=True), server_default=func.now()),
    Column("updated", DateTime(timezone=True), onupdate=func.now()),
)


class System(Base):
    __tablename__ = "system"
    system_id = Column(String(15), primary_key=True)
    description = Column(String(1024), nullable=False)
    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(DateTime(timezone=True), onupdate=func.now())


class Company(Base):
    __tablename__ = "company"
    company_id = Column(String(8), primary_key=True, unique=True, nullable=False)
    description = Column(String(1024), nullable=False)
    users = relationship("User", secondary=user_company, back_populates="companies")
    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(DateTime(timezone=True), onupdate=func.now())


class Area(Base):
    __tablename__ = "area"
    area_id = Column(String(32), primary_key=True, unique=True, nullable=False)
    description = Column(String(1024), nullable=False)
    users = relationship("User", secondary=user_area, back_populates="areas")
    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(DateTime(timezone=True), onupdate=func.now())


class Role(Base):
    __tablename__ = "role"
    role_id = Column(String(32), primary_key=True, unique=True, nullable=False)
    description = Column(String(1024), nullable=False)
    users = relationship("User", secondary=user_role, back_populates="roles")
    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(DateTime(timezone=True), onupdate=func.now())


class User(Base):
    __tablename__ = "user"
    email = Column(String(128), primary_key=True, unique=True, nullable=False)
    first_name = Column(String(128), nullable=False)
    middle_name = Column(String(128), nullable=False, default="")
    last_name = Column(String(128), nullable=False)
    phone = Column(String(15), nullable=False, default="")
    companies = relationship("Company", secondary=user_company, back_populates="users")
    key_user_groups = relationship("KeyUserGroup", secondary=user_key_user_group, back_populates="users")
    areas = relationship("Area", secondary=user_area, back_populates="users")
    roles = relationship("Role", secondary=user_role, back_populates="users")
    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(DateTime(timezone=True), onupdate=func.now())


class KeyUserGroup(Base):
    __tablename__ = "key_user_group"
    kug_id = Column(String(32), primary_key=True, unique=True, nullable=False)
    description = Column(String(1024), nullable=False)
    users = relationship("User", secondary=user_key_user_group, back_populates="key_user_groups")
    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(DateTime(timezone=True), onupdate=func.now())


class Status(Base):
    __tablename__ = "status"
    status_id = Column(String(32), primary_key=True, nullable=False)
    status_type = Column(String(1), primary_key=True, nullable=False)  # P, C, S
    description = Column(String(1024), nullable=False)
    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(DateTime(timezone=True), onupdate=func.now())


class Project(Base):
    __tablename__ = "project"
    project_id = Column(String(256), primary_key=True, unique=True, nullable=False)
    description = Column(String(1024), nullable=False)
    version = Column(String(8), nullable=False)
    planned_state_date = Column(Date, nullable=True)
    planned_end_date = Column(Date, nullable=True)
    actual_start_date = Column(Date, nullable=True)
    actual_end_date = Column(Date, nullable=True)
    estimated_finish_date = Column(Date, nullable=True)
    duration = Column(Float, nullable=False, default=1.0)
    project_manager_id = Column(String(128), ForeignKey("user.email"))
    business_owner_id = Column(String(128), ForeignKey("user.email"))
    it_owner_id = Column(String(128), ForeignKey("user.email"))
    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(DateTime(timezone=True), onupdate=func.now())
    status_id = Column(String(32), nullable=False)
    status_type = Column(String(1), nullable=False, default="S")
    __table_args__ = (
        ForeignKeyConstraint(
            [status_id, status_type], 
            [Status.status_id, Status.status_type]
        ), 
        {}
    )


class Case(Base):
    __tablename__ = "case"
    case_id = Column(String(256), primary_key=True, unique=True, nullable=False)
    description = Column(String(1024), nullable=False)
    version = Column(String(8), nullable=False)
    planned_state_date = Column(Date, nullable=True)
    planned_end_date = Column(Date, nullable=True)
    actual_start_date = Column(Date, nullable=True)
    actual_end_date = Column(Date, nullable=True)
    estimated_finish_date = Column(Date, nullable=True)
    duration = Column(Integer, nullable=False, default=1)
    duration_uom = Column(String(10), nullable=False, default="day")
    system = Column(String(15), ForeignKey("system.system_id"), nullable=False)
    project_id = Column(String(256), ForeignKey("project.project_id"), nullable=True)
    business_owner_id = Column(String(128), ForeignKey("user.email"))
    it_owner_id = Column(String(128), ForeignKey("user.email"))
    company_id = Column(String(8), ForeignKey("company.company_id"))
    area_id = Column(String(32), ForeignKey("area.area_id"))
    documentation = Column(Text, nullable=False, default="")
    date_format = Column(Text, nullable=False, default="%m/%d/%Y")
    explicit_wait = Column(Float, nullable=False, default=0.25)  # Seconds
    screenshot_on_pass = Column(Boolean, nullable=False, default=False)
    screenshot_on_fail = Column(Boolean, nullable=False, default=False)
    fail_on_error = Column(Boolean, nullable=False, default=False)
    close_on_cleanup = Column(Boolean, nullable=False, default=False)
    data = Column(BLOB, nullable=False, default=b'')
    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(DateTime(timezone=True), onupdate=func.now())


class Step(Base):
    __tablename__ = "step"
    step_id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(1024), nullable=False)
    sequence = Column(Integer, nullable=False)
    case_id = Column(String(256), ForeignKey("case.case_id"))
    kug_id = Column(String(32), ForeignKey("key_user_group.kug_id"))
    tester_id = Column(String(128), ForeignKey("user.email"))
    transaction = Column(String(20), nullable=False, default="")
    action = Column(String(128), nullable=False)
    element = Column(String(1024), nullable=False, default="")
    data = Column(Text, nullable=True)
    documentation = Column(Text, nullable=False, default="")
    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(DateTime(timezone=True), onupdate=func.now())


class Record(Base):
    __tablename__ = "record"
    record_id = Column(Integer, primary_key=True, autoincrement=True)
    case_id = Column(String(256), ForeignKey("case.case_id"))
    step_id = Column(Integer, ForeignKey("step.step_id"))
    document = Column(String(64), nullable=True)
    error = Column(String(2048), nullable=True)
    user = Column(Text, nullable=False)
    language = Column(String(2), nullable=False)
    app_server = Column(String(128), nullable=False)
    system_number = Column(Text, nullable=False)
    system_session_id = Column(Text, nullable=False)
    program = Column(String(20), nullable=True)
    screen_number = Column(String(4), nullable=True)
    response_time = Column(Float, nullable=False)
    round_trips = Column(Integer, nullable=False)
    sap_major_version = Column(Integer, nullable=False)
    sap_minor_version = Column(Integer, nullable=False)
    sap_patch_level = Column(Integer, nullable=False)
    sap_revision = Column(Integer, nullable=False)
    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(DateTime(timezone=True), onupdate=func.now())
    status_id = Column(String(32), nullable=False)
    status_type = Column(String(1), nullable=False, default="S")
    __table_args__ = (
        ForeignKeyConstraint(
            [status_id, status_type], 
            [Status.status_id, Status.status_type]
        ), 
        {}
    )


Base.metadata.create_all(engine)
