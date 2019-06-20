#!"/Users/M0US3/AppData/Local/Programs/Python/Python37-32/python.exe"   

import pyodbc
import getpass
import re
import time
import os
import _thread

os.system('cls')

def conexaoBanco():
	#senha = getpass.getpass('Entre com a senha do SQL Server: ')
	
	conexaoBanco = pyodbc.connect('DRIVER={ODBC Driver 11 for SQL Server};'
	                      'SERVER=NOTE\SQLEXPRESS;'
	                      'DATABASE=tpch;'
	                      'UID=sa;'
	                      'PWD=;')

	cursor = conexaoBanco.cursor()
	return cursor
#tabelas = input("Entre com as tabelas, sepadaradas por espaço: ")
#tabelas_juncao = tabelas.split()

#atrib_join1 = input("Entre com o atrib de juncao para tabelas "+tabelas_juncao[0]+" e "+tabelas_juncao[1]+" :")
#atrib_join2 = input("Entre com o atrib de juncao para tabelas "+tabelas_juncao[1]+" e "+tabelas_juncao[2]+" :")


###########Colunas de uma tabela#####################
#cursor.execute("SELECT column_name from information_schema.columns where table_name = '"+tabelas_juncao[0]+"'")

#for row in cursor:
#	auxiliar = str(row) + ' '
#	#aux = re.sub("[],[',()]", "", aux)
#	auxiliar = re.sub('[,()]', '', auxiliar)
#	print(auxiliar, end ="")
#	arquivo.write(str(auxiliar))
#arquivo.write("\n")

###############Carregando tabela em arquivo.txt########

def selecionarTABELA(cursor, tab):
	arqtab = tab + ".txt"
	open(arqtab, 'w').close()
	arquivo = open(arqtab, "a+")
	inicio = time.time()
	cursor.execute("SELECT * from "+tab+"")
	
	for row in cursor:
		auxiliar = ""
		for campo in row:
			auxiliar = auxiliar + str(campo) + " "
		arquivo.write(str(auxiliar) + '\n')
		

	fim = time.time()
	print("Tempo total para selecionar tabela "+tab+": ",fim-inicio)
	return tab

def getfieldIdex(cursor, campos, tabelas):
	camposindex = []
	for tabela in tabelas:
		cursor.execute("SELECT column_name from information_schema.columns where table_name = '"+tabela+"'")
		i = 0
		for row in cursor:
			for campo2 in row:
				for campo in campos:
					if(campo == campo2):
						newvalues = {campo : i}
						camposindex.append(newvalues);
						
				i = i + 1
	return camposindex	
			
	
def mostrarAtribTabela(cursor, tabela = 'name'):
	cursor.execute("SELECT column_name from information_schema.columns where table_name = '"+tabela+"'")
	auxiliar = ''
	i = 0
	for row in cursor:
		
		tupla = '['+str(i)+']'+str(row) + ' '
		auxiliar = auxiliar + tupla
		#aux = re.sub("[],[',()]", "", aux)
		auxiliar = re.sub("[,(')]", '', auxiliar)
		i=i+1
	#print(auxiliar, end = "")
	print("\n")
	#return auxiliar

"""	auxiliar = re.sub("[ ()]", "", auxiliar)
	auxiliar = re.sub(",", " ",auxiliar)
	auxiliar = re.sub(",", "",auxiliar)"""

"""
##################SQL SERVER###############


import pyodbc 
# Some other example server values are
# server = 'localhost\sqlexpress' # for a named instance
# server = 'myserver,port' # to specify an alternate port
server = 'tcp:myserver.database.windows.net' 
database = 'mydb' 
username = 'myusername' 
password = 'mypassword' 
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()    

SELECT * FROM sys.columns WHERE object_id = object_id('nation')
"""


c = conexaoBanco()
#mostrarAtribTabela(c, "nation")
#print(aux)
#c = conexaoBanco()

#selecionarTABELA(c)