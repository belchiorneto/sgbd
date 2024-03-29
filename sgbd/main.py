import re
import os
import _thread
import pyodbc
import getpass
from conexaosql import *
from sqlFormat import sqlFormat


#################CONEXAO COM O BANCO#################
cursor = conexaoBanco()
'''
exemplo deconsultasusando TPC-H
exemplo com tabelas grandes
select partsupp.ps_suppkey, supplier.s_suppkey from partsupp, supplier where partsupp.ps_suppkey = supplier.s_suppkey
exemplo com tabelas pequenas
select nation.n_regionkey, region.r_regionkey from nation, region where nation.n_regionkey = region.r_regionkey
'''

print("=================================================\n")
print("Formato do SQL \"select t1.campo1, t2.campo2, tn.campon from t1, t2, tn where t1.campo1 = t2.campo1 and t2.campo2 = t3.campo3 and tn.campon = tn.campon\" (ENTER)\n")
print("=================================================\n")
sqlcmd = input("Entre o comando SQL")

sqlformat = sqlFormat(cursor, sqlcmd)
sqlformat.getTableFromSqlCmd()

for table in sqlformat.tabelas:
    print("Nome: " + table.name)
    print("Fields: " + str(table.fields))
    print("joins: " + str(table.joins))
    print("tamanho: " + str(table.size))
    print("indexes: " + str(table.fieldsIdx))
    
#sqlformat.criaDiretorios()
#sqlformat.gerarTXTs()
#sqlformat.geraBuckets()
sqlformat.joins(0) # chama primeira join (tabela 0 com tabela 1)
