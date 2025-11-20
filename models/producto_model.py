from extensions import db


class Producto(db.Model):
    __tablename__ = 'productos'
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(120),nullable=False)
    precio = db.Column(db.Float(11,2),nullable=False)
    stock= db.Column(db.Integer,nullable=False)
#relaciones con ventas 
    ventas = db.relationship('Venta',back_populates='producto')


    def __init__(self, descripcion=None, precio=None, stock=None):
        self.descripcion = descripcion
        self.precio = precio
        self.stock = stock

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @staticmethod
    def get_by_id(id):
        return Producto.query.get(id)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, descripcion=None, precio=None, stock=None):
        # Actualiza solo los campos provistos
        if descripcion is not None:
            self.descripcion = descripcion
        if precio is not None:
            self.precio = precio
        if stock is not None:
            self.stock = stock
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()