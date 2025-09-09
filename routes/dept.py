from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db
from models import Dept  # import model Dept

dept_bp = Blueprint('dept', __name__, template_folder='templates')

# Hiển thị danh sách phòng ban
@dept_bp.route('/depts')
def list_depts():
    depts = Dept.query.all()
    return render_template('depts.html', depts=depts)

# Form thêm phòng ban
@dept_bp.route('/depts/add', methods=['GET', 'POST'])
def add_dept():
    if request.method == 'POST':
        name = request.form.get('name')
        manager_email = request.form.get('manager_email')
        description = request.form.get('description')

        if not name:
            flash("Name is required!", "error")
            return redirect(url_for('dept.add_dept'))

        dept = Dept(name=name, manager_email=manager_email, description=description)
        db.session.add(dept)
        db.session.commit()
        flash(f"Department '{name}' added successfully.", "success")
        return redirect(url_for('dept.list_depts'))

    return render_template('add_dept.html')

# Form sửa phòng ban
@dept_bp.route('/depts/edit/<int:dept_id>', methods=['GET', 'POST'])
def edit_dept(dept_id):
    dept = Dept.query.get_or_404(dept_id)

    if request.method == 'POST':
        dept.name = request.form.get('name')
        dept.manager_email = request.form.get('manager_email')
        dept.description = request.form.get('description')
        db.session.commit()
        flash(f"Department '{dept.name}' updated successfully.", "success")
        return redirect(url_for('dept.list_depts'))

    return render_template('edit_dept.html', dept=dept)

# Xóa phòng ban
@dept_bp.route('/depts/delete/<int:dept_id>', methods=['POST'])
def delete_dept(dept_id):
    dept = Dept.query.get_or_404(dept_id)
    db.session.delete(dept)
    db.session.commit()
    flash(f"Department '{dept.name}' deleted.", "success")
    return redirect(url_for('dept.list_depts'))
