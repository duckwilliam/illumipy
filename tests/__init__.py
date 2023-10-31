#!/usr/bin/env python

class Test:
    def __init__(self,
                 arg1 = None, 
                 arg2 = None, 
                 arg6 = None
                 ):
            self.arg1 = arg1
            self.arg2 = arg2
            self.arg6 = arg6
    def somefunc(self):
        print("this")
        

obj = Test(arg1='foo', arg2='bar')

print(__dict__(obj) 