LVR-sat
=======

Ekipa PBK (Urška, Jan, Luka)

V repositoriju je napisan SAT solver, osnova za logične izraze in nekaj prevedb problemov v Boolove formule.
___


**Datoteke:**

- *basic_example.py* ... nekaj primerov Boolovih formul
- *graphColoring_example.py* ... nekaj primerov reševanja barvanja grafov
- *sudoku_example.py* ... nekaj primerov reševanja sudokujev
- *sudoku_example_mt.py* ... nekaj primerov reševanja sudokujev z večnitnih SAT solverjem
- *src/graphColoring.py* ... prevedba problema barvanja grafov v Boolovo formulo
- *src/logConstruct.py* ... elementi za predstavitev Boolove formule
- *src/sat.py* ... SAT solver
- *src/sudoku.py* ... prevedba reševanja sudokuja v Boolovo formulo
- *src/test.py* ... nekaj testnih primerov za preverjanje pravilnosti implementacije
- *src/automated_test/test_cnf_basic.py* ... testi za preverjanje delovanja funkcije cnf
- *src/automated_test/test_sat.py* ... testi za preverjanje delovanja SAT solverja
- *src/automated_test/test_sat_mt.py* ... testi za preverjanje delovanja večnitnega SAT solverja
- *src/automated_test/test_simplify_basic.py* ... testi za preverjanje delovanja funkcije simplify
- *src/automated_test/test_system.py* ... požene vse tri zgoraj naštete teste

___

**Navodila:**

- Boolovo formulo sestavimo na naslednji način: 
    npr. *Not(Or([And([Var("x"), Var("y")]), false()]))* ustreza formuli *¬(((x ∧ y) ∨ ⊥))* 
- Za uporabo prevedbe barvanja grafov, podamo funkciji *graphColoring.py* graf predstavljen 
  z matriko sosednosti kot prvi argument, npr. *G= [[1, 0],[0, 1]]*, in željeno število barv 
  kot drugi:		
    npr. *graphColoring(G,st_barv)* 
- Za uporabo prevedbe reševanja sudokuja, podamo funkciji *sudoku.py* sudoku zapisan v matriki 
  velikosti 9x9:		
    npr. *sudoku(matrika_sudoku)* 
- Avtomatizirani testi:
    1. premakni se v mapo *src/automated_test*
    2. napisi python "ime_testa"
- Primeri vsebujejo nekaj osnovnih Boolovih formul, barvanje grafov, sudoku. 
    1. premakni se v koren projekta
    2. napisi python ./"ime_primera"

___

**SAT solver**
- značilnosti:
    - izhod v berljivi obliki (UTF-8 kodiranje)
    -  večnitna in enonitna podpora
    -  hevristika na podlagi števila izločenih stavkov
- koda
    - [vir za DPLL algoritem] (http://www.dis.uniroma1.it/~liberato/ar/dpll/dpll.html)
    - večnitna možnost: 
        - vzdrževalna nit (zagotavlja čiščenje niti in vzdržuje zgornjo mejo, ki je nastavljiva)
        - drsteča nit (glavna nit, ki periodično skrbi za nastajanje novih niti; perioda je nastavljiva)
        - n delovnih niti (dejansko opravljajo delo)

___

**Zahteva**

Python

___

**Kontakt**

https://github.com/urska19






