from pulp import LpProblem, LpMaximize, LpVariable, lpSum

numFabricas=0 #numFabricas = n
numPaises=0 #numPaises = m
numCriancas=0 #numCriancas = t

#fabricas
listaFabricas = []
paisesFabricas = {} #fabrica : pais que está localizada
stockFabricas = {} #fabrica : stock máximo

#paises
listaPaises = []
exportacoesPaises = {} #pais : exportacoes máxima
prendasPaises = {} #pais : minimo de prendas que recebe

#criancas
listaCriancas=[]
paisesCriancas={} #crianca : pais que vive
fabricasCriancas = {} #crianca : fábricas que quer

#variaveis problema
x=0
y=0

def inputFabricas():
    global numFabricas
    for n in range(numFabricas):
        idFabrica, paisFabrica, stockFabrica = [int(i) for i in input().split()]
        listaFabricas.append(idFabrica)
        paisesFabricas[idFabrica] = paisFabrica
        stockFabricas[idFabrica] = stockFabrica

def inputPaises():
    global numPaises
    for m in range(numPaises):
        idPais, maxExportacoes, minPrendas = [int(i) for i in input().split()]
        listaPaises.append(idPais)
        exportacoesPaises[idPais]=maxExportacoes
        prendasPaises[idPais]=minPrendas
 
def inputCriancas():
    global numCriancas
    for t in range(numCriancas):
        fullStr = input().split()
        idCrianca = int(fullStr[0])
        idPais = int(fullStr[1])
        fabricasDesejadas = [int(i) for i in fullStr[2:]] 
        listaCriancas.append(idCrianca)
        paisesCriancas[idCrianca]=idPais
        fabricasCriancas[idCrianca]=fabricasDesejadas

def getInput():
    global numFabricas, numPaises, numCriancas
    numFabricas, numPaises, numCriancas = [int(i) for i in input().split()]
    
    inputFabricas()
    inputPaises()
    inputCriancas()
    
def createProblem(prob):
    global x,y
    
    #VARIAVEIS DE DECISAO
    # Países -> Crianças que vivem no País, peso = 0 ou 1
    x = LpVariable.dicts(
        "x", [(pais,crianca) for pais in listaPaises for crianca in listaCriancas if paisesCriancas[crianca]==pais], lowBound=0, cat="Binary"
    )
    # Crianças -> Fábricas que querem, peso = 0 ou 1
    y = LpVariable.dicts(
        "y", [(crianca,fabrica) for crianca in listaCriancas for fabrica in fabricasCriancas[crianca]], lowBound=0, cat="Binary"
    )
    
    #FUNCAO OBJETIVO
    prob += lpSum(x[pais, crianca] for pais in listaPaises for crianca in listaCriancas if paisesCriancas[crianca]==pais) #Soma das valores de crianças, que nos dará o número de crianças com prenda
    
    #RESTRICOES
    #1: ⁠o número de prendas q uma criança recebe é igual a soma do número de prendas q cada fábrica dá a essa criança
    for crianca in listaCriancas:
        prob += lpSum(x[pais, crianca] for pais in listaPaises if paisesCriancas[crianca]==pais) == lpSum(y[crianca,fabrica] for fabrica in fabricasCriancas[crianca])
        
    #2: ⁠o número de prendas q um país recebe é igual a soma do num de prendas q as crianças desse país recebem
    for pais in listaPaises:
        prob += lpSum(x[pais,crianca] for crianca in listaCriancas if paisesCriancas[crianca]==pais) == lpSum(y[crianca,fabrica] for fabrica in fabricasCriancas[crianca])
    
    #3: ⁠o número de prendas q uma fábrica produz é igual a soma do número de prendas q essa fábrica dá a cada criança e é menor que o stock dela
    for fabrica in listaFabricas:
        prob += lpSum(y[crianca,fabrica] for crianca in listaCriancas if fabrica in fabricasCriancas[crianca]) <= stockFabricas[fabrica]
    
    #4: ⁠o conjunto de fábricas de um país n pode dar mais presentes a crianças de países diferentes do que o limite de exportação
    for pais in listaPaises:
        prob += lpSum(y[crianca,fabrica] for crianca in listaCriancas for fabrica in fabricasCriancas[crianca] if paisesCriancas[crianca]!=pais and paisesFabricas[fabrica]==pais) <= exportacoesPaises[pais]
        
    #5: cada país recebe no mínimo min_prendas
    for pais in listaPaises:
        prob += lpSum(x[pais,crianca] for crianca in listaCriancas if paisesCriancas[crianca]==pais) >= prendasPaises[pais]

def printSolution(prob):   
    prob.solve()
    print("Status:", prob.status)
    if prob.status!=-1:
        print("Distribuição de brinquedos (País -> Criança):")
        for (pais, crianca) in x:
            if x[pais, crianca].value() > 0:
                print(f"País {pais} para Criança {crianca}: {x[pais, crianca].value()}")
    
        print("Brinquedos atribuídos às crianças (Criança -> Fábrica):")
        for (crianca, fabrica) in y:
            if y[crianca, fabrica].value() > 0:
                print(f"Criança {crianca} recebe de Fábrica {fabrica}")
        total = 0
        for pais in listaPaises:
            for crianca in listaCriancas:
                if paisesCriancas[crianca] == pais:
                    total += x[pais, crianca].value()
    
        print(f"Total de prendas atribuídas: {total}")
    

def main():
    getInput()
    prob = LpProblem("Maximizar_Brinquedos", LpMaximize)
    createProblem(prob)
    printSolution(prob)
    
main()