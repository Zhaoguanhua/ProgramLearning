# -*- coding:utf-8 -*-

class Animal:
	def eat(self):
		print("%s eat food"%self.name)

class Cat(Animal):
	def __init__(self,name):
		self.name = name
		self.breed = '猫'

	def cry(self):
		print('%s喵喵叫'%self.name)

class Dog(Animal):
	def __init__(self,name):
		self.name = name
		self.breed = '狗'

	def cry(self):
		print('汪汪叫')

c1 = Cat('小白家的小黑猫')
c1.eat()

c2 = Cat('小黑家的小白猫')
c2.eat()
c2.cry()

d1 = Dog('小胖家的小瘦狗')
d1.eat()
d1.cry()