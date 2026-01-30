import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Carregar dados
df = pd.read_excel("resultado_classificacao.xlsx")

st.title("Dashboard de Classificação de Pedidos e-SIC")

# Gráfico de pizza
st.subheader("Distribuição dos Pedidos")
contagem = df["classificação"].value_counts()
fig1, ax1 = plt.subplots()
ax1.pie(contagem, labels=contagem.index, autopct="%1.1f%%", startangle=90)
st.pyplot(fig1)

# Gráfico de barras
st.subheader("Tipos de Dados Pessoais Detectados")
dados = {
    "CPF": df["contém_CPF"].sum(),
    "RG": df["contém_RG"].sum(),
    "Telefone": df["contém_Telefone"].sum(),
    "Nome": df["contém_Nome"].sum()
}
fig2, ax2 = plt.subplots()
ax2.bar(dados.keys(), dados.values(), color=["blue","orange","green","red"])
st.pyplot(fig2)

# Tabela resumo
st.subheader("Resumo dos Dados Pessoais Detectados")
st.table(pd.DataFrame(dados.items(), columns=["Tipo de Dado", "Quantidade"]))

import io

st.subheader("Baixar resultado em Excel")

# Criar buffer de memória com o Excel
excel_buffer = io.BytesIO()
df.to_excel(excel_buffer, index=False)
excel_buffer.seek(0)

# Botão de download
st.download_button(
    label="📥 Baixar resultado_classificacao.xlsx",
    data=excel_buffer,
    file_name="resultado_classificacao.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
