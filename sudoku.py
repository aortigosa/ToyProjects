# versión donde tablero es un diccionario indexado por duplas
# cada elemento es un numero (final) o una lista (candidatos)


def inicializaTablero():
    tablero = {}
    for i in range(9):
        for j in range(9):
            tablero[(i, j)] = [k for k in range(1, 10)]
    return tablero

def verificarSolucion(tablero):
    """ Retorna True si el tablero constituye una solucion valida
    """
    for i in range(9):
        for j in range(9):
            if not isinstance(tablero[(i,j)], int):
                return False
    # TODO: VER si no hay conflictos
    return True

def verificarHayOpciones(tablero):
    """Retorna falso si hay una celda con 0 opciones"""
    for i in range(9):
        for j in range(9):
            if isinstance(tablero[(i,j)], list) and not tablero[(i,j)]:
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

def generaRegionCelda(celda, contieneCelda=True):
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

def candidatoUnicoCelda(tablero):
    """Verifica si existe alguna celda que tenga un único candidato.
        Retorna la primera celda del tablero que cumpla la condición.
    """
    for i in range(9):
        for j in range(9):
            if isinstance(tablero[(i,j)], list) and len(tablero[(i,j)])==1:
                return (i, j)

def celdasEnRegion(x_region, y_region):
    celdas = []
    for i in range(3):
        for j in range(3):
            celdas.append((x_region*3+i, y_region*3+j))
    return celdas

def celdaUnicaCandidatoRegion(tablero):
    """ Retorna una celda (la primera que encuentre) de la region que contiene un candidato que 
    NO se repite en otra celda de la misma región, y también retorna el candidato.
    """
    for x_region in range(3):
        for y_region in range(3):
            celdas = celdasEnRegion(x_region, y_region)
            for c in celdas:
                if isinstance(tablero[c], list):
                    for d in tablero[c]:
                        celda = c
                        # ver si d está en otra celda de celdas
                        for c2 in celdas:
                            if c != c2 and isinstance(tablero[c2], list) and d in tablero[c2]:
                                celda = None
                                break #sale del for c2, prueba con el proximo digito de c
                        if celda: # significa que ha encontrado un candidato que no está en otra celda
                            return celda, d
    return None,None

def celdaUnicaCandidatoFila(tablero):
    """ Retorna una celda (la primera que encuentre) de la fila que contiene un candidato que 
    NO se repite en otra celda de la misma fila, y también retorna el candidato.
    """
    for fila in range(9):
        celdas = []
        for col in range(9):
            celdas.append((fila, col))
        for c in celdas:
            if isinstance(tablero[c], list):
                for d in tablero[c]:
                    celda = c
                    # ver si d está en otra celda de celdas
                    for c2 in celdas:
                        if c != c2 and isinstance(tablero[c2], list) and d in tablero[c2]:
                            celda = None
                            break #sale del for c2, prueba con el proximo digito de c
                    if celda: # significa que ha encontrado un candidato que no está en otra celda
                        return celda, d
    return None,None

def celdaUnicaCandidatoCol(tablero):
    """ Retorna una celda (la primera que encuentre) de la columna que contiene un candidato que 
    NO se repite en otra celda de la misma columna, y también retorna el candidato.
    """
    for col in range(9):
        celdas = []
        for fila in range(9):
            celdas.append((fila, col))
        for c in celdas:
            if isinstance(tablero[c], list):
                for d in tablero[c]:
                    celda = c
                    # ver si d está en otra celda de celdas
                    for c2 in celdas:
                        if c != c2 and isinstance(tablero[c2], list) and d in tablero[c2]:
                            celda = None
                            break #sale del for c2, prueba con el proximo digito de c
                    if celda: # significa que ha encontrado un candidato que no está en otra celda
                        return celda, d
    return None,None


def celdaUnicaCandidato(tablero):
    """ Retorna si existe alguna celda que contiene un candidato que no se repite en
    otra celda de la region/fila/columna.
    Retorna la primera fila que cumpla esa condición, junto con dígito candidato
    """
    # por regiones
    celda, candidato = celdaUnicaCandidatoRegion(tablero)
    if celda:
        return celda, candidato
    celda, candidato =  celdaUnicaCandidatoFila(tablero)
    if celda:
        return celda, candidato
    
    celda, candidato =  celdaUnicaCandidatoColumna(tablero)
    return celda, candidato

def confirmaCandidato(tablero, celda, candidato=None):
    """Si candidato no es suministrado, asume que celda contiene un candidato único.
        En todo caso, pone el candidado pasado como argumento o el que contiene la celda
        como definitivo, y se encarga de quitar los candidatos de la fila, columna y region correspondiente
    """
    # if not isinstance(tablero[celda], list):
    #     print(f"ERROR, llama a confirmaCandidado pero celda={celda} no tiene candidato unico en tablero {tablero[celda]}")
    #     return False
    # if isinstance(tablero[celda], list) and not len(tablero[celda])==1:
    #     print(f"ERROR, llama a confirmaCandidado pero celda={celda} no tiene candidato unico en tablero {tablero[celda]}")
    #     return False
    if not candidato:
        final = tablero[celda][0]
    else:
        final = candidato
    tablero[celda] = final
    lista = generaRegionCelda(celda, contieneCelda=False)
    for c in lista:
        if isinstance(tablero[c], list):
            if final in tablero[c]:
                tablero[c].remove(final)

    lista = generaFila(celda, contieneCelda=False)
    for c in lista:
        if isinstance(tablero[c], list):
            if final in tablero[c]:
                tablero[c].remove(final)

    lista = generaColumna(celda, contieneCelda=False)
    for c in lista:
        if isinstance(tablero[c], list):
            if final in tablero[c]:
                tablero[c].remove(final)

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
        celda = candidatoUnico(tablero)
        if celda:
            tablero = confirmaCandidato(tablero, celda)
            continue

        # - ver si candidato único region, fila o columna
        #   + poner número (candidato) en tablero
        #   + next
        celda, candidato = celdaUnicaCandidato(tablero)
        if celda:
            tablero = confirmaCandidato(tablero, celda, candidato=candidato)
            continue
        
        # - ver si par candidatos en par de celdas región, fila o columna
        #   + quitar par como candidatos de otras celdas de la región/fila/columna
        #   + next
        # - ver si trio candidatos en trio de celdas región, fila o columna
        #   + quitar trio como candidatos de otras celdas de la región/fila/columna
        #   + next

tablero = inicializaTablero()
# tablero[(0,3)] = [1, 2,3,4,5,6,7,8]
# tablero[(1,3)] = [1, 2,3,4,5,6,7,8]
# tablero[(2,3)] = [1, 2,3,4,5,6,7,8]
# tablero[(4,3)] = [1, 2,3,4,5,6,7,8]
# tablero[(5,3)] = [1, 2,3,4,5,6,7,8]
# tablero[(6,3)] = [1, 2,3,4,5,6,7,8]
# tablero[(7,3)] = [1, 2,3,4,5,6,7,8]
# tablero[(8,3)] = [1, 2,3,4,5,6,7,8]


celda, candidato = celdaUnicaCandidatoCol(tablero)
print(celda)
print(candidato)
#tablero = confirmaCandidato(tablero, (8,8))
#prettyPrint(tablero)
# print(tablero[(0,8)])
# print(tablero[(1,8)])
# print(tablero[(4,8)])
# print(tablero[(8,0)])
# print(tablero[(8,5)])
# print(tablero[(6,6)])
# print()
# print(tablero[(5,5)])


