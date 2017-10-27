# !usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys

def main():
	RootInputPath = sys.argv[1]
	for root,dirs,RSFiles in os.walk(RootInputPath):
		print(root)
		print(dirs)
		print(RSFiles)
		print(' ')

if __name__ == '__main__':
	main()