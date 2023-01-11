import numpy as np
import heapq
import collections

######################################################################
#                                                                    #
#                     GENERACION DE INSTANCIAS                       #
#                                                                    #
######################################################################

def genera_instancia(M, low = 1, high = 1000):
    return np.random.randint(low = low, high = high, size = (M, M), dtype = int)

######################################################################
#                                                                    #
#                       ALGORITMOS VORACES                           #
#                                                                    #
######################################################################

def compute_score(costMatrix, solution):
    return sum(costMatrix[pieza, instante]
               for pieza, instante in enumerate(solution))

def naive_solution(costMatrix):
    solution = list(range(costMatrix.shape[0]))
    return compute_score(costMatrix, solution), solution

def voraz_x_pieza(costMatrix):
    # costMatrix[i,j] el coste de situar pieza i en instante j
    M = costMatrix.shape[0] # nº piezas
    solution = []
    score = 0
    for pieza in range(M):
        costeMin = float('inf')
        for i, cost in enumerate(costMatrix[pieza]):
            if cost < costeMin and i not in solution:
                costeMin = cost
                x = i
        solution.append(x)
        score += costeMin
    return score, solution

def voraz_x_instante(costMatrix):
    # costMatrix[i,j] el coste de situar pieza i en instante j
    aux = []
    solution = []
    score = 0
    piezaSeleccionada = None
    for instante in range(costMatrix.shape[1]): # Por columnas
        costMin = float('inf')
        for pieza, cost in enumerate(costMatrix[:, instante]):
            if cost < costMin and pieza not in solution:
                costMin = cost
                piezaSeleccionada = pieza
        aux.append(piezaSeleccionada)
        score += costMin
    for pieza in range(costMatrix.shape[0]):
        for piezaSol in range(len(aux)):
            if (pieza == aux[piezaSol]):
                solution.append(piezaSol)
    return score, solution

def voraz_x_coste(costMatrix):
    # costMatrix[i,j] el coste de situar pieza i en instante j
    # Crear lista de elementos ordenados por valor
    ordenados = [(i, j, costMatrix[i][j]) for i in range(costMatrix.shape[0]) for j in range(costMatrix.shape[1])]
    ordenados = sorted(ordenados, key = lambda x: x[2])
    # Inicializar contadores
    piezasUtilizadas = []
    instantesUtilizados = []
    score = 0
    solution = []
    # Recorrer elementos ordenados
    for fila, columna, valor in ordenados:
        # Si hay piezas e instantes disponibles, utilizar elemento
        if fila not in piezasUtilizadas and columna not in instantesUtilizados:
            piezasUtilizadas.append(fila)
            instantesUtilizados.append(columna)
            score += valor
    for p, pieza in enumerate(piezasUtilizadas):
        for i, instante in enumerate(instantesUtilizados):
            if p == i:
                solution.insert(pieza, instante)
    return score, solution

def voraz_combina(costMatrix):
    
    scorePieza, solutionPieza = voraz_x_pieza(costMatrix)
    scoreInstante, solutionInstante = voraz_x_instante(costMatrix)
    scoreCoste, solutionCoste = voraz_x_coste(costMatrix)

    min_score = min([scorePieza, scoreInstante, scoreCoste])

    if min_score == scorePieza:
        return scorePieza, solutionPieza
    elif min_score == scoreInstante:
        return scoreInstante, solutionInstante
    else:
        return scoreCoste, solutionCoste
        
######################################################################
#                                                                    #
#                       RAMIFICACION Y PODA                          #
#                                                                    #
######################################################################

