#!/usr/bin/env python
#title           :busy_load.py
#description     :Get the busiest or the most loaded disk from a trace
#author          :Vincentius Martin
#date            :20150203
#version         :0.1
#usage           :
#notes           :
#python_version  :2.7.5+  
#precondition    :ordered
#==============================================================================

import operator

def checkCongestedTime(inlist, isBusiest, devno, hrs, top = 1):
  timerange = int(hrs * 3600000000) #ns

  result = {}

  for elm in inlist:
    tok = map(str.lstrip, elm.split(" "))
    if int(tok[1]) == devno:
      if (int(tok[0])/timerange) not in result:
        result[int(tok[0])/timerange] = 0.0

      if isBusiest:
        result[int(tok[0])/timerange] += 1
      else:
        result[int(tok[0])/timerange] += (float(tok[3]) / 1024)

  i = 0
  for elm in sorted(result.items(), key=operator.itemgetter(1), reverse=True):
    print "time(hrs): " + str(elm[0] * hrs) + "-" + str(elm[0] *hrs + hrs) + ": " + str(elm[1]).rstrip('0').rstrip('.')
    i += 1
    if i >= top:
      break

#lowerb = max(result.iteritems(), key=operator.itemgetter(1))[0] * 3600000000
#upperb = (max(result.iteritems(), key=operator.itemgetter(1))[0] + args.hours) * 3600000000

#iolist = []

#for elm in inlist:
  #tok = map(str.lstrip, elm.split(" "))
  #if lowerb <= int(tok[0]) < upperb:
    #iolist.append(int(tok[3]))

# CDF part
#cfreq = 0

#for elm in sorted(iolist):
#  cfreq = (1.0/len(iolist)) + cfreq
#  print(str(elm) + " " + str(cfreq))





