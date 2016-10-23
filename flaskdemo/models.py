import os

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref
from marshmallow_sqlalchemy import ModelSchema

db_name = ':memory:'
db_name = 'demo.db'
db_url = 'sqlite:///' + db_name

engine = sa.create_engine(db_url, echo=False)
session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()

#
# Define tables using sqlalchemy
#
class Author(Base):
    __tablename__ = 'authors'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String)
    nationality = sa.Column(sa.String)

    def __repr__(self):
        return '<Author(name={self.name!r})>'.format(self=self)

class Book(Base):
    __tablename__ = 'books'
    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.String)
    author_id = sa.Column(sa.Integer, sa.ForeignKey('authors.id'))
    author = relationship("Author", backref=backref('books'))

#
# Define serializing rules using Marshmallow
# 
class AuthorSchema(ModelSchema):
    class Meta:
        model = Author

class BookSchema(ModelSchema):
    class Meta:
        model = Book
        # optionally attach a Session
        # to use for deserialization
        sqla_session = session

author_schema = AuthorSchema()

def Test():
    author = Author(name='Chuck Paluhniuk')
    book = Book(title='Fight Club', author=author)
    session.add(author)
    session.add(book)
    session.commit()

    dump_data = author_schema.dump(author).data
    print(dump_data)
    # {'books': [123], 'id': 321, 'name': 'Chuck Paluhniuk'}

    author_schema.load(dump_data, session=session).data
    # <Author(name='Chuck Paluhniuk')>

if __name__ == '__main__':
    import utils
    engine.echo = True
    if os.path.exists(db_name):
        if utils.prompt('Do you want to delete any existing DB and start over?'):
            os.remove(db_name)
    Base.metadata.create_all(engine)

