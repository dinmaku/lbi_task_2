# create_account.py

from app import db, Users  # import db and model from app.py
from werkzeug.security import generate_password_hash

# This is important to make sure the app context is available when working with db
from app import app

with app.app_context():
    email = "user@example.com"
    firstname = "Test"
    lastname = "User"
    username = "testuser"
    password = "user123"
    contact = "1234567890"
    address = "123 Test Street"
    user_type = "admin"
    status = "Active"

    existing_user = Users.query.filter_by(email=email).first()
    if existing_user:
        print(f"User with email {email} already exists.")
    else:
        hashed_password = generate_password_hash(password)
        new_user = Users(
            email=email,
            firstname=firstname,
            lastname=lastname,
            username=username,
            password=hashed_password,
            contact=contact,
            address=address,
            user_type=user_type,
            status=status
        )
        db.session.add(new_user)
        db.session.commit()
        print(f"User {email} created successfully.")