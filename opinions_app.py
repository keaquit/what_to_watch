from datetime import datetime
from random import randrange

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)


class Opinion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    text = db.Column(db.Text, unique=True, nullable=False)
    source = db.Column(db.String(256))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

@app.route('/')
def index_view():
     # Определить количество мнений в базе данных.
    quantity = Opinion.query.count()
    # Если мнений нет...
    if not quantity:
        # ...то вернуть сообщение:
        return 'В базе данных мнений о фильмах нет.'
    # Иначе выбрать случайное число в диапазоне от 0 до quantity...
    offset_value = randrange(quantity)
    # Извлечь все записи, пропуская первые offset_value записей
    # и взять первую запись из получившегося набора.
    opinion = Opinion.query.offset(offset_value).first()
    # Передать в шаблон весь объект opinion.
    return render_template('opinion.html', opinion=opinion)

@app.route('/add')
def add_opinion_view():
    return render_template('add_opinion.html')


if __name__ == '__main__':
    app.run()