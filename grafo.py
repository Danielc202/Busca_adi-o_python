from collections import deque


def carregar_grafo(caminho="arestas.txt"):
    grafo = {}
    with open(caminho, encoding="utf-8") as arq:
        for linha in arq:
            linha = linha.strip()
            if not linha:
                continue
            partes = linha.split()
            if len(partes) != 3:
                continue
            a, b, peso = partes
            peso = int(peso)
            a = a.upper()
            b = b.upper()
            grafo.setdefault(a, []).append((b, peso))
            grafo.setdefault(b, []).append((a, peso))
    return grafo


def contar_arestas_unicas(grafo):
    arestas = set()
    for u, vizinhos in grafo.items():
        for v, _ in vizinhos:
            arestas.add(tuple(sorted([u, v])))
    return len(arestas)


def testar_alcance_bfs(grafo, inicio="LABTEC"):
    inicio = inicio.upper()
    if inicio not in grafo:
        return False, set(), set(grafo.keys())

    visitados = {inicio}
    fila = deque([inicio])

    while fila:
        atual = fila.popleft()
        for vizinho, _ in grafo.get(atual, []):
            if vizinho not in visitados:
                visitados.add(vizinho)
                fila.append(vizinho)

    todas_portas = set(grafo.keys())
    nao_alcancadas = todas_portas - visitados
    completo = (len(nao_alcancadas) == 0)

    return completo, visitados, nao_alcancadas


if __name__ == "__main__":
    grafo = carregar_grafo("arestas.txt")
    total_portas = len(grafo)
    total_arestas = contar_arestas_unicas(grafo)

    print("=== Conferencia do Grafo ===")
    print(f"Total de portas: {total_portas}")
    print(f"Total de arestas: {total_arestas}")

    alcance_ok, visitadas, nao_visitadas = testar_alcance_bfs(grafo, "LABTEC")
    print(f"Portas alcancadas saindo de LABTEC: {len(visitadas)}/{total_portas}")

    if alcance_ok:
        print("Tudo certo! Todas as portas foram alcancadas.")
    else:
        print(f"Atencao, portas nao alcancadas: {nao_visitadas}")
