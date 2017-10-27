class D(object):
	def bar(self):
		print('D.bar')

class C(D):
	pass
	# def bar(self):
	# 	print('C.bar')

class B(D):
	pass
	# def bar(self):
	# 	print('B.bar')

class A(B,C):
	def __init__(self):
		pass

	# def bar(self):
	# 	print('A.bar')

a = A()
a.bar()