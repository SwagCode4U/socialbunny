"""
Seed the theree Members or admin accounts : Hani Zeel Misbah 
Run this Once
"""

from app.database import SessionLocal
from app.models import User, UserRole
from app.utils import hash_password

admins = [
    {
        "username": "hani2902",
        "name": "Hani",
        "email": "hani@socialbunny.app",
        "password": "Hani203040@#",
        "referral_code": "ha8080k",
    },
    {
        "username": "zeel2901",
        "name": "Zeel",
        "email": "zeel@socialbunny.app",
        "password": "Zeel102030@#",
        "referral_code": "ze7070r",
    },
    {
        "username": "misbah2903",
        "name": "Misbah",
        "email": "misbah@socialbunny.app",
        "password": "Misbah304050@#",
        "referral_code": "mis9090v",
    },
]

db = SessionLocal()

for a in admins:
    exists = db.query(User).filter(User.username == a["username"]).first()
    if exists:
        print(f"  ⏭️  {a['name']} ({a['username']}) already exists, skipping")
        continue

    user =User(
        username=a["username"],
        name=a["name"],
        email=a["email"],
        role=UserRole.admin,
        password_hash=hash_password(a["password"]),
        referral_code=a["referral_code"],
    )
    db.add(user)
    db.commit()
    print(f"  ✅ {a['name']:7s} | username: {a['username']:10s} | ref_code: {a['referral_code']}")
db.close()
print("Done.")
