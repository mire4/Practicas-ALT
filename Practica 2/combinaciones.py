# AUTORES:
# Mireia Pires State

def combinaciones(elementos, cantidad):
    sol = [None]*cantidad
    def backtracking(longSol, i):
        # Caso base: Hemos llegado al ultimo elemento
        # Tenemos una combinacion posible
        if longSol == cantidad:
            yield sol.copy()
        else:
            # Para cada elemento cogemos su indice y el elemento
            for ind, child in enumerate(elementos):
                # Comprobamos que el elemento no forme parte de la solucion
                # y que cumpla el orden original
                if(child not in sol and ind >= i):
                    sol[longSol] = child
                    yield from backtracking(longSol + 1, ind + 1)
            sol[longSol] = None
    yield from backtracking(0, 0)

if __name__ == "__main__":    
    for x in combinaciones(['tomate','queso','anchoas', 'aceitunas'], 3):
        print(x)