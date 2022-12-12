#!/usr/bin/env python

#import re

filename = "input.txt"

"""
Part 1:
Find number of characters received when we see first set of 4 unique characters when processing from left to right.

Part 2:
  How many characters need to be processed before the first 14 distinct characters is detected?



Example input:
  rdrgrcggjrgrddfqfqrqppptr

"""

def main(window_length=4):
  result = 0
  with open(filename, "r") as fh:
    line = fh.readline()
    left = 0
    right = window_length
    while right < len(line):

      s = set( line[left:right] )
      if len(s) == window_length:
        result = right
        break
      left += 1
      right += 1
  print(f"result is {result}") # should be 1920 for part 1

def sliding(window_length=4):
  excess = 0
  with open(filename, "r") as fh:
    line = fh.readline()
    buffer = [0] * 26
    for c in line[0:window_length]:
      pos = ord(c) - ord('a')
      if buffer[pos] > 0:
        excess += 1
      buffer[pos] += 1

    if excess == 0:
      print(f"result is {window_length}")
      return

    for i in range(window_length, len(line)):
      left = line[i-window_length]
      pos = ord(left) - ord('a')

      if buffer[pos] > 1: excess -= 1
      buffer[pos] -=1

      right = line[i]
      pos = ord(right) - ord('a')
      if buffer[pos] > 0:
        excess += 1
      buffer[pos] += 1
      if excess == 0:
        print(f"result is {i+1}") # indexing
        break

if __name__ == "__main__":
  main()
  main(window_length=14)
  sliding(4)
  sliding(14)
