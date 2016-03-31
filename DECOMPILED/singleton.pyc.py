# 2016.01.27 00:42:53 MSK

class Singleton(object):

    def __new__(cls, *args, **kwds):
        it = cls.__dict__.get('__it__')
        if it is not None:
            return it
        cls.__it__ = it = object.__new__(cls)
        it.init(*args, **kwds)
        return it



    def init(self, *args, **kwds):
        pass




+++ okay decompyling ./singleton.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2016.01.27 00:42:53 MSK
