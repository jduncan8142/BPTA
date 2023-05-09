from sqlalchemy.orm import Session
from core import *
from datetime import datetime

_systems = [
    System(system_id="1.2 ERP - RQ2", description="ERP Quality Assurance System"),
    System(system_id="1.3 ERP - RE4", description="ERP Development System"),
    System(system_id="4.2 EWM - EWQ", description="EWM Quality Assurance System"),
    System(system_id="4.3 EWM - EWE", description="EWM Development System"),
    System(system_id="8.6 ERP - RS2", description="S4HANA Sandbox System"),
]

_companies = [
    Company(company_id="muus", description="Multivac US"),
    Company(company_id="muwo", description="Multivac HQ"),
]

_areas = [
    Area(area_id="otc", description="Order to Cash"),
    Area(area_id="ptp", description="Procure to Pay"),
    Area(area_id="p2p", description="Plan to Produce"),
    Area(area_id="pti", description="Plan to Inventory"),
    Area(area_id="qtc", description="Quote to Cash"),
    Area(area_id="rtr", description="Record to Report"),
    Area(area_id="htr", description="Hire to Retire"),
    Area(area_id="atr", description="Acquire to Retire"),
    Area(area_id="itr", description="Issue to Resolution"),
    Area(area_id="ftd", description="Forecast to Delivery"),
    Area(area_id="mto", description="Market to Order"),
    Area(area_id="ito", description="Idea to Offering")
]

_roles = [
    Role(role_id="tester", description="Tester"),
    Role(role_id="business_owner", description="Business Owner"),
    Role(role_id="it_owner", description="IT Owner"),
    Role(role_id="project_manager", description="Project Manager"),
]

_key_user_groups = [
    KeyUserGroup(kug_id="accounting", description="Accounting"),
    KeyUserGroup(kug_id="controlling", description="Controlling"),
    KeyUserGroup(kug_id="customer_service", description="Customer Service"),
    KeyUserGroup(kug_id="distribution", description="Distribution"),
    KeyUserGroup(kug_id="human_resources", description="Human Resources"),
    KeyUserGroup(kug_id="logistics", description="Logistics"),
    KeyUserGroup(kug_id="procurement", description="Procurement"),
    KeyUserGroup(kug_id="production", description="Production"),
    KeyUserGroup(kug_id="sales", description="Sales"),
    KeyUserGroup(kug_id="sales_sp", description="Sales Spare Parts"),
    KeyUserGroup(kug_id="scm_opec", description="SCM - Order Process External Customer"),
    KeyUserGroup(kug_id="scm_opic", description="SCM - Order Processing Internal Customer"),
]

_statuses = [
    Status(status_id="open", description="Open", status_type="S"),
    Status(status_id="na", description="N/A", status_type="S"),
    Status(status_id="successful", description="Successful", status_type="S"),
    Status(status_id="error", description="Error", status_type="S"),
    Status(status_id="on_hold", description="On Hold", status_type="S"),
    Status(status_id="retest", description="Retest", status_type="S"),
    Status(status_id="retested_ok", description="Retested - Successful", status_type="S"),
    Status(status_id="retested_error", description="Retested - Error", status_type="S"),
    Status(status_id="open", description="Open", status_type="C"),
    Status(status_id="na", description="N/A", status_type="C"),
    Status(status_id="successful", description="Successful", status_type="C"),
    Status(status_id="error", description="Error", status_type="C"),
    Status(status_id="on hold", description="On Hold", status_type="C"),
    Status(status_id="pending", description="Pending", status_type="P"),
    Status(status_id="active", description="Active", status_type="P"),
    Status(status_id="closed", description="Closed", status_type="P"),
]

_users = [
    User(first_name="Jason", middle_name="", last_name="Duncan", email="jason.duncan@multivac.com", phone="8168336466"),
]

_user_company = [
    {"user_id": "jason.duncan@multivac.com", "company_id": "muus"},
]

_user_area = [
    {"user_id": "jason.duncan@multivac.com", "area_id": "sales"},
    {"user_id": "jason.duncan@multivac.com", "area_id": "procurement"},
    {"user_id": "jason.duncan@multivac.com", "area_id": "goods_movement"},
]

_user_key_user_group = [
    {"user_id": "jason.duncan@multivac.com", "key_user_group": "sales"},
    {"user_id": "jason.duncan@multivac.com", "key_user_group": "distribution"},
    {"user_id": "jason.duncan@multivac.com", "key_user_group": "logistics"},
    {"user_id": "jason.duncan@multivac.com", "key_user_group": "procurement"},
]

_user_role = [
    {"user_id": "jason.duncan@multivac.com", "role": "it_owner"},
]

_projects = [
    Project(
        project_id="STARS2023", 
        description="MCoA reorg", 
        version="01.01.01",
        status_id="active",
        status_type="P",
        project_manager_id="jason.duncan@multivac.com",
        business_owner_id="jason.duncan@multivac.com",
        it_owner_id="jason.duncan@multivac.com",
    )
]

