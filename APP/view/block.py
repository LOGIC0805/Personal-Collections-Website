from flask import Flask, render_template, request, jsonify, session, Blueprint
from bson import json_util

bp = Blueprint("block", __name__,url_prefix="/block")


@bp.route("/add", methods=["POST"])
def add_block():
    type = request.form.get('type')
    content = request.form.get("content")
    ret = {'msg': 'succuss'}
    """
    插入最末尾
    ret['id'] = 
    """
    return json_util.dumps()


@bp.route("/select", methods=["POST"])
def get_block():
    # 查询这个id的collection的block
    id = request.form.get('id')
    blocks = []
    """
    blocks.append({'id': '1', 'content': 'xuanz','type':'text'})
    blocks.append({'id': '2', 'content': 'mingg','type':'url'})
    blocks.append({'id': '3', 'content': 'wnqian','type':'picture'})
    """
    ans = {'blocks':blocks,'msg':'succuss'}
    return json_util.dumps(ans)



@bp.route("/delete", methods=["POST"])
def delete():
    collection_id = request.form.get('collection_id')
    block_id = request.form.get('block_id')
    """
    删除这个id的collection的block，记得刷新顺序
    """
    ret = {'msg':'succuss'}
    return json_util.dumps(ret)

@bp.route("/swap", methods=["POST"])
def swap():
    id = request.form.get('id')
    collection_id = request.form.get('collection_id')
    order = request.form.get('new_order')
    """
    把这个collection_id的collection的这个id的块和顺序是order的块交换
    编号从零开始，有可能是自己
    """
    ret = {'msg':'succuss'}
    return json_util.dumps(ret)

@bp.route("/edit", methods=["POST"])
def edit():
    collection_id = request.form.get('collection_id')
    block_id = request.form.get('block_id')
    content = request.form.get('content',None)
    
    """
    content = none的情况请直接返回
    """
    ret = {'msg':'succuss'}
    return json_util.dumps(ret)


@bp.route("/get_web_name", methods=["POST"])
def get_web_name():
    url = request.form.get('url')
    ret = {'msg':'succuss'}
    """
    ret['name'] = url对应的网站的title，没有就返回url
    """
    
    return json_util.dumps(ret)