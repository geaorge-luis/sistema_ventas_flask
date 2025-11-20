from flask import Blueprint, request, redirect, url_for, render_template, abort, flash
from extensions import db
from models.cliente_model import Cliente
from views import cliente_view

cliente_bp = Blueprint('cliente', __name__, url_prefix='/clientes')

@cliente_bp.route('/', methods=['GET'])
def index():
    clientes = Cliente.query.all()
    return cliente_view.list(clientes)

@cliente_bp.route('/new', methods=['GET'])
def new():
    # Muestra el formulario para crear un cliente
    return render_template('clientes/create.html')

@cliente_bp.route("/create", methods=['GET','POST'])
def create():
    if request.method == 'POST':
        nombre = (request.form.get('nombre') or request.form.get('Nombre') or '').strip()
        # Aceptar diferentes posibles "name" en el formulario
        email = (request.form.get('email') or request.form.get('correo') or request.form.get('Email') or request.form.get('Correo') or '').strip()
        telefono = (request.form.get('telefono') or request.form.get('Telefono') or '').strip()

        # Validación: obligatorio y formato básico
        if not email:
            flash('El campo email es obligatorio.', 'danger')
            return render_template('clientes/create.html', nombre=nombre, telefono=telefono, email=email)

        if '@' not in email or '.' not in email.split('@')[-1]:
            flash('Ingrese un email válido.', 'danger')
            return render_template('clientes/create.html', nombre=nombre, telefono=telefono, email=email)

        cliente = Cliente(nombre, email, telefono)
        cliente.save()
        return redirect(url_for('cliente.index'))

    return cliente_view.create() 


@cliente_bp.route("/edit/<int:id>", methods=['GET','POST'])
def edit(id):
    cliente = Cliente.query.get_or_404(id)
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        telefono = request.form.get('telefono')
      
        # actualizar campos explícitamente (no existe cliente.update)
        cliente.update(nombre = nombre,email = email,telefono = telefono)
        db.session.commit()
        return redirect(url_for('cliente.index'))
    return cliente_view.edit(cliente)

   # return render_template('clientes/edit.html', cliente=cliente)

@cliente_bp.route("/delete/<int:id>")
def delete(id):
    cliente = Cliente.get_by_id(id)
    cliente.delete()
    return redirect(url_for('cliente.index'))
