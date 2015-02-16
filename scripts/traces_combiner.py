#!/usr/bin/env python
#title           :tracescombiner.py
#description     :Parse hourly I/O size for MS traces format
#author          :Vincentius Martin
#date            :20150203
#version         :0.1
#usage           :python hourlyiosize.py file (--filter read/write)
#notes           :
#python_version  :2.6.6  
#==============================================================================

import argparse
from os import listdir

def combine(tracesdir, filtertype):
 
  type_filter = -1
  if filtertype == "write":
    type_filter = 0	
  elif filtertype == "read":
    type_filter = 1

  # get all files
  listoffiles = []
  for ftrace in listdir(tracesdir):
    listoffiles.append(str(ftrace))

  listoffiles.sort()

  # combine

  timeoffset = 0
  outlist = []

  for tracefile in listoffiles:
    with open(tracesdir + "/" + tracefile) as f:
      for line in f:
        if line[:9] == "EndHeader":
          break
      timetmp = 0
      for line in (f):
        tok = map(str.lstrip, line.split(","))
        flags = -1

        if tok[0] == "DiskWrite":
          flags = 0
        elif tok[0] == "DiskRead":
          flags = 1

        if flags == -1:
          continue
        if type_filter != -1 and type_filter != flags:
          continue
      
        t = {
          "time": int(tok[1]) + timeoffset,
          "devno": int(tok[8]),
          "blkno": int(tok[5], 16),
          "bcount": int(tok[6], 16),
          "flags": flags,
        };
      
        timetmp = int(tok[1])
        outlist.append("%s %d %d %d %d\n" % (t['time'], t['devno'], t['blkno'], t['bcount'], t['flags']))

    timeoffset += timetmp
    
  return outlist


      
