import re
import os
import _thread
import pyodbc
import getpass
from funcoes import *
from conexaosql import *

#################CONEXAO COM O BANCO#################
cursor = conexaoBanco()

sqlcmd = input("Entre o comando SQL")


tabelas = getTableFromSqlCmd(sqlcmd);
campos = getfieldsFromSqlCmd(sqlcmd);
joinconditions = getJoinFromSqlCmd(sqlcmd);
print(joinconditions)
camposIdex = getfieldIdex(cursor, campos, tabelas);

        
criaDiretorios(tabelas);

for tabela in tabelas:
    tabela_ = selecionarTABELA(cursor,tabela)
    mostrarAtribTabela(cursor,tabela_)
    for index in camposIdex:
        varrerTab(tabela,index)

for tabelaA in tabelas:
    for tabelaB in tabelas:
        qtdeArqA = qtdeArquivosPasta(tabelaA)
        qtdeArqB = qtdeArquivosPasta(tabelaA)
        if(qtdeArqA < qtdeArqB):
            lerHashJuncao(indiceTabelaA,indiceTabelaB,qtdeArqA, tabelaA, tabelaB)
        else:
            lerHashJuncao(indiceTabelaB,indiceTabelaA,qtdeArqB, tabelaA, tabelaB)
