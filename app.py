from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456789@localhost:5432/flask_database'

db = SQLAlchemy(app)

class task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    done = db.Column(db.Boolean, default=False)

with app.app_context():
    db.create_all()

@app.route('/tasks')
def get_tasks():
    tasks = task.query.all()
    task_list = [
        {
            'id': task.id,
            'title': task.title,
            'done': task.done
        }
        for task in tasks
    ]

    return jsonify({"tasks":task_list}) 

if __name__ == '__main__':
    app.run(debug=True)
