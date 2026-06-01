import sys
import heapq
from collections import deque

# Aumentar o limite de recursão caso seja testado com grafos muito grandes
sys.setrecursionlimit(200000)

# DADOS GLOBAIS (GRAFOS)
grafo_produtos = {
    "brush": ["nail_polish"],
    "nail_polish": ["brush", "eye_shadow", "nails"],
    "eye_shadow": ["eye_glasses", "nail_polish"],
    "eye_glasses": ["eye_shadow"],
    "nails": ["hammer", "nail_polish", "needles", "pins"],
    "pins": ["nails", "needles"],
    "needles": ["nails", "pins"],
    "hammer": ["drill", "nails", "saw"],
    "drill": ["hammer"],
    "saw": ["hammer", "knife"],
    "knife": ["fork", "saw", "spoon"],
    "fork": ["knife"],
    "spoon": ["knife"],
}
for k in grafo_produtos:
    grafo_produtos[k].sort()

grafo_social = {
    "Idris": ["Kamil", "Talia"],
    "Kamil": ["Idris", "Lina"],
    "Talia": ["Idris", "Ken"],
    "Lina": ["Kamil", "Sasha"],
    "Sasha": ["Lina", "Marco"],
    "Marco": ["Ken", "Sasha"],
    "Ken": ["Marco", "Talia"],
}

grafo_direcionado = {
    "Inicio": ["A", "B"],
    "A": ["C"],
    "B": ["C", "F"],
    "C": ["D"],
    "D": ["E"],
    "F": ["E"],
    "E": [],
}

grafo_porto = {
    "Berco_A": {"Patio_1": 4, "Patio_2": 7},
    "Berco_B": {"Patio_2": 3, "Patio_3": 6},
    "Patio_1": {"Berco_A": 4, "Patio_2": 2, "Alfandega": 8},
    "Patio_2": {"Berco_A": 7, "Berco_B": 3, "Patio_1": 2, "Patio_3": 2, "Alfandega": 5},
    "Patio_3": {"Berco_B": 6, "Patio_2": 2, "Centro_Logistico": 4},
    "Alfandega": {"Patio_1": 8, "Patio_2": 5, "Centro_Logistico": 3},
    "Centro_Logistico": {"Patio_3": 4, "Alfandega": 3},
}

# --- Exercício 1: Formação de times a partir de amizades ---
def contar_times(n, amizades):
    grafo = {i: [] for i in range(1, n + 1)}
    for u, v in amizades:
        grafo[u].append(v)
        grafo[v].append(u)

    visitados = set()
    times = 0

    def dfs(nodo):
        pilha = [nodo]
        while pilha:
            atual = pilha.pop()
            for vizinho in grafo[atual]:
                if vizinho not in visitados:
                    visitados.add(vizinho)
                    pilha.append(vizinho)

    for i in range(1, n + 1):
        if i not in visitados:
            visitados.add(i)
            dfs(i)
            times += 1

    return times


# --- Exercício 2: Validação de passeios em uma rede de túneis ---
def contar_passeios_validos(S, tuneis, passeios):
    grafo = {i: [] for i in range(1, S + 1)}
    for x, y in tuneis:
        grafo[x].append(y)
        grafo[y].append(x)

    def tem_caminho_bfs(origem, destino):
        if origem == destino:
            return True
        visitados = set([origem])
        fila = deque([origem])
        while fila:
            atual = fila.popleft()
            if atual == destino:
                return True
            for vizinho in grafo[atual]:
                if vizinho not in visitados:
                    visitados.add(vizinho)
                    fila.append(vizinho)
        return False

    validos = 0
    for passeio in passeios:
        if len(passeio) <= 1:
            validos += 1
            continue
        passeio_possivel = True
        for i in range(len(passeio) - 1):
            if not tem_caminho_bfs(passeio[i], passeio[i + 1]):
                passeio_possivel = False
                break
        if passeio_possivel:
            validos += 1
    return validos


