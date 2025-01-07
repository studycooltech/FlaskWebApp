from functools import wraps
from flask import Blueprint, jsonify, request
from extensions import db
from blueprints.user.models import User
from sqlalchemy import text
import jwt
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the secret key from the environment
SECRET_KEY = os.getenv("JWT_SECRET_KEY")

user_bp = Blueprint('user_bp', __name__)




# Function to extract token from the Authorization header
def get_token_auth_header():
    auth = request.headers.get("Authorization", None)
    if not auth:
        return None, "Authorization header is expected"

    parts = auth.split()

    if parts[0].lower() != "bearer":
        return None, "Authorization header must start with Bearer"
    elif len(parts) == 1:
        return None, "Token not found"
    elif len(parts) > 2:
        return None, "Authorization header must be Bearer token"

    token = parts[1]
    return token, None


# Decorator for route protection
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token, error = get_token_auth_header()
        if error:
            return jsonify({'msg': error}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({'msg': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'msg': 'Invalid token'}), 401

        # Pass the decoded data to the decorated function
        return f(data, *args, **kwargs)
    
    return decorated

# @user_bp.route('/', methods=['GET'])
# def get_users():
#     # Fetch all users from the database
#     users = User.query.all()
#     return jsonify([user.to_dict() for user in users])  # Return user data as JSON
    


# Route for login
@user_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    name = data.get('name')

    # Replace with your authentication logic
    user = User.query.filter_by(email=email, name=name).first()
    if user:
        # Generate JWT token
        payload = {
            "name": name,
            "email": email
        }
        access_token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return jsonify(access_token=access_token), 200
    return jsonify({'msg': 'Invalid credentials'}), 401



# Protected route
@user_bp.route('/take', methods=['GET'])
@token_required
def take_msg(decoded_data):
    return {'message': f"Hello user {decoded_data['name']}"}, 200
  


@user_bp.route('/', methods=['GET'])
@token_required
def get_users(decoded_data):
    try:
        # Fetch users from the database
        result = db.session.execute(text('SELECT * FROM users'))
        columns = result.keys()
        users = [dict(zip(columns, row)) for row in result.fetchall()]
        return jsonify(users), 200
    except Exception as e:
        return jsonify({'msg': str(e)}), 500




# @user_bp.route('/', methods=['POST'])
# def add_user():
#     # Get user data from the request body
#     data = request.json
    
#     # Create a new User instance
#     new_user = User(name=data['name'], email=data['email'])
    
#     # Add the new user to the session and commit to the database
#     db.session.add(new_user)
#     db.session.commit()
    
#     # Return the newly created user data as JSON with a 201 status
#     return jsonify(new_user.to_dict()), 201


@user_bp.route('/', methods=['POST'])
def add_user():
    # Get user data from the request body
    data = request.json
    
    # Prepare the raw SQL query to insert a new user
    query = text('''
        INSERT INTO users (name, email) 
        VALUES (:name, :email)
    ''')
    
    # Execute the query
    db.session.execute(query, {'name': data['name'], 'email': data['email']})
    
    # Commit the changes to the database
    db.session.commit()
    
    # Fetch the newly created user by email (or other unique identifier)
    result = db.session.execute(
        text("SELECT * FROM users WHERE email = :email"),
        {'email': data['email']}
    )
    user = result.fetchone()
    
    # Convert the result to a dictionary and return it
    return jsonify(dict(zip(result.keys(), user))), 201







