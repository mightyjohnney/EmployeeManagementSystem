from flask import Blueprint
from flask import render_template, redirect, url_for, request, session, jsonify
from flask_login import login_user, logout_user, current_user
from app.master import bp
from app.master.model import Department, DepartmentSchema
from app import db, ma


# Emp. Cat Master Routes


@bp.route('/get/department', methods=['GET'])
def get_department():
    if request.method == 'GET':
        data_schema = DepartmentSchema(many=True)
        data = Department.query.all()
        json_data = data_schema.dump(data)
        return jsonify(json_data)


@bp.route('/add/department', methods=['POST'])
def add_department():
    if request.method == 'POST':
        payload = request.json
        if payload['name'] is not None:

            check_data = Department.query.filter_by(name=payload['name'])
            if check_data.first():
                return jsonify({'message': 'Department - '+check_data.first().name+' already exists.'})
            else:
                try:
                    new_data = Department(payload['name'])
                    db.session.add(new_data)
                    db.session.commit()
                    return jsonify({'success': 'Data Added'})

                except Exception as e:
                    db.session.rollback()
                    db.session.close()
                    return jsonify({'message': 'Something unexpected happened. Check logs', 'log': str(e)})
        else:
            return jsonify({'message': 'Empty Data.'})

    else:
        return jsonify({'message': 'Invalid HTTP method . Use POST instead.'})


@bp.route('/edit/department', methods=['POST'])
def edit_department():
    if request.method == 'POST':
        payload = request.json
        if payload['name'] is not None:

            check_data = Department.query.filter_by(name=payload['name'])
            if check_data.first():
                return jsonify({'message': 'Department - '+check_data.first().name+' already exists.'})
            else:
                try:
                    new_data = Department.query.filter_by(
                        id=payload['id']).first()
                    new_data.name = payload['name']
                    db.session.commit()
                    return jsonify({'success': 'Data Updated'})

                except Exception as e:
                    db.session.rollback()
                    db.session.close()
                    return jsonify({'message': 'Something unexpected happened. Check logs', 'log': str(e)})
        else:
            return jsonify({'message': 'Empty Data.'})

    else:
        return jsonify({'message': 'This is Invalid HTTP method . Use POST instead.'})


@bp.route('/delete/department', methods=['POST'])
def delete_department():
    if request.method == 'POST':
        payload = request.json
        check_data = Department.query.filter_by(id=payload['id'])
        if check_data.first():
            if(len(check_data.first().emp_department) != 0):
                return jsonify({'message': 'Cannot delete , data being used. '})
            else:
                try:
                    check_data.delete()
                    db.session.commit()
                    return jsonify({'success': 'Data deleted'})
                except Exception as e:
                    db.session.rollback()
                    db.session.close()
                    return jsonify({'message': 'Something unexpected happened. Check logs', 'log': str(e)})
        else:
            return jsonify({'message': 'Data does not exist.'})

    else:
        return jsonify({'message': 'Invalid HTTP method . Use POST instead.'})