# --- Exercício 3: Conectividade dinâmica entre ilhas ---
def conectividade_dinamica(n, operacoes):
    grafo = {i: [] for i in range(1, n + 1)}
    resultados = []

    for tipo, a, b in operacoes:
        if tipo == 1:
            grafo[a].append(b)
            grafo[b].append(a)
        elif tipo == 0:
            if a == b:
                resultados.append(1)
                continue
            visitados = set([a])
            fila = deque([a])
            encontrou = False
            while fila and not encontrou:
                atual = fila.popleft()
                if atual == b:
                    encontrou = True
                    break
                for vizinho in grafo[atual]:
                    if vizinho not in visitados:
                        visitados.add(vizinho)
                        fila.append(vizinho)
            resultados.append(1 if encontrou else 0)

    return resultados


# --- Exercício 4: Exploração de recomendações com DFS ---
def dfs_produtos(origem):
    visitados = set()
    ordem = []

    def dfs_rec(nodo):
        if nodo not in visitados:
            visitados.add(nodo)
            ordem.append(nodo)
            for vizinho in grafo_produtos[nodo]:
                dfs_rec(vizinho)

    dfs_rec(origem)
    return ordem


# --- Exercício 5: Exploração de recomendações com BFS ---
def bfs_produtos(origem):
    visitados = set([origem])
    fila = deque([origem])
    ordem = []
    while fila:
        atual = fila.popleft()
        ordem.append(atual)
        for vizinho in grafo_produtos[atual]:
            if vizinho not in visitados:
                visitados.add(vizinho)
                fila.append(vizinho)
    return ordem


# --- Exercício 6: Menor caminho em rede social ---
def menor_caminho_bfs(origem, destino):
    fila = deque([origem])
    pred = {origem: None}

    while fila:
        atual = fila.popleft()
        if atual == destino:
            break
        for vizinho in grafo_social[atual]:
            if vizinho not in pred:
                pred[vizinho] = atual
                fila.append(vizinho)

    caminho = []
    passo = destino
    while passo:
        caminho.append(passo)
        passo = pred[passo]

    return caminho[::-1], len(caminho) - 1


# --- Exercício 7: Travessia em grafo direcionado ---
def travessia_dir(origem):
    visitados_dfs = []
    pilha = [origem]
    while pilha:
        atual = pilha.pop()
        if atual not in visitados_dfs:
            visitados_dfs.append(atual)
            for vizinho in reversed(grafo_direcionado[atual]):
                pilha.append(vizinho)

    visitados_bfs = []
    fila = deque([origem])
    set_bfs = set([origem])
    while fila:
        atual = fila.popleft()
        visitados_bfs.append(atual)
        for vizinho in grafo_direcionado[atual]:
            if vizinho not in set_bfs:
                set_bfs.add(vizinho)
                fila.append(vizinho)

    return visitados_dfs, visitados_bfs


# --- Exercício 8: Viabilidade operacional ---
def bfs_porto_alcançaveis(origem):
    fila = deque([origem])
    visitados = set([origem])
    while fila:
        atual = fila.popleft()
        for vizinho in grafo_porto[atual].keys():
            if vizinho not in visitados:
                visitados.add(vizinho)
                fila.append(vizinho)
    return list(visitados)


def bfs_porto_caminho(origem, destino):
    fila = deque([origem])
    pred = {origem: None}
    while fila:
        atual = fila.popleft()
        if atual == destino:
            break
        for vizinho in grafo_porto[atual].keys():
            if vizinho not in pred:
                pred[vizinho] = atual
                fila.append(vizinho)

    caminho, passo = [], destino
    while passo:
        caminho.append(passo)
        passo = pred[passo]
    caminho = caminho[::-1]

    custo_total = sum(
        grafo_porto[caminho[i]][caminho[i + 1]] for i in range(len(caminho) - 1)
    )
    return caminho, custo_total


