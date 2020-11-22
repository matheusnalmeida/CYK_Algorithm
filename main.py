import numpy as np
from Models.ProcessaArquivo import ProcessaArquivo
from Models.CYK import CYK

if __name__ == "__main__":
  processaArquivo = ProcessaArquivo('arquivo.txt')
  gramatica = processaArquivo.gramatica
  cykProcessor = CYK(gramatica)

  while True:
    opcao = input("Escolha uma opção do menu:\n1 - Testar palavra\n2 - Finalizar programa\n")
    if opcao == '1':
      palavra = input('Digite uma palavra: ')
      resultado = cykProcessor.cyk(palavra)
      if resultado:
        print('Palavra aceita pela gramática!')
      else:
        print('Palavra não aceita pela gramática!')
    elif opcao == '2':
      print('Programa finalizado!')
      break
    else:
      print('Opção inválida')