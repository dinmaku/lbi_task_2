from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask import request, jsonify
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from sqlalchemy import LargeBinary
import base64
import jwt
import datetime
import re
import logging


app = Flask(__name__)
CORS(app, supports_credentials=True, origins=["http://localhost:5173"])

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+pg8000://postgres:1234@localhost/lbi_user_management'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'access_token'


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

db = SQLAlchemy(app)

class Users(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(225), nullable=True)
    lastname = db.Column(db.String(225), nullable=True)
    username = db.Column(db.String(225), nullable=True)
    email = db.Column(db.String(225), nullable=True)
    password = db.Column(db.String(225), nullable=True)
    contact = db.Column(db.String(225), nullable=True)
    address = db.Column(db.String(225), nullable=True)
    user_type = db.Column(db.String(255), nullable=True) 
    status = db.Column(db.String(50), nullable=True, default='Active')

    def serialize(self):
        return {
            'user_id': self.user_id,
            'firstName': self.firstname,
            'lastName': self.lastname,
            'username': self.username,
            'email': self.email,
            'contact': self.contact,
            'address': self.address,
            'user_type': self.user_type,
            'status': self.status
        }

#Login Route
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    status = 'Active'

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    user = Users.query.filter_by(email=email).first()

    if user.status != 'Active':
        return jsonify({"error": "User account is inactive"}), 403


     # Verify password

    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid email or password"}), 401

        

    # Generate JWT
    token_payload = {
        'user_id': user.user_id,
        'email': user.email,
        'user_type': user.user_type,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2)  # expires in 2 hours
    }

    token = jwt.encode(token_payload, app.config['SECRET_KEY'], algorithm='HS256')

    return jsonify({
        "message": "Login successful",
        "access_token": token,
        "user": user.serialize()
    }), 200

#Fetch Users
@app.route('/users', methods=['GET'])
def get_users():
    users = Users.query.all()
    return jsonify([user.serialize() for user in users]), 200

#Add Account
def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

@app.route('/addAccount', methods=['POST'])
def add_account():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Log received data
        logger.info(f"Received registration data: {data}")

        # Extract data with default values
        email = data.get('email', '').strip()
        firstname = data.get('firstname', '').strip()
        lastname = data.get('lastname', '').strip()
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        contact = data.get('contact', '').strip()
        address = data.get('address', '').strip()
        user_type = data.get('user_type', '').strip()
        status = 'Active'

        # Validate required fields
        if not all([email, firstname, lastname, username, password, contact, address, user_type]):
            logger.warning("Missing required fields")
            return jsonify({"error": "All fields are required"}), 400

        # Validate email format
        if not is_valid_email(email):
            logger.warning(f"Invalid email format: {email}")
            return jsonify({"error": "Invalid email format"}), 400

        # Check for existing user
        existing_user = Users.query.filter_by(email=email).first()
        if existing_user:
            logger.warning(f"Email already exists: {email}")
            return jsonify({"error": "User with this email already exists"}), 400

        # Hash password and create new user
        try:
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
            
            logger.info(f"Successfully created user: {email}")
            return jsonify({
                "message": "User created successfully", 
                "user": new_user.serialize()
            }), 201

        except Exception as e:
            db.session.rollback()
            logger.error(f"Database error: {str(e)}")
            return jsonify({"error": "Failed to create user"}), 500

    except Exception as e:
        logger.error(f"Server error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/update_account/<int:userid>', methods=['PUT'])
def edit_staff(userid):
    try:
        data = request.get_json(force=True, silent=True) or {}

        # Validate required fields
        required_fields = ['firstname', 'lastname', 'username', 'email', 'address', 'contact', 'user_type']
        if not all(data.get(field) for field in required_fields):
            logger.warning("Missing required fields")
            logger.info(f"Received data: {data}")
            return jsonify({"message": "All fields are required"}), 400

        # Validate email format
        if not is_valid_email(data['email']):
            logger.warning(f"Invalid email format: {data['email']}")
            return jsonify({"message": "Invalid email format"}), 400

        # Find user by ID
        user = Users.query.get(userid)
        if not user:
            logger.warning(f"User not found: {userid}")
            return jsonify({"message": "User not found"}), 404

      
        if data['email'] != user.email:
            existing = Users.query.filter_by(email=data['email']).first()
            if existing:
                logger.warning(f"Email already exists: {data['email']}")
                return jsonify({"message": "Email already exists"}), 400

       
        user.firstname = data['firstname'].strip()
        user.lastname = data['lastname'].strip()
        user.username = data['username'].strip()
        user.email = data['email'].strip()
        user.address = data['address'].strip()
        user.contact = data['contact'].strip()
        user.user_type = data['user_type'].strip()

        db.session.commit()

        logger.info(f"User updated successfully: {user.email}")
        return jsonify({
            "message": "Staff updated successfully",
            "user": user.serialize()
        }), 200

    except Exception as e:
        db.session.rollback()
        logger.info(f"Received data: {data}")
        logger.error(f"Error updating user: {e}")
        return jsonify({"message": "Internal server error"}), 500

@app.route('/update_status/<int:userid>', methods=['PUT'])
def update_status(userid):
    try:
        data = request.get_json(force=True, silent=True) or {}
        new_status = data.get('status', '').strip()

        if new_status not in ['Active', 'Inactive']:
            logger.warning(f"Invalid status value: {new_status}")
            return jsonify({"message": "Invalid status value"}), 400

        user = Users.query.get(userid)
        if not user:
            logger.warning(f"User not found: {userid}")
            return jsonify({"message": "User not found"}), 404

        user.status = new_status
        db.session.commit()

        logger.info(f"User status updated successfully: {user.email} to {new_status}")
        return jsonify({
            "message": "User status updated successfully",
            "user": user.serialize()
        }), 200

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating user status: {e}")
        return jsonify({"message": "Internal server error"}), 500


@app.route('/inactive_users', methods=['GET'])
def get_inactive_users():
    try:
        
        inactive_users = Users.query.filter_by(status='Inactive').all()
        
       
        logger.info(f"Found {len(inactive_users)} inactive users")
        
        
        serialized_users = [user.serialize() for user in inactive_users]
        
        return jsonify({
            'message': 'Inactive users retrieved successfully',
            'inactive_users': serialized_users
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching inactive users: {str(e)}")
        return jsonify({
            'error': 'Failed to fetch inactive users'
        }), 500



if __name__ == '__main__':
    app.run(debug=True)