from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime, Enum
from datetime import datetime

app = Flask(__name__)
app.secret_key = "gizli-bir-anahtar"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    assigned_to = db.Column(db.String(100), nullable=True)

    status = db.Column(Enum('pending', 'in_progress', 'completed', name='status_types'),
                       default='pending', nullable=False)
    priority = db.Column(Enum('urgent', 'medium', 'low', name='priority_levels'),
                         default='medium', nullable=False)

    execution_state = db.Column(Enum('late', 'not_started_yet', 'on_time', 'early',
                         name='execution_states'), default='not_started_yet', nullable=False)

    created_at = db.Column(DateTime, default=datetime.utcnow, nullable=False)
    start_at = db.Column(DateTime, nullable=True)
    estimated_end_at = db.Column(DateTime, nullable=True)
    completed_at = db.Column(DateTime, nullable=True)
    updated_at = db.Column(DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow, nullable=False)

@app.route('/')
def index():
    tasks = Task.query.order_by(Task.created_at.desc()).all()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    title = request.form.get("title")
    if not title:
        flash("Görev başlığı boş olamaz", "warning")
        return redirect(url_for('index'))

    new_task = Task(title=title)
    db.session.add(new_task)
    db.session.commit()

    flash("Görev oluşturuldu", "success")
    return redirect(url_for('index'))

@app.route('/update_status/<int:id>/<new_status>')
def update_status(id, new_status):
    task = Task.query.get_or_404(id)
    task.status = new_status

    if new_status == "in_progress":
        task.start_at = datetime.utcnow()

    if new_status == "completed":
        task.completed_at = datetime.utcnow()

    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>', methods=['POST'])
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    flash("Görev silindi", "danger")
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    # Görevi al, yoksa 404 döndür
    task = Task.query.get_or_404(id)

    if request.method == 'POST':
        # Formdan gelen yeni başlığı al
        title = request.form.get('title')
        if not title:
            flash("Görev başlığı boş olamaz", "warning")
            return redirect(url_for('edit', id=id))
        
        task.title = title
        db.session.commit()
        flash("Görev güncellendi", "success")
        return redirect(url_for('index'))

    # GET isteğinde edit.html sayfasını göster
    return render_template('edit.html', task=task)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
