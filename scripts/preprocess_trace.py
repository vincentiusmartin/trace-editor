#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os

def preprocess(tracefile, filtertype):
  out = open("out/" + tracefile + "-preprocess.trace", 'w')

  type_filter = -1
  if filtertype == "write":
    type_filter = 0	
  elif filtertype == "read":
    type_filter = 1

  with open("in/" + tracefile) as f:
  # skip header
    for line in f:
      if line[:9] == "EndHeader":
        break
        
    first_line = True
    for line in f:		
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

      if first_line:
        offset = -float(tok[1]) / 1000.0
        first_line = False

      t = {
        "time": (float(tok[1]) / 1000.0) + offset,
        "devno": int(tok[8]),
        "blkno": int(tok[5], 16) / 512,
        "bcount": int(tok[6], 16) / 512,
        "flags": flags,
      };

      out.write("%s %d %d %d %d\n" % ("{0:.3f}".format(t['time']), t['devno'], t['blkno'], t['bcount'], t['flags']))
      
  out.close()


