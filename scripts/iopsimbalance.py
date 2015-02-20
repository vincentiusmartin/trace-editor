#!/usr/bin/env python
#title           :tracebucketing.py
#description     :Divide a trace into some size-buckets
#author          :Vincentius Martin
#date            :20150210
#version         :0.1
#usage           :python tracebucketing.py 
#notes           :
#python_version  :2.7.5+
#==============================================================================

import numpy

def median(lst):
    return numpy.median(numpy.array(lst))

def checkIOImbalance(inputdisk, granularity):
  for i in range(len(inputdisk)):
    tracefile = open("in/" + inputdisk[i])
    inputdisk[i] = [line.strip().split(" ") for line in tracefile.readlines()]

  # get max time
  maxtime = 0.0	
  for disk in inputdisk:
    for request in disk:
      if float(request[0]) > maxtime:
        maxtime = float(request[0])

  # create the bucket
  delta = granularity * 1000
  bucket = {}
  lowerval = 0.0
  while 1:
    bucket[lowerval] = [0] * len(inputdisk)
    lowerval += delta
    if(lowerval > maxtime):
      break

  # now fill the bucket
  for i in range(0, len(inputdisk)):
    for request in inputdisk[i]:
      for key in bucket:
        if key <= float(request[0]) < key + delta:  
          bucket[key][i] += 1
          break

  for key in sorted(bucket):
    print str(int(key/1000)) + "-" + str(int((key+delta)/1000)) + ": " + str(bucket[key])  + " - imbalance:" + str(float(max(bucket[key]) / median(bucket[key])))




