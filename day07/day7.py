#!/usr/local/Cellar/python@3.11/3.11.0/bin/python3.11

import sys
filename = "input.txt"

"""
Part 1:
  Inspect file system which consists of a tree structure of directories containing files and other directories.
  Determine size of each directory which includes any subdirectories.

  Calculate sum of sizes of directories with at most 100000.

Example input:
  $ cd /
  $ ls
  dir cmjgvh
  dir czrzl
  dir fcbt
  dir hdh
  259661 hjsbd.mzp
  dir jgrdd
  dir lqblqtng
  dir pgvmpmn
  dir pqqcvcm
  dir zglbptq
  $ cd cmjgvh
  $ ls
  dir hdh
  134565 hdh.sjv
  dir hgrpfmt
  282147 mjtq.ffd
  42343 rvmzv.rtb
  dir sjgvbd
"""

class Node():
  def __init__(self, name, parent, isdir, size=0):
    self.name = name
    if parent == None:  # make root parent of itself
      self.parent = self
    else:
      self.parent = parent
    self.isdir = isdir # boolean
    self.size = size   # for files, the size can be set at node creation, directories will be initially set to zero
    if isdir:
      self.children = {} # mapping child names to node object
    else:
      self.children = None

  def add_child(self, name, isdir, size=0):
    n = Node(name, self, isdir, size)
    self.children[name] = n
    return n

  def print_path(self):
    path_arr = []
    ptr = self
    while not ptr.parent == ptr:
      path_arr.insert(0,ptr.name)
      ptr = ptr.parent
    path_arr.insert(0, '/')
    return '/'.join(path_arr)

def main():
  result = 0
  ptr,root = None, None
  with open(filename, "r") as fh:
    for line in fh:
      match line.split():
        case ('$', 'cd', directory):
          if directory == '/':
            #print(f"cding into root directory {directory}")
            root = Node("/", None, True)
            ptr = root
          elif directory == '..':
            #print(f"  going up from directory {ptr.name} {ptr.size} to parent directory ")
            ptr = ptr.parent
          else:
            ptr = ptr.children[directory]
            path = ptr
            #print(f"cding into directory { ptr.print_path() }")
        case ('$', 'ls'):
          pass #print(f"  doing ls in {ptr.name}")
        case ('dir', dirname):
          #print(f"  found directory {dirname}")
          node = ptr.add_child(dirname, True, 0)
          ptr.children[dirname] = node
        case (filesize, file) if filesize.isnumeric():
          #print(f"  have file {file} with size {filesize}")
          ptr.add_child(file, False, int(filesize))
        case _:
          print(f"fell through with line {line}")
  calc_dir_size(root)
  result = find_dirs_smaller_than(root, 100000, 0) # directory mapping node path to size
  #result = sum( results.keys() )
  print (f"part 1 result is {result}")
  # should be 1077191
  print(f"root size is {root.size}")
  print(f"unused space is {70000000 - root.size}")
  del_threshold = 30000000 - (70000000 - root.size)
  print(f"space to delete is {del_threshold}")
  result2 = find_smallest_dir_larger_than(root, del_threshold, sys.maxsize)
  print (f"part 2 result is {result2}")
  
def find_smallest_dir_larger_than(node, threshold, smallest):
  if not node.isdir:
    return smallest
  if node.size < threshold:
    return sys.maxsize
  if node.size < smallest:
    smallest = node.size
  smallest = min( [smallest] + [ find_smallest_dir_larger_than(n, threshold, smallest) for n in node.children.values() ] )
  return smallest

def find_dirs_smaller_than(node, threshold, total):
  if not node.isdir:
    return (node, total)
  #print(f"checking node {node.print_path() } ")
  total += node.size if node.size <= threshold else 0
  #print(f"  have children {node.children} ")
  for c in node.children:
  #  print(f"  including children of node {node.print_path() } ")
    if node.children[c].isdir:
      total = find_dirs_smaller_than(node.children[c], threshold, total)
  #print(f"returning total {total}")
  return total

def calc_dir_size(node):
  if not node.isdir:
    return node.size
  size = sum( [ calc_dir_size(node.children[c]) for c in node.children] )
  node.size = size
  return size

"""
Example input:
  $ cd /
  $ ls
  dir cmjgvh
  dir czrzl
  dir fcbt
  dir hdh
  259661 hjsbd.mzp
  dir jgrdd
  dir lqblqtng
  dir pgvmpmn
  dir pqqcvcm
  dir zglbptq
  $ cd cmjgvh
  $ ls
  dir hdh
  134565 hdh.sjv
  dir hgrpfmt
  282147 mjtq.ffd
  42343 rvmzv.rtb
"""


if __name__ == "__main__":
  main()
