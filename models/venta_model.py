from extensions import db

class Venta(db.Model):
    __tablename__ = 'ventas'
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    fecha = db.Column(db.DateTime, nullable=False)
   # total = db.Column(db.Float(11,2), nullable=False)
    #relaciones con cliente y producto
    cliente = db.relationship('Cliente', back_populates='ventas')
    producto= db.relationship('Producto', back_populates='ventas')
    
    def __init__(self, cliente_id=None, producto_id=None, cantidad=None, fecha=None):
        self.cliente_id = cliente_id
        self.producto_id = producto_id
        self.cantidad = cantidad
        self.fecha = fecha
    @classmethod
    def get_all(cls):
        return cls.query.all()

    @staticmethod
    def get_by_id(id):
        return Venta.query.get(id)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self,cliente_id=None, producto_id=None, cantidad=None, fecha=None):
        # Actualiza solo los campos provistos
        if cliente_id is not None:
            self.cliente_id = cliente_id
        if producto_id is not None:
            self.producto_id = producto_id
        if cantidad is not None:
            self.cantidad = cantidad
        if fecha is not None:
            self.fecha = fecha
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()