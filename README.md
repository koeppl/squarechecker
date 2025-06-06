# squarechecker

**squarechecker** is a Python-based tool designed to find strings that do not exhibit squares of a specific lower threshold length under a certain matching model.

Execute the main script to start the analysis:

```bash
./squarechecker.py --type STRICT -l 3
./squarechecker.py --type PARAMETERIZED -l 3
./squarechecker.py --type ORDER_PRESERVING -l 3
./squarechecker.py --type WEAK_ORDER_PRESERVING -l 3
./squarechecker.py --type CARTESIAN -l 4

./squarechecker.py --type STRICT -l 1 -o CUBE
./squarechecker.py --type PARAMETERIZED -l 2 -o CUBE
./squarechecker.py --type ORDER_PRESERVING -l 2 -o CUBE
./squarechecker.py --type WEAK_ORDER_PRESERVING -l 3 -o CUBE
./squarechecker.py --type CARTESIAN -l 3 -o CUBE

./findmorphism.py -l 3 --codelength 2 --iterations 6 --type PARAMETERIZED
./findmorphism.py -l 3 --codelength 2 --iterations 6 --type STRICT
./findmorphism.py -l 3 --codelength 2 --iterations 6 --type ORDER_PRESERVING
./findmorphism.py -l 3 --codelength 2 --iterations 6 --type WEAK_ORDER_PRESERVING
./findmorphism.py -l 3 --codelength 2 --iterations 6 --type CARTESIAN
```


