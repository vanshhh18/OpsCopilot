from datetime import date, timedelta, datetime

from sqlalchemy.orm import Session
from sqlalchemy import func

from models import (
    User,
    Booking,
    Coach,
    Payment,
    PendingAction,
    Notification,
    AuditLog,
    Conversation,
    ToolExecution
)

def get_user_by_id(
    db: Session,
    user_id: int
):
    return (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

def get_user_by_name(
    db: Session,
    user_name: str
):
    return (
        db.query(User)
        .filter(
            User.name.ilike(f"%{user_name}%")
        )
        .first()
    )

def get_active_users(
    db: Session
):
    return (
        db.query(User)
        .filter(User.active == True)
        .all()
    )

def list_trial_users(
    db: Session,
    hobby: str
):
    return (
        db.query(User)
        .filter(
            User.is_trial == True,
            User.hobby.ilike(hobby)
        )
        .all()
    )

def get_expiring_memberships(
    db: Session
):
    today = date.today()

    future = today + timedelta(days=7)

    return (
        db.query(User)
        .filter(
            User.membership_expiry >= today,
            User.membership_expiry <= future
        )
        .all()
    )

def update_phone(
    db: Session,
    user: User,
    phone: str
):
    user.phone = phone

    db.commit()

    db.refresh(user)

    return user

def extend_membership(
    db: Session,
    user: User,
    days: int
):
    user.membership_expiry = (
        user.membership_expiry +
        timedelta(days=days)
    )

    db.commit()

    db.refresh(user)

    return user

def extend_trial(
    db: Session,
    user: User,
    days: int
):
    user.trial_end = (
        user.trial_end +
        timedelta(days=days)
    )

    db.commit()

    db.refresh(user)

    return user

def get_booking_by_id(
    db: Session,
    booking_id: int
):
    return (
        db.query(Booking)
        .filter(
            Booking.id == booking_id
        )
        .first()
    )

def get_tomorrow_bookings(
    db: Session
):
    tomorrow = date.today() + timedelta(days=1)

    return (
        db.query(Booking)
        .filter(
            Booking.booking_date == tomorrow
        )
        .all()
    )

def get_bookings_by_user(
    db: Session,
    user_id: int
):
    return (
        db.query(Booking)
        .filter(
            Booking.user_id == user_id
        )
        .all()
    )

def get_bookings_by_coach(
    db: Session,
    coach_id: int
):
    return (
        db.query(Booking)
        .filter(
            Booking.coach_id == coach_id
        )
        .all()
    )

def cancel_booking(
    db: Session,
    booking: Booking
):
    booking.status = "Cancelled"

    db.commit()

    db.refresh(booking)

    return booking

def get_today_revenue(
    db: Session
):
    revenue = (
        db.query(
            func.sum(Payment.amount)
        )
        .filter(
            Payment.payment_date == date.today(),
            Payment.status == "Paid"
        )
        .scalar()
    )

    return revenue or 0

def get_month_revenue(
    db: Session
):
    today = date.today()

    revenue = (
        db.query(
            func.sum(Payment.amount)
        )
        .filter(
            func.strftime(
                "%Y-%m",
                Payment.payment_date
            )
            ==
            today.strftime("%Y-%m"),

            Payment.status == "Paid"
        )
        .scalar()
    )

    return revenue or 0

def get_total_revenue(
    db: Session
):
    revenue = (
        db.query(
            func.sum(Payment.amount)
        )
        .filter(
            Payment.status == "Paid"
        )
        .scalar()
    )

    return revenue or 0

def get_failed_payments(
    db: Session
):
    return (
        db.query(Payment)
        .filter(
            Payment.status == "Failed"
        )
        .all()
    )

def get_dashboard_summary(
    db: Session
):
    return {

        "users":
        db.query(User).count(),

        "coaches":
        db.query(Coach).count(),

        "bookings":
        db.query(Booking).count(),

        "payments":
        db.query(Payment).count(),

        "today_revenue":
        get_today_revenue(db)

    }

import json


# =====================================================
# PENDING ACTIONS
# =====================================================

def create_pending_action(
    db: Session,
    action: str,
    user_id: int,
    payload: dict,
    requested_by: str = "Vendor"
):

    pending = PendingAction(

        action=action,

        user_id=user_id,

        payload=json.dumps(payload),

        status="pending",

        requested_by=requested_by

    )

    db.add(pending)

    db.commit()

    db.refresh(pending)

    return pending


def get_pending_action_by_id(
    db: Session,
    action_id: int
):
    return (
        db.query(PendingAction)
        .filter(PendingAction.id == action_id)
        .first()
    )


def get_pending_actions(
    db: Session
):
    return (
        db.query(PendingAction)
        .filter(PendingAction.status == "pending")
        .all()
    )


def approve_pending_action(
    db: Session,
    pending: PendingAction,
    approved_by: str = "Vendor"
):

    pending.status = "approved"

    pending.approved_by = approved_by

    pending.completed_at = datetime.utcnow()

    db.commit()

    db.refresh(pending)

    return pending


def reject_pending_action(
    db: Session,
    pending: PendingAction,
    approved_by: str = "Vendor"
):

    pending.status = "rejected"

    pending.approved_by = approved_by

    pending.completed_at = datetime.utcnow()

    db.commit()

    db.refresh(pending)

    return pending

# =====================================================
# NOTIFICATIONS
# =====================================================

def create_notification(
    db: Session,
    vendor_id: int,
    title: str,
    message: str,
    notification_type: str = "info"
):

    notification = Notification(

        vendor_id=vendor_id,

        title=title,

        message=message,

        notification_type=notification_type

    )

    db.add(notification)

    db.commit()

    db.refresh(notification)

    return notification


def get_notifications(
    db: Session,
    vendor_id: int
):

    return (

        db.query(Notification)

        .filter(Notification.vendor_id == vendor_id)

        .order_by(Notification.created_at.desc())

        .all()

    )


def mark_notification_read(
    db: Session,
    notification_id: int
):

    notification = (

        db.query(Notification)

        .filter(Notification.id == notification_id)

        .first()

    )

    if notification is None:

        return None

    notification.is_read = True

    db.commit()

    db.refresh(notification)

    return notification

# =====================================================
# AUDIT LOGS
# =====================================================

def create_audit_log(
    db: Session,
    vendor_id: int,
    action: str,
    target_type: str,
    target_id: int,
    performed_by: str,
    details: str
):

    log = AuditLog(

        vendor_id=vendor_id,

        action=action,

        target_type=target_type,

        target_id=target_id,

        performed_by=performed_by,

        details=details

    )

    db.add(log)

    db.commit()

    db.refresh(log)

    return log


def get_recent_audit_logs(
    db: Session,
    limit: int = 20
):

    return (

        db.query(AuditLog)

        .order_by(AuditLog.created_at.desc())

        .limit(limit)

        .all()

    )

# =====================================================
# CONVERSATIONS
# =====================================================

def save_message(
    db: Session,
    vendor_id: int,
    session_id: str,
    role: str,
    message: str
):

    chat = Conversation(

        vendor_id=vendor_id,

        session_id=session_id,

        role=role,

        message=message

    )

    db.add(chat)

    db.commit()

    db.refresh(chat)

    return chat


def get_conversation(
    db: Session,
    session_id: str
):

    return (

        db.query(Conversation)

        .filter(
            Conversation.session_id == session_id
        )

        .order_by(
            Conversation.created_at
        )

        .all()

    )

# =====================================================
# TOOL EXECUTION LOGS
# =====================================================

def log_tool_execution(
    db: Session,
    vendor_id: int,
    tool_name: str,
    user_query: str,
    tool_input: str,
    tool_output: str,
    success: bool,
    execution_time_ms: int
):

    log = ToolExecution(

        vendor_id=vendor_id,

        tool_name=tool_name,

        user_query=user_query,

        tool_input=tool_input,

        tool_output=tool_output,

        success=success,

        execution_time_ms=execution_time_ms

    )

    db.add(log)

    db.commit()

    db.refresh(log)

    return log


def get_tool_logs(
    db: Session,
    limit: int = 20
):

    return (

        db.query(ToolExecution)

        .order_by(
            ToolExecution.created_at.desc()
        )

        .limit(limit)

        .all()

    )

