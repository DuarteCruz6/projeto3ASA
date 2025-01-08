from pulp import LpProblem, LpMaximize, LpVariable, lpSum, PULP_CBC_CMD, value

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
    for n in range(numFabricas):
        idFabrica, paisFabrica, stockFabrica = [int(i) for i in input().split()]
        listaFabricas.append(idFabrica)
        paisesFabricas[idFabrica] = paisFabrica
        stockFabricas[idFabrica] = stockFabrica

def inputPaises():
    for m in range(numPaises):
        idPais, maxExportacoes, minPrendas = [int(i) for i in input().split()]
        listaPaises.append(idPais)
        exportacoesPaises[idPais]=maxExportacoes
        prendasPaises[idPais]=minPrendas
 
def inputCriancas():
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
        "x", [(paisesCriancas[crianca],crianca) for crianca in listaCriancas], lowBound=0, cat="Binary"
    )
    # Crianças -> Fábricas que querem, peso = 0 ou 1
    y = LpVariable.dicts(
        "y", [(crianca,fabrica) for crianca in listaCriancas for fabrica in fabricasCriancas[crianca]], lowBound=0, cat="Binary"
    )
    
    #FUNCAO OBJETIVO
    prob += lpSum(x[paisesCriancas[crianca],crianca] for crianca in listaCriancas), "Objective" #Soma das valores de crianças, que nos dará o número de crianças com prenda
    
    #RESTRICOES
    #1: ⁠o número de prendas q uma criança recebe é igual a soma do número de prendas q cada fábrica dá a essa criança 
    for crianca in listaCriancas:
        prob += x[paisesCriancas[crianca], crianca] == lpSum(y[crianca,fabrica] for fabrica in fabricasCriancas[crianca])

    #2: ⁠o número de prendas q uma fábrica produz é menor que o stock dela
    for fabrica in listaFabricas:
        prob += lpSum(y[crianca,fabrica] for crianca in listaCriancas if fabrica in fabricasCriancas[crianca]) <= stockFabricas[fabrica]
    
    #3: ⁠o conjunto de fábricas de um país n pode dar mais presentes a crianças de países diferentes do que o limite de exportação
    for pais in listaPaises:
        prob += lpSum(y[crianca,fabrica] for crianca in listaCriancas for fabrica in fabricasCriancas[crianca] if paisesCriancas[crianca]!=pais and paisesFabricas[fabrica]==pais) <= exportacoesPaises[pais]
        
    #4: cada país recebe no mínimo min_prendas
    for pais in listaPaises:
        prob += lpSum(x[pais,crianca] for crianca in listaCriancas if paisesCriancas[crianca]==pais) >= prendasPaises[pais]

def printSolution(prob):   
    solver = PULP_CBC_CMD(msg=False)
    prob.solve(solver)
    if prob.status!=-1:
        print(int(value(prob.objective)))
    else:
        print(-1)
    
def main():
    getInput()
    prob = LpProblem("Maximizar_Brinquedos", LpMaximize)
    createProblem(prob)
    printSolution(prob)
    
main()