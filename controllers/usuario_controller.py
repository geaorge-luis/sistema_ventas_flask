from flask import Blueprint, request, redirect, url_for, render_template, abort
from extensions import db
from models.usuario_model import Usuario
from views import usuario_view

usuario_bp = Blueprint('usuario', __name__, url_prefix='/usuarios')

@usuario_bp.route('/', methods=['GET'])
def index():
    usuarios = Usuario.query.all()
    return usuario_view.list(usuarios)

@usuario_bp.route('/new', methods=['GET'])
def new():
    # Muestra el formulario para crear un usuario
    return render_template('usuarios/create.html')

@usuario_bp.route('/create', methods=['POST'])
def create():
    if request.method == 'POST':
        nombre = request.form['nombre']
        username = request.form['username']
        email = request.form.get('email')
        password = request.form['password']
        rol = request.form['rol']
        # Validar email/username único básico
        if email and Usuario.query.filter_by(email=email).first():
            return "El correo ya está registrado", 400
        if Usuario.query.filter_by(username=username).first():
            return "El usuario ya existe", 400

        usuario = Usuario(nombre=nombre, username=username, email=email, password=password, rol=rol)
        db.session.add(usuario)
        db.session.commit()
        return redirect(url_for('usuario.index'))
    return usuario_view.create()

@usuario_bp.route("/edit/<int:id>", methods=['GET','POST'])
def edit(id):
    usuario = Usuario.query.get_or_404(id)
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        rol = request.form.get('rol')

        # actualizar campos explícitamente (no existe usuario.update)
        usuario.nombre = nombre
        usuario.username = username
        if email:
            usuario.email = email
        if password:
            usuario.password = Usuario.hash_password(password)
        usuario.rol = rol

        db.session.commit()
        return redirect(url_for('usuario.index'))

    return render_template('usuarios/edit.html', usuario=usuario)

@usuario_bp.route("/delete/<int:id>")
def delete(id):
    usuario = Usuario.get_by_id(id)
    usuario.delete()
    return redirect(url_for('usuario.index'))
