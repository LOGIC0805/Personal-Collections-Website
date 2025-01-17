from sqlalchemy import Column, Integer, String, BLOB
from APP.view.database import Base


class Users(Base):
    __tablename__ = 'users'
    phonenum = Column(String(255), primary_key=True)
    password = Column(String(255))
    name = Column(String(255))

    def __init__(self, name=None, password=None, phonenum=None):
        self.name = name
        self.password = password
        self.phonenum = phonenum


class Collection(Base):
    __tablename__ = 'collection'
    id = Column(String(255), primary_key=True)
    name = Column(String(255))
    tag = Column(String(255))
    phonenum = Column(String(255))
    like = Column(Integer)
    order = Column(Integer)

    def __init__(self, id=None, name=None, tag=None, phonenum=None, like=0, order=None):
        self.id = id
        self.name = name
        self.tag = tag
        self.phonenum = phonenum
        self.like = like
        self.order = order


class Block(Base):
    __tablename__ = 'block'
    id = Column(String(255), primary_key=True)
    content_text = Column(String(255))
    content_pic = Column(BLOB)
    type = Column(String(255))
    order = Column(Integer)

    # type = Column(String(255))
    def __init__(self, id=None, content_text=None, content_pic=None, order=None, type=None):
        self.id = id
        self.content_text = content_text
        self.content_pic = content_pic
        self.type = type
        self.order = order


class CollectionBlock(Base):
    __tablename__ = 'collection_block'
    id = Column(String(255), primary_key=True)
    # password = Column(String(255))
    block_id = Column(String(255), primary_key=True)

    def __init__(self, id=None, block_id=None):
        self.id = id

        self.block_id = block_id


class UserLike(Base):
    __tablename__ = 'user_like'
    phonenum = Column(String(255), primary_key=True)
    collection_id = Column(String(255), primary_key=True)
    state = Column(Integer)

    def __init__(self, phonenum=None, collection_id=None, state=None):
        self.phonenum = phonenum
        self.collection_id = collection_id
        self.state = state
