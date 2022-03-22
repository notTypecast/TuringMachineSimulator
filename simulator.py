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
from string import ascii_letters, digits
from sys import argv

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

	def run(self, w):
		"""
		Runs machine for input w
		"""
		tape = TuringMachine.Tape(w)

		while self.current_state != self.accept_state and self.current_state != self.reject_state:
			try:
				res = self.transitions[self.current_state, tape.current()]
			except KeyError:
				return False

			self.current_state = res[0]
			tape.write(res[1])
			if res[2] == "R":
				tape.move_right()
			elif res[2] == "L":
				tape.move_left()
			else:
				raise ValueError("Invalid head move instruction")


		return self.current_state == self.accept_state



# get TM
with open(argv[1], "r") as f:
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

if len(argv) >= 3:
	word = argv[2]
else:
	word = ""

print(TM.run(word))

