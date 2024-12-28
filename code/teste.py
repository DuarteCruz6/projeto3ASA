from pulp import LpProblem, LpMaximize, LpVariable, lpSum

listaFabricas=[] #lista de todas as fabricas
stocksFabricas={} #dicionario fabrica:stock

listaPaises=[] #lista de todos os paises
minPrendasPais={} #dicionario pais:minPrendasRecebidas
maxExportacoesPais={} #dicionario pais:maxPrendasExportadas
criancasPais={} #dicionario pais:criancas

listaCriancas=[] #lista de todas as criancas
prendasCrianca={} #dicionario crianca:prendas que quer

def getInput():
    numFabricas,numPaises,numCriancas = [int(i) for i in input().split()]
    
    for n in range(numFabricas):
        idFabrica,paisFabrica,stockFabrica = [int(i) for i in input().split()]
        listaFabricas.append(idFabrica) #adiciona a fabrica à lista de fábricas
        stocksFabricas[idFabrica]=stockFabrica  #adiciona o stock da fabrica
        
    for m in range(numPaises):
        idPais,maxExportacoes,minPrendas = [int(i) for i in input().split()]  
        listaPaises.append(idPais) #adiciona o pais À lista de paises
        maxExportacoesPais[idPais]=maxExportacoes #adiciona o max de exportacoes do pais
        minPrendasPais[idPais]=minPrendas #adiciona o min de prendas recebidas pelo pais
        
    for t in range(numCriancas):
        fullStr = input().split()
        idCrianca = int(fullStr[0])
        paisCrianca = int(fullStr[1])
        fabricasCrianca = fullStr[2:]
        
        listaCriancas.append(idCrianca) #adiciona a crianca à lista de criancas
        criancasPais[idCrianca]=paisCrianca #adiciona a crianca ao pais
        prendasCrianca[idCrianca]=fabricasCrianca #adiciona as prendas que a crianca quer

def createProblem():
    prob = LpProblem("Maximizar_Brinquedos", LpMaximize)
    
    #VARIAVEIS DE DECISAO   
    #ligar paises às criancas
    x = LpVariable.dicts(
    "x", [(pais,crianca) for pais in listaPaises for crianca, paisCrianca in criancasPais.items() if paisCrianca == pais], lowBound=0, cat="Integer"
    )
    #ligar criancas às fábricas
    y = LpVariable.dicts(
    "y", [(crianca,fabrica) for crianca in listaCriancas for fabrica in prendasCrianca[crianca]], lowBound=0, cat="Binary"
    )
    
    #FUNCAO OBJETIVO
    prob += lpSum(x[pais, crianca] for pais in listaPaises for crianca, paisCrianca in criancasPais.items() if paisCrianca == pais)
    
    #RESTRICOES
    #1: cada fabrica nao pode produzir mais do que o seu stock
    for fabrica in listaFabricas:
        prob+= lpSum(y[crianca,fabrica]for crianca in listaCriancas if fabrica in prendasCrianca[crianca]) <= stocksFabricas[fabrica]
        
    #2: cada pais tem de receber >=min_prendas
    for pais in listaPaises:
        prob+= lpSum(x[pais,crianca] for crianca, paisCrianca in criancasPais.items() if paisCrianca == pais) >= minPrendasPais[pais]
    
    #3: cada crianca recebe ou 0 ou 1 prenda
    for crianca in listaCriancas:
        prob += lpSum(y[crianca,fabrica] for fabrica in prendasCrianca[crianca]) <=1
        
    #4: ⁠o número de prendas q uma criança recebe é igual a soma do número de prendas q cada fábrica dá a essa criança 
    for crianca in listaCriancas:
        prob+= lpSum(y[crianca,fabrica] for fabrica in prendasCrianca[crianca])==lpSum(x[pais,crianca] for pais in listaPaises for crianca, paisCrianca in criancasPais.items() if paisCrianca == pais)
    
    #5: ⁠o número de prendas q um país recebe é igual a soma do num de prendas q as crianças desse país recebem
    for pais in listaPaises:
        prob+=lpSum(x[pais,crianca] for crianca, paisCrianca in criancasPais.items() if paisCrianca == pais) == lpSum(y[crianca,fabrica] for fabrica in prendasCrianca[crianca])
    
    #6: ⁠o número de prendas q uma fábrica produz é igual a soma do número de prendas q essa fábrica dá a cada criança
    for fabrica in listaFabricas:
        prob+= lpSum(y[crianca,fabrica] for crianca in listaCriancas if fabrica in prendasCrianca[crianca]) <=stocksFabricas[fabrica]
        
    #7: ⁠o conjunto de fábricas de um país n pode dar mais presentes a crianças de países diferentes do que o limite de exportação
    for pais in listaPaises:
        prob += lpSum(y[crianca,fabrica] for crianca in listaCriancas for fabrica in listaFabricas if criancasPais[crianca]!= pais and fabrica in prendasCrianca[crianca]) <=maxExportacoesPais[pais]
    
    prob.solve()
    print("Status:", prob.status)
    print("Distribuição de brinquedos (País -> Criança):")
    for (p, c) in x:
        if x[p, c].value() > 0:
            print(f"País {p} para Criança {c}: {x[p, c].value()}")

    print("Brinquedos atribuídos às crianças (Criança -> Fábrica):")
    for (c, f) in y:
        if y[c, f].value() > 0:
            print(f"Criança {c} recebe de Fábrica {f}")
            
def main():
    getInput()  
    createProblem()
    
    
main()