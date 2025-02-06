from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'  # Required for flash messages

db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route("/", methods=['GET'])
def index():
    data = Todo.query.order_by(Todo.date_created.desc()).all()
    return render_template("index.html", data=data)

@app.route("/create_task", methods=['POST'])
def create_task():
    title = request.form.get('title', '').strip()
    desc = request.form.get('desc', '').strip()

    if not title or not desc:
        flash("Title and description cannot be empty!", "danger")
        return redirect("/")

    try:
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
        flash("Task added successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error: {str(e)}", "danger")

    return redirect('/')

@app.route("/edit_task/<int:sno>", methods=['GET', 'POST'])
def edit_task(sno):
    todo = Todo.query.get_or_404(sno)
    
    if request.method == 'POST':
    
        title = request.form.get('title', '').strip()
        desc = request.form.get('desc', '').strip()

        try:
            todo.title = title
            todo.desc = desc
            db.session.commit()
            return redirect("/")
        except Exception as e:
            db.session.rollback()
            flash(f"Error: {str(e)}", "danger")

    return render_template("update.html", data=todo)


@app.route("/delete_task/<int:sno>", methods=['POST'])
def delete_task(sno):
    todo = Todo.query.get_or_404(sno)
    
    try:
        db.session.delete(todo)
        db.session.commit()
        flash("Task deleted successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error: {str(e)}", "danger")

    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
