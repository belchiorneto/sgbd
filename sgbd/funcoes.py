import re
import os
import time
def funcaoHash(elem = 1):
	m = 2047
	#m = 16383
	chave = elem % m
	return chave
def criaDiretorios(tab1, tab2):
	try:
		os.mkdir(tab1)
		print("Directory " , tab1 ,  " Created ")
	except FileExistsError:
		print("Directory " , tab1 ,  " already exists")

	try:
		os.mkdir(tab2)
		print("Directory " , tab2 ,  " Created ")
	except FileExistsError:
		print("Directory " , tab2 ,  " already exists")
	
	try:
		os.mkdir(tab1+"_"+tab2)
		print("Directory " , tab1+"_"+tab2 ,  " Created ")
	except FileExistsError:
		print("Directory " , tab1+"_"+tab2 ,  " already exists")
def varrerTab(tabela, indice=0):
	arquivo = open(tabela + ".txt", "r")
	arq_tab_hash = open("TabelaHash.txt", "w+")
	arq_tab_hash.close()
	for linha_arquivo in arquivo:
		capt_chave = capChave(linha_arquivo,indice)
		chave = funcaoHash(capt_chave)
		tab_hash(chave)
		arq_bucket_criacao = criarBucket(chave)
		preencher_bucket = preencherBucket(linha_arquivo, arq_bucket_criacao)
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
	print(tuplaF)	
	vetor = tuplaF[indicevetor]
	#print(vetor)
	return int(vetor) #ou a posicao desejada do vetor

#valor é numero, para ser comparado a tabela
#devemos adicionar um \n que é o final da linha da tabela
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

def funcaoJuncaoAB(atriJuncaoA, atriJuncaoB, indice, tab1, tab2):
	
	
    	
    	
	
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

#formato do diretório: TabelaAB
def qtdeArquivosPasta(diretorio="TabelaA/"):
	vetor=""
	for _, _, arquivo in os.walk(''+diretorio+''):
		vetor = vetor + str(arquivo) +" "
	
	v = len(vetor.split())
	return v

#jun = qtdeArquivosPasta()
def lerHashJuncao(atrA,atrB,v):
	inicio = time.time()
	abrir = open("TabelaHash.txt", "r")
	v = 0
	for line in abrir:
		v = int(line.replace("\n",""))
		funcaoJuncao(atrA,atrB, v)
		#print(v)
	fim = time.time()

	print("Tempo total para juncao: ",fim-inicio)