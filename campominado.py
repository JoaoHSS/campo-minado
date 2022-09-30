from random import randrange
from time import sleep
from sys import stdout
from os import system

ALTURA = 10
LARGURA = 10
BOMBAS = 15

ponto, bomba, bandeira = '.', 'X', '!'
adjacentes = [(1,1), (1,0), (1,-1), (0,1), (0,-1), (-1,1), (-1,0), (-1,-1)]

def imprimirJogo(matriz):               #   essa funçao não abrange mais que 10 colunas, a formatação vai sair errada devido ao espaçamento        
    system('cls')
    stdout.write("  ") 
    for i in range(0,len(matriz)):
        stdout.write("  %s" %(i))       #   índices em cima
    stdout.write("\n   %s" %(" - "*len(matriz[0])))
    for i in range(0,len(matriz)):
        stdout.write("\n%s :" %(i))     #    índices à esquerda
        for j in matriz[i]:
            stdout.write(" %s " %(j))   #    valores
    print("\n")

def dicas(campo,a,b):                   #   todas as coordenadas em volta de [a][b](bomba) receberão +1
    for par in adjacentes:
        try:
            if a+par[0] < 0 or b+par[1] < 0:    #   impede que coordenadas como matriz[-1] sejam acessadas
                continue
            campo[a+par[0]][b+par[1]] += 1
        except IndexError:
            pass

def gerarBombas(campo,nBombas):
    i =  0
    while i < nBombas:                      #   como bombas podem ser sorteadas em locais repetidos, não é certo o número de loops
        a = randrange(0,len(campo))         #   sorteio das coordenadas 
        b = randrange(0,len(campo[0]))
        if campo[a][b] < 9:                 #   verifica se não há bomba na coordenada sorteada
            campo[a][b] = 9
            dicas(campo,a,b)                #   põe dicas em volta da bomba
            i += 1                          #   caso haja bomba, a iteração não é contada

def zeros(matriz, matriz2, a, b):
    for par in adjacentes:
        try:
            if a+par[0] < 0 or b+par[1] < 0:                                #   impede que coordenadas como matriz[-1] sejam acessadas
                continue
            if matriz[a+par[0]][b+par[1]] == ponto:                           
                matriz[a+par[0]][b+par[1]] = matriz2[a+par[0]][b+par[1]]    #   revela as casas escondidas
                if matriz[a+par[0]][b+par[1]] == 0:                         #   cada zero adjacente revelará todos os vizinhos
                    zeros(matriz , matriz2, a+par[0] , b+par[1])
        except IndexError:
            pass

def gerarMatriz(altura, largura, elemento):
    matriz = []
    for _ in range(0,altura):
        linha = []
        for _ in range(0,largura):
            linha.append(elemento)
        matriz.append(linha)
    return matriz

def obterOpcao():
    while True:
        opcao = input(" Deseja abrir(a) ou colocar bandeira(b): ")
        if opcao == 'a':
            return 1
        elif opcao == 'b':
            return 2
        print(" Digite uma opcao válida")

def obterValores():
    try:
        a = int(input(" Digite a linha: "))
        b = int(input(" Digite a coluna: "))
        
        if a >= 0 and a < ALTURA and b >= 0 and b < LARGURA:        #   verifica se a coordenada esta dentro do alcance
            return False, a, b
        print(" Digite um numero que está nas colunas e linhas.")
        sleep(1.5)
    except ValueError:
        print(" Tipo de valor inválido")
        sleep(1.5)
    return True, 0, 0

def verifVitoria(matriz):               #   vai contar quantos espaçoes estão revelados
    count = 0
    for i in range(0,ALTURA):
        for j in range(0,LARGURA):
            if type(matriz[i][j]) == type(str()):
                count += 1
    return count

def main():
    
    campo = gerarMatriz(ALTURA, LARGURA, 0)             #   gerar matriz não vista do campo minado com bordas a mais
    
    campoEscondido = gerarMatriz(ALTURA, LARGURA, ponto)#   cria um campo com todas as posições escondidas
    
    gerarBombas(campo, BOMBAS)                          #   posiciona n bombas na matriz campo
    
    for i in range(0, ALTURA):                          #   embelezar (troca as bombas, numeros >s que 8 por um X)
        for j in range(0, LARGURA):
            if campo[i][j] > 8:                         #   apenas bombas podem ser >s que 8
                campo[i][j] = bomba

    while True:                                         #   loop principal do jogo
        GetValues = True
        while GetValues:                                #   loop para obter a escolha do jogador

            imprimirJogo(campoEscondido)                #   atualiza o campo para o jogador ver o estado atual
            
            GetValues, a, b = obterValores()            

        if obterOpcao() == 1:
            campoEscondido[a][b] = campo[a][b]          #   a coordenada digitada é passada para a tela visível
            
            if campo[a][b] == 0:                        #   se tiver valor zero, tudo em volta é revelado, o mesmo para zeros adjacentes
                zeros(campoEscondido, campo, a, b)

            if campo[a][b] == bomba:                    #   o jogador perde se atingir uma bomba
                imprimirJogo(campo)                     #   para o jogador possa ver onde errou
                print(" VOCÊ PERDEU !")
                break

            if verifVitoria(campoEscondido) == BOMBAS:  #   verifica se venceu
                imprimirJogo(campo)
                print(" VOCE VENCEU !!")
                break

        else:
            if campoEscondido[a][b] == ponto:           #   colocar bandeira
                campoEscondido[a][b] = bandeira
            elif campoEscondido[a][b] == bandeira:      #   tirar bandeira
                campoEscondido[a][b] = ponto

if __name__ == "__main__":
    main()