from extensions import db


class Cliente(db.Model):
    __tablename__ = 'clientes'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    email = db.Column(db.String(120))
    telefono = db.Column(db.String(20))

    #relaciones con ventas
    ventas = db.relationship('Venta',back_populates='cliente')
   
    def __init__(self, nombre=None, email=None, telefono=None):
        self.nombre = nombre
        self.email = email
        self.telefono = telefono

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @staticmethod
    def get_by_id(id):
        return Cliente.query.get(id)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, nombre=None, email=None, telefono=None):
        # Actualiza solo los campos provistos
        if nombre is not None:
            self.nombre = nombre
        if email is not None:
            self.email = email
        if telefono is not None:
            self.telefono = telefono
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()