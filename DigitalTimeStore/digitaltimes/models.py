from . import db
from datetime import datetime

class Watch(db.Model):
    __tablename__='watches'
    id = db.Column(db.Integer, primary_key=True)
    shortDesc = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text, nullable=False)
    specifications = db.Column(db.Text, nullable=False)
    colour = db.Column(db.String(64), nullable=False)
    style = db.Column(db.String(64), nullable=False)
    review = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(64), nullable=False)
    featured = db.Column(db.Boolean, default=False)

    def __repr__(self):
        str = "id: {}, shortDesc: {}, description: {}, specifications: {} \
                colour: {}, style: {}, price: {}, image: {}, featured: {} \n"
        str = str.format(self.id, self.shortDesc, self.description, self.specifications, self.colour, 
                        self.style, self.price, self.image, self.featured)
        return str

orderdetails = db.Table('orderdetails',
    db.Column('order_id', db.Integer, db.ForeignKey('orders.id'), nullable=False),
    db.Column('watch_id', db.Integer, db.ForeignKey('watches.id'), nullable=False),
    db.Column('quantity', db.Integer, default=1),
    db.PrimaryKeyConstraint('order_id', 'watch_id') )

class Order(db.Model):
    __tablename__='orders'
    id = db.Column(db.Integer, primary_key=True)
    completed = db.Column(db.Boolean, default=False)
    date = db.Column(db.DateTime, default=datetime.now())
    total_cost = db.Column(db.Float)
    name_first = db.Column(db.String(64))
    name_last = db.Column(db.String(64))
    address = db.Column(db.Text)
    email = db.Column(db.String(64))
    phone = db.Column(db.String(64))
    watches = db.relationship("Watch", secondary=orderdetails, backref="orders")

    def get_order_details(self):
        return str(self)

    def __repr__(self):
        str = "id: {}, completed: {}, date: {}, watches: {}, \
                total_cost: {}, name_first: {}, name_last: {}, address: {}, email: {}, phone: {}\n"
        str = str.format(self.id, self.completed, self.date, self.watches, 
                        self.total_cost, self.name_first, self.name_last, self.address, self.email, self.phone)
        return str