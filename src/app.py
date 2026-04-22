
import stripe
import psycopg2
import os
import json
import datetime


from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from decimal import Decimal

from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user


from src.config import config
from src.models.ModelUser import ModelUser
from src.models.entities.User import User


app = Flask(__name__)

print(">>> DB:", os.getenv("DATABASE_URL"))

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

app.config.from_object(config['development'])
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY") # necesario para CSRF

csrf = CSRFProtect(app)

login_manager_app = LoginManager(app)

def get_db_connection():
    return psycopg2.connect(
        os.getenv("DATABASE_URL"),
        sslmode="require"
    )

@login_manager_app.user_loader
def load_user(user_id):
    conn = get_db_connection()
    user = ModelUser.get_by_id(conn, user_id)
    return user

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        conn = get_db_connection()

        logged_user = ModelUser.login(conn, username, password)

        conn.close()

        if logged_user is not None:
            login_user(logged_user)

            print(current_user.role)

            if current_user.role == 'user':
                return redirect(url_for('home'))
            elif current_user.role == 'admin':
                return redirect(url_for('administrador'))
            else:
                return redirect(url_for('home'))

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

    conn = get_db_connection()
    ModelUser.register(conn, user)

    return redirect(url_for("login"))

@app.route('/registrarse')
def registrarse():
    return render_template('registrarse.html')


@app.route('/home')
@login_required
def home():
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = "SELECT * FROM producto"
    cursor.execute(sql)
    data = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template('home.html', productos=data)

@app.route('/buscar')
def buscar():
    try:
        texto = request.args.get('q', '')

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM producto WHERE nombre ILIKE %s",
            ('%' + texto + '%',)
        )

        data = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template('home.html', productos=data)

    except Exception as e:
        print("ERROR BUSCAR:", e)
        return "Error en búsqueda", 500

    

@app.route("/categoria/<nombre>")
def categoria(nombre):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM producto WHERE tipo = %s", (nombre,))
    productos = cursor.fetchall()

    cursor.close()
   

    return render_template("home.html", productos=productos)

@app.route("/productos")
def productos():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM producto")
    productos = cursor.fetchall()

    cursor.close()
   

    return render_template("home.html", productos=productos)



@app.route("/add/<int:id>")
def add_to_cart(id):
    conn = get_db_connection()
    cursor = conn.cursor()
   
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

    # volver a dict para mantener la estructura original
    carrito_ordenado = dict(productos)

    return render_template("carrito.html", carrito=carrito_ordenado)

@app.route("/update-carrito", methods=["POST"])
def update_carrito():
    data = request.get_json()

    session["carrito"] = data.get("carrito", {})
    session.modified = True

    return jsonify({"ok": True})


@csrf.exempt
@app.route('/crear-pago', methods=['POST'])
def crear_pago():
    try:
        carrito = session.get("carrito", {})

        user_id = str(current_user.id)

        total = 0
        products = []

        for pid, item in carrito.items():
            total += item["precio"] * item["cantidad"]
            products.append({
                "id": pid,
                "cantidad": item["cantidad"]
            })

        session_stripe = stripe.checkout.Session.create(
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
            metadata={
                'user_id': user_id,
                'products': json.dumps(products)
            },
            success_url='https://proyecto-tienda-s1y8.onrender.com/exito',
            cancel_url='https://proyecto-tienda-s1y8.onrender.com/cancelado',
        )

        return jsonify({'url': session_stripe.url})

    except Exception as e:
        print("ERROR:", e)
        return jsonify({'error': str(e)}), 500



@csrf.exempt
@app.route('/stripe-webhook', methods=['POST'])
def stripe_webhook():

    payload = request.data
    sig_header = request.headers.get('Stripe-Signature')
    endpoint_secret = os.getenv("STRIPE_WEBHOOK_SECRET")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except Exception as e:
        print("❌ Webhook error:", e)
        return '', 400

    if event['type'] == 'checkout.session.completed':

        session_id = event['data']['object']['id']

        session = stripe.checkout.Session.retrieve(session_id)

        metadata = session.metadata or {}

        user_id = metadata.get('user_id')
        products = json.loads(metadata.get('products') or '[]')

        print("USER:", user_id)
        print("PRODUCTS:", products)

        conn = get_db_connection()
        cursor = conn.cursor()

        for p in products:

            product_id = p["id"] if isinstance(p, dict) else p
            cantidad = p.get("cantidad", 1) if isinstance(p, dict) else 1

            cursor.execute("""
                INSERT INTO venta (id_usuario, id_producto)
                VALUES (%s, %s, %s)
            """, (user_id, product_id ))

        conn.commit()
        cursor.close()
        conn.close()

        print("✅ VENTA REGISTRADA")

    return '', 200
@app.route('/exito')
def exito():
    return "Pago realizado correctamente"
    

#administrador
@app.route('/administrador')
@login_required
def administrador():
    return render_template('home.html')


def status_401(error):
    return redirect(url_for('login'))


def status_404(error):
    return "<h1>Página no encontrada</h1>", 404


app.config.from_object(config['development'])
csrf.init_app(app)

app.register_error_handler(401, status_401)
app.register_error_handler(404, status_404)

if __name__ == '__main__':
    app.run(debug=True)
     