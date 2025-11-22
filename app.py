from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime, Enum
from datetime import datetime

app = Flask(__name__)
app.secret_key = "gizli-bir-anahtar"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Görev modeli
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    assigned_to = db.Column(db.String(100), nullable=True)

    status = db.Column(
        Enum('pending', 'in_progress', 'completed', name='status_types'),
        default='pending', nullable=False
    )

    priority = db.Column(
        Enum('low', 'medium', 'high', name='priority_levels'),
        default='medium', nullable=False
    )

    execution_state = db.Column(
        Enum('late', 'not_started_yet', 'on_time', 'early', name='execution_states'),
        default='not_started_yet', nullable=False
    )

    created_at = db.Column(DateTime, default=datetime.utcnow, nullable=False)
    start_at = db.Column(DateTime, nullable=True)
    due_date = db.Column(DateTime, nullable=True)  # Düzeltildi: formdaki due_date ile eşleşiyor
    completed_at = db.Column(DateTime, nullable=True)
    updated_at = db.Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


# Anasayfa
@app.route('/')
def index():
    # Tüm görevleri sırala
    tasks_query = Task.query.order_by(Task.created_at.desc())

    # URL parametrelerinden filtreleri al
    time_filter = request.args.get('time_filter')  # 1. blok
    status_filter = request.args.get('status_filter')  # 2. blok (sonra ekleyeceğiz)
    priority_filter = request.args.get('priority_filter')  # 3. blok (sonra ekleyeceğiz)

    # selected_filters dict'i template için
    selected_filters = {
        'time_filter': time_filter,
        'status_filter': status_filter,
        'priority_filter': priority_filter
    }

    # 1️⃣ Zaman filtreleme (ilk blok)
    if time_filter:
        tasks_query = tasks_query.filter(Task.execution_state == time_filter)

    # 2️⃣ Durum filtreleme (2. blok)
    if status_filter:
        tasks_query = tasks_query.filter(Task.status == status_filter)

    tasks = tasks_query.all()

    # Aktif görev
    active_task = Task.query.filter_by(status='in_progress').first()

    today = datetime.utcnow().date()
    return render_template('index.html', tasks=tasks, active_task=active_task, today=today, selected_filters=selected_filters)


# Yeni görev sayfası
@app.route('/new_task', methods=['GET'])
def new_task():
    return render_template('new_task.html')


# Görev ekleme
@app.route('/add', methods=['POST'])
def add():
    title = request.form['title']
    description = request.form.get('description')
    due_date = request.form.get('due_date')
    priority = request.form.get('priority')

    new_task = Task(
        title=title,
        description=description,
        due_date=datetime.strptime(due_date, '%Y-%m-%d') if due_date else None,
        priority=priority,
        status='pending'
    )

    db.session.add(new_task)
    db.session.commit()
    flash('Görev başarıyla eklendi!', 'success')
    return redirect(url_for('index'))


# Görev durumu güncelleme
@app.route('/update_status/<int:id>/<new_status>')
def update_status(id, new_status):
    task = Task.query.get_or_404(id)
    task.status = new_status

    if new_status == "in_progress":
        task.start_at = datetime.utcnow()
    elif new_status == "completed":
        task.completed_at = datetime.utcnow()

    db.session.commit()
    return redirect(url_for('index'))


# Görev silme
@app.route('/delete/<int:id>', methods=['POST'])
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    flash("Görev silindi", "danger")
    return redirect(url_for('index'))


# Görev düzenleme
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    task = Task.query.get_or_404(id)

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        due_date = request.form.get('due_date')
        priority = request.form.get('priority')

        if not title:
            flash("Görev başlığı boş olamaz", "warning")
            return redirect(url_for('edit', id=id))

        task.title = title
        task.description = description
        task.priority = priority
        task.due_date = datetime.strptime(due_date, '%Y-%m-%d') if due_date else None

        db.session.commit()
        flash("Görev güncellendi", "success")
        return redirect(url_for('index'))

    return render_template('edit.html', task=task)

# Aktif görev için global değişken (basit çözüm, prod için session veya DB flag daha iyi)
active_task_id = None

# Başlat butonuna tıklandığında
@app.route('/start_task/<int:id>')
def start_task(id):
    global active_task_id
    task = Task.query.get_or_404(id)
    task.status = 'in_progress'
    task.start_at = datetime.utcnow()
    db.session.commit()
    active_task_id = id
    return redirect(url_for('index'))

# Duraklat
@app.route('/pause_task/<int:id>')
def pause_task(id):
    task = Task.query.get_or_404(id)
    if task.status == 'in_progress':
        task.status = 'pending'
    db.session.commit()
    global active_task_id
    active_task_id = None
    return redirect(url_for('index'))

# Bitir
@app.route('/finish_task/<int:id>')
def finish_task(id):
    task = Task.query.get_or_404(id)
    task.status = 'completed'
    task.completed_at = datetime.utcnow()
    db.session.commit()
    global active_task_id
    active_task_id = None
    return redirect(url_for('index'))




if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
