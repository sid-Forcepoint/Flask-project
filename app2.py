from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///manager.db'
app.secret_key = '131101'
db = SQLAlchemy(app)

# Define the database model for tasks
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    is_completed = db.Column(db.Boolean, default=False)

# Define the User model (for simplicity, we're using a basic model here)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

@app.route('/')
def home():
    tasks = Task.query.all()
    return render_template('task.html', tasks=tasks)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        is_admin = False
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return render_template('register.html', error='Username already taken.')

        user = User(username=username, password=password, is_admin=is_admin)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['user_id'] = user.id
            session['is_admin'] = user.is_admin
            return redirect(url_for('admin_panel' if user.is_admin else 'user_tasks'))

    return render_template('login.html')


@app.route('/admin_panel', methods=['GET', 'POST'])
def admin_panel():
    if 'user_id' not in session or not session['is_admin']:
        return redirect(url_for('login'))  # Redirect unauthorized users to login page

    if request.method == 'POST':
        # Check if the request is to add a new task
        if 'add_task' in request.form:
            title = request.form['title']
            description = request.form['description']

            # Create a new task and add it to the database
            new_task = Task(title=title, description=description)
            db.session.add(new_task)
            db.session.commit()

            # Redirect back to the admin panel after adding the task
            return redirect(url_for('admin_panel'))

        # Check if the request is to set admin access for a user
        elif 'set_admin_user_id' in request.form:
            user_id = int(request.form['set_admin_user_id'])
            user = User.query.get_or_404(user_id)
            user.is_admin = True
            db.session.commit()
            return redirect(url_for('admin_panel'))

        # ... Handle other actions for the admin_panel route ...

    tasks = Task.query.all()
    users = User.query.all()  # Fetch all users to display in the admin panel
    return render_template('admin_panel.html', tasks=tasks, users=users)


@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('admin_panel'))

@app.route('/update/<int:task_id>', methods=['GET', 'POST'])
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    if request.method == 'POST':
        task.title = request.form['title']
        task.description = request.form['description']
        db.session.commit()
        return redirect(url_for('admin_panel'))

    return render_template('update_task.html', task=task)

@app.route('/user_tasks', methods=['GET', 'POST'])
def user_tasks():
    if request.method == 'POST':
        task_id = request.form['task_id']
        task = Task.query.get_or_404(task_id)
        task.is_completed = True
        db.session.commit()

    tasks = Task.query.filter_by(is_completed=False).all()
    return render_template('user_tasks.html', tasks=tasks)


def create_admin_user():
    admin_user = User(username='admin', password='password', is_admin=True)
    db.session.add(admin_user)
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_admin_user()
    app.run(debug=True)