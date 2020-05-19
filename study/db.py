# File Name: db.py

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Table

engine = create_engine('mysql://root@localhost/study?charset=UTF8')
Base = declarative_base(engine)

class User(Base):
	__tablename__ = 'user'
	id = Column(Integer, primary_key=True)
	name = Column(String(64), unique=True, nullable=False)
	email = Column(String(64), unique=True)
	
	def __repr__(self):
		return '<User: {}>'.format(self.name)

class Course(Base):
	__tablename__ = 'course'
	id = Column(Integer, primary_key=True)
	name = Column(String(64))
	user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))
	user = relationship('User', backref=backref('course', cascade='all, delete-orphan'))
	
	def __repr__(self):
		return '<Course: {}>'.format(self.name)

class Lab(Base):
	__tablename__ = 'lab'
	# 设置主键为外键，关联 course 表的 id 字段
	# 注意参数顺序，先定义外键，再定义主键
	id = Column(Integer, ForeignKey('course.id'), primary_key=True)
	name = Column(String(128))
	# 设置查询借口，Lab 实例的 course 属性值为 Course 实例
	# Course 实例的 Lab 属性值默认为列表，列表中有一个 Lab 实例
	# uselist 参数可以设置 Course 实例的 Lab 属性值为 Lab 实例而非列表
	course = relationship('Course', backref=backref('lab', uselist=False))
	
	def __repr__(self):
		return '<Lab: {}>'.format(self.name)

# 创建 Table 类的实例，即中间表映射类，赋值给变量 Rela
# 该类在实例话时，接收4个参数：
# 1、数据表名字 2、Base.metadata
# 3 和 4、两个 Column (列明，数据类型，外键，主键)
Rela = Table('rela', Base.metadata,
			Column('tag_id', Integer, ForeignKey('tag.id'), primary_key=True),
			Column('course_id', Integer, ForeignKey('course.id'), primary_key=True)
			)

class Tag(Base):
	__tablename__ = 'tag'
	id = Column(Integer, primary_key=True)
	name = Column(String(64), unique=True)
	# 设置查询接口，secondary 指定多对多关系的中间表，注意数据类型不是字符串
	course = relationship('Course', secondary=Rela, backref='tag')
	
	def __repr(self):
		return '<Tag: {}>'.format(self.name)					
if __name__ == '__main__':
	# 使用声明基类的 metadata 对象的 create_all 方法创建数据表：
	Base.metadata.create_all() 
