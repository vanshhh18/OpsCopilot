from datetime import date, datetime

from sqlalchemy import (
    String,
    Integer,
    Date,
    DateTime,
    Boolean,
    ForeignKey
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from database import Base


# =====================================================
# Vendor
# =====================================================

class Vendor(Base):
    __tablename__ = "vendors"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(120),
        unique=True,
        nullable=False
    )

    phone: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    academy_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    city: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    # Relationships

    users = relationship(
        "User",
        back_populates="vendor",
        cascade="all, delete-orphan"
    )

    coaches = relationship(
        "Coach",
        back_populates="vendor",
        cascade="all, delete-orphan"
    )

    conversations = relationship(
        "Conversation",
        back_populates="vendor",
        cascade="all, delete-orphan"
    )

    notifications = relationship(
        "Notification",
        back_populates="vendor",
        cascade="all, delete-orphan"
    )

    audit_logs = relationship(
        "AuditLog",
        back_populates="vendor",
        cascade="all, delete-orphan"
    )

    tool_logs = relationship(
        "ToolExecution",
        back_populates="vendor",
        cascade="all, delete-orphan"
    )


# =====================================================
# User
# =====================================================

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    vendor_id: Mapped[int] = mapped_column(
        ForeignKey("vendors.id"),
        nullable=False
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(120),
        unique=True,
        nullable=False
    )

    phone: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    hobby: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    membership_plan: Mapped[str] = mapped_column(
        String(30),
        default="Trial"
    )

    membership_expiry: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    is_trial: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    trial_end: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    # Relationships

    vendor = relationship(
        "Vendor",
        back_populates="users"
    )

    bookings = relationship(
        "Booking",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    payments = relationship(
        "Payment",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    pending_actions = relationship(
        "PendingAction",
        back_populates="user",
        cascade="all, delete-orphan"
    )


# =====================================================
# Coach
# =====================================================

class Coach(Base):
    __tablename__ = "coaches"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    vendor_id: Mapped[int] = mapped_column(
        ForeignKey("vendors.id"),
        nullable=False
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    sport: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    phone: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    experience: Mapped[int] = mapped_column(
        Integer,
        default=1
    )

    specialization: Mapped[str] = mapped_column(
        String(100),
        default="General"
    )

    active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    # Relationships

    vendor = relationship(
        "Vendor",
        back_populates="coaches"
    )

    bookings = relationship(
        "Booking",
        back_populates="coach",
        cascade="all, delete-orphan"
    )


from sqlalchemy import Float, Text


# =====================================================
# Booking
# =====================================================

class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    coach_id: Mapped[int] = mapped_column(
        ForeignKey("coaches.id"),
        nullable=False
    )

    booking_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    start_time: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    end_time: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    court: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="Confirmed"
    )

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    # Relationships

    user = relationship(
        "User",
        back_populates="bookings"
    )

    coach = relationship(
        "Coach",
        back_populates="bookings"
    )

    payments = relationship(
        "Payment",
        back_populates="booking",
        cascade="all, delete-orphan"
    )


# =====================================================
# Payment
# =====================================================

class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    booking_id: Mapped[int | None] = mapped_column(
        ForeignKey("bookings.id"),
        nullable=True
    )

    amount: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    payment_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )
    # Examples:
    # Membership
    # Trial Upgrade
    # Court Booking
    # Coaching Fee

    payment_method: Mapped[str] = mapped_column(
        String(30),
        default="UPI"
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="Paid"
    )

    payment_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    transaction_id: Mapped[str] = mapped_column(
        String(100),
        unique=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    # Relationships

    user = relationship(
        "User",
        back_populates="payments"
    )

    booking = relationship(
        "Booking",
        back_populates="payments"
    )


# =====================================================
# Pending Actions
# =====================================================

class PendingAction(Base):
    __tablename__ = "pending_actions"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    action: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )
    # extend_membership
    # extend_trial
    # cancel_booking
    # update_phone

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    payload: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="pending"
    )
    # pending
    # approved
    # rejected

    requested_by: Mapped[str] = mapped_column(
        String(100),
        default="Vendor"
    )

    approved_by: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    # Relationships

    user = relationship(
        "User",
        back_populates="pending_actions"
    )

# =====================================================
# Audit Log
# =====================================================

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    vendor_id: Mapped[int] = mapped_column(
        ForeignKey("vendors.id"),
        nullable=False
    )

    action: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    target_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )
    # User
    # Booking
    # Payment

    target_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    performed_by: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    details: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    vendor = relationship(
        "Vendor",
        back_populates="audit_logs"
    )


# =====================================================
# Conversation History
# =====================================================

class Conversation(Base):
    __tablename__ = "conversations"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    vendor_id: Mapped[int] = mapped_column(
        ForeignKey("vendors.id"),
        nullable=False
    )

    session_id: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True
    )

    role: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )
    # user
    # assistant

    message: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    vendor = relationship(
        "Vendor",
        back_populates="conversations"
    )


# =====================================================
# Notification
# =====================================================

class Notification(Base):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    vendor_id: Mapped[int] = mapped_column(
        ForeignKey("vendors.id"),
        nullable=False
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    message: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    notification_type: Mapped[str] = mapped_column(
        String(50),
        default="info"
    )
    # info
    # success
    # warning
    # error

    is_read: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    vendor = relationship(
        "Vendor",
        back_populates="notifications"
    )


# =====================================================
# Tool Execution Logs
# =====================================================

class ToolExecution(Base):
    __tablename__ = "tool_executions"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    vendor_id: Mapped[int] = mapped_column(
        ForeignKey("vendors.id"),
        nullable=False
    )

    tool_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    user_query: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    tool_input: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    tool_output: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    success: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    execution_time_ms: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    vendor = relationship(
        "Vendor",
        back_populates="tool_logs"
    )