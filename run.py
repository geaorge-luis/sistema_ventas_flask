from flask import Flask
import os
from controllers import usuario_controller, cliente_controller
from controllers import producto_controller
from controllers import venta_controller
from extensions import db
from sqlalchemy import inspect

app = Flask(__name__)

# SECRET_KEY necesaria para sesiones de Flask. En producción use una variable de entorno
# segura, p. ej. `setx SECRET_KEY (openssl rand -hex 32)` en Windows o configure en su
# sistema de despliegue. Aquí usamos una clave por defecto para desarrollo.
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ventas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  # Registrar la instancia db con la app

with app.app_context():
    # Comprobamos si la tabla 'usuarios' tiene la columna 'email'.
    # En desarrollo: si falta, dropeamos y recreamos todas las tablas para sincronizar el esquema.
    try:
        inspector = inspect(db.engine)
        if db.engine.has_table('usuarios'):
            cols = [c['name'] for c in inspector.get_columns('usuarios')]
            if 'email' not in cols:
                print("La columna 'email' falta en 'usuarios'. Recreate tablas (desarrollo).")
                db.drop_all()
                db.create_all()
            else:
                # Tablas existentes ya contienen la columna esperada
                db.create_all()
        else:
            # No existe la tabla, crear todo
            db.create_all()
    except Exception as e:
        print("Error inspeccionando la base de datos:", e)
        # Fallback: intentar recrear (desarrollo)
        try:
            db.drop_all()
            db.create_all()
        except Exception as e2:
            print("No se pudo recrear la base de datos automáticamente:", e2)

    app.register_blueprint(usuario_controller.usuario_bp)

    app.register_blueprint(cliente_controller.cliente_bp)
    
    app.register_blueprint(producto_controller.producto_bp)
    app.register_blueprint(venta_controller.venta_bp)
@app.route("/")
def home():
    return "<h1>apliacion de ventas</h1>"

if __name__ == "__main__":

    app.run(debug=True)
