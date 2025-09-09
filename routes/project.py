from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Project, User, Dept

project_bp = Blueprint('project', __name__, template_folder='templates/project')

# List all projects
@project_bp.route('/projects')
def list_projects():
    projects = Project.query.all()
    users = User.query.all()
    depts = Dept.query.all()
    return render_template('projects.html', projects=projects, users=users, depts=depts, title="Projects")

# Add project
@project_bp.route('/projects/add', methods=['POST'])
def add_project():
    name = request.form.get('name')
    owner_id = request.form.get('owner_id')
    dept_id = request.form.get('dept_id')
    description = request.form.get('description')

    if not name or not owner_id or not dept_id:
        flash("Name, Owner và Dept bắt buộc!", "error")
        return redirect(url_for('project.list_projects'))

    project = Project(name=name, owner_id=owner_id, dept_id=dept_id, description=description)
    db.session.add(project)
    db.session.commit()
    flash(f"Project '{name}' added.", "success")
    return redirect(url_for('project.list_projects'))

# Edit project
@project_bp.route('/projects/edit/<int:project_id>', methods=['POST'])
def edit_project(project_id):
    project = Project.query.get_or_404(project_id)
    project.name = request.form.get('name')
    project.owner_id = request.form.get('owner_id')
    project.dept_id = request.form.get('dept_id')
    project.description = request.form.get('description')
    db.session.commit()
    flash(f"Project '{project.name}' updated.", "success")
    return redirect(url_for('project.list_projects'))

# Delete project
@project_bp.route('/projects/delete/<int:project_id>', methods=['POST'])
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    flash(f"Project '{project.name}' deleted.", "success")
    return redirect(url_for('project.list_projects'))
