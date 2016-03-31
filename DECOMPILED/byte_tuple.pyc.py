# 2016.01.27 00:42:35 MSK

def tupleToLong(t, size):
    i = 0L
    if type(t) is not tuple:
        raise TypeError('Expected a tuple')
    if len(t) != size:
        raise ValueError('Expected a tuple with %i elements' % size)
    for n in t:
        if n < 0 or n > 255:
            raise ValueError('Out of range')
        i <<= 8
        i |= n

    return i



def tupleToHexString(t, size, leading_0x = True):
    fmt = '%%0%dx' % (size * 2)
    if leading_0x:
        fmt = '0x' + fmt
    return fmt % tupleToLong(t, size)



def longToTuple(l, size):
    t = []
    if type(l) is not long:
        raise TypeError('Expected a long')
    if l < 0 or l > pow(2, 8 * size) - 1:
        raise ValueError('Out of range')
    for n in range(size):
        t.insert(0, int(l & 255))
        l >>= 8

    return tuple(t)



def hexStringToTuple(s, size):
    return longToTuple(long(s, 16), size)


_EUI64_SIZE = 8

def _reverse(t):
    l = list(t)
    l.reverse()
    return tuple(l)



def eui64ToLong(t):
    return tupleToLong(_reverse(t), _EUI64_SIZE)



def eui64ToHexString(t, leading_0x = True):
    return tupleToHexString(_reverse(t), _EUI64_SIZE, leading_0x)



def longToEui64(l):
    return _reverse(longToTuple(l, _EUI64_SIZE))



def hexStringToEui64(s):
    return _reverse(hexStringToTuple(s, _EUI64_SIZE))



def convertToEui64(x):
    if type(x) == tuple:
        return x
    if type(x) == long:
        return longToEui64(x)
    if type(x) == str or type(x) == unicode:
        return hexStringToEui64(x)
    raise TypeError('Expected a tuple, long or string')


_EXTPANID_SIZE = 8

def extPanToLong(t):
    return tupleToLong(_reverse(t), _EXTPANID_SIZE)



def extPanToHexString(t, leading_0x = True):
    return tupleToHexString(_reverse(t), _EXTPANID_SIZE, leading_0x)



def longToExtPan(l):
    return _reverse(longToTuple(l, _EXTPANID_SIZE))



def hexStringToExtPan(s):
    return _reverse(hexStringToTuple(s, _EXTPANID_SIZE))



def convertToExtPan(x):
    if type(x) == tuple:
        return x
    if type(x) == long:
        return longToExtPan(x)
    if type(x) == str:
        return hexStringToExtPan(x)
    raise TypeError('Expected a tuple, long or string')


_KEY_SIZE = 16

def keyToLong(t):
    return tupleToLong(t, _KEY_SIZE)



def keyToHexString(t, leading_0x = True):
    return tupleToHexString(t, _KEY_SIZE, leading_0x)



def longToKey(l):
    return longToTuple(l, _KEY_SIZE)



def hexStringToKey(s):
    return hexStringToTuple(s, _KEY_SIZE)



def convertToKey(x):
    if type(x) == tuple:
        return x
    if type(x) == long:
        return longToKey(x)
    if type(x) == str:
        return hexStringToKey(x)
    raise TypeError('Expected a tuple, long or string')



+++ okay decompyling ./byte_tuple.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2016.01.27 00:42:35 MSK
