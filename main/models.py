from main import db
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import hashlib

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True,nullable=False,unique=True)
    name = db.Column(db.String(100),nullable=False)
    pswd = db.Column(db.String(256),nullable=False)
    resist_date = db.Column(db.DateTime,default=datetime.now())
    
    def __init__(self,name=None,pswd=None):
        self.name = name
        self.pswd = pswd
        
    def __repr__(self):
        return f"<ID:{self.id}, Name:{self.name}, pswd:{self.pswd}>"

class Menu(db.Model):
    __tablename__ = 'menu'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True,nullable=False,unique=True)
    name = db.Column(db.String(100),nullable=False)
    path = db.Column(db.String(100))
    base = db.Column(db.String(100))
    caption = db.Column(db.String(300))
    
    def __init__(self,name=None,path=None,base=None,caption=None):
        self.name = name
        self.path = path
        self.base = base
        self.caption = caption
    
    def __repr__(self):
        return f"<ID:{self.id}, Name:{self.name}, path:{self.path}, base:{self.base}, caption:{self.caption}>"

class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True,nullable=False,unique=True)
    order_date = db.Column(db.DateTime,default=datetime.now())
    user = db.Column(db.String(100),nullable=False)
    menu = db.Column(db.String(100),nullable=False)
    serve_date = db.Column(db.DateTime)
    done = db.Column(db.Boolean,nullable=False,default=False)
    
    def __init__(self,order_date=None,user=None,menu=None,serve_date=None):
        self.order_date = order_date
        self.user = user
        self.menu = menu
        self.serve_date = serve_date
    
    def __repr__(self):
        return f"<ID:{self.id}, date:{self.date}, user:{self.user}, menu:{self.menu}>"

def init():
    db.create_all()
    user = User.query.filter_by(name='test').first()
    if user is None:
        test_user= User(
            name="test",
            pswd = hashlib.sha256("test".encode("utf-8")).hexdigest()
        )
        db.session.add(test_user)#追加
        db.session.commit()#コミット