import re
import os
import _thread
import pyodbc
import getpass
from funcoes import *
from conexaosql import *

#################CONEXAO COM O BANCO#################
cursor = conexaoBanco()

tabelas = input("Entre com as tabelas, sepadaradas por espaço: ")
tabelas_join = tabelas.split()


tabela1 = selecionarTABELA(cursor,tabelas_join[0])
tabela2 = selecionarTABELA(cursor,tabelas_join[1])
#tabela3 = selecionarTABELA(cursor,tabelas_join[2])


mostrarAtribTabela(cursor,tabela1)
mostrarAtribTabela(cursor,tabela2)

atrib_juncao1 = input("Entre com o num do atrib de juncao para tabelas "+tabela1+" e "+tabela2+" :")
atrib_selec = re.sub(" ", "", atrib_juncao1)
atrib_selec.split()

indiceTabelaA = int(atrib_selec[0])
indiceTabelaB = int(atrib_selec[1])

#mostrarAtribTabela(cursor,tabela2)
#mostrarAtribTabela(cursor,tabela3)

#atrib_juncao1 = input("Entre com o num do atrib de juncao para tabelas "+tabela1+" e "+tabela2+" :")
#atrib_selec = re.sub(" ", "", atrib_juncao1)
#atrib_selec.split()

indiceTabelaBB = int(atrib_selec[0])
indiceTabelaC = int(atrib_selec[1])

#####################################################

#################VARRENDO AS TABELAS#################
criaDiretorios(tabela1, tabela2);
varrerTab(tabela1,indiceTabelaA)
varrerTab(tabela2,indiceTabelaB)
#varrerTab(tabela3,indiceTabelaC)
#####################################################

#################JOIN DAS AS TABELAS#################
qtdeArq = qtdeArquivosPasta("TabelaA/")
#lerHashJuncao(indiceTabelaA,indiceTabelaB,qtdeArq)

#####################################################