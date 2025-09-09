from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Staff, Dept

staff_bp = Blueprint('staff', __name__, template_folder='templates')

# Hiển thị danh sách nhân viên
@staff_bp.route('/staffs')
def list_staffs():
    staffs = Staff.query.all()
    depts = Dept.query.all()
    return render_template('staffs.html', staffs=staffs, depts=depts)

# Thêm nhân viên
@staff_bp.route('/staffs/add', methods=['POST'])
def add_staff():
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    dept_id = request.form.get('dept_id') or None

    if not name or not email:
        flash("Tên và email là bắt buộc!", "error")
        return redirect(url_for('staff.list_staffs'))

    staff = Staff(name=name, email=email, phone=phone, dept_id=dept_id)
    db.session.add(staff)
    db.session.commit()
    flash(f"Nhân viên '{name}' đã được thêm.", "success")
    return redirect(url_for('staff.list_staffs'))

# Sửa nhân viên
@staff_bp.route('/staffs/edit/<int:staff_id>', methods=['POST'])
def edit_staff(staff_id):
    staff = Staff.query.get_or_404(staff_id)
    staff.name = request.form.get('name')
    staff.email = request.form.get('email')
    staff.phone = request.form.get('phone')
    staff.dept_id = request.form.get('dept_id') or None
    db.session.commit()
    flash(f"Nhân viên '{staff.name}' đã được cập nhật.", "success")
    return redirect(url_for('staff.list_staffs'))

# Xóa nhân viên
@staff_bp.route('/staffs/delete/<int:staff_id>', methods=['POST'])
def delete_staff(staff_id):
    staff = Staff.query.get_or_404(staff_id)
    db.session.delete(staff)
    db.session.commit()
    flash(f"Nhân viên '{staff.name}' đã bị xóa.", "success")
    return redirect(url_for('staff.list_staffs'))
