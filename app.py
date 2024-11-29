from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newflask.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Auto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, server_default=db.func.now())

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    auto = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, server_default=db.func.now())



@app.route('/kbase')
def kbase():
    posts = Client.query.all()
    return render_template('kbase.html', posts=posts)

@app.route('/edit/<int:client_id>', methods=['GET', 'POST'])
def edit(client_id):
    client = Client.query.get_or_404(client_id)
    if request.method == 'POST':
        client.title = request.form['title']
        client.text = request.form['text']
        client.auto = request.form['auto']
        db.session.commit()
        return redirect(url_for('kbase'))
    return render_template('edit.html', client=client)

@app.route("/index")
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/posts")
def posts():
    posts = Auto.query.all()
    return render_template('posts.html', posts=posts)

@app.route("/client", methods=['POST', 'GET'])
def client():
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']
        auto = request.form['auto']
        post = Client(title=title, text=text, auto=auto)
        try:
            db.session.add(post)
            db.session.commit()
            return redirect('/kbase')
        except Exception as e:
            return f"Ошибка при добавлении клиента: {e}"
    else:
        return render_template('client.html')


@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/kontact")
def kontact():
    return render_template('kontact.html')

if __name__ == '__main__':
    app.run(debug=True)
