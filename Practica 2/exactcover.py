# AUTORA:
# (poner aquí el nombre o 2 nombres del equipo de prácticas

def exact_cover(listaConjuntos):
    U = set().union(*listaConjuntos) # para saber qué universo tenemos
    N = len(listaConjuntos)
    solucion = []
    def backtracking(longSol, cjtAcumulado):
        # Caso base: El conjunto forma parte del universo
        if set().union(*cjtAcumulado) == U:
            yield solucion.copy()
        # Ramificamos
        elif longSol < N:
            cjt = listaConjuntos[longSol]
            # Comprobamos que sean disjuntos
            if set().union(*cjtAcumulado).isdisjoint(cjt):
                solucion.append(cjt)
                yield from backtracking(longSol + 1, solucion)
                solucion.pop()
            # En culaquier otro caso ramificamos saltandonos cjt
            yield from backtracking(longSol + 1, solucion)
    yield from backtracking(0, set())

if __name__ == "__main__":
    cjtdcjts = [{"casa","coche","gato"},
                {"casa","bici"},
                {"bici","perro"},
                {"boli","gato"},
                {"coche","gato","bici"},
                {"casa", "moto"},
                {"perro", "boli"},
                {"coche","moto"},
                {"casa"}]
    for solucion in exact_cover(cjtdcjts):
        print(solucion)