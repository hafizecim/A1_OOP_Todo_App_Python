from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime, Enum
from datetime import datetime, date, timezone


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

    
    #Görev bitirme durumu: geç, zamanında, erken """
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
    tasks = Task.query.order_by(Task.created_at.desc()).all()
    active_task = Task.query.filter_by(status='in_progress').first()
    #today = datetime.utcnow().date()
    # Bugünü UTC zaman dilimine duyarlı olarak alıyoruz
    today = datetime.now(timezone.utc).date() # GÜNCEL VE DOĞRU KULLANIM # GÜNCELLENDİ: datetime.utcnow() yerine datetime.now(datetime.UTC).date()

    # GET parametreleri
    time_filter = request.args.get('time_filter')
    status_filter = request.args.get('status_filter')
    priority_filter = request.args.get('priority_filter')

    # Filtreleri dict içinde tut
    selected_filters = {
        'time_filter': time_filter,
        'status_filter': status_filter,
        'priority_filter': priority_filter
    }

    # Başlangıç: tüm görevler
    filtered_tasks = tasks

    # Zaman filtresi
    if time_filter:
        if time_filter == 'late':
            filtered_tasks = [t for t in filtered_tasks if t.due_date and t.due_date.date() < today and t.status != 'completed']
        elif time_filter == 'not_due':
            filtered_tasks = [t for t in filtered_tasks if t.due_date and t.due_date.date() > today]
        elif time_filter == 'on_time':
            filtered_tasks = [t for t in filtered_tasks if t.due_date and t.due_date.date() == today]
        elif time_filter == 'early':
            filtered_tasks = [t for t in filtered_tasks if t.due_date and t.due_date.date() < today and t.status == 'completed']

    # Durum filtresi
    if status_filter:
        filtered_tasks = [t for t in filtered_tasks if t.status == status_filter]

    # Öncelik filtresi
    if priority_filter:
        filtered_tasks = [t for t in filtered_tasks if t.priority == priority_filter]
        
    # Aktif görevi bul
    active_task = Task.query.filter_by(status='in_progress').first()
    
    # Kalan Süre Değişkenlerini Tanımla (Varsayılan değerler)
    kalan_sure_text = "Başlatılmış görev yok."
    kalan_sure_color = "secondary"


    # --- KRİTİK GÖREV ÖZETİ MANTIĞI (Öncelikli Sıralama) ---
    
    # Tüm görevler üzerinde filtreleme yapmak için kolaylık sağlıyoruz
    pending_tasks = [t for t in tasks if t.status == 'pending']
    
    summary_message = {
        'text': "Şu an için kritik bir uyarı bulunmamaktadır. 💪",
        'color': "success"
    }
    
    # 1. Gecikmiş (late) + Bekleyen (pending) + Acil (high)
    count_1 = sum(1 for t in pending_tasks if t.priority == 'high' and t.due_date and t.due_date.date() < today)
    if count_1 > 0:
        summary_message['text'] = f" ACİL UYARI! {count_1} adet **Gecikmiş, Bekleyen ve Acil** öncelikli göreviniz var!"
        summary_message['color'] = "danger"
    else:
        # 2. Gecikmiş (late) + Bekleyen (pending) + Orta (medium)
        count_2 = sum(1 for t in pending_tasks if t.priority == 'medium' and t.due_date and t.due_date.date() < today)
        if count_2 > 0:
            summary_message['text'] = f" DİKKAT! {count_2} adet **Gecikmiş ve Bekleyen Orta** öncelikli göreviniz bulunmaktadır."
            summary_message['color'] = "warning"
        else:
            # 3. Zamanı Gelmemiş (not_due) + Bekleyen (pending) + Acil (high)
            count_3 = sum(1 for t in pending_tasks if t.priority == 'high' and t.due_date and t.due_date.date() > today)
            if count_3 > 0:
                summary_message['text'] = f" {count_3} adet **Yaklaşan ve Acil** göreviniz var. Planlamayı unutmayın."
                summary_message['color'] = "info"
            else:
                # 4. Zamanı Gelmemiş (not_due) + Bekleyen (pending) + Orta (medium)
                count_4 = sum(1 for t in pending_tasks if t.priority == 'medium' and t.due_date and t.due_date.date() > today)
                if count_4 > 0:
                    summary_message['text'] = f" {count_4} adet **Yaklaşan Orta** öncelikli göreviniz mevcut."
                    summary_message['color'] = "secondary"
                else:
                    # 5. Varsayılan Durum (Kritik bir şey yok)
                    # Gecikmiş Acil/Orta veya Yaklaşan Acil/Orta görev yok.
                    pass # summary_message zaten varsayılan (success) değerde kalacak
    
    
    # AKTİF GÖREV VARSA KALAN SÜREYİ HESAPLA !!!
    if active_task:
        kalan_sure_text, kalan_sure_color = calculate_remaining_time(active_task)

    return render_template(
        'index.html',
        tasks=filtered_tasks,
        active_task=active_task,
        today=today,
        selected_filters=selected_filters,
        kalan_sure_text=kalan_sure_text,  # 
        kalan_sure_color=kalan_sure_color,# 
        summary_message=summary_message
    )

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


