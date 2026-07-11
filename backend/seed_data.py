from datetime import date, timedelta
import random

from faker import Faker

from database import Base, engine, SessionLocal

from models import (
    Vendor,
    User,
    Coach,
    Booking,
    Payment,
    PendingAction,
    AuditLog,
    Conversation,
    Notification,
    ToolExecution
)

fake = Faker("en_IN")


# -----------------------------------
# Reset Database
# -----------------------------------

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

db = SessionLocal()


# -----------------------------------
# Create Vendor
# -----------------------------------

vendor = Vendor(

    name="Vansh Mittal",

    email="vendor@hobbyfi.com",

    phone="9876543210",

    academy_name="HobbyFi Sports Arena",

    city="Delhi"

)

db.add(vendor)

db.commit()

db.refresh(vendor)

print("Vendor Created")


# -----------------------------------
# Coaches
# -----------------------------------

sports = [
    "Badminton",
    "Football",
    "Cricket",
    "Tennis"
]

coach_names = [

    "Rohit Sharma",

    "Amit Verma",

    "Priya Kapoor",

    "Ankit Singh",

    "Rahul Jain",

    "Sneha Mehta",

    "Karan Arora",

    "Neha Gupta"

]

coaches = []

for i in range(8):

    coach = Coach(

        vendor_id=vendor.id,

        name=coach_names[i],

        sport=random.choice(sports),

        phone=fake.phone_number(),

        experience=random.randint(2,15),

        specialization=random.choice(

            [

                "Beginner",

                "Intermediate",

                "Professional"

            ]

        ),

        active=True

    )

    db.add(coach)

    coaches.append(coach)

db.commit()

print("Coaches Created")


# -----------------------------------
# Users
# -----------------------------------

membership_plans = [

    "Trial",

    "Silver",

    "Gold",

    "Platinum"

]

users = []

for i in range(20):

    trial = random.choice([True, False])

    expiry = date.today() + timedelta(
        days=random.randint(10,120)
    )

    trial_end = date.today() + timedelta(
        days=random.randint(2,10)
    )

    user = User(

        vendor_id=vendor.id,

        name=fake.name(),

        email=fake.email(),

        phone=fake.msisdn()[:10],

        hobby=random.choice(sports),

        membership_plan=(
            "Trial"
            if trial
            else random.choice(
                ["Silver","Gold","Platinum"]
            )
        ),

        membership_expiry=expiry,

        is_trial=trial,

        trial_end=trial_end,

        active=random.choice(
            [True, True, True, False]
        )

    )

    db.add(user)

    users.append(user)

db.commit()

print("Users Created")


# -----------------------------------
# Refresh ORM Objects
# -----------------------------------

for coach in coaches:
    db.refresh(coach)

for user in users:
    db.refresh(user)


print()

print("----------------------")
print("Seed Part 1 Complete")
print("----------------------")

print(f"Vendor : 1")
print(f"Coaches : {len(coaches)}")
print(f"Users : {len(users)}")
print()

# -----------------------------------
# Create Bookings
# -----------------------------------

booking_status = [

    "Confirmed",

    "Completed",

    "Cancelled"

]

courts = [

    "Court 1",

    "Court 2",

    "Court 3",

    "Court 4"

]

time_slots = [

    ("06:00 AM","07:00 AM"),

    ("07:00 AM","08:00 AM"),

    ("08:00 AM","09:00 AM"),

    ("05:00 PM","06:00 PM"),

    ("06:00 PM","07:00 PM"),

    ("07:00 PM","08:00 PM")

]

bookings = []

for _ in range(60):

    user = random.choice(users)

    hobby = user.hobby

    matching_coaches = [

        c for c in coaches

        if c.sport == hobby

    ]

    if matching_coaches:

        coach = random.choice(matching_coaches)

    else:

        coach = random.choice(coaches)

    slot = random.choice(time_slots)

    booking = Booking(

        user_id=user.id,

        coach_id=coach.id,

        booking_date=date.today() + timedelta(
            days=random.randint(-5,10)
        ),

        start_time=slot[0],

        end_time=slot[1],

        court=random.choice(courts),

        status=random.choice(booking_status),

        notes=random.choice(

            [

                "Regular practice",

                "Private coaching",

                "Tournament preparation",

                "Fitness session",

                None

            ]

        )

    )

    db.add(booking)

    bookings.append(booking)

db.commit()

for booking in bookings:

    db.refresh(booking)

print(f"Bookings Created : {len(bookings)}")

# -----------------------------------
# Create Payments
# -----------------------------------

payment_types = [

    "Membership",

    "Court Booking",

    "Coaching Fee",

    "Tournament Registration"

]

payment_methods = [

    "UPI",

    "Card",

    "Cash",

    "Net Banking"

]

payment_status = [

    "Paid",

    "Paid",

    "Paid",

    "Failed"

]

payments = []

for _ in range(80):

    booking = random.choice(bookings)

    user = booking.user

    payment = Payment(

        user_id=user.id,

        booking_id=booking.id,

        amount=random.choice(

            [

                199,

                299,

                499,

                799,

                999,

                1499,

                1999,

                2999

            ]

        ),

        payment_type=random.choice(payment_types),

        payment_method=random.choice(payment_methods),

        status=random.choice(payment_status),

        payment_date=date.today() + timedelta(

            days=random.randint(-15,0)

        ),

        transaction_id=f"TXN{random.randint(100000,999999)}"

    )

    db.add(payment)

    payments.append(payment)

