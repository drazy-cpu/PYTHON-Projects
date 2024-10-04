def gerar_matriz(N):
    num_linhas = 2 ** N
    matriz = []

    # Preenche a matriz com combinações binárias
    for i in range(num_linhas):
        linha = []
        for j in range(N):
            valor = (i // (2 ** (N - j - 1))) % 2
            linha.append(valor)
        matriz.append(linha)

    return matriz

def exibir_matriz(matriz):
    for linha in matriz:
        print(" ".join(map(str, linha)))


def main():
    N = int(input("Digite o número de variáveis lógicas (N): "))

    # Gera e exibe a matriz
    matriz = gerar_matriz(N)
    exibir_matriz(matriz)

if __name__ == "__main__":
    main()
