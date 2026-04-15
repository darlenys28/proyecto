import mysql
import stripe

from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from decimal import Decimal
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user


from config import config
from models.ModelUser import ModelUser
from models.entities.User import User


app = Flask(__name__)

import os
stripe.api_key = os.getenv("STRIPE_KEY")

app.config.from_object(config['development'])
app.config['SECRET_KEY'] = 'una_clave_secreta'  # necesario para CSRF

csrf = CSRFProtect(app)
db = MySQL(app)
login_manager_app = LoginManager(app)

@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        logged_user = ModelUser.login(db, username, password)

        if logged_user is not None:
            # Login correcto
            login_user(logged_user)
            print(current_user.role)

            # Redirección según rol
            if current_user.role == 'user':
                return redirect(url_for('home'))
            elif current_user.role == 'admin':
                return redirect(url_for('administrador'))
            else:
                return redirect(url_for('home'))  # fallback por si hay otro rol


        else:
            flash("Usuario o contraseña incorrectos")
            return render_template('auth/login.html')

    return render_template('auth/login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=["POST"])
def register():

    username = request.form["username"]
    password = request.form["password"]
    fullname = request.form["fullname"]
    role= 'user'
    correo = request.form["correo"]

    user = User(0, username, password, fullname,correo, role)

    ModelUser.register(db, user)

    return redirect(url_for("login"))

@app.route('/registrarse')
def registrarse():
    return render_template('registrarse.html')


@app.route('/home')
@login_required
def home():
    cursor = db.connection.cursor()
    sql = "SELECT * FROM producto"
    cursor.execute(sql)
    data = cursor.fetchall()
    return render_template('home.html', productos=data)

@app.route('/buscar')
def buscar():
    texto = request.args.get('q')
    cursor = db.connection.cursor()
    sql = "SELECT * FROM producto WHERE nombre LIKE %s"
    cursor.execute(sql, ('%' + texto + '%',))
    
    data = cursor.fetchall()
    return render_template('home.html', productos=data)

    

@app.route("/categoria/<nombre>")
def categoria(nombre):
    cursor = db.connection.cursor()
    
    cursor.execute("SELECT * FROM producto WHERE tipo = %s", (nombre,))
    productos = cursor.fetchall()

    cursor.close()
   

    return render_template("home.html", productos=productos)

@app.route("/productos")
def productos():
    cursor = db.connection.cursor()
    
    cursor.execute("SELECT * FROM producto")
    productos = cursor.fetchall()

    cursor.close()
   

    return render_template("home.html", productos=productos)



@app.route("/add/<int:id>")
def add_to_cart(id):
    cursor = db.connection.cursor()
   
    # 1. Buscar producto
    cursor.execute("SELECT * FROM producto WHERE id = %s", (id,))
    producto = cursor.fetchone()

    if producto and producto[5] > 0:

        # 2. Crear carrito si no existe
        if "carrito" not in session:
            session["carrito"] = {}

        carrito = session["carrito"]

        # 3. Añadir o incrementar
        if str(id) in carrito:
            carrito[str(id)]["cantidad"] += 1
        else:
            carrito[str(id)] = {
                "nombre": producto[1],
                "precio": float(producto[4]),
                "imagen": producto[6],
                "cantidad": 1
            }
        

        session["carrito"] = carrito
        session.modified = True

        

    cursor.close()
    return redirect(url_for('home'))



@app.route("/carrito")
def carrito():
    carrito = session.get("carrito", {})

    orden = request.args.get("orden")

    # convertir dict -> lista para poder ordenar
    productos = list(carrito.items())

    if orden == "asc":
        productos.sort(key=lambda x: x[1]["precio"])

    elif orden == "desc":
        productos.sort(key=lambda x: x[1]["precio"], reverse=True)

    # volver a dict si quieres mantener tu estructura original
    carrito_ordenado = dict(productos)

    return render_template("carrito.html", carrito=carrito_ordenado)

@csrf.exempt
@app.route('/crear-pago', methods=['POST'])
def crear_pago():
    try:
        data = request.get_json()
        total = float(data['total'])

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'eur',
                    'product_data': {'name': 'Compra en tienda'},
                    'unit_amount': int(total * 100),
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='http://127.0.0.1:5000/exito',
            cancel_url='http://127.0.0.1:5000/cancelado',
        )

        return jsonify({'url': session.url})

    except Exception as e:
        print("ERROR:", e)
        return jsonify({'error': str(e)}), 500

