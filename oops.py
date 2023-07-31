class A:
    # In python there is no constructor with the same name
    var=0
    def A(self):
        print("This is the constructore calling ")

    # __init__ method is used as a constructor in python
    def __init__(self,x):
        self.var=x


    def print(self):
        print("This is ",self.var)


temp=A(5)
temp.print()


