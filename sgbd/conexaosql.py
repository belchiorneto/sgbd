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
	                      'DATABASE=tpc_h;'
	                      'UID=sa;'
	                      'PWD;')

	cursor = conexaoBanco.cursor()
	return cursor