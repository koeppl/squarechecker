# squarechecker

**squarechecker** is a Python-based tool designed to find strings that do not exhibit squares of a specific lower threshold length under a certain matching model.

Execute the main script to start the analysis:


```bash
./squarechecker.py --type STRICT -l 3
```
Compute the longest 3+ square free word with strict equivalence of the square roots.


```bash
./squarechecker.py --type PARAMETERIZED -l 3
```
Compute the longest 3+ square free word with parameterized equivalence of the square roots.

```bash
./squarechecker.py --type ORDER_PRESERVING -l 3
```
Compute the longest 3+ square free word with order preserving equivalence of the square roots.

```bash
./squarechecker.py --type WEAK_ORDER_PRESERVING -l 3
```
Compute the longest 3+ square free word with weak order preserving equivalence of the square roots,
where weak order means that we compare only x[i] <> x[j] for i < j.

```bash
./squarechecker.py --type CARTESIAN -l 4
```
Compute the longest 4+ square free word with cartesian equivalence of the square roots.

```bash
./squarechecker.py --type STRICT -l 1 -o CUBE
./squarechecker.py --type PARAMETERIZED -l 2 -o CUBE
./squarechecker.py --type ORDER_PRESERVING -l 2 -o CUBE
./squarechecker.py --type WEAK_ORDER_PRESERVING -l 3 -o CUBE
./squarechecker.py --type CARTESIAN -l 3 -o CUBE
```
The same as above, but omitting cubes.

```bash
./findmorphism.py -l 3 --codelength 2 --iterations 6 --type PARAMETERIZED
./findmorphism.py -l 3 --codelength 2 --iterations 6 --type STRICT
./findmorphism.py -l 3 --codelength 2 --iterations 6 --type ORDER_PRESERVING
./findmorphism.py -l 3 --codelength 2 --iterations 6 --type WEAK_ORDER_PRESERVING
./findmorphism.py -l 3 --codelength 2 --iterations 6 --type CARTESIAN
```
Find codings that, applied to a square free ternary word, gives a 3+ square free word in one of the specified equivalence classes.
The number of iterations correlates with the length of the input square free ternary word.
The codelength is the maximum length of an image of a character produced by the coding.
