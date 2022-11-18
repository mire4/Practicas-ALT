# -*- coding: utf-8 -*-

# AUTORA:
# Mireia Pires State

import sys

def langford(N):
    N2   = 2*N
    seq  = [0]*N2
    def backtracking(num):
        if num<=0:
            yield "-".join(map(str, seq))
        else:
            # buscamos una posicion para situar una pareja num
            # Queremos saber tanto el indice como el valor
            for ind, valor in enumerate(seq):
                # Calculamos la segunda posicion donde bede ir el numero
                siguientePos = ind + num + 1
                if siguientePos < N2 and valor == 0 and seq[siguientePos] == 0:
                    # Insertamos los dos numeros iguales en sus posiciones
                    seq[ind] = num
                    seq[siguientePos] = num
                    yield from backtracking(num - 1)
                    seq[ind] = 0
                    seq[siguientePos] = 0
    if N%4 in (0,3):
        yield from backtracking(N)

if __name__ == "__main__":
    if len(sys.argv) not in (2,3):
        print('\nUsage: %s N [maxsoluciones]\n' % (sys.argv[0],))
        sys.exit()
    try:
        N = int(sys.argv[1])
    except ValueError:
        print('First argument must be an integer')
        sys.exit()
    numSolutions = None
    if len(sys.argv) == 3:
        try:
            numSolutions = int(sys.argv[2])
        except ValueError:
            print('Second (optional) argument must be an integer')
            sys.exit()

    i = 0
    for sol in langford(N):
        if numSolutions is not None and i>=numSolutions:
            break
        i += 1
        print(f'sol {i:4} ->',sol)
