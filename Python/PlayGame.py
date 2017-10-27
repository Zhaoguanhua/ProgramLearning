# -*- coding:utf-8 -*-

class Person:
	def __init__(self,na,gen,age,fig):
		self.name = na
		self.gender =gen
		self.age = age
		self.fight = fig

	def grassland(self):
		self.fight = self.fight - 200

	def incest(self):
		self.fight = self.fight - 500

	def practice(self):
		self.fight = self.fight + 200

	def detail(self):
		temp = "姓名:%s;性别:%s;年龄:%s;战斗力:%s" %(self.name,self.gender,self.age,self.fight)
		print(temp)

li = Person('李','女',18,1000)
wang = Person('王','男',20,1600)
zhao = Person('赵','男',25,2500)

li.detail()
wang.detail()
zhao.detail()

li.incest()
wang.practice()
zhao.grassland()

li.detail()
wang.detail()
zhao.detail()

li.incest()
wang.practice()
zhao.grassland()

li.detail()
wang.detail()
zhao.detail()
