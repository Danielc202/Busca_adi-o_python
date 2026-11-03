from collections import deque
import heapq

grafo_escola = {
    'LABTEC': [('201', 5), ('RUA1', 7), ('ATENDIMENTO', 10)],
    'ATENDIMENTO': [('LABTEC', 10), ('MK', 2), ('FINANCEIRO', 2), ('SECRETARIA', 2), ('RUA1', 5), ('SAIDA', 5)],
    'MK': [('ATENDIMENTO', 2)],
    'FINANCEIRO': [('ATENDIMENTO', 2), ('SECRETARIA', 2)],
    'SECRETARIA': [('ATENDIMENTO', 2), ('FINANCEIRO', 2)],
    'RUA1': [('LABTEC', 7), ('ATENDIMENTO', 5), ('CANTINA', 5), ('PATIO', 1)],
    'SAIDA': [('ATENDIMENTO', 5)],
    'CANTINA': [('RUA1', 5), ('RUA2', 5), ('CANTINA2', 5)],
    'CANTINA2': [('RUA2', 5), ('CANTINA', 5)],
    'RUA2': [('CANTINA', 5), ('CANTINA2', 5), ('RUA3', 5), ('RUA4', 12), ('PATIO', 1), ('BM', 5)],
    'RUA3': [('RUA2', 5), ('RUA4', 10), ('BIBLIOTECA', 10), ('PATIO', 1)],
    'RUA4': [('RUA2', 12), ('RUA3', 10), ('BIBLIOTECA', 5), ('PATIO', 1)],
    'PATIO': [('RUA1', 1), ('RUA2', 1), ('RUA3', 1), ('RUA4', 1), ('PD1', 1), ('PD2', 1), ('P108', 1)],
    'PD1': [('PATIO', 1), ('PD2', 1)],
    'PD2': [('PATIO', 1), ('PD1', 1)],
    'P108': [('PATIO', 1), ('IDIOMAS', 5), ('208', 7), ('209', 2), ('210', 5), ('PD3', 7), ('207', 12), ('206', 14), ('SAIDA2', 17)],
    'IDIOMAS': [('P108', 5), ('208', 2)],
    '208': [('P108', 7), ('IDIOMAS', 2), ('209', 5)],
    '209': [('P108', 2), ('208', 5), ('210', 2)],
    '210': [('P108', 5), ('209', 2)],
    'PD3': [('P108', 7), ('207', 5)],
    '207': [('P108', 12), ('PD3', 5), ('206', 2)],
    '206': [('P108', 14), ('207', 2), ('SAIDA2', 5)],
    'SAIDA2': [('P108', 17), ('206', 5)],
    '201': [('LABTEC', 5), ('202', 5)],
    '202': [('201', 5), ('203', 5)],
    '203': [('202', 5), ('BF', 5)],
    'BF': [('203', 5), ('BM', 5)],
    'BM': [('RUA2', 5), ('BF', 5), ('204', 5), ('CORREDORBIBLIOTECA', 2)],
    'CORREDORBIBLIOTECA': [('BM', 2), ('204', 3), ('PSE', 1), ('INTEGRAL', 1), ('SECRETARIA2', 1), ('DIRETOR', 1), ('SALALID', 1), ('PROFESSORES', 1), ('BIBLIOTECA', 1)],
    'PSE': [('CORREDORBIBLIOTECA', 1), ('SECRETARIA2', 5)],
    'INTEGRAL': [('CORREDORBIBLIOTECA', 1), ('DIRETOR', 5)],
    'SECRETARIA2': [('CORREDORBIBLIOTECA', 1), ('PSE', 5), ('SALALID', 5)],
    'DIRETOR': [('CORREDORBIBLIOTECA', 1), ('INTEGRAL', 5), ('PROFESSORES', 5)],
    'SALALID': [('CORREDORBIBLIOTECA', 1), ('SECRETARIA2', 5), ('BIBLIOTECA', 5)],
    'PROFESSORES': [('CORREDORBIBLIOTECA', 1), ('DIRETOR', 5), ('BIBLIOTECA', 5)],
    'BIBLIOTECA': [('RUA3', 10), ('RUA4', 5), ('CORREDORBIBLIOTECA', 1), ('SALALID', 5), ('PROFESSORES', 5), ('TI', 5), ('REUNIAO1', 5), ('REUNIAO2', 5)],
    'TI': [('BIBLIOTECA', 5)],
    'REUNIAO1': [('BIBLIOTECA', 5)],
    'REUNIAO2': [('BIBLIOTECA', 5)],
    '204': [('BM', 5), ('CORREDORBIBLIOTECA', 3), ('COPA', 5)],
    'COPA': [('204', 5), ('205', 5)],
    '205': [('COPA', 5), ('102', 5)],
    '102': [('205', 5), ('MASSAGEM', 5), ('PD4', 5)],
    'MASSAGEM': [('102', 5), ('PD4', 5)],
    'PD4': [('102', 5), ('MASSAGEM', 5)],
}


