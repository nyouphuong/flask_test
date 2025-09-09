from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, TaskSetup, Dept

task_bp = Blueprint('task', __name__, template_folder='templates')

# Hiển thị danh sách task
@task_bp.route('/tasks')
def list_tasks():
    tasks = TaskSetup.query.all()
    depts = Dept.query.all()
    return render_template('tasks.html', tasks=tasks, depts=depts)

# Thêm task
@task_bp.route('/tasks/add', methods=['POST'])
def add_task():
    title = request.form.get('title')
    description = request.form.get('description')
    dept_id = request.form.get('dept_id')

    if not title or not dept_id:
        flash("Tên công việc và phòng ban là bắt buộc!", "error")
        return redirect(url_for('task.list_tasks'))

    task = TaskSetup(title=title, description=description, dept_id=dept_id)
    db.session.add(task)
    db.session.commit()
    flash(f"Công việc '{title}' đã được thêm.", "success")
    return redirect(url_for('task.list_tasks'))

# Sửa task
@task_bp.route('/tasks/edit/<int:task_id>', methods=['POST'])
def edit_task(task_id):
    task = TaskSetup.query.get_or_404(task_id)
    task.title = request.form.get('title')
    task.description = request.form.get('description')
    task.dept_id = request.form.get('dept_id')
    task.status = request.form.get('status') or task.status
    db.session.commit()
    flash(f"Công việc '{task.title}' đã được cập nhật.", "success")
    return redirect(url_for('task.list_tasks'))

# Xóa task
@task_bp.route('/tasks/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    task = TaskSetup.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    flash(f"Công việc '{task.title}' đã bị xóa.", "success")
    return redirect(url_for('task.list_tasks'))
