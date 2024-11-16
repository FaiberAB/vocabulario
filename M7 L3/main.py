# Importar
from flask import Flask, render_template, request, redirect
# Conexión de la biblioteca de bases de datos
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
# Conexión con SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Creación de una base de datos
db = SQLAlchemy(app)
# Creación de una tabla

# Tarea #1. Creación de una base de datos


class Card(db.Model):
    # Creación de campos de columna
    # id
    id = db.Column(db.Integer, primary_key=True)
    # Título
    title = db.Column(db.String(100), nullable=False)
    # Descripción
    subtitle = db.Column(db.String(300), nullable=False)
    # Texto
    text = db.Column(db.Text, nullable=False)

    # Salida del objeto
    def __repr__(self):
        return f'<Card {self.id}>'


# Ejecutar la página con el contenido
@app.route('/')
def index():
    # Salida de los objetos de la base de datos
    # Tarea #2. Hacer que los objetos de la base de datos se muestren en index.html
    cards = Card.query.order_by(Card.id).all()

    return render_template('index.html', cards=cards)

# Ejecución de la página con la tarjeta


@app.route('/card/<int:id>')
def card(id):
    # Tarea #2. Utilice el id para mostrar la tarjeta correcta
    card = Card.query.get(id)

    return render_template('card.html', card=card)

# Ejecutar la página con la inicialización de la tarjeta


@app.route('/create')
def create():
    return render_template('create_card.html')

# El formulario de la tarjeta


@app.route('/form_create', methods=['GET', 'POST'])
def form_create():
    if request.method == 'POST':
        title = request.form['title']
        subtitle = request.form['subtitle']
        text = request.form['text']

        # Creación de un objeto para pasarlo a la base de datos

        # Tarea #2. Crear una forma de almacenar datos en la base de datos
        card = Card(title=title, subtitle=subtitle, text=text)

        db.session.add(card)
        db.session.commit()
        return redirect('/')
    else:
        return render_template('create_card.html')


if __name__ == "__main__":
    app.run(debug=True)
