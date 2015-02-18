#!/usr/bin/env python

import math


def createRaidSubtrace(infile, ndisk, odisk, stripe):
  out = open("out/" + infile + "-raiddisk" + str(odisk) + ".trace" , 'w')

  blk_size = 512
  scaler = stripe / blk_size # = chunk size
  
  def calculate_raid_blk(blk_start, blk_count, time=0):
    blk_count_per_disk = [0] * ndisk
    blk_start_per_disk = [None] * ndisk

    current_blk = blk_start
    for _ in range(blk_count):
	    current_disk = (current_blk / scaler) % ndisk
	    blk_count_per_disk[current_disk] += 1
	    if blk_start_per_disk[current_disk] is None:
                    blk_start_per_disk[current_disk] = calculate_raid_offset(current_blk)
	    current_blk += 1

    return blk_start_per_disk[odisk], blk_count_per_disk[odisk]
    
  def calculate_raid_offset(offset_input):
    return ((offset_input / (scaler * int(ndisk))) * scaler) + ((offset_input % (scaler * int(ndisk))) % scaler)

  with open("in/" + infile) as f:
    for line in f:
      token = line.split(" ")
      time = token[0]
      devno = token[1]
      blkno = int(token[2].strip())
      blkcount = int(token[3].strip())
      flags = token[4]
	
      blkno, blkcount = calculate_raid_blk(blkno, blkcount, time=time)
      if blkcount != 0:
        out.write("{} {} {} {} {}".format(time, devno, blkno, blkcount, flags))
