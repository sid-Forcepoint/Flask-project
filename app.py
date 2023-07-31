import traceback
from datetime import datetime
from app import app,db
from flask import Flask,render_template,url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test1.db'
db=SQLAlchemy(app)

class Todo(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    desc=db.Column(db.String(200),nullable=False)
    completed=db.Column(db.Integer,default=0)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)
    date_modified=db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/delete/<int:id>')
def delete(id):
    task=Todo.query.get_or_404(id)
    try:
        db.session.delete(task)
        db.session.commit()
    except:
        return "The task cannot be deleted"
    return redirect('/')

@app.route('/update/<int:id>',methods=['POST','GET'])
def update(id):
    task=Todo.query.get_or_404(id)
    if request.method=="POST":
        task.desc=request.form['description']
        task.date_modified=datetime.utcnow()
        try:
            db.session.commit()
        except:
            return "unable to update the task"
        return redirect('/')
    else:
        tasks = Todo.query.order_by(Todo.date_modified).all()
        return render_template('update.html',task=task)





@app.route('/',methods=['POST','GET'])
def index():
    if request.method=='POST':
        task_desc=request.form['description']
        new_task=Todo(desc=task_desc)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:

            return "There was an issue adding your task "

    else:
        tasks = Todo.query.order_by(Todo.date_modified).all()
        return render_template('base.html',tasks=tasks)


if __name__=="__main__":
    app.run(debug=True)