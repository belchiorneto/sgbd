import re
import os
import time
import hashlib
from _overlapped import NULL

def funcaoHash(elem):
	hash_object = hashlib.md5(str(elem).encode())
	hex_dig = hash_object.hexdigest()
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
	arq_tab_hash = open("TabelaHash.txt", "a+")
	
	for linha_arquivo in arquivo:
		capt_chave = capChave(linha_arquivo,indice)
		chave = funcaoHash(capt_chave)
		tab_hash(chave, arq_tab_hash)
		arq_bucket_criacao = criarBucket(chave, tabela)
		preencher_bucket = preencherBucket(linha_arquivo, arq_bucket_criacao, tabela)
		#chave vai pra tabela hash
		#com a chave tambem cria o bucket
		
	arquivo.close()
	arq_tab_hash.close()

#arq = open("teste.txt", "r+")

#essa funcao captura uma chave numerica
# de uma tupla e a partir disso, cria uma chave
# para a tabela de dispersao
#aux = re.sub("[],[',()]", "", aux)

def capChave(tupla, indicevetor):
	tuplaF = tupla.split()
	vetor = ""
	print(indicevetor)
	print(tuplaF)
	vetor = tuplaF[indicevetor]
	return vetor #ou a posicao desejada do vetor
	

#valor é numero, para ser comparado a tabela
#devemos adicionar um \n que é o final da linha da tabela
#valor = funcaoHash(245)
#valor = str(valor) + '\n'

def tab_hash(chave, hashtable):
	#get line
	lista = open("TabelaHash.txt", 'r').read().split()
	chave = str(chave)
	
	if chave in lista:
		#print("encontrado")
		return
	else:
		file = open("TabelaHash.txt", 'a+')
		file.write(chave +'\n')
		file.close()

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



def funcaoJuncao(atriJuncaoA, atriJuncaoB, indice, tab1, tab2):
	
	try:
		os.mkdir(tab1+"_"+tab2)
		print("Directory " , tab1+"_"+tab2 ,  " Created ")
	except FileExistsError:
		print("Directory " , tab1+"_"+tab2 ,  " already exists")
	bucketA = open(tab1+"/Bucket"+str(indice)+".txt","r")
	tabAB = open(tab1+"_"+tab2+"/"+tab1+"_"+tab2+".txt","w+")
	for A in bucketA:
		linhaA = A.split()
		#print(linhaA)
		bucketB = open(tab2+"/Bucket"+str(indice)+".txt","r")
		for B in bucketB:
			linhaB = B.split()
			
			if (linhaA[atriJuncaoA]==linhaB[atriJuncaoB]):
				tabAB.write(str(linhaA)+str(linhaB)+"\n")
		bucketB.close()
	bucketA.close()
	tabAB.close()




#formato do diretório: TabelaAB
def qtdeArquivosPasta(diretorio="TabelaA/"):
	vetor=""
	for _, _, arquivo in os.walk(''+diretorio+''):
		vetor = vetor + str(arquivo) +" "
	
	v = len(vetor.split())
	return v

#jun = qtdeArquivosPasta()
def lerHashJuncao(camposindex, atributos, v, tabA, tabB):
	
	inicio = time.time()
	abrir = open("TabelaHash.txt", "r")
	v = 0
	atrA = ""
	atrB = ""
	keyforA = 0
	keyforB = 0
	if isinstance(atributos, str):
		partes = atributos.split(" = ")
		for parte in partes:
			parte = parte.strip()
			if(parte.split(".")[0] == tabA):
				atrA = parte.split(".")[1]
			if(parte.split(".")[0] == tabB):
				atrB = parte.split(".")[1]
	else:
		
		for atributo in atributos:
			partes = atributo.split(" = ")
			parte = parte.strip()
			
			if(partes.split(".")[0] == tabA):
				atrA = partes.split(".")[1]
				
			if(partes.split(".")[0] == tabB):
				atrB = partes.split(".")[1]
				
	
	for campo in camposindex:
				
		for k in campo:
			if(campo.get(atrA) != None):
				keyforA = campo.get(atrA)
			if(campo.get(atrB) != None):
				keyforB = campo.get(atrB)
						
	print("Atributo a: " +str(keyforA))
	
	print("Atributo b: " +str(keyforB))
	
	for line in abrir:
		v = line.replace("\n","")
		if(os.path.isfile(tabA+"/Bucket"+str(v)+".txt")):
			funcaoJuncao(keyforA ,keyforB, v, tabA, tabB)
		#print(v)
	fim = time.time()

	print("Tempo total para juncao: ",fim-inicio)
	

	