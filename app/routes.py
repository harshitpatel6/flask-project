from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Todo

# Create a blueprint
main = Blueprint('main', __name__)

@main.route('/')
def index():
    todos = Todo.query.order_by(Todo.created_at.desc()).all()
    return render_template('index.html', todos=todos)

@main.route('/add', methods=['POST'])
def add():
    title = request.form.get('title')
    description = request.form.get('description')
    
    if not title:
        flash('Title is required!')
        return redirect(url_for('main.index'))
    
    new_todo = Todo(title=title, description=description)
    db.session.add(new_todo)
    db.session.commit()
    
    return redirect(url_for('main.index'))

@main.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    todo = Todo.query.get_or_404(id)
    
    if request.method == 'POST':
        todo.title = request.form.get('title')
        todo.description = request.form.get('description')
        
        db.session.commit()
        return redirect(url_for('main.index'))
    
    return render_template('update.html', todo=todo)

@main.route('/delete/<int:id>')
def delete(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    
    return redirect(url_for('main.index'))

@main.route('/complete/<int:id>')
def complete(id):
    todo = Todo.query.get_or_404(id)
    todo.completed = not todo.completed
    db.session.commit()
    
    return redirect(url_for('main.index')) 