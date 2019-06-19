import re
import os
import time
import hashlib
from _overlapped import NULL

def funcaoHash(elem):
	hash_object = hashlib.md5(str(elem).encode())
	hex_dig = hash_object.hexdigest()
	#print(hex_dig)
	#m = 2047
	#m = 16383
	#chave = elem % m
	return hex_dig
def criaDiretorios(tabelas):
	count = len(tabelas)
	while (count >= 0):
		folder = "" #para as pastas com mais de uma tabela
		for i in range(count):
			
			if(i == count-1):
				folder = folder + tabelas[i]
			else:
				folder = folder + tabelas[i] + "_"
		count = count - 1
		if(count > 0):
			try:
				os.mkdir(folder)
				print("Directory " , folder ,  " Created ")
			except FileExistsError:
				print("Directory " , folder ,  " already exists")
		else:
			try:
				os.mkdir(tabelas[count])
				print("Directory " , tabelas[count] ,  " Created ")
			except FileExistsError:
				print("Directory " , tabelas[count] ,  " already exists")
	
		

def varrerTab(tabela, indice=0):
	arquivo = open(tabela + ".txt", "r")
	arq_tab_hash = open("TabelaHash.txt", "w+")
	arq_tab_hash.close()
	for linha_arquivo in arquivo:
		capt_chave = capChave(linha_arquivo,indice)
		chave = funcaoHash(capt_chave)
		tab_hash(chave)
		arq_bucket_criacao = criarBucket(chave, tabela)
		preencher_bucket = preencherBucket(linha_arquivo, arq_bucket_criacao, tabela)
		#chave vai pra tabela hash
		#com a chave tambem cria o bucket
		
	arquivo.close()

#arq = open("teste.txt", "r+")

#essa funcao captura uma chave numerica
# de uma tupla e a partir disso, cria uma chave
# para a tabela de dispersao
#aux = re.sub("[],[',()]", "", aux)

def capChave(tupla = "0, cidade, UF", indicevetor = 0):
	tuplaF = tupla.split()
	vetor = ""
	vetor = tuplaF[indicevetor]
	return vetor #ou a posicao desejada do vetor
	

#valor Ã© numero, para ser comparado a tabela
#devemos adicionar um \n que Ã© o final da linha da tabela
#valor = funcaoHash(245)
#valor = str(valor) + '\n'

def tab_hash(chave):
	tabela_hash = open("TabelaHash.txt", "r+")
	chave = str(chave)+'\n'

	if chave not in tabela_hash:
		tabela_hash.write(chave)
		#tabela_hash.write("\n")
	tabela_hash.close()

def criarBucket(valor, tab):
	nomearq = "Bucket" + str(valor) + ".txt"
	arq_bucket = open(tab+"/"+nomearq, "a+")
	arq_bucket.close()
	return nomearq

def preencherBucket(tuplaInteira, nomearq, tab):
	#tuplaInteira = tuplaInteira + '\n'
	#print(tuplaInteira)
	bucket = open(tab+"/"+nomearq, "a+")
	bucket.write(tuplaInteira)
	bucket.close()

#valor = capChave2("(38, 'seashell floral bisque midnight black', 'Manufacturer#4           ', 'Brand#43  ', 'ECONOMY ANODIZED BRASS', 11, 'SM JAR    ', 938.030029296875, 'furiously pend') ",0)
#print(valor)	

def funcaoJuncao(atriJuncaoA, atriJuncaoB, indice, tab1, tab2):
	
	#bucketB = open("TabelaB/Bucket"+str(1)+".txt","r")
	bucketA = open(tab1+"/Bucket"+str(indice)+".txt","r")
	tabAB = open(tab1+"_"+tab2+"/"+tab1+"_"+tab2+".txt","a+")
	for A in bucketA:
		linhaA = A.split()
		#print(linhaA)
		bucketB = open(tab2+"/Bucket"+str(indice)+".txt","r")
		for B in bucketB:
			linhaB = B.split()
			#print("		"+str(linhaB))
			if (linhaA[atriJuncaoA]==linhaB[atriJuncaoB]):
				tabAB.write(str(linhaA)+str(linhaB)+"\n")
		bucketB.close()
	bucketA.close()
	tabAB.close()


