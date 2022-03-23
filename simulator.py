"""
Turing machine simulator
Accepts a turing machine M and a word W
Runs M with w as input
Simulates M with input w and outputs True, False, or gets stuck in infinite loop
Turing machine is given as input through tm.txt input file
Lines 1, 2 and 3 must contain starting state, accept state and reject state respectively
Remaining lines must contain transition function in following form:
t(q,c)=(r,d,R) or
t(q,c)=(r,d,L), where:
q is the current state
c is the character being read
r is the next state
d is the character to be written
R/L represents whether the head should be moved right or left
"""
import re
import argparse
from string import ascii_letters, digits
from time import sleep

TRANSITION_REGEX = "t\(([a-zA-Z0-9]+),(.)\)=\(([a-zA-Z0-9]+),(.|NULL),(R|L)\)"
STATE_CHARS = set(ascii_letters) | set(digits)

def valid_state(q):
	"""
	Returns True or False, depending on whether given state name is valid
	"""
	return q[0] in ascii_letters and bool(q) and not (set(q) - STATE_CHARS)


class TuringMachine:

	class Tape:
		def __init__(self, w):
			self.tape = list(w)
			self.head = 0

			if not self.tape:
				self.tape.append("⊔")

		def move_left(self):
			if self.head > 0:
				self.head -= 1

		def move_right(self):
			self.head += 1
			while len(self.tape) <= self.head:
				self.tape.append("⊔")

		def write(self, s):
			if s == "NULL":
				return

			if len(s) != 1:
				raise ValueError("Symbol required")

			self.tape[self.head] = s

		def current(self):
			return self.tape[self.head]

		def print(self):
			print("\r" + "".join(self.tape) + " "*10)
			print("\r" + " "*self.head + "^" + " "*10, end="\033[A")


	def __init__(self, M):
		"""
		Initializes a new TM from given representation M
		"""
		if not (valid_state(M[0]) and valid_state(M[1]) and valid_state(M[2])):
			raise ValueError("Invalid state")

		self.current_state = M[0]
		self.initial_state = M[0]
		self.accept_state = M[1]
		self.reject_state = M[2]

		self.transitions = {}

		for transition in M[3:]:
			vals = re.findall(TRANSITION_REGEX, transition)[0]
			if len(vals) != 5:
				raise ValueError("Invalid transition")

			if not (valid_state(vals[0]) and valid_state(vals[2])):
				raise ValueError("Invalid state")

			self.transitions[vals[0], vals[1]] = vals[2], vals[3], vals[4]

	def run(self, w, graphics=False, delay=.5):
		"""
		Runs machine for input w
		"""
		tape = TuringMachine.Tape(w)

		if graphics:
			print()

		while self.current_state != self.accept_state and self.current_state != self.reject_state:
			if graphics:
				tape.print()
				sleep(delay)

			try:
				res = self.transitions[self.current_state, tape.current()]
			except KeyError:
				break

			self.current_state = res[0]
			tape.write(res[1])
			if res[2] == "R":
				tape.move_right()
			elif res[2] == "L":
				tape.move_left()
			else:
				raise ValueError("Invalid head move instruction")

		if graphics:
			print()

		return self.current_state == self.accept_state

parser = argparse.ArgumentParser(description="Turing Machine Simulator")
parser.add_argument("tm_file", type=str, help="Name or directory of file describing turing machine to simulate")
parser.add_argument("word", type=str, nargs="?", default="", help="The input of the turing machine; empty string is used if argument is not passed")
parser.add_argument("-g", action="store_true", help="Enables graphically showcasing the execution of the simulated turing machine")
parser.add_argument("-d", type=float, default=.5, help="Delay between each step when graphically showcasing machine execution")

args = parser.parse_args()

# get TM
with open(args.tm_file, "r") as f:
	M = f.read().split("\n")
	out = []
	for line in M:
		try:
			line = line[:line.index("//")].strip()
		except ValueError:
			line = line.strip()
			if line:
				out.append(line)
			continue

		if line:
			out.append(line)

TM = TuringMachine(out)

print(TM.run(args.word, args.g, args.d))

