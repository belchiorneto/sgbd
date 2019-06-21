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
	                      'SERVER=SERVIDOR\SQLEXPRESS;'
	                      'DATABASE=lojas;'
	                      'UID=sa;'
	                      'PWD=1234;')

	cursor = conexaoBanco.cursor()
	return cursor