_cases = [
    Case(
        case_id="OTC - ZSPO Sales Order",
        description="Create, deliver, pick, GI amd invoice a ZSPO Spare Parts Sales Order for sales org 3000.",
        version="01.01.01",
        planned_state_date=datetime(2023, 3, 29),
        planned_end_date=datetime(2023, 4, 25),
        actual_start_date=datetime(2023, 3, 29),
        actual_end_date=datetime(2023, 4, 25),
        estimated_finish_date=datetime(2023, 4, 21),
        duration=30,
        duration_uom="minutes",
        system="8.6 ERP - RS2",
        project_id="STARS2023", 
        business_owner_id="jason.duncan@multivac.com",
        it_owner_id="jason.duncan@multivac.com",
        company_id="muus",
        area_id="otc", 
        documentation="",
        date_format="%m/%d/%Y",
        explicit_wait=0.25,
        screenshot_on_pass=False,
        screenshot_on_fail=False,
        fail_on_error=False,
        close_on_cleanup=False,
        data=b'''{
            "order_type": "ZSPO",
            "sales_org": "3000",
            "dist_ch": "50",
            "division": "50",
            "sold_to": "10060026",
            "ship_to": "10060026",
            "items": [
                {
                    "material": "101105492",
                    "qty": "1",
                    "uom": "PC",
                }
            ]
        }
        '''
    )
]

_steps = [
    Step(
        description="Open SAP connection",
        sequence=1,
        case_id="OTC - ZSPO Sales Order",
        kug_id="sales_sp",
        tester_id="jason.duncan@multivac.com",
        action="open_connection",
        documentation="Open SAP connection"
    ),
    Step(
        description="Open VA01",
        sequence=2,
        case_id="OTC - ZSPO Sales Order",
        kug_id="sales_sp",
        tester_id="jason.duncan@multivac.com",
        transaction="VA01",
        action="start_transaction",
        documentation="Open transaction VA01"
    ),
    Step(
        description="Set sales order type ZSPO",
        sequence=3,
        case_id="OTC - ZSPO Sales Order",
        kug_id="sales_sp",
        tester_id="jason.duncan@multivac.com",
        transaction="VA01",
        action="set_text",
        element="/app/con[0]/ses[0]/wnd[0]/usr/ctxtVBAK-AUART",
        data="order_type",
        documentation="Set text for order type"
    ),
    Step(
        description="Set sales org",
        sequence=4,
        case_id="OTC - ZSPO Sales Order",
        kug_id="sales_sp",
        tester_id="jason.duncan@multivac.com",
        transaction="VA01",
        action="set_text",
        element="/app/con[0]/ses[0]/wnd[0]/usr/ctxtVBAK-VKORG",
        data="sales_org",
        documentation="Set text for sales organization"
    ),
    Step(
        description="Set distribution channel",
        sequence=5,
        case_id="OTC - ZSPO Sales Order",
        kug_id="sales_sp",
        tester_id="jason.duncan@multivac.com",
        transaction="VA01",
        action="set_text",
        element="/app/con[0]/ses[0]/wnd[0]/usr/ctxtVBAK-VTWEG",
        data="dist_ch",
        documentation="Set text for distribution channel"
    ),
    Step(
        description="Set division",
        sequence=6,
        case_id="OTC - ZSPO Sales Order",
        kug_id="sales_sp",
        tester_id="jason.duncan@multivac.com",
        transaction="VA01",
        action="set_text",
        element="/app/con[0]/ses[0]/wnd[0]/usr/ctxtVBAK-SPART",
        data="division",
        documentation="Set text for division"
    ),
    Step(
        description="Press Enter",
        sequence=7,
        case_id="OTC - ZSPO Sales Order",
        kug_id="sales_sp",
        tester_id="jason.duncan@multivac.com",
        transaction="VA01",
        action="enter",
    ),
]

_records = [
    Record(
        case_id="OTC - ZSPO Sales Order",
        step_id=1,
        user="DUNCAN",
        language="EN",
        app_server="",
        system_number="",
        system_session_id="",
        program="", 
        screen_number="",
        response_time=1.0,
        round_trips=1,
        sap_major_version=1,
        sap_minor_version=1,
        sap_patch_level=1,
        sap_revision=1,
        status_id="successful",
        status_type="S",
    ),
]


if __name__ == "__main__":
    with Session(engine) as session, session.begin():
        session.add_all(_systems)
        session.add_all(_companies)
        session.add_all(_areas)
        session.add_all(_roles)
        session.add_all(_key_user_groups)
        session.add_all(_statuses)
        session.add_all(_users)
        session.execute(user_company.insert(), _user_company)
        session.execute(user_area.insert(), _user_area)
        session.execute(user_key_user_group.insert(), _user_key_user_group)
        session.execute(user_role.insert(), _user_role)
        session.add_all(_projects)
        session.add_all(_cases)
        session.add_all(_steps)
        session.add_all(_records)
