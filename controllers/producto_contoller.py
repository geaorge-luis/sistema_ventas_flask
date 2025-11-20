import os
import sys
from flask import Blueprint, request, redirect, url_for, render_template, abort, flash

# Si ejecutas este archivo directamente (no recomendado), Python no añade
# la raíz del proyecto a sys.path. Añadimos la carpeta padre para que
# `from extensions import db` funcione cuando se ejecuta el script aislado.
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from extensions import db
from models.producto_model import Producto
from views import producto_view

producto_bp = Blueprint('producto', __name__, url_prefix='/productos')

@producto_bp.route('/', methods=['GET'])
def index():
    productos = Producto.query.all()
    return producto_view.list(productos)

@producto_bp.route('/new', methods=['GET'])
def new():
    # Muestra el formulario para crear un producto
    return render_template('productos/create.html')

@producto_bp.route("/create", methods=['GET','POST'])
def create():
    if request.method == 'POST':
        descripcion = (request.form.get('descripcion') or request.form.get('descripcion') or '').strip()
        # Aceptar diferentes posibles "name" en el formulario
        precio = (request.form.get('precio') or request.form.get('correo') or request.form.get('precio') or request.form.get('Correo') or '').strip()
        stock = (request.form.get('stock') or request.form.get('stock') or '').strip()

        # Validación: obligatorio y formato básico
        if not precio:
            flash('El campo precio es obligatorio.', 'danger')
            return render_template('productos/create.html', descripcion=descripcion, stock=stock, precio=precio)

        if '@' not in precio or '.' not in precio.split('@')[-1]:
            flash('Ingrese un precio válido.', 'danger')
            return render_template('productos/create.html', descripcion=descripcion, stock=stock, precio=precio)

        producto = producto(descripcion, precio, stock)
        producto.save()
        return redirect(url_for('producto.index'))

    return producto_view.create() 


@producto_bp.route("/edit/<int:id>", methods=['GET','POST'])
def edit(id):
    producto = Producto.query.get_or_404(id)
    if request.method == 'POST':
        descripcion = request.form.get('descripcion')
        precio = request.form.get('precio')
        stock = request.form.get('stock')
      
        # actualizar campos explícitamente (no existe producto.update)
        producto.update(descripcion = descripcion,precio = precio,stock = stock)
        db.session.commit()
        return redirect(url_for('producto.index'))
    return producto_view.edit(producto)

   # return render_template('productos/edit.html', producto=producto)

@producto_bp.route("/delete/<int:id>")
def delete(id):
    producto = producto.get_by_id(id)
    producto.delete()
    return redirect(url_for('producto.index'))
