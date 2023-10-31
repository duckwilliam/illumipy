import inspect

class tclass:
    def __init__(self,
                 eins,
                 zwei,
                 drei
                ):
        self.einz = eins
        self.zwei = zwei
        self.dfei = drei
     
    def catalogue(self):
        _catalogue = vars(self)
        return _catalogue

    def somefunc(self):
        print('foobar')


o = tclass(1, 2, 3)

#for i in vars(o).items():
  #  print(i)
print(o.catalogue().items())