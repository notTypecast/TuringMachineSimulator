# Turing Machine Simulator

An implementation of a turing machine simulator in Python.

### Execution
The script simulating a turing machine for a given input should be run with two arguments: the name or directory of the file containing the turing machine description, as well as the word the turing machine should be run for. Additional, optional arguments include -g (to enable graphical showcase of machine execution) and -d followed by a float (to set the delay between each step).

### Describing a turing machine
A turing machine can be described in a text file, by following these rules:
* State names should start with a letter and only contain letters and digits.
* The first line should contain the name of the starting state.
* The second line should contain the name of the accept state.
* The third line should contain the name of the reject state.
* Any of the following lines should contain values of the transition function. The given format for each line should be exactly `t(q,x)=(r,y,M)`, where `q` is the current state, `x` is the symbol being read, `r` is the next state, `y` is the symbol to write and `M` is either `R` or `L`, depending on whether the head of the tape should be moved right or left respectively. `y` can be given the special value `NULL`, if nothing should be written.
* Any amount of lines can be left blank and will not be considered.
* Comments can be created using the `//` syntax. Anything written after the `//` symbol will be ignored.

### Examples
There are various example turing machine descriptions provided.
* `tm1.txt`: A turing machine deciding the language `a*b*`.
* `tm2.txt`: A turing machine deciding the language `a^(i)b^(j), 0≤j≤i`, given that the input is in `a*b*`.
* `tm3.txt`: A turing machine recognizing the language `a*b`, but which gets stuck on any word containing `ad` before any `b` or `c`, or having `d` as its first letter. Used to showcase how a turing machine which recognizes a language might get indefinitely stuck.