"""

@app.route('/telefono')
@login_required
def telefono():
    cursor = db.connection.cursor()
    sql = "SELECT * FROM producto where tipo ='telefono'"
    cursor.execute(sql)
    data = cursor.fetchall()
    return render_template('telefono.html', telefono=data)

@app.route('/lapto')
@login_required
def lapto():
    cursor = db.connection.cursor()
    sql = "SELECT * FROM producto where tipo ='lapto'"
    cursor.execute(sql)
    data = cursor.fetchall()
    return render_template('lapto.html', lapto =data)

@app.route('/administrador')
@login_required
def administrador():
    cursor = db.connection.cursor()
    sql = "SELECT * FROM telefono"
    cursor.execute(sql)
    data_telef = cursor.fetchall()

    cursor = db.connection.cursor()
    sql = "SELECT * FROM lapto"
    cursor.execute(sql)   
    data_lapto = cursor.fetchall()

    cursor = db.connection.cursor()
    sql = "SELECT * FROM venta join detalle_venta on venta.id = id_venta"
    cursor.execute(sql)
    vent_telef = cursor.fetchall()

    cursor = db.connection.cursor()
    sql = "SELECT precio FROM venta join detalle_venta on venta.id = id_venta"
    cursor.execute(sql)
    precioT = cursor.fetchall()


    from decimal import Decimal
    preciosT = [Decimal(row[0]) for row in precioT]


    precio_total_telef = sum(preciosT)


    cursor = db.connection.cursor()
    sql = "SELECT precio FROM venta_lapto"
    cursor.execute(sql)
    precioL = cursor.fetchall()

    from decimal import Decimal
    preciosL = [Decimal(row[0]) for row in precioL]

    # Sumar los precios
    precio_total_lap = sum(preciosL)


    cursor = db.connection.cursor()
    sql = "SELECT * FROM venta_lapto"
    cursor.execute(sql)
    vent_lapto = cursor.fetchall()
    return render_template('administrador.html', telefono=data_telef, lapto=data_lapto, venta_tel = vent_telef, venta_lap= vent_lapto, ptt=precio_total_telef, ptl=precio_total_lap)

@app.route('/comprar/<string:id>')
def comprar_telef(id):
    cursor = db.connection.cursor()
    print(id)
    mode = "SELECT modelo FROM telefono WHERE id = {0}".format(id)
    cursor.execute(mode)
    modelo = cursor.fetchone()

    mar = "SELECT marca FROM telefono WHERE id = {0}".format(id)
    cursor.execute(mar)
    marca = cursor.fetchone()

    pre = "SELECT precio FROM telefono WHERE id = {0}".format(id)
    cursor.execute(pre)
    precio = cursor.fetchone()


    sql = 'INSERT INTO venta_telefono(modelo, marca, precio) VALUES (%s, %s, %s)'
    valores =(modelo, marca, precio)
    cursor.execute(sql, valores)
    db.connection.commit()

    flash('telefono comprado')

    sql = 'UPDATE telefono SET cantidad = cantidad-1 WHERE id ={0}'.format(id)
    cursor.execute(sql)
    db.connection.commit()

    return redirect(url_for('telefono'))

@app.route('/comprar_lap/<string:id>')
def comprar_lapto(id):
    cursor = db.connection.cursor()
    print (id)
    mode = "SELECT modelo FROM lapto WHERE id = {0}".format(id)
    cursor.execute(mode)
    modelo = cursor.fetchone()

    mar = "SELECT marca FROM lapto WHERE id = {0}".format(id)
    cursor.execute(mar)
    marca = cursor.fetchone()

    pre = "SELECT precio FROM lapto WHERE id = {0}".format(id)
    cursor.execute(pre)
    precio = cursor.fetchone()


    sql = 'INSERT INTO venta_lapto(id_lapto, modelo, marca, precio) VALUES (%s,%s, %s, %s)'
    valores =(id,modelo, marca, precio)
    cursor.execute(sql, valores)
    db.connection.commit()

    flash('lapto comprada')
    sql = 'UPDATE lapto SET cantidad = cantidad-1 WHERE id ={0}'.format(id)
    cursor.execute(sql)
    db.connection.commit()

    return redirect(url_for('lapto'))

"""

def status_401(error):
    return redirect(url_for('login'))


def status_404(error):
    return "<h1>Página no encontrada</h1>", 404


if __name__=='__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.run(debug=True)
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
     