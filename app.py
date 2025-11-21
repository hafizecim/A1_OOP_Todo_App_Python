from flask import Flask, render_template, request,redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'

db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200))
    complete = db.Column(db.Boolean)

@app.route('/')
def index():
    todos = Todo.query.all()
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add():
    todo = Todo(text=request.form['todoitem'], complete=False)
    db.session.add(todo)
    db.session.commit()
    return '<h1>{}</h1>'.format(request.form['todoitem'])

@app.route('/complete/<id>')
def complete(id):
    return '<h1>{}</h1>'.format(id)
    #return redirect(url_for('index'))
    
if __name__ == '__main__':
    with app.app_context():  # Flask uygulama bağlamını açıyoruz
        db.create_all()      # Bu satır veritabanını ve tabloyu oluşturur
    
    app.run(debug=True)