# Kalan süre hesaplama fonksiyonu
def calculate_remaining_time(task):
    if not task.due_date:
        return "Tahmini Bitiş Yok", "secondary"
    
    now_date = datetime.utcnow().date()
    due_date = task.due_date.date()
    
    delta = due_date - now_date
    
    if task.status == 'completed':
        # Tamamlanmışsa (completed_at vs due_date karşılaştırılması daha doğru olurdu, şimdilik basit tutalım)
        return "Görev Tamamlandı", "success"
    
    elif delta.days < 0:
        return f"{-delta.days} gün gecikti", "danger"
    elif delta.days == 0:
        return "Bugün son gün!", "warning"
    else:
        return f"{delta.days} gün kaldı", "success"



def determine_execution_state(completed_at, due_date):
    """
    Görevin bitirme durumunu (late, on_time, early) belirler.
    Tarih karşılaştırmaları sadece gün bazında yapılır.
    """
    if not due_date:
        return 'on_time' # Tahmini bitiş tarihi yoksa zamanında bitmiş kabul edelim

    # Sadece tarih kısımlarını karşılaştır
    completed_date = completed_at.date()
    due_date = due_date.date()

    if completed_date > due_date:
        return 'late' # Geç bitmiş
    elif completed_date < due_date:
        return 'early' # Erken bitmiş
    else: # completed_date == due_date
        return 'on_time' # Tam zamanında bitmiş
"""
@app.route('/finish_task_form/<int:id>', methods=['GET'])
def finish_task_form(id):
    task = Task.query.get_or_404(id)
    
    # Eğer görev zaten completed durumundaysa, ana sayfaya yönlendir
    if task.status == 'completed':
        flash('Bu görev zaten tamamlanmış.', 'info')
        return redirect(url_for('index'))
        
    return render_template('finish_task_form.html', task=task)

@app.route('/finish_task/<int:id>', methods=['POST'])
def finish_task(id):
    task = Task.query.get_or_404(id)
    
    # 1. completed_at ve updated_at'i ayarla
    completed_at = datetime.utcnow()
    task.completed_at = completed_at
    task.status = 'completed'
    
    # 2. Açıklama alanını güncelle (Kullanıcı tarafından girilen yeni açıklama)
    new_description = request.form.get('description')
    if new_description is not None:
        task.description = new_description

    # 3. execution_state'i belirle ve güncelle
    if task.due_date:
        task.execution_state = determine_execution_state(completed_at, task.due_date)
    else:
        # Tahmini bitiş tarihi yoksa zamanında bitmiş kabul edilebilir.
        task.execution_state = 'on_time' 

    db.session.commit()
    flash(f"Görev başarıyla tamamlandı. Durum: {task.execution_state}", 'success')
    
    # Bitirme işleminden sonra aktif görevi sıfırla (eğer varsa)
    global active_task_id
    if active_task_id == id:
        active_task_id = None
        
    return redirect(url_for('index'))
"""
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
