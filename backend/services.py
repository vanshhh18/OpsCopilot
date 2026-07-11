import json
from datetime import timedelta, datetime
from sqlalchemy.orm import Session

import crud

def dashboard_service(
    db: Session
):

    return crud.get_dashboard_summary(db)

def today_revenue_service(
    db: Session
):

    revenue = crud.get_today_revenue(db)

    return {

        "today_revenue": revenue

    }

def trial_users_service(
    db: Session,
    hobby: str
):

    users = crud.list_trial_users(
        db,
        hobby
    )

    return users

def active_users_service(
    db: Session
):

    return crud.get_active_users(db)

def expiring_members_service(
    db: Session
):

    return crud.get_expiring_memberships(db)

def tomorrow_bookings_service(
    db: Session
):

    return crud.get_tomorrow_bookings(db)

def extend_membership_request_service(

    db: Session,

    user_name: str,

    days: int

):

    user = crud.get_user_by_name(

        db,

        user_name

    )

    if user is None:

        return {

            "success": False,

            "message": "User not found."

        }

    new_date = (

        user.membership_expiry +

        timedelta(days=days)

    )

    pending = crud.create_pending_action(

        db,

        action="extend_membership",

        user_id=user.id,

        payload={

            "days": days

        }

    )

    crud.create_notification(

        db,

        vendor_id=user.vendor_id,

        title="Approval Required",

        message=(
            f"Membership extension pending "
            f"for {user.name}"
        ),

        notification_type="warning"

    )

    return {

        "success": True,

        "pending_id": pending.id,

        "current_expiry": str(
            user.membership_expiry
        ),

        "new_expiry": str(
            new_date
        ),

        "message":
        "Waiting for approval."

    }

def extend_trial_request_service(

    db: Session,

    user_name: str,

    days: int

):

    user = crud.get_user_by_name(

        db,

        user_name

    )

    if user is None:

        return {

            "success": False,

            "message": "User not found."

        }

    pending = crud.create_pending_action(

        db,

        action="extend_trial",

        user_id=user.id,

        payload={

            "days": days

        }

    )

    crud.create_notification(

        db,

        vendor_id=user.vendor_id,

        title="Approval Required",

        message=f"Trial extension pending for {user.name}",

        notification_type="warning"

    )

    return {

        "success": True,

        "pending_id": pending.id,

        "current_trial": str(
            user.trial_end
        ),

        "new_trial": str(

            user.trial_end +

            timedelta(days=days)

        )

    }

def update_phone_request_service(
    db: Session,
    user_name: str,
    new_phone: str
):

    user = crud.get_user_by_name(
        db,
        user_name
    )

    if user is None:

        return {
            "success": False,
            "message": "User not found."
        }

    pending = crud.create_pending_action(

        db,

        action="update_phone",

        user_id=user.id,

        payload={
            "new_phone": new_phone
        }

    )

    crud.create_notification(

        db,

        vendor_id=user.vendor_id,

        title="Approval Required",

        message=f"Phone update pending for {user.name}",

        notification_type="warning"

    )

    return {

        "success": True,

        "pending_id": pending.id,

        "old_phone": user.phone,

        "new_phone": new_phone,

        "message": "Waiting for approval."

    }


def cancel_booking_request_service(
    db: Session,
    booking_id: int
):

    booking = crud.get_booking_by_id(
        db,
        booking_id
    )

    if booking is None:

        return {
            "success": False,
            "message": "Booking not found."
        }

    pending = crud.create_pending_action(

        db,

        action="cancel_booking",

        user_id=booking.user_id,

        payload={
            "booking_id": booking.id
        }

    )

    crud.create_notification(

        db,

        vendor_id=booking.user.vendor_id,

        title="Approval Required",

        message=f"Booking #{booking.id} waiting for approval.",

        notification_type="warning"

    )

    return {

        "success": True,

        "pending_id": pending.id,

        "booking": booking.id,

        "message": "Waiting for approval."

    }


def approve_pending_action_service(
    db: Session,
    pending_id: int,
    approved_by: str = "Vendor"
):

    pending = crud.get_pending_action_by_id(
        db,
        pending_id
    )
    if pending.status != "pending":

        return {

        "success": False,

        "message": "Action already processed."

    }

    if pending is None:

        return {

            "success": False,

            "message": "Pending action not found."

        }

    payload = json.loads(
        pending.payload
    )

    user = crud.get_user_by_id(
        db,
        pending.user_id
    )

    if user is None:

        return {

            "success": False,

            "message": "User not found."

        }

    # --------------------------------
    # Execute Approved Action
    # --------------------------------

    if pending.action == "extend_membership":

        crud.extend_membership(
            db,
            user,
            payload["days"]
        )

    elif pending.action == "extend_trial":

        crud.extend_trial(
            db,
            user,
            payload["days"]
        )

    elif pending.action == "update_phone":

        crud.update_phone(
            db,
            user,
            payload["new_phone"]
        )

    elif pending.action == "cancel_booking":

        booking = crud.get_booking_by_id(
            db,
            payload["booking_id"]
        )

        if booking:
            crud.cancel_booking(
                db,
                booking
            )

    crud.approve_pending_action(
        db,
        pending,
        approved_by
    )

    crud.create_audit_log(

        db,

        vendor_id=user.vendor_id,

        action=pending.action,

        target_type="User",

        target_id=user.id,

        performed_by=approved_by,

        details=f"{pending.action} executed."

    )

    crud.create_notification(

        db,

        vendor_id=user.vendor_id,

        title="Action Completed",

        message=f"{pending.action} approved.",

        notification_type="success"

    )

    return {

        "success": True,

        "message": f"{pending.action} executed successfully."

    }


def reject_pending_action_service(
    db: Session,
    pending_id: int,
    approved_by: str = "Vendor"
):

    pending = crud.get_pending_action_by_id(
        db,
        pending_id
    )

    if pending is None:

        return {

            "success": False,

            "message": "Pending action not found."

        }

    user = crud.get_user_by_id(
        db,
        pending.user_id
    )

    crud.reject_pending_action(
        db,
        pending,
        approved_by
    )

    crud.create_notification(

        db,

        vendor_id=user.vendor_id,

        title="Request Rejected",

        message=f"{pending.action} rejected.",

        notification_type="warning"

    )

    crud.create_audit_log(

        db,

        vendor_id=user.vendor_id,

        action="Reject " + pending.action,

        target_type="User",

        target_id=user.id,

        performed_by=approved_by,

        details="Vendor rejected request."

    )

    return {

        "success": True,

        "message": "Request rejected."

    }

