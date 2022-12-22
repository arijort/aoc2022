#!/usr/local/bin/python3.11

filename = "input.txt"
#filename = "small"
#filename = "medium"

"""
Part 1:

  Receive a serious of instructions (noop or addx). "noop" takes 1 cycle and does nothing. "addx" takes 2 cycles and add to the only register.
  Register starts at 1

addx 1
addx 4
noop
noop
noop
addx 5
addx 3
noop
addx 2
noop

Part 2

Given a 3-pixel wide sprite and a CRT with 240 pixels (6 rows of 40).
The CRT draws 1 pixel per cycle. If the sprite is on pixel, draw #, else draw "."
What 8 letters are drawn once we paint all the pixels?
"""

def main():
  instructions = []
  with open(filename, "r") as fh:
    for line in fh:
      instructions.append( (line.strip().split() ) ) # unpack tuple into instructions 

  results = { c:0 for c in [20, 60, 100, 140, 180, 220 ]}
  register, counter = 1, 1
  pixels = []
  for op in instructions:
    incr = 0
    if op[0] == "noop":
      incr = 1
      addend = [0]
    elif op[0] == "addx":
      incr = 2
      addend = [0, op[1]]

    char = ""
    for n in range(incr):
      pixel = counter - 1
      chars = ['.', '#']
      char = chars[abs(( pixel % 40 ) - register ) < 2] # index into char array
      #print(f"count {counter} drawing pixel {len(pixels)} sprite at {register} painting {char}")
      pixels.append(char)
      counter += 1
      register += int(addend[n])
      if counter in results:
        results[counter] = register

  result = sum( k * v for k,v in results.items() )
  print (f"part 1 result is {result}") # 13720
  for n in range(6):
    print("".join(pixels[ n*40: n*40 + 39])) # FBURHZCH

if __name__ == "__main__":
  main()
