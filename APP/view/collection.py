from flask import Flask, render_template, request, jsonify, session, Blueprint
from bson import json_util
import random
from APP.view.database import db_session
from APP.view.model import Collection, UserLike

bp_collection = Blueprint("collection", __name__, url_prefix="/collection")


@bp_collection.route("/add", methods=["POST"])
def add_collection():
    name = request.form.get('name')
    tag = request.form.get('tag', None)
    phonenum = request.form.get('phonenum')
    try:
        count = Collection.query.count()
        print(count)
        c = Collection(id=count + 1, name=name, tag=tag, phonenum=phonenum)
        db_session.add(c)
        db_session.commit()
    except BaseException as e:
        print(e)
        ret = {'msg': 'failed!', 'name': name}
        return json_util.dumps(ret)

    ret = {'msg': 'succuss', 'name': name, 'id': str(count + 1)}
    """；
    插入最末尾
    ret['id'] = 
    """
    return json_util.dumps(ret)


@bp_collection.route("/select", methods=["POST"])
def get_collection():
    # 搜索的关键词
    name = request.form.get('name', None)
    # 搜索对象
    phonenum = request.form.get('phonenum', None)
    collections = []
    """
    collections.append({'id': '1', 'name': 'xuanz','like':1})
    collections.append({'id': '2', 'name': 'mingg','like':2})
    collections.append({'id': '3', 'name': 'wnqian','like':3})
    """
    try:
        row = db_session.query(Collection).filter(Collection.name.like('%' + name + '%'),
                                                  Collection.phonenum == phonenum).all()
        for item in row:
            collection_tmp = {}
            collection_tmp['id'] = item.id
            collection_tmp['name'] = item.name
            collection_tmp['like'] = item.like
            collection_tmp['tag'] = item.tag
            collections.append(collection_tmp)

    except BaseException as e:
        print(str(e))
        ret = {'msg': 'failed!'}
        return json_util.dumps(ret)
    ret = {'collections': collections, 'msg': 'succuss'}
    return json_util.dumps(ret)


@bp_collection.route("/recommand", methods=["POST"])
def recommand_collection():
    collections = []
    """
    返回推荐的内容
    collections.append({'id': '1', 'name': 'xuanz','like':1})
    collections.append({'id': '2', 'name': 'mingg','like':2})
    collections.append({'id': '3', 'name': 'wnqian','like':3})
    """
    try:
        row = db_session.query(Collection).filter().all()
        for item in row:
            collection_tmp = {}
            collection_tmp['id'] = item.id
            collection_tmp['name'] = item.name
            collection_tmp['like'] = item.like
            collection_tmp['tag'] = item.tag
            random_int = random.randint(0, 9)
            if random_int <= 4:
                continue
            else:
                collections.append(collection_tmp)
    except BaseException as e:
        print(str(e))
        ret = {'msg': 'failed!'}
        return json_util.dumps(ret)
    ret = {'collections': collections, 'msg': 'succuss'}
    return json_util.dumps(ret)


@bp_collection.route("/isLike", methods=["POST"])
def islike():
    id = request.form.get('collection_id')
    phonenum = request.form.get('phonenum')
    """
    返回当前用户（用session确定）对这个id的collection是否有点赞
    ans['isLike'] = True
    """
    row = db_session.query(UserLike).filter(UserLike.collection_id == id, UserLike.phonenum == phonenum,
                                            UserLike.state == 1).first()
    print(row, id, phonenum)
    if row is not None:
        islike = True
    else:
        islike = False
    ret = {'msg': 'succuss', 'isLike': islike}
    return json_util.dumps(ret)


@bp_collection.route("/like", methods=["POST"])
def get_like():
    id = request.form.get('collection_id')
    """
    增加点赞数
    更新用户的点赞状态
    """
    ret = {'msg': 'succuss'}
    return json_util.dumps(ret)


@bp_collection.route("/unlike", methods=["POST"])
def get_unlike():
    id = request.form.get('colllection_id')
    """
    减少点赞数
    更新用户的点赞状态
    """
    ret = {'msg': 'succuss'}
    return json_util.dumps(ret)


@bp_collection.route("/swap", methods=["POST"])
def swap():
    id = request.form.get('id')
    order = request.form.get('new_order')
    """
    把这个id的collection和顺序是order的collection交换
    编号从零开始，有可能是自己
    """
    ret = {'msg': 'succuss'}
    return json_util.dumps(ret)


@bp_collection.route("/delete", methods=["POST"])
def delete():
    id = request.form.get('collection_id')
    """
    删除这个id的collection，记得刷新顺序
    """
    ret = {'msg': 'succuss'}
    return json_util.dumps(ret)


@bp_collection.route("/edit", methods=["POST"])
def edit():
    id = request.form.get('collection_id')
    name = request.form.get('name', None)
    tag = request.form.get('tag', None)

    """
    全部是none的情况请直接返回
    """
    ret = {'msg': 'succuss'}
    return json_util.dumps(ret)
