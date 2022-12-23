#!/usr/local/bin/python3.11

import re
import math
from functools import partial
from collections import deque
from collections import Counter
filename = "input.txt"
#filename = "small"
#filename = "medium"

"""
Part 1:
  Parse instructions on mokeys throwing items to each other. Track the 2 busiest monkeys in terms of
  how many items they inspected. The product of the number of inspections of the 2 busiest monkeys
  is the monkey business value. Find the level of monkey business after 20 rounds.

Monkey 0:
  Starting items: 89, 95, 92, 64, 87, 68
  Operation: new = old * 11
  Test: divisible by 2
    If true: throw to monkey 7
    If false: throw to monkey 4

Part 2

"""

func_d = { '+': lambda x, y: x + y, '*': lambda x, y: x * y }

monkey_items, monkey_ops, monkey_test, monkey_targets = {}, {}, {}, {}

inspections = Counter()
num_rounds = 20

def main():
  parse()
  monkey_chase()

def monkey_chase():
  for round in range(num_rounds):
    for monkey in monkey_items:
      while len(monkey_items[monkey]) > 0:
        worry_level = int(monkey_items[monkey].popleft())
        inspections[monkey] += 1
        worry_level = monkey_ops[monkey](worry_level)
        worry_level = worry_level // 3
        target_monkey = monkey_targets[monkey][ (worry_level % int(monkey_test[monkey])) == 0 ]
        monkey_items[target_monkey].append(worry_level)
  result = math.prod([ mb[1] for mb in inspections.most_common(2) ])
  print(f"monkey business value is {result}") # 72884

def parse():
  with open(filename, "r") as fh:
    for block in fh.read().split("\n\n"):
      lines = block.split("\n")
      m_id = re.findall(r'Monkey (\d*):', lines[0])[0]
      monkey_items[m_id] = deque(re.findall(r'(\d+)', lines[1]))
      # create lambdas for monkey operations
      op, param = re.findall(r'new = old (.) (\w+)', lines[2])[0]
      if param.isnumeric():
        monkey_ops[m_id] = partial(func_d[op], int(param)) # make lambdas into 1 param funcs
      elif param == 'old' and op == '*':
        monkey_ops[m_id] = lambda x: x*x

      monkey_test[m_id] =  re.findall(r'Test: divisible by (\d+)', lines[3])[0]
      t_result = re.findall(r'If true: throw to monkey (\d+)', lines[4] )[0]
      f_result = re.findall(r'If false: throw to monkey (\d+)', lines[5])[0]

      monkey_targets[m_id] = ( f_result, t_result )

if __name__ == "__main__":
  main()
