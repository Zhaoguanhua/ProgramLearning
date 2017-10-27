class Foo:
	def __init__(self,name,age,gender):
		self.name = name
		self.age = age
		self.gender = gender

	def prt(self):
		print(self)

	def kanchai(self):
		print("%s,%s岁,%s,上山去砍柴"%(self.name,self.age,self.gender))

	def qudongbei(self):
		print("%s,%s岁,%s,去东北"%(self.name,self.age,self.gender))

xiaoming = Foo('小明',10,'男')
xiaoming.kanchai()
xiaoming.qudongbei()

laoli = Foo('老李',20,'女')
laoli.kanchai()
laoli.qudongbei()
