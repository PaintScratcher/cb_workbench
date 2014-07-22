#!/usr/bin/env python
# Program for logging response times to a Couchbase server
from couchbase import Couchbase
from pprint import pprint
import time
import datetime

# Initialise time keeping variable
i = 0

# Connect to Couchbase
cb = Couchbase.connect(bucket='beer-sample', host='192.168.67.101')

with open('Responses', 'a') as f:
  while(True):

    before = datetime.datetime.now()
    rows = cb.query("beer", "by_name", stale=False)
    after = datetime.datetime.now()

    offset = after - before # Calculate the response time
    offset = int(offset.microseconds)

    if (offset > 300): # Log any high response times
      f.write("Response time of "+str(offset)+" at point "+str(i)+"("+str(i/5)+"s)\n")
      f.flush()

    print offset
    i+=1
    time.sleep(0.2) # 5 requests per sec
