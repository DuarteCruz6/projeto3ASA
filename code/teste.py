from pulp import LpProblem, LpMaximize, LpVariable

prob = LpProblem("Maximizar_Brinquedos", LpMaximize)

nFabricas,mPaises,tCriancas = (int(i) for i in input().split())
fabricas = LpVariable.dicts("fabrica",[i for i in range(1,nFabricas+1)], lowBound=0, cat= "Continuous")
paises =  LpVariable.dicts("pais",[i for i in range(1,mPaises+1)], lowBound=0, cat= "Continuous")
criancas = LpVariable.dicts("crianca",[i for i in range(1,tCriancas+1)], lowBound=0, cat= "Continuous")

listaStocks=[]
for n in range(nFabricas):
    idFabrica, paisFabrica, stockFabrica = (int(i) for i in input().split())
    listaStocks.append(stockFabrica)

producaoFabrica = LpVariable.dicts("producao_fabrica",[i for i in range(1,nFabricas+1)], lowBound=0, cat= "Continuous")
for i in range(1,nFabricas+1):  
    prob += producaoFabrica[i]<=listaStocks[i-1] #producao de cada fabrica <= stock dela 
        
listaExportacoes=[]
listaImportacoes=[]   
for m in range(mPaises):
    idPais, exportacoesPais, importacoesPais = (int(i) for i in input().split())
    listaExportacoes.append(exportacoesPais)
    listaImportacoes.append(importacoesPais)
    
importacoesPais = LpVariable.dicts("importacoes_pais",[i for i in range(1,mPaises+1)], lowBound=0, cat= "Continuous")
exportacoesPais = LpVariable.dicts("exportacoes_pais",[i for i in range(1,mPaises+1)], lowBound=0, cat= "Continuous")
for i in range(1,mPaises+1):
    prob += importacoesPais[i]>=listaImportacoes[i-1] #importacoes de cada pais >= min_importacoes
    prob += exportacoesPais[i]<=listaExportacoes[i-1] #exportacoes de cada pais <= max_exportacoes
        

for t in range(tCriancas):
    fullStr = input().split()
    idCrianca = int(fullStr[0])
    paisCrianca = int(fullStr[1])
    fabricasCrianca = fullStr[2:]
        


prendasCriancas = LpVariable.dicts("prendas_crianca",[i for i in range(1,tCriancas+1)],cat= "Binary")



prob += sum(prendasCriancas)
    
print(fabricas)
print(paises)
print(criancas)
print(prob)