# --- Exercício 9: Menor custo com Dijkstra ---
def dijkstra_distancias(origem):
    distancias = {nodo: float("inf") for nodo in grafo_porto}
    distancias[origem] = 0
    pred = {origem: None}
    pq = [(0, origem)]

    while pq:
        dist_atual, atual = heapq.heappop(pq)

        if dist_atual > distancias[atual]:
            continue

        for vizinho, peso in grafo_porto[atual].items():
            distancia = dist_atual + peso
            if distancia < distancias[vizinho]:
                distancias[vizinho] = distancia
                pred[vizinho] = atual
                heapq.heappush(pq, (distancia, vizinho))

    return distancias, pred


# --- Exercício 10: Reconstrução de rota ótima ---
def dijkstra_reconstrucao(origem, destino):
    distancias = {nodo: float("inf") for nodo in grafo_porto}
    distancias[origem] = 0
    pred = {origem: None}
    pq = [(0, origem)]

    while pq:
        dist_atual, atual = heapq.heappop(pq)
        if dist_atual > distancias[atual]:
            continue
        for vizinho, peso in grafo_porto[atual].items():
            distancia = dist_atual + peso
            if distancia < distancias[vizinho]:
                distancias[vizinho] = distancia
                pred[vizinho] = atual
                heapq.heappush(pq, (distancia, vizinho))

    caminho = []
    passo = destino
    while passo:
        caminho.append(passo)
        passo = pred[passo]

    return caminho[::-1]


# --- Exercício 11: Impacto dos pesos na escolha de rotas ---
def bfs_simples(origem, destino):
    fila = deque([origem])
    pred = {origem: None}
    while fila:
        atual = fila.popleft()
        if atual == destino:
            break
        for vizinho in grafo_porto[atual].keys():
            if vizinho not in pred:
                pred[vizinho] = atual
                fila.append(vizinho)
    cam = []
    p = destino
    while p:
        cam.append(p)
        p = pred[p]
    return cam[::-1]


def dijkstra_simples(origem, destino):
    distancias = {nodo: float("inf") for nodo in grafo_porto}
    distancias[origem] = 0
    pred = {origem: None}
    pq = [(0, origem)]
    while pq:
        dist_atual, atual = heapq.heappop(pq)
        if dist_atual > distancias[atual]:
            continue
        for vizinho, peso in grafo_porto[atual].items():
            d = dist_atual + peso
            if d < distancias[vizinho]:
                distancias[vizinho] = d
                pred[vizinho] = atual
                heapq.heappush(pq, (d, vizinho))
    cam = []
    p = destino
    while p:
        cam.append(p)
        p = pred[p]
    return cam[::-1], distancias[destino]


# --- Exercício 12: Análise de rotas na rede logística ---
def analise_ordem_visita(origem):
    visitados_dfs = []
    pilha = [origem]
    while pilha:
        atual = pilha.pop()
        if atual not in visitados_dfs:
            visitados_dfs.append(atual)
            for vizinho in reversed(list(grafo_porto[atual].keys())):
                pilha.append(vizinho)

    visitados_bfs = []
    fila = deque([origem])
    set_bfs = set([origem])
    while fila:
        atual = fila.popleft()
        visitados_bfs.append(atual)
        for vizinho in grafo_porto[atual].keys():
            if vizinho not in set_bfs:
                set_bfs.add(vizinho)
                fila.append(vizinho)

    return visitados_dfs, visitados_bfs


def dijkstra_todas_distancias(origem):
    distancias = {nodo: float("inf") for nodo in grafo_porto}
    distancias[origem] = 0
    pq = [(0, origem)]
    while pq:
        dist_atual, atual = heapq.heappop(pq)
        if dist_atual > distancias[atual]:
            continue
        for vizinho, peso in grafo_porto[atual].items():
            d = dist_atual + peso
            if d < distancias[vizinho]:
                distancias[vizinho] = d
                heapq.heappush(pq, (d, vizinho))
    return distancias


