from flask import Flask, render_template, request,redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = "gizli-bir-anahtar"  # flash mesajları için (gerçek projede env var kullan)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'

db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200))
    complete = db.Column(db.Boolean, default=False)

@app.route('/')
def index():
    incomplete  = Todo.query.filter_by(complete=False).all()
    complete  = Todo.query.filter_by(complete=True).all()
    return render_template('index.html', incomplete=incomplete, complete=complete)

@app.route('/add', methods=['POST'])
def add():
    text = request.form.get('todoitem', '').strip()
    if not text:
        flash("Görev boş olamaz.", "warning")
        return redirect(url_for('index'))
    
    todo = Todo(text=text, complete=False)
    db.session.add(todo)
    db.session.commit()
    flash("Görev eklendi ✅", "success")
    return redirect(url_for('index'))

@app.route('/complete/<id>')
def complete(id):
    
    todo = Todo.query.filter_by(id=int(id)).first() 
    todo.complete = True
    db.session.commit()
   
    return redirect(url_for('index'))
    
if __name__ == '__main__':
    with app.app_context():  # Flask uygulama bağlamını açıyoruz
        db.create_all()      # Bu satır veritabanını ve tabloyu oluşturur
    
    app.run(debug=True)