from flask import request, Flask, jsonify
import json
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:cui,logic@127.0.0.1/elderlyassistant'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '24'
db = SQLAlchemy(app)

class Users(db.Model):
    __tablename__ = 'users'
    phonenum = db.Column(db.String(255), primary_key=True)
    password = db.Column(db.String(255))
    name = db.Column(db.String(255))

@app.route('/', methods=['POST', 'GET'])
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        datas = json.loads(request.get_data())
        phonenum = datas['phonenum']
        password = datas['password']
        name  = ''
        msg = ''

        userlist = db.session.query(Users)
        flag = 0
        for user in userlist:
            if user.phonenum == phonenum:
                if user.password == password:
                    flag = 1
                    name = user.name
                else:
                    flag = 2
                break
        if flag == 1:
            return jsonify({'code': 1, 'name': name, 'phonenum': phonenum})
        else:
            if phonenum != '' and password != '':
                if flag == 0:
                    msg = "手机号还未注册！"
                    return jsonify({'code': 0, 'msg': msg})
                else:
                    msg = "密码错误！"
                    return jsonify({'code': 2, 'msg': msg})
            else:
                msg = "请输入完整登录信息！"
                return jsonify({'code': 3, 'msg': msg})
    else:
        msg = "提交失败，请重新登录！"
        return jsonify({'code': 4, 'msg': msg})

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        datas = json.loads(request.get_data())
        phonenum = datas['phonenum']
        name = datas['name']
        password = datas['password']
        password1 = datas['password1']
        msg = ''

        userlist = db.session.query(Users)
        flag = 1
        for user in userlist:
            if user.phonenum == phonenum:
                flag = 0
                break
        if flag == 0:
            msg = "手机号已被注册！"
            return jsonify({'code': 0, 'msg': msg})
        else:
            if phonenum != '' and password != '':
                if password == password1:
                    user = Users(phonenum=phonenum, name=name, password=password)
                    db.session.add(user)
                    db.session.commit()
                    return jsonify({'code': 1, 'name': name, 'phonenum': phonenum})
                else:
                    msg = "两次输入密码不一致！"
                    return jsonify({'code': 2, 'msg': msg})
            else:
                msg = "请输入完整登录信息！"
                return jsonify({'code': 3, 'msg': msg})
    else:
        msg = "提交失败，请重新注册！"
        return jsonify({'code': 4, 'msg': msg})

@app.route('/forget', methods=['POST', 'GET'])
def forget():
    if request.method == 'POST':
        datas = json.loads(request.get_data())
        phonenum = datas['phonenum']
        name = datas['name']
        password = datas['password']
        password1 = datas['password1']
        msg = ''

        userlist = db.session.query(Users)
        flag = 0
        for user in userlist:
            if user.phonenum == phonenum:
                if user.name == name:
                    user.password = password
                    db.session.commit()
                    flag = 1
                else:
                    flag = 2
                break
        if flag == 0:
            msg = "手机号还未注册！"
            return jsonify({'code': 0, 'msg': msg})
        else:
            if phonenum != '' and password != '':
                if password == password1:
                    if flag == 1:
                        msg = "修改密码成功！"
                        return jsonify({'code': 1, 'name': name, 'phonenum': phonenum})
                    else:
                        msg = "用户名输入错误！"
                        return jsonify({'code': 2, 'msg': msg})
                else:
                    msg = "两次输入密码不一致！"
                    return jsonify({'code': 3, 'msg': msg})
            else:
                msg = "请输入完整修改密码信息！"
                return jsonify({'code': 4, 'msg': msg})
    else:
        msg = "提交失败，请重新修改密码！"
        return jsonify({'code': 5, 'msg': msg})