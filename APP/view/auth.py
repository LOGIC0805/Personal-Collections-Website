from flask import request, Flask, jsonify, Blueprint
import json

from APP.view.database import db_session
from APP.view.model import Users

bp_auth = Blueprint("bp_auth", __name__,url_prefix="/bp_auth")
@bp_auth.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        phonenum = request.form['phonenum']
        password = request.form['password']
        name = ''
        msg = ''

        userlist = db_session.query(Users)
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


@bp_auth.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        datas = json.loads(request.get_data())
        phonenum = datas['phonenum']
        name = datas['name']
        password = datas['password']
        password1 = datas['password1']
        msg = ''

        userlist = db_session.query(Users)
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
                    db_session.add(user)
                    db_session.commit()
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


@bp_auth.route('/forget', methods=['POST', 'GET'])
def forget():
    if request.method == 'POST':
        phonenum = request.form['phonenum']
        name = request.form['name']
        password = request.form['password']
        password1 = request.form['password1']
        msg = ''

        userlist = db_session.query(Users)
        flag = 0
        for user in userlist:
            if user.phonenum == phonenum:
                if user.name == name:
                    user.password = password
                    db_session.commit()
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