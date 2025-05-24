import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import requests
from PIL import Image

# --- Logo na sidebar ---
logo = Image.open("assets/santander_logo.png")
st.sidebar.image(logo, width=160)
st.sidebar.markdown("---")

# --- Filtros na sidebar ---
st.sidebar.header("Filtros")
anos = [2022, 2023, 2024]
periodo = st.sidebar.selectbox("Período (Ano)", anos)
regiao = st.sidebar.selectbox("Região", ["Todas", "Sudeste", "Sul", "Nordeste", "Centro-Oeste", "Norte"])
setores = ["Comércio", "Serviços", "Indústria", "Tecnologia", "Saúde"]
setor = st.sidebar.selectbox("Setor de Atuação", ["Todos"] + setores)
portes = ["Pequena", "Média", "Grande"]
porte = st.sidebar.selectbox("Porte da Empresa", ["Todos"] + portes)
meses = list(range(1, 13))
mes = st.sidebar.selectbox("Mês", ["Todos"] + meses)
riscos = ["Baixo", "Médio", "Alto"]
risco_credito = st.sidebar.selectbox("Risco de Crédito", ["Todos"] + riscos)
perfil_pagamento = st.sidebar.selectbox("Perfil de Pagamento", ["Todos", "Pontual", "Atrasado", "Inadimplente"])

# --- Dados simulados ---
estados = ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG",
           "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"]

regioes_map = {
    "AC": "Norte", "AL": "Nordeste", "AP": "Norte", "AM": "Norte", "BA": "Nordeste",
    "CE": "Nordeste", "DF": "Centro-Oeste", "ES": "Sudeste", "GO": "Centro-Oeste",
    "MA": "Nordeste", "MT": "Centro-Oeste", "MS": "Centro-Oeste", "MG": "Sudeste",
    "PA": "Norte", "PB": "Nordeste", "PR": "Sul", "PE": "Nordeste", "PI": "Nordeste",
    "RJ": "Sudeste", "RN": "Nordeste", "RS": "Sul", "RO": "Norte", "RR": "Norte",
    "SC": "Sul", "SP": "Sudeste", "SE": "Nordeste", "TO": "Norte"
}

np.random.seed(42)
dados = []
for ano in anos:
    for mes_num in range(1, 13):
        for estado in estados:
            for s in setores:
                for p in portes:
                    dados.append({
                        "Ano": ano,
                        "Mês": mes_num,
                        "Estado": estado,
                        "Região": regioes_map[estado],
                        "Setor": s,
                        "Porte": p,
                        "Receita": np.random.normal(200000, 50000),
                        "VolumeTransacoes": np.random.randint(100, 1000),
                        "FluxoCaixa": np.random.normal(50000, 20000),
                        "ClientesAtivos": np.random.randint(50, 500),
                        "RiscoCredito": np.random.choice(riscos),
                        "PerfilPagamento": np.random.choice(["Pontual", "Atrasado", "Inadimplente"])
                    })
df = pd.DataFrame(dados)

# --- Aplicar filtros ---
df_filtrado = df[df["Ano"] == periodo]
if regiao != "Todas":
    df_filtrado = df_filtrado[df_filtrado["Região"] == regiao]
if setor != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Setor"] == setor]
if porte != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Porte"] == porte]
if mes != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Mês"] == mes]
if risco_credito != "Todos":
    df_filtrado = df_filtrado[df_filtrado["RiscoCredito"] == risco_credito]
if perfil_pagamento != "Todos":
    df_filtrado = df_filtrado[df_filtrado["PerfilPagamento"] == perfil_pagamento]

# --- Título ---
st.markdown("""
    <h1 style='color:#ec0000;'>Painel Estratégico do Cliente PJ - Santander</h1>
    <p style='color:#555;'>Análise integrada de indicadores financeiros e operacionais de empresas clientes do Santander</p>
    <hr>
""", unsafe_allow_html=True)

# --- KPIs ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Receita Média", f"R$ {df_filtrado['Receita'].mean():,.0f}" if not df_filtrado.empty else "N/A")
col2.metric("Transações Médias", f"{df_filtrado['VolumeTransacoes'].mean():,.0f}" if not df_filtrado.empty else "N/A")
col3.metric("Fluxo de Caixa Médio", f"R$ {df_filtrado['FluxoCaixa'].mean():,.0f}" if not df_filtrado.empty else "N/A")
col4.metric("Clientes Ativos", f"{df_filtrado['ClientesAtivos'].sum():,.0f}" if not df_filtrado.empty else "N/A")

# --- Gráfico de linha: Receita mensal ---
st.subheader("Evolução Mensal da Receita")
receita_mes = df_filtrado.groupby("Mês")["Receita"].mean().reset_index()
fig1 = px.line(receita_mes, x="Mês", y="Receita", markers=True, title="Receita Média por Mês",
               color_discrete_sequence=["#ec0000"])
st.plotly_chart(fig1, use_container_width=True)

# --- Gráfico de barras: Receita por setor ---
st.subheader("Receita Média por Setor")
receita_setor = df_filtrado.groupby("Setor")["Receita"].mean().reset_index()
fig2 = px.bar(receita_setor, x="Setor", y="Receita", title="Comparativo por Setor",
              color_discrete_sequence=["#ec0000"])
st.plotly_chart(fig2, use_container_width=True)

# --- Gráfico de caixa: Fluxo de Caixa por Porte ---
st.subheader("Distribuição do Fluxo de Caixa por Porte")
fig_box = px.box(df_filtrado, x="Porte", y="FluxoCaixa", color_discrete_sequence=["#ec0000"],
                 title="Distribuição do Fluxo de Caixa por Porte")
st.plotly_chart(fig_box, use_container_width=True)

# --- Novo gráfico: Receita por risco de crédito ---
st.subheader("Receita Média por Risco de Crédito")
receita_risco = df_filtrado.groupby("RiscoCredito")["Receita"].mean().reset_index()
fig_risco = px.bar(receita_risco, x="RiscoCredito", y="Receita", title="Receita por Risco de Crédito",
                   color_discrete_sequence=["#ec0000"])
st.plotly_chart(fig_risco, use_container_width=True)

# --- Novo gráfico: Receita por perfil de pagamento ---
st.subheader("Receita Média por Perfil de Pagamento")
receita_pgto = df_filtrado.groupby("PerfilPagamento")["Receita"].mean().reset_index()
fig_pgto = px.bar(receita_pgto, x="PerfilPagamento", y="Receita", title="Receita por Perfil de Pagamento",
                  color_discrete_sequence=["#ec0000"])
st.plotly_chart(fig_pgto, use_container_width=True)

# --- Mapa ---
st.subheader("Mapa de Receita por Estado")
url_geojson = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson"
geojson = requests.get(url_geojson).json()

receita_estado = df[df["Ano"] == periodo].groupby("Estado")["Receita"].mean().reset_index()
fig3 = px.choropleth(receita_estado,
                     geojson=geojson,
                     locations="Estado",
                     featureidkey="properties.sigla",
                     color="Receita",
                     color_continuous_scale="Reds",
                     scope="south america",
                     title="Receita Média por Estado")
fig3.update_geos(fitbounds="locations", visible=False)
st.plotly_chart(fig3, use_container_width=True)

# --- Rodapé ---
st.markdown("""
    <hr>
    <p style="text-align:center;color:#999;font-size:14px;">
    © 2025 Banco Santander Brasil S.A. | Painel de Análise de Perfil PJ (protótipo educacional)
    </p>
""", unsafe_allow_html=True)
