#!/usr/bin/env python

import hashlib
import hmac
try:
    import cPickle as pickle
except:
    import pickle
import pprint
from StringIO import StringIO

def make_digest(message):
    hash = hmac.new('secret-shared-key-goes-here',message,hashlib.sha1)
    return hash.hexdigest()

class SimpleObject(object):
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return self.name
#############
out_s = StringIO()

o = SimpleObject('digest matches')
pickled_data = pickle.dumps(o)
print pickled_data + 'I am pickled _data'
digest = make_digest(pickled_data)
header = '%s %s' % (digest,len(pickled_data))
print 'WRITING:', header + 'I am header one'
out_s.write(header + '\n')
out_s.write(pickled_data)

######################

o = SimpleObject('digest does not match')
pickled_data = pickle.dumps(o)
digest = make_digest('not the pickled data at all')
header = '%s %s' % (digest, len(pickled_data))
print '\nWRITING:',header + ' I am header two'
out_s.write(header + '\n')
out_s.write(pickled_data)

out_s.flush()

#####
in_s = StringIO(out_s.getvalue())

while True:
    first_line = in_s.readline()
    if  not first_line:
        break
    incoming_digest, incoming_length = first_line.split(' ')
    print incoming_digest + ' I am incoming_digest',incoming_length
    incoming_lenth = int(incoming_length)
    print '\nREAD:', incoming_digest, incoming_length

    incoming_pickled_data = in_s.read(int(incoming_length))
    print incoming_pickled_data + ' IIIIIII'
    actual_digest = make_digest(incoming_pickled_data)
    print 'ACTULA:', actual_digest
    if incoming_digest != actual_digest:
        print 'WARNING: Data corruption'
    else:
        obj = pickle.loads(incoming_pickled_data)
        print 'OK:', obj
