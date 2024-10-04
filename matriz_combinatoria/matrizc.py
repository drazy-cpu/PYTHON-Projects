def gerar_combinacoes(elementos, tamanho):
    def encontrar_combinacao(elementos, combinacao_parcial, tamanho, inicio):
        if tamanho == 0:
            combinacoes_finalizadas.append(combinacao_parcial)
            return
        for i in range(inicio, len(elementos)):
            nova_combinacao = combinacao_parcial + ',' + elementos[i] if combinacao_parcial else elementos[i]
            encontrar_combinacao(elementos, nova_combinacao, tamanho - 1, i + 1)

    combinacoes_finalizadas = []
    encontrar_combinacao(elementos, "", tamanho, 0)  # Gera combinações com tamanho exato
    return combinacoes_finalizadas

# Entrada de dados do usuário
entrada_usuario = input("Informe os elementos (separados por vírgula): ")
tamanho_combinacao = int(input("Informe o número exato de elementos nas combinações: "))

# Converte a entrada em uma lista de elementos
lista_elementos = entrada_usuario.split(',')

# Gera as combinações
resultado_combinacoes = gerar_combinacoes(lista_elementos, tamanho_combinacao)

# Exibe o resultado
for combinacao in resultado_combinacoes:
    print(f"{{{combinacao}}}")

