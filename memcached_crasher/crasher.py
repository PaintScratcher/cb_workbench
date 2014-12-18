#!/usr/bin/env python
# Script to crash a sabotaged memcached install
# Search for 'arithmetic_executor' in memcached.c and change 'char *key;' to
# 'char *key = NULL;' and comment out the line 'key = binary_get_key(c);'
from couchbase import Couchbase
c = Couchbase.connect(bucket='beer-sample', host='127.1.1', port='9000')

key = "key_of_doom"
value = "1"

print "Setting key {0} with value {1}".format(key, value)
result = c.set(key, value)
print "...", result

print "where we're going we don't need memcached"
rv = c.incr("key")
