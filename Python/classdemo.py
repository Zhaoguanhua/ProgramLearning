#!／usr/bin/env python
# -*- coding:utf-8 -*-

class Employee:
	empCount = 0

	def __init__(self,name,salary):
		self.name = name
		self.salary = salary
		Employee.empCount += 1

	def displayCount(self):
		print("Total Employee %d" % Employee.empCount)

	def displayEmployee(self):
		print ("Name:",self.name, ",salary:",self.salary)
	
emp1 = Employee("Zara",2000)
emp2 = Employee("Manni",5000)
#emp3 = Employee("sdsaf",10000)
emp1.displayEmployee()
emp2.displayEmployee()
#emp3.displayEmployee()
print("Total Employee %d" % Employee.empCount)	
