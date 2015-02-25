#!/usr/bin/env python
#title           :trace-editor.py
#description     :process traces
#author          :Vincentius Martin
#date            :-
#version         :0.1
#usage           :see readme
#notes           :
#python_version  :2.7.5+
#==============================================================================

# import default
import sys
import argparse
from os import listdir

sys.path.insert(0, './scripts/')

import trace_modifier
import preprocess_trace
import traces_combiner
import busy_load
import filter_raid
import iopsimbalance
import toplargeio
import cuttrace
# end of import part

# define global variables
requestlist = []

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument("-file", help="trace file to process",type=str)
  parser.add_argument("-files", nargs='+', help="trace files to process",type=str)
  parser.add_argument("-dir", help="directory file to process",type=str)
  
  parser.add_argument("-produceTrace", help="produce preprocessed trace", action='store_true')
  parser.add_argument("-preprocessMSTrace", help="preprocess the MS trace into disksim ascii format", action='store_true')
  parser.add_argument("-preprocessBlkReplayTrace", help="preprocess the blkreplay trace into disksim ascii format", action='store_true')
  parser.add_argument("-preprocessUnixBlkTrace", help="preprocess the blkreplay trace into disksim ascii format", action='store_true')
  parser.add_argument("-filterraid", help="create RAID-0 subtrace", action='store_true')
  parser.add_argument("-ioimbalance", help="check RAID IO Imbalance", action='store_true')
  parser.add_argument("-combine", help="combine preprocessed traces inside a directory", action='store_true')
  parser.add_argument("-toplargeio", help="get n top large io", action='store_true')
  parser.add_argument("-cuttrace", help="cut a trace", action='store_true')
  
  parser.add_argument("-offset", help="offset", choices=['0','32','64','128','256','512','1024'], default = '0')
  parser.add_argument("-filter", help="filter specific type", choices=['all','write','read'], default='all')
  parser.add_argument("-devno", help="disk/device number", type=int, default=0)
  parser.add_argument("-duration", help="how many hours", type=float, default=1.0)
  parser.add_argument("-mostLoaded", help="most loaded", action='store_true')
  parser.add_argument("-busiest", help="busiest", action='store_true')
  parser.add_argument("-top", help="top n", type=int, default=1)
  parser.add_argument("-resize", help="resize a trace", type=float, default=1.0)
  parser.add_argument("-rerate", help="rerate a trace", type=float, default=1.0)
  parser.add_argument("-ndisk", help="n disk for RAID", type=int, default=2)
  parser.add_argument("-odisk", help="observed disk for RAID", type=int, default=0)
  parser.add_argument("-stripe", help="RAID stripe unit size in byte", type=int, default=4096)
  parser.add_argument("-granularity", help="granularity to check RAID IO imbalance in seconds", type=int, default=300)
  parser.add_argument("-timerange", help="time range to cut the trace", type=float, nargs = 2)
  args = parser.parse_args()

  # parse to request list
  if (args.preprocessMSTrace): #preprocess
    if (not args.file and args.dir):
      for ftrace in listdir("in/" + args.dir):
        preprocess_trace.preprocessMSTrace(args.dir + "/" + ftrace, args.filter)
    else:
      preprocess_trace.preprocessMSTrace(args.file, args.filter)
  elif (args.preprocessBlkReplayTrace): #preprocess
    if (not args.file and args.dir): 
      for ftrace in listdir("in/" + args.dir):
        preprocess_trace.preprocessBlkReplayTrace(args.dir + "/" + ftrace, args.filter)
    else:
      preprocess_trace.preprocessBlkReplayTrace(args.file, args.filter)
  elif (args.preprocessUnixBlkTrace): #preprocess
    if (not args.file and args.dir):
      for ftrace in listdir("in/" + args.dir):
        preprocess_trace.preprocessUnixBlkTrace(args.dir + "/" + ftrace, args.filter)
    else:
      preprocess_trace.preprocessUnixBlkTrace(args.file, args.filter)
  elif (args.filterraid):
    filter_raid.createRaidSubtrace(args.file, args.ndisk, args.odisk, args.stripe)
  elif (args.ioimbalance):
    iopsimbalance.checkIOImbalance(args.files, args.granularity)
  elif (args.combine):
    traces_combiner.combine(args.dir)
  elif args.mostLoaded or args.busiest: #need combine
    if args.busiest:
      busy_load.checkCongestedTime(args.file, True, args.devno, args.duration, args.top)
    else:
      busy_load.checkCongestedTime(args.file, False, args.devno, args.duration, args.top)
  elif (args.toplargeio):
    toplargeio.getTopLargeIO(args.file, args.offset, args.devno, args.duration, args.top)
  elif (args.cuttrace):
    cuttrace.cut(args.file, args.timerange[0], args.timerange[1])
  else: #modify a trace
    with open("in/" + args.file) as f:
      for line in f:
        requestlist.append(line.rstrip().split(" "))
    if args.resize != 1.0 or args.rerate!= 1.0:
      if (args.resize != 1.0):
        requestlist = trace_modifier.resize(requestlist,args.resize)     
      if (args.rerate != 1.0):
        requestlist = trace_modifier.modifyRate(requestlist,args.rerate)  
      trace_modifier.printRequestList(requestlist, args.file)

  
