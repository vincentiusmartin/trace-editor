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

sys.path.insert(0, './scripts/')

import trace_modifier
import preprocess_trace
import traces_combiner
import busy_load
import filter_raid
import iopsimbalance
# end of import part

# define global variables
requestlist = []

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument("-file", help="trace file to process")
  parser.add_argument("-files", nargs='+', help="trace files to process")
  parser.add_argument("-dir", help="directory file to process")
  parser.add_argument("-preprocess", help="preprocess the trace into disksim ascii format", action='store_true')
  parser.add_argument("-filterraid", help="create RAID-0 subtrace", action='store_true')
  parser.add_argument("-ioimbalance", help="check RAID IO Imbalance", action='store_true')
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
  args = parser.parse_args()

  # parse to request list
  if (args.preprocess): #preprocess
    preprocess_trace.preprocess(args.file, args.filter)
  elif (args.filterraid):
    filter_raid.createRaidSubtrace(args.file, args.ndisk, args.odisk, args.stripe)
  elif (args.ioimbalance):
    iopsimbalance.checkIOImbalance(args.files, args.granularity)
  elif args.mostLoaded or args.busiest: #need combine
    inlist = traces_combiner.combine("in/" + args.dir, args.filter)
    if args.busiest:
      busy_load.checkCongestedTime(inlist, True, args.devno, args.duration, args.top)
    else:
      busy_load.checkCongestedTime(inlist, False, args.devno, args.duration, args.top)
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

  
