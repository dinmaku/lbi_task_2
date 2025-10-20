from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask import request, jsonify
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from sqlalchemy import LargeBinary
from werkzeug.utils import secure_filename
import base64
import jwt
import datetime
from datetime import date
import re
import logging
import os



app = Flask(__name__)
CORS(app, supports_credentials=True, origins=["http://localhost:5173"])

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+pg8000://postgres:1234@localhost/lbi_user_management'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'access_token'

# ✅ Define UPLOAD_FOLDER after app is created
UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Make sure the folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)




logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

db = SQLAlchemy(app)

class TaskType(db.Model):
    __tablename__ = 'task_type'

    task_type_id = db.Column(db.Integer, primary_key=True)
    task_type_name = db.Column(db.String(225), nullable=False, unique=True)

    # Relationship to tasks
    tasks = db.relationship('Tasks', back_populates='task_type', cascade='all, delete')

    def serialize(self):
        return {
            'task_type_id': self.task_type_id,
            'task_type_name': self.task_type_name
        }


class Tasks(db.Model):
    __tablename__ = 'tasks'

    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(225), nullable=True)
    description = db.Column(db.String(225), nullable=True)
    created_at = db.Column(db.Date, default=date.today)
    status = db.Column(db.String(225), nullable=True, default='Pending')
    task_type_id = db.Column(db.Integer, db.ForeignKey('task_type.task_type_id'))

    # Relationship to TaskType
    task_type = db.relationship('TaskType', back_populates='tasks')

    # Many-to-many relationship to users via task_by_user
    users = db.relationship('Users', secondary='task_by_user', back_populates='tasks')

    # One-to-many relationship to TasksAssigned
    assigned = db.relationship('TasksAssigned', back_populates='task', cascade='all, delete-orphan')

    def serialize(self):
        return {
            'task_id': self.task_id,
            'title': self.title,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'status': self.status,
            'task_type': self.task_type.serialize() if self.task_type else None,
            'task_type_name': self.task_type.task_type_name if self.task_type else None,
            'users': [user.serialize() for user in self.users]
        }

    def serialize_basic(self):
        return {
            'task_id': self.task_id,
            'title': self.title,
            'status': self.status,
            'task_type_name': self.task_type.task_type_name if self.task_type else None
        }

class Users(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(225))
    lastname = db.Column(db.String(225))
    username = db.Column(db.String(225))
    email = db.Column(db.String(225))
    password = db.Column(db.String(225))
    contact = db.Column(db.String(225))
    address = db.Column(db.String(225))
    user_type = db.Column(db.String(255))
    status = db.Column(db.String(50), default='Active')
    image = db.Column(db.String(225))

    tasks_assigned = db.relationship('TasksAssigned', back_populates='user', cascade='all, delete-orphan')
    tasks = db.relationship('Tasks', secondary='task_by_user', back_populates='users')

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
            'status': self.status,
            'image': self.image,
            'tasks': [task.serialize_basic() for task in self.tasks]
        }


class TasksAssigned(db.Model):
    __tablename__ = 'task_by_user'

    task_user_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.task_id'), nullable=False)

    user = db.relationship('Users', back_populates='tasks_assigned')
    task = db.relationship('Tasks', back_populates='assigned')

    def serialize(self):
        return {
            'task_user_id': self.task_user_id,
            'user_id': self.user_id,
            'task_id': self.task_id,
            'task': self.task.serialize() if self.task else None,
            'user': self.user.serialize() if self.user else None
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
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=10)  
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

