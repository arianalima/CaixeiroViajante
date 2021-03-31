from math import sqrt
import random, decimal

f = open("cidades.txt","r")
l_cidades = f.read().split()
f.close()
cidades = {} #dicionario com a posicao de todas as cidades {'city_number':[posX, posY]}

for x in range(0,len(l_cidades),3): #preenche o dicionario com as cidades e posicoes
    cidades[l_cidades[x]] = [float(l_cidades[x+1]),float(l_cidades[x+2])]

def distancia(xyA,xyB): #calcula a distancia reta entre dois pontos
    xA, xB, yA, yB = (xyA[0]), (xyB[0]), (xyA[1]), (xyB[1])
    d = sqrt((xB-xA)**2 + (yB-yA)**2)
    return round(d,12)

cidades_custo = {} #dicionario com o custo de cada viagem {('cityA_number','cityB_number'): distancia}
for k in range(1,42):
    for c in range(1,42):
        cidades_custo[(str(k),str(c))] = distancia(cidades[str(k)],cidades[str(c)])

def custo_total(lista_cidades): #retorna o custo total de uma solucao
    custo = 0
    for cidade in range(len(lista_cidades)):
        if cidade == len(lista_cidades)-1: #se chegou na ultima cidade soma o custo com a origem
            custo += cidades_custo[(str(lista_cidades[cidade]), str(lista_cidades[0]))]
        else:
            custo+=cidades_custo[(str(lista_cidades[cidade]),str(lista_cidades[cidade+1]))]
    return custo

def vizinho(solucao):
    solucao_anterior = solucao.copy()
    while True:
        posA = random.randint(0,37)
        posB = random.randint(0,37)
        a = solucao[posA]
        b = solucao[posB]
        solucao[posA] = b
        solucao[posB] = a

        posC = random.randint(0, 37)
        posD = random.randint(0, 37)
        c = solucao[posC]
        d = solucao[posD]
        solucao[posC] = d
        solucao[posD] = c
        if solucao != solucao_anterior:
            break
    return solucao

def probabilidade(custo_antigo,custo_novo,temperatura): #calcula a probabilidade de aceitacao da nova solucao
    decimal.getcontext().prec = 100
    diferenca_custo = custo_antigo - custo_novo
    custo_temp = diferenca_custo/temperatura
    p = decimal.Decimal(0)
    e = decimal.Decimal(2.71828)
    n_custo_temp = decimal.Decimal(-custo_temp)
    try:
        p = e**n_custo_temp
        resultado = repr(p)
    except decimal.Overflow:
        #print("Error decimal Overflow")
        return 0.0

    try: #caso o numero tenha casas decimais
        fim = resultado.find("')")
        resultado = round(float(resultado[9:fim-1]), 3)

    except: #numero n tem casas decimais
        resultado = round(float(resultado[9:-2]))
    return resultado

def annealing(solution):
    print("Calculando rotas.....\n")
    old_cost = custo_total(solution)
    T = 1.0
    T_min = 0.0001
    alpha = 0.9
    best_solution, best_cost = solution[::], old_cost
    while T > T_min:
        i = 1
        while i <= 500:
            new_solution = vizinho(solution)
            new_cost = custo_total(new_solution)
            p = probabilidade(old_cost, new_cost, T)
            if new_cost < best_cost:
                best_solution = new_solution[::]
                best_cost = new_cost
            if p > round(random.random(), 3):
                solution = new_solution[::]
                old_cost = new_cost
            i += 1

        T = T*alpha
    return best_solution, best_cost

def gerar_solucao(): #gera uma solucao aleatoria
    solucao_aleatoria = [x for x in range(1,39)]
    random.shuffle(solucao_aleatoria)
    return solucao_aleatoria
solucao_inicial = gerar_solucao()

solucao_final, cost = annealing(solucao_inicial)
print(solucao_final, "Solução Final \n", cost,"Custo Final")
