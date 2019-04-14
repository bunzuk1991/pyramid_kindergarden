from sqlalchemy import (
    Column,
    PrimaryKeyConstraint,
    ForeignKey,
    ForeignKeyConstraint,
    UniqueConstraint,
    Index,
)
from sqlalchemy import (
    Integer,
    BigInteger,
    Float,
    Numeric,
    Text,
    Unicode,
    UnicodeText,
    Date,
    Time,
    DateTime,
    Boolean,
    text,
    DECIMAL,
    LargeBinary
)

from .meta import Base
from zope.sqlalchemy import ZopeTransactionExtension
import datetime
from ..services import others

from sqlalchemy.orm import (
    sessionmaker,
    relationship,
    backref,
    scoped_session
)
from sqlalchemy import create_engine

# DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))



from sqlalchemy.exc import IntegrityError

# configure Session class with desired options
Session = sessionmaker()

# later, we create the engine

engine = create_engine('postgresql+psycopg2://postgres:kat221008@127.0.0.1:5432/garden')
# associate it with our custom Session class
Session.configure(bind=engine)

session_db = Session()

# work with the session
# session = Session()

DATEFORMAT = "%d.%m.%Y"



class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(255), unique=True, nullable=False)
    password = Column(Unicode(255), nullable=False)
    last_logged = Column(DateTime, default=datetime.datetime.utcnow)


class Organisation(Base):
    __tablename__ = 'organisation'
    id = Column(Integer, primary_key=True)
    name = Column(UnicodeText, nullable=False, default="")
    name_printable = Column(UnicodeText, nullable=False, default="")
    address = Column(UnicodeText, nullable=True)
    kod_zkpo = Column(Text, nullable=True)
    kod_ipn = Column(Text, nullable=True)
    disabled = Column(Boolean, default=False, nullable=False)
    slug = Column(Text, nullable=True, unique=True)
    create_date = Column(DateTime, default=datetime.datetime.utcnow)
    update_date = Column(DateTime, nullable=True)

    def __str__(self):
        return '%s (%s)' % (self.name, self.create_date.strftime(DATEFORMAT))


class GardenGroup(Base):
    __tablename__ = 'gardengroup'
    id = Column(Integer, primary_key=True)
    organisation_id = Column(Integer, ForeignKey('organisation.id'), nullable=False)
    name = Column(UnicodeText, nullable=True)
    short_name = Column(UnicodeText, nullable=True)
    slug = Column(Text, nullable=True, unique=True)
    description = Column(UnicodeText, nullable=True)
    actual = Column(Boolean, default=True, nullable=False)
    create_date = Column(DateTime, default=datetime.datetime.utcnow)
    update_date = Column(DateTime, nullable=True)

    organisation = relationship('Organisation', backref=backref('gardengroup', order_by='GardenGroup.name'))

    def __str__(self):
        return self.name


class Group(Base):
    __tablename__ = 'group'

    id = Column(Integer, primary_key=True)
    gardengroup_id = Column(Integer, ForeignKey('gardengroup.id'), nullable=False)
    name = Column(UnicodeText, nullable=False, default="")
    year_in = Column(Date, nullable=True)
    year_out = Column(Date, nullable=True)
    slug = Column(Text, nullable=True, unique=True)

    gardengroup = relationship('GardenGroup', backref=backref('group', order_by='Group.name'))

    def __str__(self):
        return self.name


class Children(Base):
    __tablename__ = 'children'
    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey('group.id'), nullable=False)
    fullname = Column(UnicodeText, nullable=False, default="")
    date_of_birth = Column(Date, nullable=True)
    growth = Column(Integer, default=0)
    weight = Column(Numeric(8, 2), default=0)
    image = Column(LargeBinary, nullable = True)
    slug = Column(Text, nullable=True, unique=True)
    actual = Column(Boolean, default=True, nullable=False)
    date_start = Column(Date, nullable=True)
    date_end = Column(Date, nullable=True)
    address = Column(UnicodeText, nullable=False, default="")

    parents = relationship('Parent', backref='child',
                                lazy='dynamic')

    def __str__(self):
        return self.fullname

    def get_url(self, request):
        if request:
            return request.route_url('children-edt', slug=self.slug)
        else:
            return 'request does\'t get'

    # def get_absolute_image_url(self):
    #     return "%s%s" % ('', self.image.url)


class Relation(Base):
    __tablename__ = 'relation'
    id = Column(Integer, primary_key=True)
    name = Column(UnicodeText, nullable=False, default="")
    actual = Column(Boolean, default=True, nullable=False)
    slug = Column(Text, nullable=True, unique=True)

    def __str__(self):
        return self.name


class Parent(Base):
    __tablename__ = 'parent'
    id = Column(Integer, primary_key=True)
    child_id = Column(Integer, ForeignKey('children.id'), nullable=False)
    relation_id = Column(Integer, ForeignKey('relation.id'), nullable=False)
    fullname = Column(UnicodeText, nullable=False, default="")
    date_of_birth = Column(Date, nullable=True)
    phone = Column(UnicodeText, default='')
    address = Column(UnicodeText, default='')
    work = Column(UnicodeText, default='')
    workplace = Column(UnicodeText, default='')
    with_child = Column(Boolean, default=True, nullable=False)

    def __str__(self):
        return '%s(%s)' % (self.fullname, self.with_child)
