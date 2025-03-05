# version donde tablero es una lista de listas
tablero = [None] * 81

def inicializaTablero():
    tablero = [[i for i in range(1, 10)] for _ in range(81)]
    return tablero

def inicializaTablero2():
    tablero = {}
    for i in range(9):
        for j in range(9):
            tablero[(i, j)] = [k for k in range(1, 10)]
    return tablero

def verificarSolucion(tablero):
    for i in range(81):
        if not isinstance(tablero[i], int):
            return False
    # TODO: VER si no hay conflictos
    return True

def verificarHayOpciones(tablero):
    for i in range(81):
        if isinstance(tablero[i], list) and not tablero[i]:
            return False
    return True

def generaFila(celda, contieneCelda=True):
    """devuelve lista de celdas con la misma fila que la celda argumento"""
    fila = celda[0]
    lista = []
    for col in range(9):
        lista.append((fila, col))
    if not contieneCelda:
        lista.remove(celda)
    return lista
    
def generaColumna(celda, contieneCelda=True):
    """devuelve lista de celdas con la misma columna que la celda argumento"""
    col = celda[1]
    lista = []
    for fila in range(9):
        lista.append((fila, col))
    if not contieneCelda:
        lista.remove(celda)
    return lista

def generaRegion(celda, contieneCelda=True):
    """devuelve la lista de celdas en la misma región que la celda argumento"""
    x = celda[0]
    y = celda[1]
    lista = []
    if x>5:
        x_region = 2
    elif x>2:
        x_region = 1
    else:
        x_region = 0

    if y>5:
        y_region = 2
    elif y>2:
        y_region = 1
    else:
        y_region = 0

    for i in range(3):
        for j in range(3):
            lista.append((x_region*3+i, y_region*3+j))
    if not contieneCelda:
        lista.remove(celda)
    return lista

def dupla2indice(x, y):
    """Dado un par x, y retorna el índice correspondiente de la lista"""
    # 1,4 = 13
    # 4,6 = 42
    return x * 9 + y

def candidatoUnico(tablero):
    """Verifica si existe alguna celda que tenga un único candidato"""
    for i in range(9):
        for j in range(9):
            indice = dupla2indice(i, j)
            if isinstance(tablero[indice], list) and len(tablero[indice])==1:
                return (i, j)

def confirmaCandidato(tablero, celda):
    """Asume que celda contiene un candidato único.
        Pone ese valor como definitivo, y se encarga de quitar los candidatos
        de la fila, columna y region correspondiente
    """
    i = celda[0]
    j = celda[1]
    indice = dupla2indice(i, j)
    if not isinstance(tablero[indice], list):
        print(f"ERROR, llama a confirmaCandidado pero celda={celda} no tiene candidato unico en tablero {tablero}")
        return False
    if isinstance(tablero[indice], list) and not len(tablero[indice])==1:
        print(f"ERROR, llama a confirmaCandidado pero celda={celda} no tiene candidato unico en tablero {tablero}")
        return False
    final = tablero[indice][0]
    tablero[indice] = final
    lista = generaRegion(celda, contieneCelda=False)
    for c in lista:
        indice = dupla2indice(c[0], c[1])
        if isinstance(tablero[indice], list):
            if final in tablero[indice]:
                tablero[indice].remove(final)

    lista = generaFila(celda, contieneCelda=False)
    for c in lista:
        indice = dupla2indice(c[0], c[1])
        if isinstance(tablero[indice], list):
            if final in tablero[indice]:
                tablero[indice].remove(final)

    lista = generaColumna(celda, contieneCelda=False)
    for c in lista:
        indice = dupla2indice(c[0], c[1])
        if isinstance(tablero[indice], list):
            if final in tablero[indice]:
                tablero[indice].remove(final)

    return tablero

def prettyPrint(tablero):
    for i in range(9):
        for j in range(9):
            print(tablero[(i,j)], end="")
        print()

def principal():
    seguir = False
    tablero = inicializaTablero()
    while seguir:
        # - ver si ya esta --> return tablero
        if verificarSolucion(tablero):
            return tablero
        # - verificar celda sin candidato --> error
        if not verificarHayOpciones():
            print(f"Error, un tablero sin solución posible: {tablero}")
            return False

        # - ver si alguna celda tiene un único candidato:
        #   + poner número (candidato) en tablero
        #   + next
        # - ver si candidato único region, fila o columna
        #   + poner número (candidato) en tablero
        #   + next
        # - ver si par candidatos en par de celdas región, fila o columna
        #   + quitar par como candidatos de otras celdas de la región/fila/columna
        #   + next
        # - ver si trio candidatos en trio de celdas región, fila o columna
        #   + quitar trio como candidatos de otras celdas de la región/fila/columna
        #   + next

tablero = inicializaTablero2()
#tablero[0] = [3]
# tablero = tablero = [1 for _ in range(81)]
prettyPrint(tablero)
#print(confirmaCandidato(tablero, (0,0)))