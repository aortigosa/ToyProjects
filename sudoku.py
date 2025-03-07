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

def generaFilaCelda(celda, contieneCelda=False):
    """devuelve lista de celdas con la misma fila que la celda argumento"""
    fila = celda[0]
    lista = []
    for col in range(9):
        lista.append((fila, col))
    if not contieneCelda:
        lista.remove(celda)
    return lista
    
def generaColumnaCelda(celda, contieneCelda=False):
    """devuelve lista de celdas con la misma columna que la celda argumento"""
    col = celda[1]
    lista = []
    for fila in range(9):
        lista.append((fila, col))
    if not contieneCelda:
        lista.remove(celda)
    return lista

def generaRegionCelda(celda, contieneCelda=False):
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
    
    celda, candidato =  celdaUnicaCandidatoCol(tablero)
    return celda, candidato

def dosCeldasDosValores(tablero):
    """Busca si hay dos celdas en una region/fila/columna con solo un par de valores (los mismos).
        Esos valore no pueden aparecer en otra celda de la misma region/fila/columna (los quita)
    """
    # vamos a recorrer todas las celdas del tablero buscando una que solo tenga un par de valores
    encontrado = False
    for clave, valor in tablero.items():
        if isinstance(valor, list) and len(valor) == 2:
            # si la encontramos, vemos si eso se repite dentro de la region, la fila o la columna.
            v1 = valor[0]
            v2 = valor[1]
            celdas = generaRegionCelda(clave)
            for c in celdas:
                contenido = tablero[c]
                if isinstance(contenido, list) and len(contenido) == 2 and v1 in contenido and v2 in contenido:
                    # si eso ocurre, eliminamos los valores como candidatos de otras celdas en la region
                    celdas.remove(c)
                    for c2 in celdas:
                        contenido = tablero[c2]
                        if isinstance(contenido, list):
                            if v1 in contenido:
                                tablero[c2].remove(v1)
                                encontrado = True
                            if v2 in contenido:
                                tablero[c2].remove(v2)
                                encontrado = True
                    if encontrado:
                        return (clave, c)
            celdas = generaFilaCelda(clave)
            for c in celdas:
                contenido = tablero[c]
                if isinstance(contenido, list) and len(contenido) == 2 and v1 in contenido and v2 in contenido:
                    # si eso ocurre, eliminamos los valores como candidatos de otras celdas en la fila
                    celdas.remove(c)
                    for c2 in celdas:
                        contenido = tablero[c2]
                        if isinstance(contenido, list):
                            if v1 in contenido:
                                tablero[c2].remove(v1)
                                encontrado = True
                            if v2 in contenido:
                                tablero[c2].remove(v2)
                                encontrado = True
                    if encontrado:
                        return (clave, c)
            celdas = generaColumnaCelda(clave)
            for c in celdas:
                contenido = tablero[c]
                if isinstance(contenido, list) and len(contenido) == 2 and v1 in contenido and v2 in contenido:
                    # si eso ocurre, eliminamos los valores como candidatos de otras celdas en la columna
                    celdas.remove(c)
                    for c2 in celdas:
                        contenido = tablero[c2]
                        if isinstance(contenido, list):
                            if v1 in contenido:
                                tablero[c2].remove(v1)
                                encontrado = True
                            if v2 in contenido:
                                tablero[c2].remove(v2)
                                encontrado = True
                    if encontrado:
                        return (clave, c)
    return encontrado                                

def xCeldasxValores(tablero):
    """Busca si hay X celdas en una region/fila/columna
    con solo un conjunto de X valores (los mismos).
    Esos valores no pueden aparecer en otra celda de la misma region/fila/columna (los quita)
    """
    # vamos a recorrer todas las celdas del tablero buscando una que solo tenga 3 valores candidatos
    encontrado = False
    for clave, valor in tablero.items():
        if isinstance(valor, list) and len(valor) == 3:
            # si la encontramos, vemos si eso se repite dentro de la region, la fila o la columna.
            v1 = valor[0]
            v2 = valor[1]
            v3 = valor[2]
            celdas = generaRegionCelda(valor)
            for c in celdas:
                contenido = tablero[c]
                if isinstance(contenido, list) and len(contenido) == 3 and v1 in contenido and v2 in contenido and v3 in contenido:
                    # si eso ocurre, eliminamos los valores como candidatos de otras celdas en la region
                    celdas.remove(c)
                    for c2 in celdas:
                        contenido = tablero[c]
                        if isinstance(contenido, list):
                            if v1 in contenido:
                                tablero[c2].remove(v1)
                                encontrado = True
                            if v2 in contenido:
                                tablero[c2].remove(v2)
                                encontrado = True
                            if v3 in contenido:
                                tablero[c2].remove(v3)
                                encontrado = True
                            if encontrado:
                                return tablero

                            

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

    lista = generaFilaCelda(celda, contieneCelda=False)
    for c in lista:
        if isinstance(tablero[c], list):
            if final in tablero[c]:
                tablero[c].remove(final)

    lista = generaColumnaCelda(celda, contieneCelda=False)
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

