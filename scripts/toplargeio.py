#!/usr/bin/env python
#title           :busy_load.py
#description     :Get the busiest or the most loaded disk from a trace
#author          :Vincentius Martin
#date            :20150203
#version         :0.1
#usage           :
#notes           :
#python_version  :2.7.5+  
#precondition    :combined
#==============================================================================

import math

def getTopLargeIO(tracefile, offset, devno, hrs, top = 1):
  timerange = int(hrs * 3600000000) #micro sec 

  result = {}
  
  with open("in/" + tracefile) as f:
    for line in f:
      tok = map(str.lstrip, line.split(" "))
    
      timeoffset = int(float(tok[0]) * 1000)/timerange
      
      if (timeoffset) not in result:
        result[timeoffset] = [0] * 7 # 32, 64, 128, 256, 512, 1024, 1024+
      
      if int(tok[1]) == devno:
        bsize = float(tok[3]) *  0.5 # (512 / 1024) kb

        if bsize < 32:
          result[timeoffset][0] += 1
        elif bsize < 64:
          result[timeoffset][1] += 1
        elif bsize < 128:
          result[timeoffset][2] += 1
        elif bsize < 256:
          result[timeoffset][3] += 1
        elif bsize < 512:
          result[timeoffset][4] += 1
        elif bsize < 1024:
          result[timeoffset][5] += 1
        else: # must be larger than 1024
          result[timeoffset][6] += 1
          
  if offset != "0":
    sortidx = int(math.log(float(offset),2) - 4)
  else:      
    sortidx = 0
    
  i = 0
  for key, value in sorted(result.items(), key=lambda e: e[1][sortidx], reverse = True):
    print str(key * hrs) + "-" + str(key * hrs + hrs) + ": " + str(value)
    i += 1
    if i == top:
      break
    
  
          
     
        
