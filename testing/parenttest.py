
class afunction():

    def mainfunction(self):
        print "testing 1"

    def secondfunction(self):
        print "testing 3"

class bfunction(afunction):

    def mainfunction(self):
        print "testing 2"



b = bfunction()
b.mainfunction()
b.secondfunction()