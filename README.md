LVR-sat
=======

V repositoriju je napisan SAT solver in nekaj prevedb problemov v Boolove formule.
___


**Datoteke:**

- *basic_example.py* ... nekaj primerov Boolovih formul
- *graphColoring_example.py* ... nekaj primerov reševanja barvanja grafov
- *sudoku_example.py* ... nekaj primerov reševanja sudokujev
- *src/graphColoring.py* ... prevedba problema barvanja grafov v Boolovo formulo
- *src/logConstruct.py* ... elementi za predstavitev Boolove formule
- *src/sat.py* ... SAT solver
- *src/sudoku.py* ... prevedba reševanja sudokuja v Boolovo formulo
- *src/test.py* ... nekaj testnih primerov za preverjanje pravilnosti implementacije
- *src/automated_test/test_cnf_basic.py* ... testi za preverjanje delovanja funkcije cnf
- *src/automated_test/test_sat.py* ... testi za preverjanje delovanja SAT solverja
- *src/automated_test/test_simplify_basic.py* ... testi za preverjanje delovanja funkcije simplify
- *src/automated_test/test_system.py* ... požene vse tri zgoraj naštete teste

___

**Navodila:**

- Boolovo formulo sestavimo na naslednji način: 
    npr. *Not(Or([And([Var("x"), Var("y")]), false()]))* ustreza formuli *¬(((x ∧ y) ∨ ⊥))* (glej *basic_example.py*)
- Za uporabo prevedbe barvanja grafov, podamo funkciji *graphColoring.py* graf predstavljen 
  z matriko sosednosti kot prvi argument, npr. *G= [[1, 0],[0, 1]]*, in željeno število barv 
  kot drugi:		
    npr. *graphColoring(G,st_barv)* (glej *graphColoring_example.py*)
- Za uporabo prevedbe reševanja sudokuja, podamo funkciji *sudoku.py* sudoku zapisan v matriki 
  velikosti 9x9:		
    npr. *sudoku(matrika_sudoku)* (glej *sudoku_example.py*)




