# Classe responsavel por processar o arquivo e carregar a gramática em memória
class ProcessaArquivo:

    def __init__(self,diretorioArquivo):
        self.gramatica = self.__lerProducao__(diretorioArquivo)

    def __tirarEspacoVazio__(self,lista):
        for i in range(0,len(lista)):
            lista[i] = lista[i].strip()
        return lista

    def __lerProducao__(self,txt):
        producoes = {}
        f = open(txt, 'r')
        for line in f:
            index = line.index('=')
            if(line != ''):
                variavelNaoTerminal = line[:(index-1)].strip()
            alfabeto = line[(index+1)+1:].rstrip().strip()
            if(alfabeto.__contains__('|')): 
                alfabeto = self.__tirarEspacoVazio__(alfabeto.split('|'))
            else: 
                alfabeto = self.__tirarEspacoVazio__(alfabeto.split(' '))
            producoes[variavelNaoTerminal] = alfabeto
        return producoes
