from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default="user")

class Dept(db.Model):
    __tablename__ = "Dept"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    manager_email = db.Column(db.String(120), nullable=True)
    description = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

class Staff(db.Model):
    __tablename__ = "staffs"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    dept_id = db.Column(db.Integer, db.ForeignKey("Dept.id"), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

class Project(db.Model):
    __tablename__ = "project"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    dept_id = db.Column(db.Integer, db.ForeignKey('Dept.id'), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    owner = db.relationship('User', backref=db.backref('owned_projects', lazy=True))
    dept = db.relationship('Dept', backref=db.backref('projects', lazy=True))
    tasks = db.relationship('TaskSetup', backref='project', lazy=True)
    files = db.relationship('File', backref='project', lazy=True)

class TaskSetup(db.Model):
    __tablename__ = "task_setups"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    dept_id = db.Column(db.Integer, db.ForeignKey("Dept.id"), nullable=False)
    status = db.Column(db.String(50), default="pending")
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

class File(db.Model):
    __tablename__ = 'file'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    task_id = db.Column(db.Integer, db.ForeignKey('task_setups.id'), nullable=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=True)

# Bảng phụ: Project-User, Project-Dept, Project-Followers, Task-Followers
project_user_link = db.Table('project_user_link',
    db.Column('project_id', db.Integer, db.ForeignKey('project.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)

project_group_link = db.Table('project_group_link',
    db.Column('project_id', db.Integer, db.ForeignKey('project.id'), primary_key=True),
    db.Column('dept_id', db.Integer, db.ForeignKey('Dept.id'), primary_key=True)
)

project_follower_link = db.Table('project_follower_link',
    db.Column('project_id', db.Integer, db.ForeignKey('project.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)

task_follower_link = db.Table('task_follower_link',
    db.Column('task_id', db.Integer, db.ForeignKey('task_setups.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)

# Sau khi khai báo bảng phụ thì có thể thêm relationship nhiều-nhiều
Project.assigned_users = db.relationship('User', secondary=project_user_link, backref='projects_assigned')
Project.assigned_groups = db.relationship('Dept', secondary=project_group_link, backref='projects_group_assigned')
Project.followers = db.relationship('User', secondary=project_follower_link, backref='projects_following')
TaskSetup.followers = db.relationship('User', secondary=task_follower_link, backref='tasks_following')
