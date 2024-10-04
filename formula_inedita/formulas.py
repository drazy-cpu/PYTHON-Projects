import sympy as sp

def calcular_coeficiente(m, j):  # O coeficiente a(m-j) é calculado
    k = sp.symbols('k', integer=True)
    somatorio = sp.Sum((-1) ** k * sp.binomial(j, k) * (1 - k + j) ** m, (k, 0, j)).doit()
    return somatorio

def calcular_formula(m):  # A fórmula da soma das potências é gerada
    n = sp.symbols('n', integer=True)
    resultado = 0
    for j in range(m + 1):
        coeficiente = calcular_coeficiente(m, j)
        termo_formula = sp.binomial(n, j + 1) * coeficiente
        resultado += termo_formula

    # Simplifica a expressão final para uma forma mais compacta
    formula_simplificada = sp.simplify(resultado)
    return formula_simplificada

m = int(input("Digite o valor de m: "))

formula_final = calcular_formula(m)

# Exibe a fórmula gerada de forma visualmente agradável
sp.pretty_print(formula_final, use_unicode=True)
