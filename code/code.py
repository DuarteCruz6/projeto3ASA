from pulp import LpProblem, LpMaximize, LpVariable
        
class Fabrica:
    def __init__(self, id, pais, stock):
        self.id = id
        self.pais = pais
        self.stock = stock
    
class Pais:
    def __init__(self, id, min_importacoes, max_exportacoes):
        self.id = id
        self.min_importacoes = min_importacoes
        self.max_exportacoes = max_exportacoes

class Crianca:
    def __init__(self, id, pais, fabricas):
        self.id=id
        self.pais=pais
        self.fabricas=fabricas
        

problem = LpProblem("Toy_Distribution", LpMaximize)

listaFabricas=[] #lista de fabricas
listaPaises=[] #lista de paises
listaCriancas=[] #lista de criancas

def getInput():
    nFabricas,mPaises,tCriancas = (int(i) for i in input().split())
    
    #coisas das fabricas
    stock_fabricas=[0 for n in range (nFabricas)] #lista dos stocks das fabricas
    
    #coisas dos paises
    min_imports=[0 for m in range(mPaises)] #lista do numero de importacoes minimas por pais
    max_exports=[0 for m in range(mPaises)] #lista do numero de exportacoes maximas por pais
    criancasPorPais=[0 for m in range(mPaises)] #lista do numero de criancas por pais
    
    for n in range(nFabricas):
        idFabrica, paisFabrica, stockFabrica = (int(i) for i in input().split())
        listaFabricas.append(Fabrica(idFabrica,paisFabrica,stockFabrica))
        
        stock_fabricas[idFabrica-1] = stockFabrica #adiciona o stock da fabrica à lista
    
    for m in range(mPaises):
        idPais, exportacoesPais, importacoesPais = (int(i) for i in input().split())
        listaPaises.append(Pais(id,importacoesPais,exportacoesPais))
        
        min_imports[idPais-1] = importacoesPais #adiciona o minimo de importacoes à lista 
        max_exports[idPais-1] = exportacoesPais #adiciona o maximo de exportacoes à lista

    for t in range(tCriancas):
        fullStr = input().split()
        idCrianca = int(fullStr[0])
        paisCrianca = int(fullStr[1])
        fabricasCrianca = fullStr[2:]
        listaCriancas.append(Crianca(idCrianca,paisCrianca,fabricasCrianca))
        
        criancasPorPais[paisCrianca-1]+=1 #adiciona a nova crianca ao número de criancas do pais

def main():
    getInput()
    
main()