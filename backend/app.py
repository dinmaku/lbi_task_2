from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import cast, Date
from flask_cors import CORS
from flask import request, jsonify
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from sqlalchemy import LargeBinary, cast, DateTime
from werkzeug.utils import secure_filename
import base64
import jwt
from datetime import datetime, timedelta, timezone
import re
import logging
import os
import traceback



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
    created_at = db.Column(db.DateTime, default=datetime.today)
    deadline = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(225), nullable=True, default='Pending')
    task_type_id = db.Column(db.Integer, db.ForeignKey('task_type.task_type_id'))

    # Relationship to TaskType
    task_type = db.relationship('TaskType', back_populates='tasks')

    # Many-to-many relationship to users via task_by_user
    users = db.relationship('Users', secondary='task_by_user', back_populates='tasks')

    # One-to-many relationship to TasksAssigned
    assigned = db.relationship('TasksAssigned', back_populates='task', cascade='all, delete-orphan')

    # One-to-many relationship to TaskComments
    comments = db.relationship('TaskComments', back_populates='task', cascade='all, delete-orphan')

    def serialize(self):
        return {
            'task_id': self.task_id,
            'title': self.title,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'deadline': self.deadline,
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
    comments = db.relationship('TaskComments', back_populates='user', cascade='all, delete-orphan')

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

class TaskComments(db.Model):
    __tablename__ = 'comments'

    comment_id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.task_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    task = db.relationship('Tasks', back_populates='comments')
    user = db.relationship('Users', back_populates='comments')

    def serialize(self):
        return {
            'comment_id': self.comment_id,
            'task_id': self.task_id,
            'user_id': self.user_id,
            'message': self.message,
            'created_at': self.created_at.isoformat(),
            'user_name': f"{self.user.firstname} {self.user.lastname}" if self.user else None,
            'user_image': self.user.image if self.user else None
        }

class Conversation(db.Model):
    __tablename__ = 'conversations'

    conversation_id = db.Column(db.Integer, primary_key=True)
    user_id_1 = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    user_id_2 = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    user1 = db.relationship('Users', foreign_keys=[user_id_1], backref='conversations_started')
    user2 = db.relationship('Users', foreign_keys=[user_id_2], backref='conversations_received')
    messages = db.relationship('Message', backref='conversation', cascade='all, delete-orphan')

    __table_args__ = (
        db.UniqueConstraint('user_id_1', 'user_id_2', name='unique_users_pair'),
    )

    def to_dict(self):
        return {
            "conversation_id": self.conversation_id,
            "user_id_1": self.user_id_1,
            "user_id_2": self.user_id_2,
            "created_at": self.created_at.isoformat()
        }


class Message(db.Model):
    __tablename__ = 'messages'

    message_id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversations.conversation_id', ondelete='CASCADE'), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    message = db.Column(db.Text)
    image = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    sender = db.relationship('Users', backref='sent_messages')

    def to_dict(self):
        return {
            "message_id": self.message_id,
            "conversation_id": self.conversation_id,
            "sender_id": self.sender_id,
            "message": self.message,
            "image": self.image,
            "created_at": self.created_at.isoformat()
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
        'exp': datetime.utcnow() + timedelta(hours=10)
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

        
        logger.info(f"Received registration data: {data}")

      
        email = data.get('email', '').strip()
        firstname = data.get('firstname', '').strip()
        lastname = data.get('lastname', '').strip()
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        contact = data.get('contact', '').strip()
        address = data.get('address', '').strip()
        user_type = data.get('user_type', '').strip()
        status = 'Active'
        image = data.get('image', default_image).strip()


        if not all([email, firstname, lastname, username, password, contact, address, user_type]):
            logger.warning("Missing required fields")
            return jsonify({"error": "All fields are required"}), 400

       
        if not is_valid_email(email):
            logger.warning(f"Invalid email format: {email}")
            return jsonify({"error": "Invalid email format"}), 400

    
        existing_user = Users.query.filter_by(email=email).first()
        if existing_user:
            logger.warning(f"Email already exists: {email}")
            return jsonify({"error": "User with this email already exists"}), 400

       
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
        deadline = data.get('deadline')
        task_type_id = data.get('task_type_id')
        assigned_user_ids = data.get('assigned_user_ids', [])

       
        if not title or not description or not task_type_id or not assigned_user_ids:
            return jsonify({'error': 'Please fill in all required fields and assign at least one user.'}), 400

        new_task = Tasks(
            title=title,
            description=description,
            deadline=deadline,
            task_type_id=task_type_id,
            created_at=datetime.today(),
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
            joinedload(Tasks.users),        
            joinedload(Tasks.task_type)     
        ).all()

        return jsonify([task.serialize() for task in tasks]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/update_task/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    try:
        data = request.get_json()

        task = Tasks.query.get(task_id)
        if not task:
            return jsonify({'error': 'Task not found'}), 404

        
        task.title = data.get('title', task.title)
        task.description = data.get('description', task.description)
        task.deadline = data.get('deadline', task.deadline)
        task.task_type_id = data.get('task_type_id', task.task_type_id)
        task.status = data.get('status', task.status)

       
        if 'assigned_user_ids' in data:
           
            TasksAssigned.query.filter_by(task_id=task_id).delete()

         
            for user_id in data['assigned_user_ids']:
                db.session.add(TasksAssigned(task_id=task_id, user_id=user_id))

        db.session.commit()
        return jsonify({'message': 'Task updated successfully'}), 200

    except Exception as e:
        db.session.rollback()
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/fetch_tasks_user/<int:user_id>', methods=['GET'])
def fetch_tasks_per_user(user_id):
    try:
        
        user_tasks = (
            db.session.query(Tasks)
            .join(TasksAssigned, Tasks.task_id == TasksAssigned.task_id)
            .filter(TasksAssigned.user_id == user_id)
            .all()
        )

        if not user_tasks:
            return jsonify({'message': 'No tasks found for this user'}), 200

      
        return jsonify([task.serialize() for task in user_tasks]), 200

    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/update_task_status/<int:task_id>', methods=['PUT'])
def update_task_status(task_id):
    try:
        data = request.get_json()
        new_status = data.get('status')

        if new_status not in ['Pending', 'In Progress', 'Done', 'Cancelled']:
            return jsonify({'error': 'Invalid status value'}), 400

        task = Tasks.query.get(task_id)
        if not task:
            return jsonify({'error': 'Task not found'}), 404

        task.status = new_status
        db.session.commit()

        return jsonify({'message': 'Task status updated successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/task_stats', methods=['GET'])
def get_task_stats():
    try:
        # Use full datetime instead of just date
        now = datetime.utcnow()               # current UTC datetime
        one_month_ago = now - timedelta(days=30)

        # Count totals
        total_done = Tasks.query.filter_by(status='Done').count()
        total_ongoing = Tasks.query.filter(Tasks.status.in_(['Pending', 'Work in Progress'])).count()
        total_cancelled = Tasks.query.filter_by(status='Cancelled').count()

        # Count tasks created in the last month (datetime-aware)
        done_last_month = Tasks.query.filter(
            Tasks.status == 'Done',
            cast(Tasks.created_at, DateTime) >= one_month_ago
        ).count()

        ongoing_last_month = Tasks.query.filter(
            Tasks.status.in_(['Pending', 'Work in Progress']),
            cast(Tasks.created_at, DateTime) >= one_month_ago
        ).count()

        cancelled_last_month = Tasks.query.filter(
            Tasks.status == 'Cancelled',
            cast(Tasks.created_at, DateTime) >= one_month_ago
        ).count()

        # Helper function for growth %
        def calc_growth(current, last_month):
            if last_month == 0:
                return 100.0 if current > 0 else 0.0
            return round(((current - last_month) / last_month) * 100, 2)

        # Return stats
        stats = {
            'done': {'count': total_done, 'growth': calc_growth(total_done, done_last_month)},
            'ongoing': {'count': total_ongoing, 'growth': calc_growth(total_ongoing, ongoing_last_month)},
            'cancelled': {'count': total_cancelled, 'growth': calc_growth(total_cancelled, cancelled_last_month)}
        }

        return jsonify(stats), 200

    except Exception as e:
        print("Error in /task_stats:", e)
        return jsonify({'error': str(e)}), 500


@app.route('/tasks/<int:task_id>/comments', methods=['GET'])
def get_task_comments(task_id):
    try:
        # Query all comments for this task, most recent first
        comments = (
            db.session.query(TaskComments)
            .filter_by(task_id=task_id)
            .order_by(TaskComments.created_at.desc())
            .all()
        )

        if not comments:
            return jsonify([]), 200  # return empty list, not error

        # Serialize each comment including user info
        result = []
        for comment in comments:
            user = Users.query.get(comment.user_id)
            result.append({
                "comment_id": comment.comment_id,
                "task_id": comment.task_id,
                "user_id": comment.user_id,
                "user_name": f"{user.firstname} {user.lastname}" if user else "Unknown User",
                "user_image": user.image if user else None,
                "message": comment.message,
                "created_at": comment.created_at.strftime("%Y-%m-%d %H:%M:%S")
            })

        return jsonify(result), 200

    except Exception as e:
        print("Error in /tasks/<task_id>/comments:", e)
        return jsonify({"error": str(e)}), 500

@app.route('/tasks/<int:task_id>/comments', methods=['POST'])
def add_task_comment(task_id):
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        message = data.get('message', '').strip()

        if not user_id or not message:
            return jsonify({'error': 'user_id and message are required'}), 400

        # Verify task exists
        task = Tasks.query.get(task_id)
        if not task:
            return jsonify({'error': 'Task not found'}), 404

        # Verify user exists
        user = Users.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Create new comment
        new_comment = TaskComments(
            task_id=task_id,
            user_id=user_id,
            message=message,
            created_at=datetime.utcnow()
        )
        db.session.add(new_comment)
        db.session.commit()

        return jsonify({'message': 'Comment added successfully'}), 201

    except Exception as e:
        db.session.rollback()
        print("Error in POST /tasks/<task_id>/comments:", e)
        return jsonify({'error': str(e)}), 500


@app.route('/conversations/<int:user_id>', methods=['GET'])
def get_user_conversations(user_id):
    try:
        # Get all conversations where the user is either user1 or user2
        conversations = Conversation.query.filter(
            (Conversation.user_id_1 == user_id) | (Conversation.user_id_2 == user_id)
        ).all()

        if not conversations:
            return jsonify({'message': 'No conversations found'}), 404

        conversation_list = []
        for convo in conversations:
            # Determine the other user in the conversation
            other_user_id = convo.user_id_2 if convo.user_id_1 == user_id else convo.user_id_1
            other_user = Users.query.get(other_user_id)

            conversation_list.append({
                'conversation_id': convo.conversation_id,
                'other_user': {
                    'user_id': other_user.user_id,
                    'firstname': other_user.firstname,
                    'lastname': other_user.lastname,
                    'image': other_user.image
                },
                'created_at': convo.created_at
            })

        return jsonify(conversation_list), 200

    except Exception as e:
        print("Error in GET /conversations/<user_id>:", e)
        return jsonify({'error': str(e)}), 500

@app.route('/conversations/<int:user1_id>/<int:user2_id>', methods=['GET'])
def get_or_create_conversation(user1_id, user2_id):
    try:
        convo = Conversation.query.filter(
            db.or_(
                db.and_(Conversation.user_id_1 == user1_id, Conversation.user_id_2 == user2_id),
                db.and_(Conversation.user_id_1 == user2_id, Conversation.user_id_2 == user1_id)
            )
        ).first()

        # Create if not exists
        if not convo:
            convo = Conversation(user_id_1=user1_id, user_id_2=user2_id)
            db.session.add(convo)
            db.session.commit()

        print(f"✅ Conversation found/created: {convo.conversation_id} for users {user1_id} & {user2_id}")

        return jsonify({
            'conversation_id': convo.conversation_id,
            'user_id_1': convo.user_id_1,
            'user_id_2': convo.user_id_2
        }), 200

    except Exception as e:
        print("Error in get_or_create_conversation:", e)
        return jsonify({'error': str(e)}), 500


@app.route('/messages/<int:conversation_id>', methods=['GET'])
def get_conversation_messages(conversation_id):
    try:
        messages = (
            Message.query
            .filter_by(conversation_id=conversation_id)
            .order_by(Message.created_at.asc())  # FIFO order
            .all()
        )

        if not messages:
            return jsonify({'message': 'No messages found'}), 404

        message_list = []
        for msg in messages:
            sender = Users.query.get(msg.sender_id)
            message_list.append({
                'message_id': msg.message_id,
                'sender': {
                    'user_id': sender.user_id,
                    'firstname': sender.firstname,
                    'lastname': sender.lastname,
                    'image': sender.image
                },
                'message': msg.message,
                'image': msg.image,
                'created_at': msg.created_at.isoformat() 
            })

        return jsonify(message_list), 200

    except Exception as e:
        print("Error in GET /messages/<conversation_id>:", e)
        return jsonify({'error': str(e)}), 500


@app.route('/messages', methods=['POST'])
def send_message():
    try:
        data = request.get_json()
        conversation_id = data.get('conversation_id')
        sender_id = data.get('sender_id')
        message_text = data.get('message', None)
        image = data.get('image', None)

        if not conversation_id or not sender_id:
            return jsonify({'error': 'Missing required fields'}), 400

        new_message = Message(
            conversation_id=conversation_id,
            sender_id=sender_id,
            message=message_text,
            image=image
        )

        db.session.add(new_message)
        db.session.commit()

        return jsonify({
            'message_id': new_message.message_id,
            'message': new_message.message,
            'created_at': new_message.created_at
        }), 201

    except Exception as e:
        print("Error in POST /messages:", e)
        return jsonify({'error': str(e)}), 500

      


if __name__ == '__main__':
    app.run(debug=True)