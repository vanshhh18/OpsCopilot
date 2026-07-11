from typing import Annotated

from langchain_core.tools import tool
from pydantic import BaseModel, Field

from database import SessionLocal
import services

# ==========================================
# INPUT SCHEMAS
# ==========================================

class HobbyInput(BaseModel):

    hobby: Annotated[
        str,
        Field(
            description="Hobby or sport name like Badminton, Football, Cricket"
        )
    ]


class MembershipInput(BaseModel):

    user_name: Annotated[
        str,
        Field(
            description="Full or partial user name"
        )
    ]

    days: Annotated[
        int,
        Field(
            description="Number of days to extend membership"
        )
    ]


class TrialInput(BaseModel):

    user_name: Annotated[
        str,
        Field(
            description="Full or partial user name"
        )
    ]

    days: Annotated[
        int,
        Field(
            description="Number of trial days"
        )
    ]


class PhoneInput(BaseModel):

    user_name: Annotated[
        str,
        Field(
            description="User name"
        )
    ]

    new_phone: Annotated[
        str,
        Field(
            description="New phone number"
        )
    ]


class BookingInput(BaseModel):

    booking_id: Annotated[
        int,
        Field(
            description="Booking ID"
        )
    ]


class PendingActionInput(BaseModel):

    pending_id: Annotated[
        int,
        Field(
            description="Pending action ID"
        )
    ]


@tool
def get_dashboard_summary():
    """
    Returns dashboard summary including
    users, coaches, bookings,
    payments and today's revenue.
    """

    db = SessionLocal()

    result = services.dashboard_service(db)

    db.close()

    return result

@tool
def get_today_revenue():
    """
    Returns today's revenue.
    """

    db = SessionLocal()

    result = services.today_revenue_service(db)

    db.close()

    return result

@tool(args_schema=HobbyInput)
def list_trial_users(
    hobby: str
):
    """
    Returns trial users of
    a particular hobby.
    """

    db = SessionLocal()

    users = services.trial_users_service(
        db,
        hobby
    )

    db.close()

    return [
        {
            "id": u.id,
            "name": u.name,
            "email": u.email,
            "trial_end": str(u.trial_end)
        }
        for u in users
    ]

@tool
def get_active_users():
    """
    Returns all active users.
    """

    db = SessionLocal()

    users = services.active_users_service(
        db
    )

    db.close()

    return [
        {
            "id": u.id,
            "name": u.name,
            "hobby": u.hobby,
            "plan": u.membership_plan
        }
        for u in users
    ]

@tool
def get_expiring_memberships():
    """
    Returns memberships
    expiring within 7 days.
    """

    db = SessionLocal()

    users = services.expiring_members_service(
        db
    )

    db.close()

    return [
        {
            "id": u.id,
            "name": u.name,
            "expiry": str(
                u.membership_expiry
            )
        }
        for u in users
    ]

@tool
def get_tomorrow_bookings():
    """
    Returns tomorrow's bookings.
    """

    db = SessionLocal()

    bookings = services.tomorrow_bookings_service(
        db
    )

    db.close()

    return [
        {
            "booking_id": b.id,
            "user": b.user.name,
            "coach": b.coach.name,
            "date": str(
                b.booking_date
            ),
            "status": b.status
        }
        for b in bookings
    ]

@tool(args_schema=MembershipInput)
def extend_membership(
    user_name: str,
    days: int
):
    """
    Creates a pending membership
    extension request.
    No update is performed until approved.
    """

    db = SessionLocal()

    result = services.extend_membership_request_service(
        db,
        user_name,
        days
    )

    db.close()

    return result

@tool(args_schema=TrialInput)
def extend_trial(
    user_name: str,
    days: int
):
    """
    Creates a pending
    trial extension request.
    """

    db = SessionLocal()

    result = services.extend_trial_request_service(
        db,
        user_name,
        days
    )

    db.close()

    return result

@tool(args_schema=PhoneInput)
def update_phone(
    user_name: str,
    new_phone: str
):
    """
    Creates a pending
    phone update request.
    """

    db = SessionLocal()

    result = services.update_phone_request_service(
        db,
        user_name,
        new_phone
    )

    db.close()

    return result

@tool(args_schema=BookingInput)
def cancel_booking(
    booking_id: int
):
    """
    Creates a pending
    booking cancellation request.
    """

    db = SessionLocal()

    result = services.cancel_booking_request_service(
        db,
        booking_id
    )

    db.close()

    return result

@tool(args_schema=PendingActionInput)
def approve_action(
    pending_id: int
):
    """
    Approves a pending action
    and executes it.
    """

    db = SessionLocal()

    try:

        result = services.approve_pending_action_service(
            db,
            pending_id
        )

        return result

    finally:

        db.close()

@tool(args_schema=PendingActionInput)
def reject_action(
    pending_id: int
):
    """
    Rejects a pending action.
    """

    db = SessionLocal()

    try:

        result = services.reject_pending_action_service(
            db,
            pending_id
        )

        return result

    finally:

        db.close()

TOOLS = [

    # -------------------------
    # READ TOOLS
    # -------------------------

    get_dashboard_summary,

    get_today_revenue,

    list_trial_users,

    get_active_users,

    get_expiring_memberships,

    get_tomorrow_bookings,

    # -------------------------
    # WRITE REQUEST TOOLS
    # -------------------------

    extend_membership,

    extend_trial,

    update_phone,

    cancel_booking,

    # -------------------------
    # APPROVAL TOOLS
    # -------------------------

    approve_action,

    reject_action

]