def principal(tablero):
    seguir = True
    #tablero = inicializaTablero()
    while seguir:
        # - ver si ya esta --> return tablero
        if verificarSolucion(tablero):
            if debug:
                print(f"encuentra solución con tablero:{tablero}")
            return tablero
        # - verificar celda sin candidato --> error
        if not verificarHayOpciones(tablero):
            print(f"Error, un tablero sin solución posible: {tablero}")
            return False

        # - ver si alguna celda tiene un único candidato:
        #   + poner número (candidato) en tablero
        #   + next
        celda = candidatoUnicoCelda(tablero)
        if celda:
            if debug:
                print(f"encuentra una celda con única posibildad:{celda}")
            tablero = confirmaCandidato(tablero, celda)
            continue

        # - ver si candidato único region, fila o columna
        #   + poner número (candidato) en tablero
        #   + next
        celda, candidato = celdaUnicaCandidato(tablero)
        if celda:
            if debug:
                print(f"encuentra una celda con candidato que no se repite:{celda, candidato}")
            tablero = confirmaCandidato(tablero, celda, candidato=candidato)
            continue

        # - ver si par candidatos en par de celdas región, fila o columna
        #   + quitar par como candidatos de otras celdas de la región/fila/columna
        #   + next
        celdas = dosCeldasDosValores(tablero)
        if celdas:
            if debug:
                print(f"encuentra 2 celdas con 2 valores: {celdas}")
            continue
        # - ver si trio candidatos en trio de celdas región, fila o columna
        #   + quitar trio como candidatos de otras celdas de la región/fila/columna
        #   + next
        print(f"No puedo seguir adelante: {tablero}")
        return None

debug = True
tablero = inicializaTablero()
tablero = confirmaCandidato(tablero, (0,6), 3)
tablero = confirmaCandidato(tablero, (0,7), 9)
tablero = confirmaCandidato(tablero, (1,2), 7)
tablero = confirmaCandidato(tablero, (1,4), 1)
tablero = confirmaCandidato(tablero, (2,2), 2)
tablero = confirmaCandidato(tablero, (2,3), 8)
tablero = confirmaCandidato(tablero, (2,5), 7)
tablero = confirmaCandidato(tablero, (3,1), 3)
tablero = confirmaCandidato(tablero, (3,3), 5)
tablero = confirmaCandidato(tablero, (3,8), 8)
tablero = confirmaCandidato(tablero, (4,1), 5)
tablero = confirmaCandidato(tablero, (4,4), 6)
tablero = confirmaCandidato(tablero, (4,6), 9)
tablero = confirmaCandidato(tablero, (5,3), 1)
tablero = confirmaCandidato(tablero, (5,4), 8)
tablero = confirmaCandidato(tablero, (5,5), 2)
tablero = confirmaCandidato(tablero, (5,8), 6)
tablero = confirmaCandidato(tablero, (6,0), 5)
tablero = confirmaCandidato(tablero, (6,4), 2)
tablero = confirmaCandidato(tablero, (7,1), 6)
tablero = confirmaCandidato(tablero, (7,2), 3)
tablero = confirmaCandidato(tablero, (8,2), 4)
tablero = confirmaCandidato(tablero, (8,6), 7)
tablero = confirmaCandidato(tablero, (8,7), 8)
print("Tablero inicial")
print(tablero)
print(principal(tablero))

# tablero[(0,3)] = [1, 2,3,4,5,6,7,8]
# tablero[(1,3)] = [1, 2,3,4,5,6,7,8]
# tablero[(2,3)] = [1, 2,3,4,5,6,7,8]
# tablero[(4,3)] = [1, 2,3,4,5,6,7,8]
# tablero[(5,3)] = [1, 2,3,4,5,6,7,8]
# tablero[(6,3)] = [1, 2,3,4,5,6,7,8]
# tablero[(7,3)] = [1, 2,3,4,5,6,7,8]
# tablero[(8,3)] = [1, 2,3,4,5,6,7,8]


# celda, candidato = celdaUnicaCandidatoCol(tablero)
# print(celda)
# print(candidato)

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


