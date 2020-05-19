# File Name: create_data.py

from sqlalchemy.orm import sessionmaker
from faker import Faker
from db import Base, engine, User, Course, Lab, Tag

session = sessionmaker(engine)()
fake = Faker('zh-cn')

def create_users():
	for i in range(10):
		# 创建10个 User 类实例，伪造 name 和 email
		user = User(name=fake.name(), email=fake.email())
		# 将实例添加到 session 会话中，以备提交到数据库
		# 注意，此时的 user 对象没有 id 属性值
		# 映射类的主键字段默认从1开始自增，在传入 session 时自动添加该属性值
		session.add(user)
		
def create_courses():
	# session 有个 query 方法用来查询数据，参数为映射类的类名
	# all 方法表示查询全部，这里也可以省略不写
	# user 就是上一个函数 create_users 中的 user 对象
	for user in session.query(User).all():
		# 两次循环，对每个作者创建两个课程
		for i in range(2):
			# 创建课程实例，name 的值为 8 个随机汉子
			course = Course(name=''.join(fake.words(4)), user_id=user.id)
			session.add(course)
def create_labs():
	for course in session.query(Course):
		lab = Lab(name=''.join(fake.words(5)), id=course.id)
		session.add(lab)
		
def create_tags():
	for name in ['python', 'java', 'mysql', 'linux', 'lisp']:
		tag = Tag(name=name)
		session.add(tag)
		
def main():
	# 执行四个创建实例的函数， session 会话内就有了这些实例
	create_users()
	create_courses()
	create_labs()
	create_tags()
	# 执行 session 的 commit 方法将全部数据提交到对应的数据表中
	session.commit()
	
if __name__ == '__main__':
	main()
