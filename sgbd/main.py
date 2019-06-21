import re
import os
import _thread
import pyodbc
import getpass
from funcoes import *
from conexaosql import *
from sqlFormat import sqlFormat


#################CONEXAO COM O BANCO#################
cursor = conexaoBanco()

sqlcmd = input("Entre o comando SQL")

sqlformat = sqlFormat(cursor, sqlcmd)
sqlformat.getTableFromSqlCmd()

#sqlformat.getfieldsFromSqlCmd()
#sqlformat.getJoinFromSqlCmd()

for table in sqlformat.tabelas:
    print(table.name)
    print(table.fields)
    print(table.joins)
   

#tabelas = getTableFromSqlCmd(sqlcmd);
#campos = getfieldsFromSqlCmd(sqlcmd);
#joinconditions = getJoinFromSqlCmd(sqlcmd);
camposIdex = getfieldIdex(cursor, campos, tabelas);


        
criaDiretorios(tabelas);

for tabela in tabelas:
    tabela_ = selecionarTABELA(cursor,tabela)
    mostrarAtribTabela(cursor,tabela_)
    for index in camposIdex:
        
        for k in index:
            varrerTab(tabela,index.get(k))

for tabelaA in tabelas:
    for tabelaB in tabelas:
        qtdeArqA = qtdeArquivosPasta(tabelaA)
        qtdeArqB = qtdeArquivosPasta(tabelaB)
        if(tabelaA != tabelaB):
            
            if(qtdeArqA < qtdeArqB):
                lerHashJuncao(camposIdex, joinconditions, qtdeArqA, tabelaA, tabelaB)
            else:
                lerHashJuncao(camposIdex, joinconditions, qtdeArqB, tabelaB, tabelaA)
