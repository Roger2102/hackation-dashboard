import pandas as pd
import re

print('Carregando arquivos AMOSTRA_e-SIC.xlsx...')

# 1. Carregar o arquivo CSV ou Excel
# Substitua pelo caminho do arquivo baixado da amostra
df = pd.read_excel("AMOSTRA_e-SIC.xlsx")

print('Detectando dados pessoais nos pedidos...')

# 2. Funções para detectar padrões de dados pessoais
def detect_cpf(texto):
    # Padrão de CPF: 000.000.000-00
    return bool(re.search(r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b", str(texto)))

def detect_rg(texto):
    # Padrão simples de RG (números com 7 a 9 dígitos)
    return bool(re.search(r"\b\d{7,9}\b", str(texto)))

def detect_telefone(texto):
    # Padrão de telefone brasileiro
    return bool(re.search(r"\(?\d{2}\)?\s?\d{4,5}-\d{4}", str(texto)))

def detect_nome(texto):
    # Detecta palavras com inicial maiúscula seguidas de sobrenome
    return bool(re.search(r"\b[A-Z][a-z]+ [A-Z][a-z]+\b", str(texto)))

# 3. Aplicar as funções em cada pedido
df["contém_CPF"] = df["Texto Mascarado"].apply(detect_cpf)
df["contém_RG"] = df["Texto Mascarado"].apply(detect_rg)
df["contém_Telefone"] = df["Texto Mascarado"].apply(detect_telefone)
df["contém_Nome"] = df["Texto Mascarado"].apply(detect_nome)

print('Classificando os pedidos...')

# 4. Criar uma coluna de classificação
def classificar(row):
    if row["contém_CPF"] or row["contém_RG"] or row["contém_Telefone"] or row["contém_Nome"]:
        return "Não Público"
    else:
        return "Público"

df["classificação"] = df.apply(classificar, axis=1)

# 5. Exportar resultados
df.to_excel("resultado_classificacao.xlsx", index=False)

print('Classificação concluída. Resultados salvos em resultado_classificacao.xlsx.')
