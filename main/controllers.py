from main import db
import hashlib
from main.models import User,Menu,Order
from flask import session,redirect

def login(data):
    name = data['name']
    pswd = hashlib.sha256(data['pswd'].encode("utf-8")).hexdigest()
    user = User.query.filter_by(name=name).first()
    if user is None:
        #ユーザーが存在しなければ登録
        new_user = User(
            name = name,
            pswd = pswd)
        db.session.add(new_user)#追加
        db.session.commit()#コミット
        user = User.query.filter_by(name=name).first()
    #パスワードを確認
    if user.pswd == pswd:
        #ログイン
        session['login'] = True
        session['user_id'] = user.id
        session['user_name'] = user.name
        return "ログインしました。"
    else:
        #パスワードエラー
        session['login'] = False
        return "パスワードが違います。"

def logout():
    session.pop('login',None)
    session.pop('user_name',None)
    session.pop('user_id',None)
    return "ログアウトしました。"