def calcular_custo(grafo, caminho):
    if not caminho or len(caminho) < 2:
        return 0
    custo = 0
    for i in range(len(caminho) - 1):
        orig = caminho[i]
        dest = caminho[i + 1]
        peso_aresta = None
        for vizinho, peso in grafo.get(orig, []):
            if vizinho == dest:
                peso_aresta = peso
                break
        if peso_aresta is None:
            return float("inf")
        custo += peso_aresta
    return custo


def bfs(grafo, origem, destino):
    origem = origem.upper()
    destino = destino.upper()

    if origem not in grafo or destino not in grafo:
        return [], 0, 0
    if origem == destino:
        return [origem], 0, 1

    visitados = {origem}
    veio_de = {}
    fila = deque([origem])

    while fila:
        atual = fila.popleft()

        if atual == destino:
            break

        for vizinho, _ in grafo.get(atual, []):
            if vizinho not in visitados:
                visitados.add(vizinho)
                veio_de[vizinho] = atual
                fila.append(vizinho)

    if destino not in veio_de and origem != destino:
        return [], 0, len(visitados)

    caminho = [destino]
    while caminho[-1] != origem:
        caminho.append(veio_de[caminho[-1]])
    caminho.reverse()

    custo = calcular_custo(grafo, caminho)
    return caminho, custo, len(visitados)


def dfs(grafo, origem, destino):
    origem = origem.upper()
    destino = destino.upper()

    if origem not in grafo or destino not in grafo:
        return [], 0, 0
    if origem == destino:
        return [origem], 0, 1

    visitados = set()
    caminho = []

    def buscar(atual):
        visitados.add(atual)
        caminho.append(atual)

        if atual == destino:
            return True

        for vizinho, _ in grafo.get(atual, []):
            if vizinho not in visitados:
                if buscar(vizinho):
                    return True

        caminho.pop()
        return False

    achou = buscar(origem)
    if not achou:
        return [], 0, len(visitados)

    custo = calcular_custo(grafo, caminho)
    return list(caminho), custo, len(visitados)


def gulosa(grafo, origem, destino):
    origem = origem.upper()
    destino = destino.upper()

    if origem not in grafo or destino not in grafo:
        return [], 0, 0
    if origem == destino:
        return [origem], 0, 1

    visitados = set()
    caminho = []

    def buscar(atual):
        visitados.add(atual)
        caminho.append(atual)

        if atual == destino:
            return True

        vizinhos = [(peso, viz) for viz, peso in grafo.get(atual, []) if viz not in visitados]
        vizinhos.sort(key=lambda x: x[0])

        for _, vizinho in vizinhos:
            if vizinho not in visitados:
                if buscar(vizinho):
                    return True

        caminho.pop()
        return False

    achou = buscar(origem)
    if not achou:
        return [], 0, len(visitados)

    custo = calcular_custo(grafo, caminho)
    return list(caminho), custo, len(visitados)


def dijkstra(grafo, origem, destino):
    origem = origem.upper()
    destino = destino.upper()

    if origem not in grafo or destino not in grafo:
        return [], 0, 0
    if origem == destino:
        return [origem], 0, 1

    distancia = {p: float("inf") for p in grafo}
    anterior = {}
    distancia[origem] = 0
    fila = [(0, origem)]
    finalizadas = set()

    while fila:
        d, atual = heapq.heappop(fila)

        if atual in finalizadas:
            continue
        finalizadas.add(atual)

        if atual == destino:
            break

        for vizinho, peso in grafo.get(atual, []):
            if vizinho not in finalizadas:
                nova_dist = d + peso
                if nova_dist < distancia.get(vizinho, float("inf")):
                    distancia[vizinho] = nova_dist
                    anterior[vizinho] = atual
                    heapq.heappush(fila, (nova_dist, vizinho))

    if distancia.get(destino, float("inf")) == float("inf"):
        return [], 0, len(finalizadas)

    caminho = []
    atual = destino
    while atual is not None:
        caminho.append(atual)
        atual = anterior.get(atual)
    caminho.reverse()

    return caminho, distancia[destino], len(finalizadas)


if __name__ == "__main__":
    origem_teste = "LABTEC"
    destino_teste = "CANTINA"

    print("=== Testando os 4 Algoritmos com o grafo_escola ===")
    print(f"Origem: {origem_teste} -> Destino: {destino_teste}\n")

    for nome, func in [("BFS", bfs), ("DFS", dfs), ("Gulosa", gulosa), ("Dijkstra", dijkstra)]:
        cam, cus, vis = func(grafo_escola, origem_teste, destino_teste)
        print(f"[{nome}]")
        print(f"  Caminho: {' -> '.join(cam) if cam else 'Nao encontrado'}")
        print(f"  Custo: {cus} passos")
        print(f"  Portas visitadas: {vis}\n")
