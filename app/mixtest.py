class Mixin(object):
    def __init__(self):
        self.val = "Mixin"
    def test(self):
        print "from mixin {0} {2}".format(self.val,self.camper)
class MyClass(Mixin,object):
    def __init__(self):
        self.camper = "VW"
    def test(self):
        print "from myclass {0}".format(self.val)