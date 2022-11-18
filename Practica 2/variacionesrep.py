# AUTORES:
# Mireia Pires State

def variacionesRepeticion(elementos, cantidad):
    sol = [None]*cantidad
    def backtracking(longSol):
        if longSol == cantidad:
            yield sol.copy()
        else:
            for child in elementos:
                if (child not in elementos):
                    sol[longSol] = child
                    yield from backtracking(longSol+1)
            sol[longSol] = None    
    yield from backtracking(0)

if __name__ == "__main__":    
    for x in variacionesRepeticion(['tomate','queso','anchoas'],3):
        print(x)