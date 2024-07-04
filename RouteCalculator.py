import heapq

## Definimos la clase Node que representa un nodo en el mapa con sus coordenadas, costos y nodo padre
class Node():
    def __init__(self, x, y, costo=0, heuristica=0):
        self.x = x
        self.y = y
        self.costo = costo
        self.heuristica = heuristica
        self.costo_total = costo + heuristica
        self.padre = None  # Nodo padre para reconstruir el camino

    ## Método para comparar nodos basado en el costo total, necesario para la cola de prioridad
    def __lt__(self, other):
        return self.costo_total < other.costo_total

## Calcula la distancia Manhattan entre dos nodos a y b
def heuristica(a, b):
    return abs(a.x - a.y) + abs(b.x - b.y)

## Función que implementa el algoritmo A* para encontrar el camino más corto
def busqueda_a_star(mapa, inicio, final):
    nodo_inicial = Node(inicio[0], inicio[1])
    nodo_final = Node(final[0], final[1])
    lista_abierta = []
    heapq.heappush(lista_abierta, nodo_inicial)  # Añadimos el nodo inicial a la lista abierta
    lista_cerrada = set()
    g_costo = {(nodo_inicial.x, nodo_inicial.y): 0}  # Costos acumulados desde el nodo inicial

    while lista_abierta:
        nodo_actual = heapq.heappop(lista_abierta)  # Nodo con menor costo total
        lista_cerrada.add((nodo_actual.x, nodo_actual.y))  # Añadimos a la lista cerrada

        if (nodo_actual.x, nodo_actual.y) == (nodo_final.x, nodo_final.y):  # Si hemos llegado al objetivo
            path = []
            while nodo_actual:
                path.append((nodo_actual.x, nodo_actual.y))  # Reconstruimos el camino
                nodo_actual = nodo_actual.padre
            return path[::-1]  # Devolvemos el camino en el orden correcto
        
        # Definimos los nodos vecinos (arriba, abajo, izquierda, derecha)
        vecinos = [
            (nodo_actual.x - 1, nodo_actual.y),
            (nodo_actual.x + 1, nodo_actual.y),
            (nodo_actual.x, nodo_actual.y - 1),
            (nodo_actual.x, nodo_actual.y + 1)
        ]

        for vx, vy in vecinos:
            if (0 <= vx < len(mapa)) and (0 <= vy < len(mapa[0])) and (vx, vy) not in lista_cerrada:
                if mapa[vx][vy] == 1:  # Pared
                    continue
                elif mapa[vx][vy] == 0:
                    new_costo = g_costo[(nodo_actual.x, nodo_actual.y)] + 1
                elif mapa[vx][vy] == 2:  # Agua
                    new_costo = g_costo[(nodo_actual.x, nodo_actual.y)] + 5
                elif mapa[vx][vy] == 3:  # Árbol caído
                    new_costo = g_costo[(nodo_actual.x, nodo_actual.y)] + 10

                # Si no se ha visitado antes o se encuentra un camino más barato
                if (vx, vy) not in g_costo or new_costo < g_costo[(vx, vy)]:
                    nodo_vecino = Node(vx, vy, new_costo, heuristica(Node(vx, vy), nodo_final))
                    nodo_vecino.padre = nodo_actual  # Establecemos el nodo actual como padre
                    g_costo[(vx, vy)] = new_costo  # Actualizamos el costo
                    heapq.heappush(lista_abierta, nodo_vecino)  # Añadimos el vecino a la lista abierta

    return []  # Si no se encuentra un camino, devolvemos una lista vacía

## Función para imprimir el mapa y el camino encontrado
def imprimir_mapa(mapa, path=None):
    if path is None:
        path = []

    for i in range(len(mapa)):
        for j in range(len(mapa[0])):
            if (i, j) in path:
                print('*', end=' ')  # Representamos el camino con '0'
            elif mapa[i][j] == 0:
                print('.', end=' ')  # Representamos celdas vacías con '.'
            elif mapa[i][j] == 1:
                print('|', end=' ')  # Representamos paredes con 'X'
            elif mapa[i][j] == 2:
                print('~', end=' ')  # Representamos agua con '~'
            elif mapa[i][j] == 3:
                print('\\', end=' ')  # Representamos árboles caídos con '\\'
        print()
    print()

## Función principal para ejecutar el programa
def main():
    mapa = [
        [0, 0, 0, 0, 0],
        [0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ]

    while True:
        print("Mapa Actual: ")
        imprimir_mapa(mapa)

        try:
            inicio_x = int(input("Ingrese la coordenada X del punto de inicio: "))
            inicio_y = int(input("Ingrese la coordenada Y del punto de inicio: "))
            inicio = (inicio_x, inicio_y)

            fin_x = int(input("Ingrese la coordenada X del punto de fin: "))
            fin_y = int(input("Ingrese la coordenada Y del punto de fin: "))
            fin = (fin_x, fin_y)

            # Verificamos que las coordenadas estén dentro del rango del mapa
            if not (0 <= inicio[0] < len(mapa)) or not (0 <= inicio[1] < len(mapa[0])) or not (0 <= fin[0] < len(mapa)) or not (0 <= fin[1] < len(mapa[0])):
                raise ValueError("Las coordenadas están fuera del rango del mapa.")
        except ValueError as e:
            print(f"Error de coordenadas: {e}. Por favor, ingrese nuevamente.")
            continue

        # Ejecutamos la búsqueda A* y obtenemos el camino
        path = busqueda_a_star(mapa, inicio, fin)
        if path:
            print("Ruta encontrada: ")
            imprimir_mapa(mapa, path)
        else:
            print("No se encontró ninguna ruta válida.")

        # Preguntamos si el usuario quiere agregar un obstáculo
        agregar_obstaculo = input("¿Desea agregar algún obstáculo? (s/n): ").strip().lower()
        if agregar_obstaculo == 's':
            try:
                obstaculo_x = int(input("Ingrese la coordenada X del obstáculo: "))
                obstaculo_y = int(input("Ingrese la coordenada Y del obstáculo: "))
                obstaculo = (obstaculo_x, obstaculo_y)
                
                tipo_obstaculo = input("Ingrese el tipo de obstáculo (pared=1, agua=2, árbol=3): ").strip()
                if tipo_obstaculo not in ['1', '2', '3']:
                    print("Tipo de obstáculo inválido. Por favor, ingrese nuevamente.")
                    continue

                # Verificamos que las coordenadas del obstáculo estén dentro del rango del mapa
                if (0 <= obstaculo[0] < len(mapa)) and (0 <= obstaculo[1] < len(mapa[0])):
                    mapa[obstaculo[0]][obstaculo[1]] = int(tipo_obstaculo)
                else:
                    print("Las coordenadas del obstáculo están fuera del rango del mapa.")
            except ValueError:
                print("Formato de coordenadas inválido. Por favor, ingrese otra vez.")
                continue

        # Preguntamos si el usuario quiere buscar otra ruta
        continuar = input("¿Desea buscar otra ruta? (s/n): ").strip().lower()
        if continuar != 's':
            break

if __name__ == "__main__":
    main()
