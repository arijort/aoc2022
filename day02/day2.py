#!/usr/bin/env python

import os
import sys

filename = "input.txt"

max_size = sys.maxsize
min_size = -sys.maxsize - 1


"""
Input data represents a strategy guide for playing rock papaer scissors:

  A X
  B Z
  C Z
  B Z
  B Z
  A Y
  A Y
  A Z
  A Y
  B Y

The first column is what your opponent is going to play: A for Rock, B for Paper, and C for Scissors.
The second column, ..., must be what you should play   : X for Rock, Y for Paper, and Z for Scissors

Your total score is the sum of your scores for each round. The score for a single round is the score for the shape you selected:
1 for Rock, 2 for Paper, and 3 for Scissors

plus the score for the outcome of the round (0 if you lost, 3 if the round was a draw, and 6 if you won
"""

shape_scores = { 'X': 1, 'Y': 2, 'Z': 3 }
# 9 possible outcomes
outcome_scores = {
  ('A', 'X') : 3, # 3 for a draw rock rock
  ('A', 'Y') : 6, # 6 for a win  rock paper
  ('A', 'Z') : 0, # 0 for a loss rock scissors

  ('B', 'X') : 0, # 0 for a loss paper rock
  ('B', 'Y') : 3, # 3 for a draw paper paper
  ('B', 'Z') : 6, # 6 for a win  paper scissors

  ('C', 'X') : 6, # 6 for a win scissors rock
  ('C', 'Y') : 0, # 0 for a loss scissors paper
  ('C', 'Z') : 3, # 3 for a draw scissors scissors

}

updated_outcomes = { 'X': 0, 'Y': 3, 'Z': 6}
updated_shapes = {
  ('A', 'X') : 3, # oppo rock, I lose, thus play scissors
  ('A', 'Y') : 1, # oppo rock, I draw, thus play rock
  ('A', 'Z') : 2, # oppo rock, I win, thus play paper

  ('B', 'X') : 1, # oppo paper, I lose, thus play rock
  ('B', 'Y') : 2, # oppo paper, I draw, thus play paper
  ('B', 'Z') : 3, # oppo paper, I win, thus play scissors

  ('C', 'X') : 2, # oppo scissors, I lose, thus play paper
  ('C', 'Y') : 3, # oppo scissors, I draw, thus play scissors
  ('C', 'Z') : 1, # oppo scissors, I win, thus play rock

}

def main():
  total_score = 0
  with open(filename, "r") as fh:
    for line in fh:
      oppo_play, my_play = line.split()
      shape_score = shape_scores[my_play]
      outcome_score = outcome_scores[(oppo_play, my_play)]
      total_score += shape_score + outcome_score
      #print(f"shape score is {shape_score} ")
      #print(f"outcome score is {outcome_score} ")
  print(f"total score is {total_score} ")

def updated():
  total_score = 0
  with open(filename, "r") as fh:
    for line in fh:
      oppo_play, should = line.split()
      shape_score = updated_shapes[(oppo_play, should)]
      outcome_score = updated_outcomes[should]
      total_score += shape_score + outcome_score
      #print(f"shape score is {shape_score} ")
      #print(f"outcome score is {outcome_score} ")
  print(f"updated score is {total_score} ")

if __name__ == "__main__":
  main()
  updated()

