from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456789@localhost:5432/flask_database'

db = SQLAlchemy(app)

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    task_title = db.Column(db.String(100), nullable=False)
    task_description = db.Column(db.String(200), nullable=True)
    task_status = db.Column(db.String(20), nullable=False)

@app.route('/tasks', methods=['post'])
def create_task():
    data = request.get_json()
    new_task = Task(
        task_title=data['task_title'],
        task_description=data.get('task_description', ''),
        task_status=data['task_status']
    )
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'message': 'Task created successfully'}), 201

@app.route('/tasks', methods=['GET'])
def get_all_tasks():
    tasks = Task.query.all()
    return jsonify([{
        'task_id': task.task_id,
        'task_title': task.task_title,
        'task_description': task.task_description,
        'task_status': task.task_status
    }for task in tasks]), 200

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task_status(task_id):
    data = request.get_json()
    print(f"Received data: {data}")
    task = Task.query.get_or_404(task_id)
    print(f"Task before update: {task}")
    task.task_status = data['task_status']
    db.session.commit()
    print(f"Task after update: {task}")
    return jsonify({'message': 'Task status updated successfully'}), 200


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted successfully'}), 200



with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
