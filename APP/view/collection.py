from flask import Flask, render_template, request, jsonify, session, Blueprint
from bson import json_util
import random
from APP.view.database import db_session
from APP.view.model import Collection, UserLike
import uuid

bp_collection = Blueprint("collection", __name__, url_prefix="/collection")


@bp_collection.route("/add", methods=["POST"])
def add_collection():
    name = request.form.get('name')
    tag = request.form.get('tag', None)
    phonenum = request.form.get('phonenum')
    id = str(uuid.uuid1())
    try:
        count = Collection.query.count()
        print(count)
        c = Collection(id=id, name=name, tag=tag, phonenum=phonenum, order=count)
        db_session.add(c)
        db_session.commit()
    except BaseException as e:
        print(e)
        ret = {'msg': 'failed!', 'name': name}
        return json_util.dumps(ret)

    ret = {'msg': 'succuss', 'name': name, 'id': id}
    """；
    插入最末尾
    ret['id'] = 
    """
    return json_util.dumps(ret)


@bp_collection.route("/select", methods=["POST"])
def get_collection():
    # 搜索的关键词
    name = request.form.get('name', "")
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
                                                  Collection.phonenum == phonenum).order_by(Collection.order).all()
        for item in row:
            collection_tmp = {}
            collection_tmp['id'] = item.id
            collection_tmp['name'] = item.name
            collection_tmp['like'] = item.like
            collection_tmp['tag'] = item.tag
            collection_tmp['order'] = item.order
            collections.append(collection_tmp)

    except BaseException as e:
        print(str(e))
        ret = {'msg': 'failed!'}
        return json_util.dumps(ret)
    ret = {'collections': collections, 'msg': 'succuss'}
    return json_util.dumps(ret)


@bp_collection.route("/recommand", methods=["POST"])
def recommand_collection():
    phonenum = request.form.get('phonenum')
    collections = []
    """
    返回推荐的内容
    collections.append({'id': '1', 'name': 'xuanz','like':1})
    collections.append({'id': '2', 'name': 'mingg','like':2})
    collections.append({'id': '3', 'name': 'wnqian','like':3})
    """
    try:
        row0 = db_session.query(Collection).join(UserLike, UserLike.collection_id == Collection.id).filter(
            UserLike.phonenum == phonenum).all()
        # 构建用户tag字典
        user_like = {}
        for collection in row0:
            tag_tmp = collection.tag
            if tag_tmp in user_like.keys():
                user_like[tag_tmp] += 1
            else:
                user_like[tag_tmp] = 1
        print(user_like)

        row = db_session.query(Collection).filter().all()
        for item in row:
            collection_tmp = {}
            collection_tmp['id'] = item.id
            collection_tmp['name'] = item.name
            collection_tmp['like'] = item.like
            collection_tmp['tag'] = item.tag
            collection_tmp['priority'] = user_like[item.tag] if item.tag in user_like.keys() else 0
            collections.append(collection_tmp)
        # 对tag相关性进行排序
        collections_new = sorted(collections, key=lambda x: x.__getitem__('priority'), reverse=True)
    except BaseException as e:
        print(str(e))
        ret = {'msg': 'failed!'}
        return json_util.dumps(ret)
    ret = {'collections': collections_new, 'msg': 'succuss'}
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
    phonenum = request.form.get('phonenum')
    """
    增加点赞数
    更新用户的点赞状态
    """
    ret = {'msg': 'succuss'}
    try:
        s = UserLike(phonenum=phonenum, collection_id=id, state=1)
        row = db_session.query(UserLike).filter(UserLike.collection_id == id, UserLike.phonenum == phonenum).first()
        if row is None:
            db_session.add(s)
            db_session.query(Collection).filter(Collection.id == id).update({Collection.like: Collection.like + 1})
            db_session.commit()
        else:
            db_session.query(UserLike).filter(UserLike.collection_id == id, UserLike.phonenum == phonenum).update(
                {UserLike.state: 1})
            db_session.query(Collection).filter(Collection.id == id).update({Collection.like: Collection.like + 1})
            db_session.commit()

    except BaseException as e:
        print(str(e))
        ret = {'msg': 'failed!'}
        return json_util.dumps(ret)
    return json_util.dumps(ret)


@bp_collection.route("/unlike", methods=["POST"])
def get_unlike():
    id = request.form.get('collection_id')
    phonenum = request.form.get('phonenum')
    """
    减少点赞数
    更新用户的点赞状态
    """
    ret = {'msg': 'succuss'}
    try:
        db_session.query(UserLike).filter(UserLike.collection_id == id, UserLike.phonenum == phonenum).update(
            {UserLike.state: 0})
        db_session.query(Collection).filter(Collection.id == id).update({Collection.like: Collection.like - 1})
        db_session.commit()
    except BaseException as e:
        print(str(e))
        ret = {'msg': 'failed!'}
        return json_util.dumps(ret)
    return json_util.dumps(ret)


@bp_collection.route("/swap", methods=["POST"])
def swap():
    id = request.form.get('id')
    order = request.form.get('new_order')
    """
    把这个id的collection和顺序是order的collection交换
    编号从零开始，有可能是自己
    """
    try:
        item1 = db_session.query(Collection).filter(Collection.id == id).first()
        item2 = db_session.query(Collection).filter(Collection.order == order).first()
        order1 = item1.order
        # order2 = item2.order
        id2 = item2.id
        db_session.query(Collection).filter(Collection.id == id).update({Collection.order: order})
        db_session.query(Collection).filter(Collection.id == id2).update({Collection.order: order1})
        db_session.commit()
    except BaseException as e:
        print(str(e))
        ret = {'msg': 'failed!'}
        return json_util.dumps(ret)

    ret = {'msg': 'succuss'}
    return json_util.dumps(ret)


@bp_collection.route("/delete", methods=["POST"])
def delete():
    id = request.form.get('collection_id')
    """
    删除这个id的collection，记得刷新顺序
    """
    try:
        # 删除collection
        item = db_session.query(Collection).filter(Collection.id == id).first()
        order_item = item.order
        db_session.delete(item)

        # 刷新order顺序
        db_session.query(Collection).filter(Collection.order > order_item).update(
            {Collection.order: Collection.order - 1})
        db_session.commit()
    except BaseException as e:
        print(str(e))
        ret = {'msg': 'failed!'}
        return json_util.dumps(ret)

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
    if id is None and name is None and tag is None:
        ret = {'msg': 'id,name,tag are all none!'}
        return json_util.dumps(ret)
    try:
        db_session.query(Collection).filter(Collection.id == id).update({Collection.name: name, Collection.tag: tag})
        db_session.commit()
    except BaseException as e:
        print(str(e))
        ret = {'msg': 'failed!'}
        return json_util.dumps(ret)

    ret = {'msg': 'succuss'}
    return json_util.dumps(ret)