class Ensamblaje:

    def __init__(self, costMatrix, initial_sol = None):
        '''
        costMatrix es una matriz numpy MxM con valores positivos
        costMatrix[i,j] es el coste de ensamblar la pieza i cuando ya
        se han ensamblado j piezas.
        '''
        # no har�a falta pero por si acaso comprobamos que costMatrix
        # es una matriz numpy cuadrada y de costMatrix positivos
        assert(type(costMatrix) is np.ndarray and len(costMatrix.shape) == 2
               and costMatrix.shape[0] == costMatrix.shape[1]
               and costMatrix.dtype == int and costMatrix.min() >= 0)
        self.costMatrix = costMatrix
        self.M = costMatrix.shape[0]
        # la forma m�s barata de ensamblar la pieza i si podemos
        # elegir el momento de ensamblaje que m�s nos convenga:
        self.minPieza = [costMatrix[i, :].min() for i in range(self.M)]
        self.x = initial_sol
        if initial_sol is None:
            self.fx = np.inf
        else:
            self.fx = compute_score(costMatrix, initial_sol)
        
    def branch(self, s_score, s):
        '''
        s_score es el score de s
        s es una soluci�?³n parcial
        '''
        i = len(s) # i es la siguiente pieza a montar, i < M
        
        # costMatrix[i, j] coste ensamblar objeto i en instante j
        for j in range(self.M): # todos los instantes
            # si j no ha sido utilizado en s
            if j not in s: # NO es la forma m�s eficiente
                           # al ser lineal con len(s)
                new_score = s_score - self.minPieza[i] + self.costMatrix[i, j]
                yield (new_score, s + [j])

    def is_complete(self, s):
        '''
        s es una soluci�?³n parcial
        '''
        return len(s) == self.M

    def initial_solution(self):
        return (sum(self.minPieza), [])

    def solve(self):
        A = [self.initial_solution()] # cola de prioridad
        iterations = 0 # n� iteraciones
        gen_states = 0 # n� estados generados
        podas_opt  = 0 # n� pod  as por cota optimista
        maxA       = 0 # tama�o m�ximo alzanzado por A
        # bucle principal ramificacion y poda (PODA IMPLICITA)
        while len(A) > 0 and A[0][0] < self.fx:
            iterations += 1
            lenA = len(A)
            maxA = max(maxA, lenA)
            s_score, s = heapq.heappop(A)
            for child_score, child in self.branch(s_score, s):
                gen_states += 1
                if self.is_complete(child): # si es terminal
                    # es factible (pq branch solo genera factibles)
                    # falta ver si mejora la mejor solucion en curso
                    if child_score < self.fx:
                        self.fx, self.x = child_score, child
                else: # no es terminal
                    # lo metemos en el cjt de estados activos si
                    # supera la poda por cota optimista:
                    if child_score < self.fx:
                        heapq.heappush(A, (child_score, child) )
                    else:
                        podas_opt += 1
                        
        stats = { 'iterations': iterations,
                  'gen_states': gen_states,
                  'podas_opt': podas_opt,
                  'maxA': maxA}
        return self.fx, self.x, stats

def functionRyP(costMatrix):
    e = Ensamblaje(costMatrix)
    fx, x, stats = e.solve()
    return fx, x

######################################################################
#                                                                    #
#                        EXPERIMENTACION                             #
#                                                                    #
######################################################################

cjtAlgoritmos = {'naif': naive_solution,
                 'x_pieza': voraz_x_pieza,
                 'x_instante': voraz_x_instante,
                 'x_coste': voraz_x_coste,
                 'combina': voraz_combina,
                 'RyP': functionRyP
                }


def probar_ejemplo():
    ejemplo = np.array([[7, 3, 7, 2],
                        [9, 9, 4, 1],
                        [9, 4, 8, 1],
                        [3, 4, 8, 4]], dtype=int)
    print(ejemplo)
    for label, function in cjtAlgoritmos.items():
        score, solution = function(ejemplo)
        print(f'Algoritmo {label:10}', solution, score)

def comparar_algoritmos():
    print('talla', end=' ')
    for label in cjtAlgoritmos:
        print(f'{label:>10}', end=' ')
    print()
    numInstancias = 10
    for talla in range(5, 15 + 1):
        dtalla = collections.defaultdict(float)
        for instancia in range(numInstancias):
            cM = genera_instancia(talla)
            for label, function in cjtAlgoritmos.items():
                score, solution = function(cM)
                dtalla[label] += score
        print(f'{talla:>5}', end = ' ')
        for label in cjtAlgoritmos:
            media = dtalla[label] / numInstancias
            print(f'{media:10.2f}', end=' ')
        print()

def probar_ryp():
    ejemplo = np.array([[7, 3, 7, 2],
                        [9, 9, 4, 1],
                        [9, 4, 8, 1],
                        [3, 4, 8, 4]], dtype=int)
    # scorevoraz, solvoraz = voraz_combina(ejemplo)
    # bb = Ensamblaje(ejemplo, solvoraz)
    bb = Ensamblaje(ejemplo)
    fx, x, stats = bb.solve()
    print(x, fx, compute_score(ejemplo, x))
    print(stats)
    
######################################################################
#                                                                    #
#                             PRUEBAS                                #
#                                                                    #
######################################################################
    
if __name__ == '__main__':
    probar_ejemplo()
    print('-' * 70)
    probar_ryp()
    print('-' * 70)
    comparar_algoritmos()
