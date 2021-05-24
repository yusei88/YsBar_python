from flask import render_template, request, redirect,Response, abort,session
from main import app, db, controllers
from main.models import User,Menu,Order
from werkzeug.utils import secure_filename
import os, hashlib
from datetime import datetime

#画像拡張子チェック関数
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

#Top画面
@app.route('/')
def index():
    return render_template('index.html',title="Y'sBar")

@app.route('/login',methods=['GET','POST'])
def login():
    #ログイン画面表示
    if request.method == 'GET':
        return render_template('login.html',title="ログイン")
    #ログイン情報受け取り
    else:
        session['msg'] = controllers.login(request.form)
        return redirect('/')

@app.route('/logout')
def logout():
    session['msg'] = controllers.logout()
    return redirect('/')

#メニュー一覧画面
@app.route('/menu',methods=['GET'])
def menu():
    menu = Menu.query.all()
    return render_template('menu.html', title="メニュー",data=menu)

#メニュー登録画面
@app.route('/resister',methods=['GET'])
def resist_get():
    print(os.getcwd())
    return render_template('menu_resist.html', title="メニュー登録",message=False)

#メニュー登録送信先
@app.route('/resister',methods=['POST'])
def resist_post():
    pswd = hashlib.sha256(request.form['pswd'].encode("utf-8")).hexdigest()
    if (pswd == app.config['UPLOAD_PSWD']):
        enter_name = request.form['name']
        enter_caption = request.form['caption']
        enter_base = request.form['base']
        enter_img = request.files['img']
        if enter_img and allowed_file(enter_img.filename):
            img_path = os.path.join(app.config['UPLOAD_FOLDER'], enter_img.filename)
            enter_img.save(os.path.join("./main",img_path))
            exist = Menu.query.filter_by(name=enter_name).count()#カクテルの名前が登録されているか確認する
            if exist == 0:#メニューに名前が登録されていなければ登録する
                print("NewMenu!!Welcome!")
                #インスタンス作成
                new_menu = Menu(
                    name=enter_name,
                    path=img_path,
                    caption=enter_caption,
                    base=enter_base)
                db.session.add(new_menu)#追加
                db.session.commit()#コミット
                msg="登録しました。"
            else:
                msg="既に存在するメニューです。"
        else:
            msg="不正なファイルです。"
    else:
        msg = 'パスワードが違います。'
    return render_template('menu_resist.html', title="メニュー登録",message=msg)

@app.route('/order',methods=['GET'])
def order_get():
    order = Order.query.filter_by(done=False).all()
    return render_template('order.html',title="オーダー",data=order)

#送信されたオーダーをDBに登録
@app.route('/api/orders',methods=['POST'])
def orders_post():
    order=request.form['order']
    #インスタンス作成
    new_order = Order(
        menu=order,
        user=session['user_name'])
    db.session.add(new_order)#追加
    db.session.commit()#コミット
    return Response('OK')

#完了したオーダーを更新
@app.route('/api/orders/<order_id>',methods=['PUT'])
def put_order(order_id):
    print(order_id)
    order = Order.query.filter_by(id=order_id).first()
    if not order:
        abort(404,{'code':'Not found.','message':'order not found.'})#エラー表示
    order.serve_date = datetime.now()
    order.done = True
    db.session.commit()
    return Response('OK')
