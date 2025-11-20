from flask import Blueprint, request, redirect, url_for, render_template, flash
from datetime import datetime
from extensions import db
from models.venta_model import Venta
from models.producto_model import Producto
from models.cliente_model import Cliente

from views import venta_view


venta_bp = Blueprint('venta', __name__, url_prefix='/ventas')


@venta_bp.route('/', methods=['GET'])
def index():
    ventas = Venta.get_all()
    return venta_view.list(ventas)


@venta_bp.route('/new', methods=['GET'])
def new():
    return render_template('ventas/create.html')


@venta_bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        cliente_id= (request.form.get('cliente_id') or '').strip()
        producto_id = (request.form.get('producto_id') or '').strip()
        cantidad = (request.form.get('cantidad') or '').strip()
        fecha_str= (request.form.get('fecha') or '').strip()

        fecha= datetime.strptime(fecha_str, '%Y-%m-%d') if fecha_str else None


        venta = Venta(cliente_id=cliente_id, producto_id=producto_id, cantidad=cantidad, fecha=fecha)
        venta.save()
        return redirect(url_for('venta.index'))

    clientes = Cliente.query.all()
    productos = Producto.query.all()

    return venta_view.create(clientes, productos)


@venta_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    venta = Venta.get_by_id(id)


    if venta is None:
        return render_template('ventas/index.html'), 404

    if request.method == 'POST':
        cliente_id= (request.form.get('cliente_id') or '').strip()
        producto_id = (request.form.get('producto_id') or '').strip()
        cantidad = (request.form.get('cantidad') or '').strip()
        fecha_str= (request.form.get('fecha') or '').strip()

        fecha= datetime.strptime(fecha_str, '%Y-%m-%d') if fecha_str else None

        venta.update(cliente_id=cliente_id, producto_id=producto_id, cantidad=cantidad, fecha=fecha)
        return redirect(url_for('venta.index'))

    clientes = Cliente.query.all()
    productos = Producto.query.all()

    return venta_view.edit(venta, clientes, productos)


@venta_bp.route('/delete/<int:id>')
def delete(id):
    venta = Venta.get_by_id(id)
    if venta:
        venta.delete()
    return redirect(url_for('venta.index'))
