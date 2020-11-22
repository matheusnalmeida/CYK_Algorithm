import numpy as np

# Classe responsável por processar a gramática e verificar se uma palavra é ou não aceita pela gramática
class CYK:

    def __init__(self, gramatica):
        self.gramatica = gramatica

    # Metodo principal, que dada uma palavra, verifica se a mesma pertence a linguagem
    def cyk(self,palavra):
        numero_combinacoes = 0
        tabelaCYK = {}
        for i in reversed(range(len(palavra))):
            combinacoes = self.__gerarCombinacoes(list(palavra), numero_combinacoes)
            numero_combinacoes += 1
            for combinacao in combinacoes:
                finalCombinacao = len(combinacao) - \
                    1 if len(combinacao) > 1 else len(combinacao)
                for x in range(0, finalCombinacao):
                    subParteCombinacao1 = combinacao[0:x+1]
                    subParteCombinacao2 = combinacao[x+1:len(combinacao)]
                    naoTerminalCombinacao1 = None
                    naoTerminalCombinacao2 = None

                    # Procurando naoTerminalEquivalente para combinacao1
                    naoTerminalCombinacao1 = self.__procuraNaoTerminalParaCombinacao(
                        tabelaCYK, self.gramatica, subParteCombinacao1)
                    # Procurando naoTerminalEquivalente para combinacao2
                    if subParteCombinacao2 != '':
                        naoTerminalCombinacao2 = self.__procuraNaoTerminalParaCombinacao(
                            tabelaCYK, self.gramatica, subParteCombinacao2)

                    if (naoTerminalCombinacao1 == '' or naoTerminalCombinacao1 == None) and (naoTerminalCombinacao2 == '' or naoTerminalCombinacao2 == None):
                        if subParteCombinacao1+subParteCombinacao2 not in tabelaCYK:
                            tabelaCYK[subParteCombinacao1+subParteCombinacao2] = ''
                    else:
                        # Realizando produto cartesiano entre as combinações
                        naoTerminalCombinacao2 = naoTerminalCombinacao2 if naoTerminalCombinacao2 != None else ''
                        naoTerminaisGeradores1Processados = naoTerminalCombinacao1.split(
                            ',')
                        naoTerminaisGeradores2Processados = naoTerminalCombinacao2.split(
                            ',')
                        geradoresNaoTerminais = self.__produtoCartesianoEntreGeradores(
                            naoTerminaisGeradores1Processados, naoTerminaisGeradores2Processados)
                        # Primeira interação não aplica plano cartesiano e não pega da gramática
                        if numero_combinacoes == 1:
                            tabelaCYK[subParteCombinacao1+subParteCombinacao2] = ','.join(
                                naoTerminaisGeradores1Processados)
                            break
                        geradoresDosNaoTerminais = []
                        for gerador in geradoresNaoTerminais:
                            if gerador != '':
                                naoTerminaisGeradores = self.__procuraNaoTerminais(
                                    self.gramatica, ''.join(gerador))
                                if naoTerminaisGeradores != '':
                                    geradoresDosNaoTerminais.append(
                                        naoTerminaisGeradores)

                        if subParteCombinacao1+subParteCombinacao2 not in tabelaCYK:
                            tabelaCYK[subParteCombinacao1 +
                                    subParteCombinacao2] = ','.join(geradoresDosNaoTerminais)
                        else:
                            geradoresNaoExistentes = self.__verificaGeradorParaCombinacaoTabelaCYK(
                                tabelaCYK, subParteCombinacao1+subParteCombinacao2, geradoresDosNaoTerminais)
                            tabelaCYK[subParteCombinacao1+subParteCombinacao2] += ',' + \
                                ','.join(geradoresNaoExistentes)

        if ('S' in tabelaCYK[palavra]):
            return True
        else:
            return False

    def __procuraNaoTerminais(self, gramatica, terminais):
        naoTerminaisGeradores = []
        for naoTerminal in gramatica:
            alfabeto = gramatica[naoTerminal]
            for producoes in alfabeto:
                if (terminais == producoes):
                    naoTerminaisGeradores.append(naoTerminal)
                    break

        return ','.join(naoTerminaisGeradores)

    def __produtoCartesianoEntreGeradores(self,geradores1, geradores2):
        x = np.array(geradores1)
        y = np.array(geradores2)
        return np.transpose([np.tile(x, len(y)), np.repeat(y, len(x))]).tolist()

    # Ira gerar as combinacoes dado um conjunto de letras, agrupando as mesmas de acordo com a quantidade de letras por combinação
    # Ex: [a,b,c,d,e] com uma letra por combinação => ['ab','bc','cd','ce']
    def __gerarCombinacoes(self,letras, letrasPorCombinacao):
        combinacoes = []
        for y in range(0, len(letras)):
            ultimaPosicao = y + letrasPorCombinacao
            if ultimaPosicao < len(letras):
                combinacoes.append(''.join(letras[y:ultimaPosicao+1]))

        return combinacoes

    # Dada uma combinacao, será procurado na tabela cyk e na gramática se a combinação existe e retornado seu(s) geradore(s)
    # Ex: Dada a combinação 'ab' será verificada na tabela e na gramática o gerador de dessa combinação
    def __procuraNaoTerminalParaCombinacao(self,tabelaCYK, gramatica, combinacao):
        gerador = None
        if combinacao in tabelaCYK:
            gerador = tabelaCYK[combinacao]
        else:
            geradorNaGramatica = self.__procuraNaoTerminais(gramatica, combinacao)
            if geradorNaGramatica != '':
                gerador = geradorNaGramatica

        return gerador

    # Verifica para uma dada combinacao na tabelaCYK, quais dos novos geradores
    # que ainda não estão presentes para essa dada combinação da tabelaCYK, evitando geradores duplicados
    def __verificaGeradorParaCombinacaoTabelaCYK(self,tabelaCYK, combinacao, novosGeradores):
        geradoresNaoExistentes = []
        combinacoesExistentes = tabelaCYK[combinacao].split(',')
        for gerador in novosGeradores:
            if gerador not in combinacoesExistentes:
                geradoresNaoExistentes.append(gerador)
                break

        return geradoresNaoExistentes