db.commit()

print(f"Payments Created : {len(payments)}")

# -----------------------------------
# Revenue Summary
# -----------------------------------

today_revenue = sum(

    p.amount

    for p in payments

    if p.payment_date == date.today()

    and p.status == "Paid"

)

print()

print("-----------------------------")

print("Today's Revenue")

print(f"₹ {today_revenue}")

print("-----------------------------")

print()

print("Current Database")

print("------------------------")

print(f"Vendor      : 1")

print(f"Users       : {len(users)}")

print(f"Coaches     : {len(coaches)}")

print(f"Bookings    : {len(bookings)}")

print(f"Payments    : {len(payments)}")

print("------------------------")

print()

import json

# -----------------------------------
# Create Pending Actions
# -----------------------------------

actions = [

    "extend_membership",

    "extend_trial",

    "update_phone",

    "cancel_booking"

]

pending_actions = []

for _ in range(8):

    user = random.choice(users)

    action = random.choice(actions)

    payload = {}

    if action == "extend_membership":

        payload = {

            "days": random.choice([7,15,30])

        }

    elif action == "extend_trial":

        payload = {

            "days": random.choice([3,5,7])

        }

    elif action == "update_phone":

        payload = {

            "new_phone": fake.msisdn()[:10]

        }

    else:

        booking = random.choice(bookings)

        payload = {

            "booking_id": booking.id

        }

    pending = PendingAction(

        action=action,

        user_id=user.id,

        payload=json.dumps(payload),

        status="pending",

        requested_by="Vendor"

    )

    db.add(pending)

    pending_actions.append(pending)

db.commit()

print(f"Pending Actions : {len(pending_actions)}")

# -----------------------------------
# Notifications
# -----------------------------------

titles = [

    "Membership Extended",

    "Booking Cancelled",

    "Phone Updated",

    "Trial Extended",

    "Pending Approval"

]

notifications = []

for _ in range(12):

    notification = Notification(

        vendor_id=vendor.id,

        title=random.choice(titles),

        message=fake.sentence(),

        notification_type=random.choice(

            [

                "info",

                "success",

                "warning"

            ]

        ),

        is_read=random.choice(

            [True, False]

        )

    )

    db.add(notification)

    notifications.append(notification)

db.commit()

print(f"Notifications : {len(notifications)}")


# -----------------------------------
# Audit Logs
# -----------------------------------

audit_logs = []

for _ in range(15):

    user = random.choice(users)

    audit = AuditLog(

        vendor_id=vendor.id,

        action=random.choice(actions),

        target_type="User",

        target_id=user.id,

        performed_by="Vendor",

        details=fake.sentence()

    )

    db.add(audit)

    audit_logs.append(audit)

db.commit()

print(f"Audit Logs : {len(audit_logs)}")

# -----------------------------------
# Conversation History
# -----------------------------------

conversation_messages = [

    ("user","Show today's revenue"),

    ("assistant","Today's revenue is ₹14,999."),

    ("user","List badminton trial users."),

    ("assistant","Found 4 badminton trial users."),

    ("user","Extend Rahul's membership."),

    ("assistant","Approval required before updating.")

]

conversations = []

session_id = "session_001"

for role, message in conversation_messages:

    chat = Conversation(

        vendor_id=vendor.id,

        session_id=session_id,

        role=role,

        message=message

    )

    db.add(chat)

    conversations.append(chat)

db.commit()

print(f"Conversation Messages : {len(conversations)}")

# -----------------------------------
# Tool Execution Logs
# -----------------------------------

tool_names = [

    "get_today_revenue",

    "list_trial_users",

    "extend_membership",

    "cancel_booking",

    "get_dashboard_summary"

]

tool_logs = []

for _ in range(15):

    tool = ToolExecution(

        vendor_id=vendor.id,

        tool_name=random.choice(tool_names),

        user_query=fake.sentence(),

        tool_input="{}",

        tool_output="Success",

        success=random.choice(

            [True, True, True, False]

        ),

        execution_time_ms=random.randint(

            25,

            300

        )

    )

    db.add(tool)

    tool_logs.append(tool)

db.commit()

print(f"Tool Logs : {len(tool_logs)}")

# -----------------------------------
# Database Summary
# -----------------------------------

print()

print("=" * 50)

print("DATABASE SEEDED SUCCESSFULLY")

print("=" * 50)

print(f"Vendor           : 1")

print(f"Users            : {len(users)}")

print(f"Coaches          : {len(coaches)}")

print(f"Bookings         : {len(bookings)}")

print(f"Payments         : {len(payments)}")

print(f"Pending Actions  : {len(pending_actions)}")

print(f"Notifications    : {len(notifications)}")

print(f"Audit Logs       : {len(audit_logs)}")

print(f"Conversations    : {len(conversations)}")

print(f"Tool Executions  : {len(tool_logs)}")

print("=" * 50)

db.close()