from flask import Blueprint, request, redirect, url_for, render_template, flash
from extensions import db
from models.producto_model import Producto
from views import producto_view

producto_bp = Blueprint('producto', __name__, url_prefix='/productos')


@producto_bp.route('/', methods=['GET'])
def index():
    productos = Producto.get_all()
    return producto_view.list(productos)


@producto_bp.route('/new', methods=['GET'])
def new():
    return render_template('productos/create.html')


@producto_bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        descripcion = (request.form.get('descripcion') or '').strip()
        precio_raw = (request.form.get('precio') or '').strip()
        stock_raw = (request.form.get('stock') or '').strip()

        if not precio_raw:
            flash('El campo precio es obligatorio.', 'danger')
            return render_template('productos/create.html', descripcion=descripcion, stock=stock_raw, precio=precio_raw)

        try:
            precio = float(precio_raw)
        except ValueError:
            flash('Ingrese un precio numérico válido.', 'danger')
            return render_template('productos/create.html', descripcion=descripcion, stock=stock_raw, precio=precio_raw)

        try:
            stock = int(stock_raw) if stock_raw != '' else 0
        except ValueError:
            flash('Ingrese un stock entero válido.', 'danger')
            return render_template('productos/create.html', descripcion=descripcion, stock=stock_raw, precio=precio_raw)

        producto = Producto(descripcion=descripcion, precio=precio, stock=stock)
        producto.save()
        return redirect(url_for('producto.index'))

    return producto_view.create()


@producto_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    producto = Producto.get_by_id(id)
    if producto is None:
        return render_template('productos/index.html'), 404

    if request.method == 'POST':
        descripcion = request.form.get('descripcion')
        precio_raw = request.form.get('precio')
        stock_raw = request.form.get('stock')

        precio = None
        stock = None
        if precio_raw is not None and precio_raw != '':
            try:
                precio = float(precio_raw)
            except ValueError:
                flash('Ingrese un precio numérico válido.', 'danger')
                return producto_view.edit(producto)
        if stock_raw is not None and stock_raw != '':
            try:
                stock = int(stock_raw)
            except ValueError:
                flash('Ingrese un stock entero válido.', 'danger')
                return producto_view.edit(producto)

        producto.update(descripcion=descripcion, precio=precio, stock=stock)
        return redirect(url_for('producto.index'))

    return producto_view.edit(producto)


@producto_bp.route('/delete/<int:id>')
def delete(id):
    producto = Producto.get_by_id(id)
    if producto:
        producto.delete()
    return redirect(url_for('producto.index'))
