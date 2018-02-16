#Programa para efetuar os ajustes nos arquivos de auditoria da oracle
import fileinput
import sys
import logging
import os

class OracleChangeScript:

    def __init__(self):
        self._arquivo_log = "C:\\temp\\OracleChangeScript.log"
        self._string_del_linha = "remover" #identificador utilizado para deletar a linha
        self._diretorio = "C:\\temp\\scripts_oracle_fev2018\\"
        logging.basicConfig(filename=self._arquivo_log,\
            level=logging.INFO,format="%(asctime)s %(message)s",datefmt="[%d/%m/%Y %H:%M:%S]")

    def FileList(self, diretorio):
       try:
           if diretorio is None:
               diretorio = self._diretorio
           resultado = []
           for folder, subfolders, files in os.walk(diretorio):
               for file in files:
                   resultado.append(str(os.path.join(os.path.abspath(folder), file)))
       except Exception as e:
           logging.info("Erro na func FileList: %s "%e)
           print "Erro na func FileList: %s"%e
       return resultado

  

    def ReplaceLine(self,arquivo,dicReplace):
#        try:
            linha = 0
            f = open(arquivo,"r")
            novo_arquivo = f.readlines()
            f.close()
            f = open(arquivo,"w")
            logging.info("Inicio do processamento do arquivo %s \n"%(arquivo))
            print "Inicio do processamento do arquivo %s \n"%(arquivo)
            for line in novo_arquivo:
                linha = linha +1
                for searchExp,replaceExp in dicReplace.iteritems():
                    if str(searchExp).strip() in str(line).strip():
                        line = replaceExp
                        print "O valor da linha %s : %s sera substituido por: %s"%(linha,searchExp,replaceExp)
                        logging.info("O valor da linha %s : %s sera substituido por: %s"%(linha,searchExp,replaceExp))   
                #removendo linhas *remover
                if str(self._string_del_linha).strip() not in str(line).strip():
                    f.write(line)
                else:
                    logging.info("A linha: %s foi removida"%line)
                    print "A linha: %s foi removida"%line                    
            f.close()
            logging.info("Fim do processamento, Total de linhas verificadas %s"%linha)
            print "Fim do processamento, Total de linhas verificadas %s"%linha
#        except Exception as e:
#            print "Erro na func ReplaceLine: %s"%e


        
        


if __name__ == '__main__':        
#Linhas as serem substituidas
   param = \
   "control_management_pack_access;control_management_pack_access                                                            1 NONE\n,\
   ADDM;remover                                                                        ,\
   awr_snapshot_time_offset;awr_snapshot_time_offset								  1 0 ,\
   AWR;remover                                                                         ,\
   EM Performance;remover                                                              ,\
   SQL Monitoring and Tuning pages;remover                                             ,\
   SQL Tuning Advisor;remover                                                          ,\
   selected.;remover                                                                \
   "
   #Convert param string to dic
   dic_param = dict((p.split(';') for p in param.split(',')))
   #Iniciar
   #arquivo = "C:\\temp\\scripts_oracle_fev2018\\ORAINST1_NSCFN4UCS3D1860.txt"
   #ajuste = OracleChangeScript()
   #ajuste.ReplaceLine(arquivo,dic_param)
# Leitura de totdos os arquivos da pasta 
   ajuste = OracleChangeScript()
   for file in ajuste.FileList(None):
       print ajuste.ReplaceLine(file,dic_param)