#Fetch User Profile
@app.route('/users/profile', methods=['GET'])
def get_user_profile():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'status': 'error', 'message': 'Missing or invalid token'}), 401

    token = auth_header.split(' ')[1]

    try:
        decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        current_user_id = decoded['user_id']
    except jwt.ExpiredSignatureError:
        return jsonify({'status': 'error', 'message': 'Token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'status': 'error', 'message': 'Invalid token'}), 401

    user = Users.query.get(current_user_id)
    if user:
        return jsonify({'status': 'success', 'data': user.serialize()}), 200
    else:
        return jsonify({'status': 'error', 'message': 'User not found'}), 404

#Update User Profile
@app.route('/api/admin/update-profile', methods=['PUT'])
def update_profile():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'status': 'error', 'message': 'Missing or invalid token'}), 401

    token = auth_header.split(' ')[1]

    try:
        decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        user_id = decoded['user_id']
    except jwt.ExpiredSignatureError:
        return jsonify({'status': 'error', 'message': 'Token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'status': 'error', 'message': 'Invalid token'}), 401

    user = Users.query.get(user_id)
    if not user:
        return jsonify({'status': 'error', 'message': 'User not found'}), 404

    data = request.get_json()
    user.firstname = data.get('firstname', user.firstname)
    user.lastname = data.get('lastname', user.lastname)
    user.username = data.get('username', user.username)
    user.contact = data.get('contact', user.contact)
    user.address = data.get('address', user.address)

    try:
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Profile updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': 'Failed to update profile'}), 500

#Change Password
@app.route('/api/admin/change-password', methods=['POST'])
def change_password():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'status': 'error', 'message': 'Missing or invalid token'}), 401

    token = auth_header.split(' ')[1]

    try:
        decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        user_id = decoded['user_id']
    except jwt.ExpiredSignatureError:
        return jsonify({'status': 'error', 'message': 'Token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'status': 'error', 'message': 'Invalid token'}), 401

    data = request.get_json()
    current_password = data.get('current_password')
    new_password = data.get('new_password')

    user = Users.query.get(user_id)
    if not user:
        return jsonify({'status': 'error', 'message': 'User not found'}), 404

    if not check_password_hash(user.password, current_password):
        return jsonify({'status': 'error', 'message': 'Current password is incorrect'}), 400

    user.password = generate_password_hash(new_password)

    try:
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Password changed successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': 'Failed to change password'}), 500        

#Upload Profile Picture
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/update-profile-picture', methods=['POST'])
def update_profile_picture():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        print('❌ Missing or invalid token')
        return jsonify({'status': 'error', 'message': 'Missing or invalid token'}), 401

    token = auth_header.split(' ')[1]
    try:
        decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        user_id = decoded['user_id']
        print('✅ Token decoded, user_id:', user_id)
    except jwt.ExpiredSignatureError:
        print('❌ Token expired')
        return jsonify({'status': 'error', 'message': 'Token expired'}), 401
    except jwt.InvalidTokenError:
        print('❌ Invalid token')
        return jsonify({'status': 'error', 'message': 'Invalid token'}), 401

    if 'profile_image' not in request.files:
        print('❌ No image file provided')
        return jsonify({'status': 'error', 'message': 'No image file provided'}), 400

    file = request.files['profile_image']
    if file.filename == '' or not allowed_file(file.filename):
        print('❌ Invalid file type:', file.filename)
        return jsonify({'status': 'error', 'message': 'Invalid file type'}), 400

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    print('📁 Saving file to:', filepath)

    try:
        file.save(filepath)
    except Exception as e:
        print('❌ File save error:', e)
        return jsonify({'status': 'error', 'message': 'Failed to save image'}), 500

    user = Users.query.get(user_id)
    if not user:
        print('❌ User not found')
        return jsonify({'status': 'error', 'message': 'User not found'}), 404

    user.image = filename
    try:
        db.session.commit()
        image_url = f"/static/uploads/{filename}"
        return jsonify({
            'status': 'success',
            'data': {
                'image_url': image_url
            }
        }), 200
    except Exception as e:
        print('❌ DB commit error:', e)
        db.session.rollback()
        return jsonify({'status': 'error', 'message': 'Failed to update profile picture'}), 500


#Add Account
def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

@app.route('/addAccount', methods=['POST'])
def add_account():
    try:
        data = request.get_json()
        default_image = '../assets/img/default_profile.png'
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
        status = 'Active',
        image = data.get('image', default_image).strip()

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
                status=status,
                image=image
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

@app.route('/task_types', methods=['GET'])
def get_task_types():
    try:
        task_types = TaskType.query.all()
        return jsonify([task_type.serialize() for task_type in task_types]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/add_task_type', methods=['POST'])
def add_task_type():
    data = request.get_json()
    name = data.get('task_type_name')

    if not name:
        return jsonify({'error': 'task_type_name is required'}), 400

    existing = TaskType.query.filter_by(task_type_name=name).first()
    if existing:
        return jsonify({'message': 'Task type already exists'}), 200

    new_type = TaskType(task_type_name=name)
    db.session.add(new_type)
    db.session.commit()
    return jsonify({'message': 'Task type added successfully'}), 201

@app.route('/assign_task', methods=['POST'])
def assign_task():
    data = request.get_json()
    task_id = data.get('task_id')
    user_ids = data.get('user_ids', [])

    try:
        for user_id in user_ids:
            existing = TasksAssigned.query.filter_by(task_id=task_id, user_id=user_id).first()
            if not existing:
                assignment = TasksAssigned(task_id=task_id, user_id=user_id)
                db.session.add(assignment)

        db.session.commit()
        return jsonify({'message': 'Users assigned successfully'}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/create_task', methods=['POST'])
def create_task():
    try:
        data = request.get_json()

        title = data.get('title')
        description = data.get('description')
        task_type_id = data.get('task_type_id')
        assigned_user_ids = data.get('assigned_user_ids', [])

        # 🔒 Require all required fields including assignment
        if not title or not description or not task_type_id or not assigned_user_ids:
            return jsonify({'error': 'Please fill in all required fields and assign at least one user.'}), 400

        new_task = Tasks(
            title=title,
            description=description,
            task_type_id=task_type_id,
            created_at=date.today(),
            status='Pending'
        )
        db.session.add(new_task)
        db.session.commit()

        for user_id in assigned_user_ids:
            db.session.add(TasksAssigned(task_id=new_task.task_id, user_id=user_id))
        
        db.session.commit()

        return jsonify({'message': 'Task created successfully'}), 201

    except Exception as e:
        db.session.rollback()
        print('Error creating task:', str(e))
        return jsonify({'error': 'An error occurred while creating the task.'}), 500



@app.route('/fetch_tasks', methods=['GET'])
def fetch_tasks():
    try:
        from sqlalchemy.orm import joinedload

        tasks = Tasks.query.options(
            joinedload(Tasks.users),         # Load assigned users
            joinedload(Tasks.task_type)      # Load task type
        ).all()

        return jsonify([task.serialize() for task in tasks]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


      


if __name__ == '__main__':
    app.run(debug=True)