# BLOCO PRINCIPAL DE EXECUÇÃO
if __name__ == "__main__":
    print("=" * 60)
    print(" INICIANDO TESTES DO TP DE GRAFOS ")
    print("=" * 60)

    # Ex 1
    print("\n[EXERCÍCIO 1]")
    print(f"Total de times independentes: {contar_times(5, [(1, 2), (3, 4), (4, 5)])}")

    # Ex 2
    print("\n[EXERCÍCIO 2]")
    print(
        f"Passeios válidos: {contar_passeios_validos(4, [(1, 2), (2, 3)], [[1, 2, 3], [1, 4]])}"
    )

    # Ex 3
    print("\n[EXERCÍCIO 3]")
    res_ex3 = conectividade_dinamica(
        3, [(1, 1, 2), (0, 1, 2), (0, 1, 3), (1, 2, 3), (0, 1, 3)]
    )
    print("Conectividade entre ilhas:")
    for r in res_ex3:
        print(r)

    # Ex 4
    print("\n[EXERCÍCIO 4]")
    print(f"Ordem DFS: {dfs_produtos('nails')}")

    # Ex 5
    print("\n[EXERCÍCIO 5]")
    print(f"Ordem BFS: {bfs_produtos('nails')}")

    # Ex 6
    print("\n[EXERCÍCIO 6]")
    cam_ex6, dist_ex6 = menor_caminho_bfs("Idris", "Lina")
    print(f"Caminho Mínimo: {' -> '.join(cam_ex6)}")
    print(f"Graus de Separação: {dist_ex6}")

    # Ex 7
    print("\n[EXERCÍCIO 7]")
    ordem_dfs_7, ordem_bfs_7 = travessia_dir("Inicio")
    print(f"DFS Direcionada: {ordem_dfs_7}")
    print(f"BFS Direcionada: {ordem_bfs_7}")

    # Ex 8
    print("\n[EXERCÍCIO 8]")
    alcancaveis_8 = bfs_porto_alcançaveis("Berco_A")
    caminho_bfs_8, custo_bfs_8 = bfs_porto_caminho("Berco_A", "Centro_Logistico")
    print(f"Áreas alcançáveis: {alcancaveis_8}")
    print(f"Caminho BFS (menor n. arestas): {' -> '.join(caminho_bfs_8)}")
    print(f"Custo real desse caminho: {custo_bfs_8}")

    # Ex 9
    print("\n[EXERCÍCIO 9]")
    dists_9, _ = dijkstra_distancias("Berco_A")
    print("Menores distâncias calculadas a partir de Berco_A:")
    for local, d in dists_9.items():
        print(f" - {local}: {d}")

    # Ex 10
    print("\n[EXERCÍCIO 10]")
    caminho_otimo_10 = dijkstra_reconstrucao("Berco_A", "Centro_Logistico")
    print(f"Caminho mínimo completo: {' -> '.join(caminho_otimo_10)}")

    # Ex 11
    print("\n[EXERCÍCIO 11]")
    caminho_bfs_11 = bfs_simples("Berco_A", "Centro_Logistico")
    custo_bfs_11 = sum(
        grafo_porto[caminho_bfs_11[i]][caminho_bfs_11[i + 1]]
        for i in range(len(caminho_bfs_11) - 1)
    )
    caminho_dj_11, custo_dj_11 = dijkstra_simples("Berco_A", "Centro_Logistico")
    print(f"Caminho encontrado por BFS: {' -> '.join(caminho_bfs_11)}")
    print(f"Custo total desse caminho na rede real: {custo_bfs_11}")
    print(f"Caminho mínimo (Dijkstra): {' -> '.join(caminho_dj_11)}")
    print(f"Custo total do caminho Dijkstra: {custo_dj_11}")

    # Ex 12
    print("\n[EXERCÍCIO 12]")
    dfs_ordem_12, bfs_ordem_12 = analise_ordem_visita("Berco_A")
    dists_dj_12 = dijkstra_todas_distancias("Berco_A")
    print(f"Ordem de visita da DFS: {dfs_ordem_12}")
    print(f"Ordem de visita da BFS: {bfs_ordem_12}")
    print("Distâncias mínimas calculadas por Dijkstra:")
    for loc, d in dists_dj_12.items():
        print(f" - {loc}: {d}")

    print("\n" + "=" * 60)
    print(" EXECUÇÃO FINALIZADA ")
    print("=" * 60)
