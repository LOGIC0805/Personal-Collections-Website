from flask import Flask, render_template, request, jsonify, session, Blueprint
from bson import json_util

bp = Blueprint("collection", __name__,url_prefix="/collection")


    
@bp.route("/add", methods=["POST"])
def add_collection():
    name = request.form.get('name')
    tag = request.form.get('tag', None)
    ret = {'msg':'succuss','name':name}
    """
    插入最末尾
    ret['id'] = 
    """
    return json_util.dumps(ret)

@bp.route("/select", methods=["POST"])
def get_collection():
    # 搜索的关键词
    name = request.form.get('name', None)
    # 搜索对象
    phonenum = request.form.get('phonenum',None)
    collections = []
    """
    collections.append({'id': '1', 'name': 'xuanz','like':1})
    collections.append({'id': '2', 'name': 'mingg','like':2})
    collections.append({'id': '3', 'name': 'wnqian','like':3})
    """
    ret = {'collections':collections,'msg':'succuss'}
    return json_util.dumps(ret)

@bp.route("/isLike", methods=["POST"])
def islike(): 
    ret = {'msg': 'succuss'}
    id = request.form.get('collection_id')
    """
    返回当前用户（用session确定）对这个id的collection是否有点赞
    ans['isLike'] = True
    """
    return json_util.dumps(ret)


@bp.route("/like", methods=["POST"])
def get_like():
    id = request.form.get('colllection_id')
    """
    增加点赞数
    更新用户的点赞状态
    """
    ret = {'msg':'succuss'}
    return json_util.dumps(ret)

@bp.route("/unlike", methods=["POST"])
def get_unlike():
    id = request.form.get('colllection_id')
    """
    减少点赞数
    更新用户的点赞状态
    """
    ret = {'msg':'succuss'}
    return json_util.dumps(ret)

@bp.route("/swap", methods=["POST"])
def swap():
    id = request.form.get('id')
    order = request.form.get('new_order')
    """
    把这个id的collection和顺序是order的collection交换
    编号从零开始，有可能是自己
    """
    ret = {'msg':'succuss'}
    return json_util.dumps(ret)

@bp.route("/delete", methods=["POST"])
def delete():
    id = request.form.get('collection_id')
    """
    删除这个id的collection，记得刷新顺序
    """
    ret = {'msg':'succuss'}
    return json_util.dumps(ret)

@bp.route("/edit", methods=["POST"])
def edit():
    id = request.form.get('collection_id')
    name = request.form.get('name', None)
    tag = request.form.get('tag', None)
    
    """
    全部是none的情况请直接返回
    """
    ret = {'msg':'succuss'}
    return json_util.dumps(ret)