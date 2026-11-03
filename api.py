from fastapi import FastAPI, HTTPException, Query
from grafo import carregar_grafo
from buscas import bfs, dfs, gulosa, dijkstra

app = FastAPI(
    title="Rotas no Prédio da Escola",
    description="API para consultar portas, vizinhos e caminhos usando BFS, DFS, Gulosa e Dijkstra."
)

grafo = carregar_grafo("arestas.txt")

ALGORITMOS = {
    "bfs": bfs,
    "dfs": dfs,
    "gulosa": gulosa,
    "dijkstra": dijkstra
}


@app.get("/portas", summary="Lista todas as portas do prédio")
def listar_portas():
    return sorted(list(grafo.keys()))


@app.get("/vizinhos/{porta}", summary="Vizinhos de uma porta")
def obter_vizinhos(porta: str):
    porta_norm = porta.upper().strip()
    if porta_norm not in grafo:
        raise HTTPException(status_code=404, detail="Porta não encontrada")

    return [{"porta": p, "peso": w} for p, w in grafo[porta_norm]]


@app.get("/rota", summary="Busca rota entre duas portas")
def buscar_rota(
    origem: str = Query(..., description="Porta de partida (ex: LABTEC)"),
    destino: str = Query(..., description="Porta de chegada (ex: CANTINA)"),
    algoritmo: str = Query("dijkstra", description="Algoritmo: bfs, dfs, gulosa ou dijkstra")
):
    origem_norm = origem.upper().strip()
    destino_norm = destino.upper().strip()
    algo_norm = algoritmo.lower().strip()

    if origem_norm not in grafo:
        raise HTTPException(status_code=404, detail=f"Porta de origem '{origem}' não encontrada")

    if destino_norm not in grafo:
        raise HTTPException(status_code=404, detail=f"Porta de destino '{destino}' não encontrada")

    if algo_norm not in ALGORITMOS:
        raise HTTPException(
            status_code=400,
            detail=f"Algoritmo '{algoritmo}' inválido. Opções disponíveis: {', '.join(ALGORITMOS.keys())}"
        )

    funcao_busca = ALGORITMOS[algo_norm]
    caminho, custo, visitados = funcao_busca(grafo, origem_norm, destino_norm)

    return {
        "algoritmo": algo_norm,
        "caminho": caminho,
        "custo": custo,
        "unidade": "passos",
        "visitados": visitados
    }


@app.get("/comparar", summary="Compara os 4 algoritmos lado a lado")
def comparar_algoritmos(
    origem: str = Query(..., description="Porta de partida (ex: LABTEC)"),
    destino: str = Query(..., description="Porta de chegada (ex: CANTINA)")
):
    origem_norm = origem.upper().strip()
    destino_norm = destino.upper().strip()

    if origem_norm not in grafo:
        raise HTTPException(status_code=404, detail=f"Porta de origem '{origem}' não encontrada")

    if destino_norm not in grafo:
        raise HTTPException(status_code=404, detail=f"Porta de destino '{destino}' não encontrada")

    comparacao = {}
    for nome, func in ALGORITMOS.items():
        caminho, custo, visitados = func(grafo, origem_norm, destino_norm)
        comparacao[nome] = {
            "caminho": caminho,
            "custo": custo,
            "visitados": visitados
        }

    return {
        "origem": origem_norm,
        "destino": destino_norm,
        "unidade": "passos",
        "comparacao": comparacao
    }