def funcaoJuncaoBC(atriJuncaoB, atriJuncaoC, indice):
	bucketB = open("TabelaB/Bucket"+str(indice)+".txt","r")
	tabBC = open("TabelaBC/TabelaBC.txt","a+")
	for B in bucketB:
		linhaB = B.split()
		#print(linhaA)
		bucketC = open("TabelaC/Bucket"+str(indice)+".txt","r")
		for C in bucketC:
			linhaC = C.split()
			#print("		"+str(linhaB))
			if (linhaB[atriJuncaoB]==linhaC[atriJuncaoC]):
				tabBC.write(str(linhaB)+str(linhaC)+"\n")
		bucketC.close()	
	
	bucketB.close()
	tabBC.close()

def funcaoJuncaoABC(atriJuncaoAB, atriJuncaoBC, indice):
	bucketAB = open("TabelaAB/Bucket"+str(indice)+".txt","r")
	tabABC = open("TabelaABC/TabelaABC.txt","a+")
	for A in bucketAB:
		linhaAB = A.split()
		#print(linhaA)
		bucketBC = open("TabelaBC/Bucket"+str(indice)+".txt","r")
		for B in bucketBC:
			linhaBC = B.split()
			#print("		"+str(linhaB))
			if (linhaAB[atriJuncaoAB]==linhaBC[atriJuncaoBC]):
				tabABC.write(str(linhaAB)+str(linhaBC)+"\n")
		bucketBC.close()

	bucketAB.close()
	tabABC.close()

#formato do diretÃ³rio: TabelaAB
def qtdeArquivosPasta(diretorio="TabelaA/"):
	vetor=""
	for _, _, arquivo in os.walk(''+diretorio+''):
		vetor = vetor + str(arquivo) +" "
	
	v = len(vetor.split())
	return v

#jun = qtdeArquivosPasta()
def lerHashJuncao(atrA,atrB,v, tabA, tabB):
	inicio = time.time()
	abrir = open("TabelaHash.txt", "r")
	v = 0
	for line in abrir:
		v = line.replace("\n","")
		funcaoJuncao(atrA,atrB, v, tabA, tabB)
		#print(v)
	fim = time.time()

	print("Tempo total para juncao: ",fim-inicio)
	
def getTableFromSqlCmd(sqlcmd):
	sqlcmd.lower()
	# tabelas
	tabs = sqlcmd.split("from");
	if(len(tabs[1].split("on")) > 1):
	    # caso de join
	    tabs = tabs[1].split(" on ");
	    tabs = tabs[0].split(" join ")
	else:
	    # caso separado por virgula
	    tabs = tabs[1].split(" where ")
	    tabs = tabs[0].split(",")
	    for i in range(len(tabs)):
		    tabs[i] = tabs[i].strip()
	return tabs

def getfieldsFromSqlCmd(sqlcmd):
	sqlcmd.lower()
	# campos
	fields = sqlcmd.split("from");
	fields = fields[0].split("select")
	fields = fields[1].split(",")
	for i in range(len(fields)):
		fields[i] = fields[i].strip()
	return fields

def getJoinFromSqlCmd(sqlcmd):
	sqlcmd.lower()
	# joins
	joins = sqlcmd.split("where");
	ands = joins[1].split("and")
	if(len(ands) > 1):
		#mais de uma condição de junção
		joins = joins[1].split("and")
	else:
		#apenas uma condicao de juncao
		joins = joins[1]
		
	for i in range(len(joins)):
		joins[i] = joins[i].strip()
				
	return joins
	