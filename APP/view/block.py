from flask import Flask, render_template, request, jsonify, session, Blueprint
from bson import json_util
import uuid

from APP.view.database import db_session
from APP.view.model import Block, CollectionBlock

bp_block = Blueprint("block", __name__, url_prefix="/block")


@bp_block.route("/add", methods=["POST"])
def add_block():
    type = request.form.get('type')
    content = request.form.get("content")
    collection_id = request.form.get("collection_id")
    id = str(uuid.uuid4())

    try:
        count = Block.query.count()
        print(count)
        if type == 'text' or type == 'url':
            b = Block(type=type, content_text=content, order=count, id=id)
        else:
            b = Block(type=type, content_pic=content, order=count, id=id)
        db_session.add(b)
        cb = CollectionBlock(id=collection_id, block_id=id)
        db_session.add(cb)
        db_session.commit()
    except BaseException as e:
        print(e)
        ret = {'msg': 'failed!', 'collection_id': collection_id}
        return json_util.dumps(ret)
    ret = {'msg': 'succuss', 'id': id}
    """
    插入最末尾
    ret['id'] = 
    """
    return json_util.dumps(ret)


@bp_block.route("/select", methods=["POST"])
def get_block():
    # 查询这个id的collection的block
    id = request.form.get('id')
    blocks = []
    """
    blocks.append({'id': '1', 'content': 'xuanz','type':'text'})
    blocks.append({'id': '2', 'content': 'mingg','type':'url'})
    blocks.append({'id': '3', 'content': 'wnqian','type':'picture'})
    """
    try:
        row = db_session.query(Block).join(CollectionBlock, CollectionBlock.block_id == Block.id).filter(
            CollectionBlock.id == id).all()
        for item in row:
            block_tmp = {}
            block_tmp['id'] = item.id
            block_tmp['type'] = item.type
            if item.type == 'url' or item.type == 'text':
                block_tmp['content'] = item.content_text
            else:
                block_tmp['content'] = item.content_pic
            block_tmp['order'] = item.order
            blocks.append(block_tmp)
    except BaseException as e:
        print(str(e))
        ans = {'msg': 'failed'}
        return json_util.dumps(ans)

    ans = {'blocks': blocks, 'msg': 'succuss'}
    return json_util.dumps(ans)


@bp_block.route("/delete", methods=["POST"])
def delete():
    collection_id = request.form.get('collection_id')
    block_id = request.form.get('block_id')
    """
    删除这个id的collection的block，记得刷新顺序
    """
    ret = {'msg': 'succuss'}
    return json_util.dumps(ret)


@bp_block.route("/swap", methods=["POST"])
def swap():
    id = request.form.get('id')
    collection_id = request.form.get('collection_id')
    order = request.form.get('new_order')
    """
    把这个collection_id的collection的这个id的块和顺序是order的块交换
    编号从零开始，有可能是自己
    """
    ret = {'msg': 'succuss'}
    return json_util.dumps(ret)


@bp_block.route("/edit", methods=["POST"])
def edit():
    collection_id = request.form.get('collection_id')
    block_id = request.form.get('block_id')
    content = request.form.get('content', None)

    """
    content = none的情况请直接返回
    """
    ret = {'msg': 'succuss'}
    return json_util.dumps(ret)


@bp_block.route("/get_web_name", methods=["POST"])
def get_web_name():
    url = request.form.get('url')
    ret = {'msg': 'succuss'}
    """
    ret['name'] = url对应的网站的title，没有就返回url
    """

    return json_util.dumps(ret)
