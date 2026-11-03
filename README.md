# Busca em Grafos - Prédio da Escola

Trabalho prático sobre algoritmos de busca em grafos. Mapeamos as salas, corredores e pontos de interesse do prédio em formato de grafo e implementamos quatro algoritmos de busca: **BFS**, **DFS**, **Busca Gulosa** e **Dijkstra**. Para testar as rotas, também criamos uma API simples com FastAPI.

---

## 1. Unidade de Medida

A unidade escolhida para os pesos das arestas foi **passos**. 

Cada valor representa a quantidade aproximada de passos necessários para ir de uma porta até a outra. Todas as respostas da API e relatórios retornam com `"unidade": "passos"`.

---

## 2. Organização dos Arquivos

* `arestas.txt`: arquivo texto onde cada linha representa uma ligação entre duas portas (`PORTA1 PORTA2 PESO`). Todas em maiúsculas, sem acento e sem espaço. Cada aresta aparece uma única vez.
* `grafo.py`: lê o `arestas.txt` e monta o grafo nos dois sentidos (já que é possível ir e voltar). Se rodar direto no terminal, ele faz uma verificação via BFS para garantir que todas as portas estão conectadas a partir do `LABTEC`.
* `buscas.py`: contém o dicionário original `grafo_escola` e as funções dos 4 algoritmos (`bfs`, `dfs`, `gulosa` e `dijkstra`). Todas seguem o mesmo padrão e devolvem: `caminho, custo, visitados`.
* `api.py`: rotas em FastAPI para consultar as portas, vizinhos e rotas pelo navegador.
* `como_rodar.txt`: instruções rápidas de como rodar a API e os testes no computador.

---

## 3. Os Algoritmos Utilizados

Todas as funções de busca recebem `(grafo, origem, destino)` e devolvem:
- `caminho`: lista com a sequência de portas percorrida;
- `custo`: soma dos passos do caminho;
- `visitados`: total de nós que o algoritmo examinou até achar o destino.

Resumo de como cada um funciona:
1. **BFS (Largura):** usa fila (`deque`). Ela vai expandindo nível por nível e acha o caminho que passa pelo menor número de portas, sem se preocupar com os pesos das arestas.
2. **DFS (Profundidade):** vai a fundo no primeiro vizinho que encontra até bater numa ponta solta ou achar o destino, guardando os visitados para não entrar em loop.
3. **Busca Gulosa:** em cada porta onde está, escolhe sempre o vizinho que tem a aresta de menor peso (mais perto). Se cair num beco sem saída, volta um passo para tentar o próximo menor.
4. **Dijkstra:** usa fila de prioridade (`heapq`) para garantir sempre o caminho de menor custo total acumulado (menor soma de passos).

---

## 4. Comparação Obrigatória: BFS x Dijkstra

O enunciado pedia para encontrar um par de portas no grafo onde a BFS e o Dijkstra entregassem caminhos diferentes e explicar o motivo.

### Par escolhido: de `LABTEC` até `BF`

* **Pela BFS:**
  - Caminho: `LABTEC -> 201 -> 202 -> 203 -> BF`
  - Número de portas: 4
  - Custo total: 20 passos
  - Nós visitados: 30

* **Pelo Dijkstra:**
  - Caminho: `LABTEC -> RUA1 -> PATIO -> RUA2 -> BM -> BF`
  - Número de portas: 5
  - Custo total: 19 passos
  - Nós visitados: 35

### Por que os caminhos são diferentes?

A diferença acontece por causa da forma como cada algoritmo toma suas decisões:

1. A **BFS** conta apenas a quantidade de portas (arestas). Para ela, tanto faz se uma ligação tem 1 passo ou 50 passos. Como ela achou o `BF` com apenas 4 portas atravessando o corredor das salas (passando por 201, 202 e 203), ela encerra a busca e devolve essa rota. O custo acabou sendo $5 + 5 + 5 + 5 = 20\text{ passos}$.

2. O **Dijkstra** leva em consideração a soma real dos passos. Ele encontrou uma rota passando pelo **Pátio** que tem 5 portas (uma a mais do que na BFS). Só que as passagens `RUA1 -> PATIO` e `PATIO -> RUA2` são muito curtas (custo de apenas 1 passo cada). Somando tudo ($7 + 1 + 1 + 5 + 5$), o custo total deu **19 passos**.

Como 19 é menor que 20, o Dijkstra escolheu o caminho que passa por mais portas, mas exige menos passos de caminhada.

*(Outro exemplo interessante é de `LABTEC` até `RUA2`: a BFS vai por `CANTINA` custando 17 passos, enquanto o Dijkstra vai por `PATIO` custando apenas 9 passos).*

---

## 5. Como Rodar

### Pré-requisitos
Ter o Python instalado e instalar as bibliotecas da API:

```bash
pip install fastapi uvicorn
```

### 1. Testar se o grafo está correto
Para ler o `arestas.txt` e ver se todas as 46 portas são alcançadas a partir do `LABTEC`:

```bash
python grafo.py
```

### 2. Testar os algoritmos no terminal
Para rodar os testes das buscas no terminal e ver os caminhos impressos:

```bash
python buscas.py
```

### 3. Subir a API
Para iniciar o servidor local:

```bash
uvicorn api:app --reload
```
*(ou `python -m uvicorn api:app --reload` caso o terminal não reconheça o uvicorn direto).*

Depois é só abrir no navegador:
* Documentação interativa (Swagger): **http://127.0.0.1:8000/docs**

---

## 6. Endpoints Disponíveis na API

- **`GET /portas`**: lista todas as portas cadastradas no prédio em ordem alfabética.
- **`GET /vizinhos/{porta}`**: mostra quem está conectado com a porta informada e o peso de cada ligação. Se colocar uma porta que não existe, devolve erro 404.
- **`GET /rota?origem=LABTEC&destino=CANTINA&algoritmo=dijkstra`**: calcula a rota entre duas portas com o algoritmo escolhido (`bfs`, `dfs`, `gulosa` ou `dijkstra`).
- **`GET /comparar?origem=LABTEC&destino=BF`**: roda os 4 algoritmos juntos para o mesmo ponto de saída e chegada, permitindo comparar caminho, custo e visitados de cada um lado a lado.
"# Buscas_Algoritimos_2026" 
