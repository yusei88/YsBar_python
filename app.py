from flask import Flask, render_template, request, redirect, session
from flask.helpers import url_for
from flask.wrappers import Response
from sqlalchemy import create_engine, Column, Integer, String, DATETIME
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from werkzeug.utils import secure_filename
import os, hashlib

app = Flask(__name__)

#画像アップロードの設定
UPLOAD_FOLDER = './static/uploads/'
ALLOWED_EXTENSIONS = set(['png', 'jpg'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = os.urandom(24)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

#DBの作成
engine = create_engine('sqlite:///ysbar.db',echo=True)
Base = declarative_base()
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer,primary_key=True,autoincrement=True,nullable=False,unique=True)
    name = Column(String(100),nullable=False)
    pswd = Column(String(256),nullable=False)

class Menu(Base):
    __tablename__ = 'menu'
    id = Column(Integer,primary_key=True,autoincrement=True,nullable=False,unique=True)
    name = Column(String(100),nullable=False)
    path = Column(String(100))
    base = Column(String(100))
    caption = Column(String(300))

class Order(Base):
    __tablename__ = 'order'
    id = Column(Integer,primary_key=True,autoincrement=True,nullable=False,unique=True)
    date = Column(String(100),nullable=False)
    user = Column(String(100),nullable=False)
    menu = Column(String(100),nullable=False)

Base.metadata.create_all(bind=engine)#db作成の実行

@app.context_processor
def add_staticfile():
    def staticfile_cp(fname):
        path = os.path.join(app.root_path, 'static', fname)
        mtime =  str(int(os.stat(path).st_mtime))
        return '/static/' + fname + '?v=' + str(mtime)
    return dict(staticfile=staticfile_cp)

@app.route('/',methods=['GET'])
def hello():
    return render_template('index.html', title="Y'sBAR")

@app.route('/login',methods=['GET'])
def login_get():
    return render_template('login.html', title="ログイン",miss=False)
@app.route('/login',methods=['POST'])
def login_post():
    enter_name = request.form.get('name').strip()
    enter_pswd = str(hashlib.sha256(request.form["pswd"].strip().encode("utf-8")).digest())
    session = sessionmaker(bind=engine)()#db用のsessionの作成
    print("Name : ",enter_name)
    print("Pass : ",enter_pswd)
    exist = session.query(User).filter(User.name == enter_name).count()#user名が登録されているか確認する
    print("exist : ",exist)
    if exist == 0:#もしユーザー名が登録されていなければパスワードとともに登録する
        print("NewUser!!Welcome!")
        new_user = User(name=enter_name,pswd=enter_pswd)#インスタンス作成
        session.add(new_user)#追加
        session.commit()#コミット
        session.close()#sessionの解放
        return redirect('/')
    else:#もしユーザー名が登録されていればパスワードのハッシュ値を確認
        session.close()#sessionの解放
        user = session.query(User).filter(User.name == enter_name).one()
        print("Name : ",user.name)
        print("ResistedPass : ",user.pswd)
        print("SendedPass : ",enter_pswd)
        if user.pswd == enter_pswd:
            #パスワードがあっていればトップページへ
            print("ResistedUser!!Welcome!")
            return redirect('/')
        else:
            #パスワードが間違っていればもう一度
            print("ユーザー名かPasswordが間違っています。")
            return render_template('/login.html',title="ログイン",miss=True)

@app.route('/menu',methods=['GET'])
def menu():
    session = sessionmaker(bind=engine)()#db用のsessionの作成
    data = session.query(Menu).all()
    return render_template('menu.html', title="メニュー",data=data)

@app.route('/resister',methods=['GET'])
def resist_get():
    return render_template('menu_resist.html', title="メニュー登録",message=False)

@app.route('/resister',methods=['POST'])
def resist_post():
    enter_name = request.form.get('name').strip()
    enter_caption = request.form.get('caption').strip()
    enter_base = request.form.get('base')
    enter_img = request.files['img']
    if enter_img and allowed_file(enter_img.filename):
        session = sessionmaker(bind=engine)()#db用のsessionの作成
        enter_img.save(os.path.join(app.config['UPLOAD_FOLDER'], enter_img.filename))
        img_path = UPLOAD_FOLDER + enter_img.filename
        exist = session.query(Menu).filter(Menu.name == enter_name).count()#カクテルの名前が登録されているか確認する
        if exist == 0:#メニューに名前が登録されていなければ登録する
            print("NewMenu!!Welcome!")
            new_menu = Menu(name=enter_name,path=img_path,caption=enter_caption,base=enter_base)#インスタンス作成
            session.add(new_menu)#追加
            session.commit()#コミット
            session.close()#sessionの解放
            msg="登録しました。"
        else:
            msg="既に存在するメニューです。"
    else:
        msg="不正なファイルです。"
    return render_template('menu_resist.html', title="メニュー登録",message=msg)

@app.route('/order',methods=['GET'])
def order_get():
    session = sessionmaker(bind=engine)()#db用のsessionの作成
    data = session.query(Order).all()
    return render_template('order.html',title="オーダー",data=data)

@app.route('/order_list',methods=['POST'])
def order_list_post():
    #送信されたオーダーをDBに登録
    order=request.form.get('order')
    order_date=request.form.get('date')
    session = sessionmaker(bind=engine)()#db用のsessionの作成
    new_order = Order(date=order_date,menu=order,user="test")#インスタンス作成
    session.add(new_order)#追加
    session.commit()#コミット
    session.close()#sessionの解放
    return Response('OK')


if __name__ == "__main__":
    app.run(debug=True)