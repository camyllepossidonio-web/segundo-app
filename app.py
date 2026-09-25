import pandas as pd
import streamlit as st

# Configuração da página (deve ser o primeiro comando do Streamlit)
st.set_page_config(
    page_title="Simulador de Custos e Orçamento",
    page_icon="💰",
    layout="wide",
)

# 1. Base de Dados Interna (12 despesas simuladas)
@st.cache_data
def carregar_dados():
    data = {
        "Item": [
            "Aço Galvanizado",
            "Placas de Circuito",
            "Solda Especial",
            "Desenvolvedor Sênior",
            "Designer UI/UX",
            "Frete Nacional",
            "Armazenamento em Nuvem",
            "Energia Elétrica",
            "Kit de Ferramentas",
            "Manutenção de Equipamentos",
            "Consultoria Jurídica",
            "Marketing Inicial",
        ],
        "Categoria": [
            "Matéria-Prima",
            "Matéria-Prima",
            "Matéria-Prima",
            "Mão de Obra",
            "Mão de Obra",
            "Logística",
            "Logística",
            "Energia",
            "Ferramentas",
            "Ferramentas",
            "Mão de Obra",
            "Logística",
        ],
        "Valor (R$)": [
            4500.0, 3200.0, 800.0, 6500.0, 4000.0, 1200.0,
            600.0, 950.0, 1500.0, 1100.0, 2500.0, 1800.0,
        ],
        "Prioridade": [
            "Alta", "Alta", "Média", "Alta", "Média", "Média",
            "Baixa", "Baixa", "Média", "Baixa", "Alta", "Média",
        ],
    }
    return pd.DataFrame(data)

df_base = carregar_dados()

# 2. Barra Lateral (Sidebar)
st.sidebar.header("⚙️ Configurações")

orcamento_total = st.sidebar.slider(
    "Orçamento Total Disponível",
    min_value=5000.0,
    max_value=50000.0,
    value=20000.0,
    step=500.0,
    format="R$ %.2f",
)

categorias_disponiveis = df_base["Categoria"].unique().tolist()
categorias_selecionadas = st.sidebar.multiselect(
    "Filtrar por Categoria",
    options=categorias_disponiveis,
    default=categorias_disponiveis,
)

# Filtragem do DataFrame
if categorias_selecionadas:
    df_filtrado = df_base[df_base["Categoria"].isin(categorias_selecionadas)]
else:
    df_filtrado = df_base.iloc[0:0]  # DataFrame vazio se nada for selecionado

# 3. Área Principal
st.title("💰 Simulador de Custos e Orçamento")
st.markdown(
    "Gerencie despesas, analise categorias e monitore o saldo do seu projeto em tempo real."
)

# Cálculos acumulados
gasto_filtrado = df_filtrado["Valor (R$)"].sum()
saldo_restante = orcamento_total - gasto_filtrado

# Painel de Métricas (st.columns e st.metric)
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Orçamento Definido", value=f"R$ {orcamento_total:,.2f}")

with col2:
    st.metric(label="Gasto Filtrado", value=f"R$ {gasto_filtrado:,.2f}")

with col3:
    st.metric(
        label="Saldo Restante",
        value=f"R$ {saldo_restante:,.2f}",
        delta=f"R$ {saldo_restante:,.2f}",
        delta_color="normal" if saldo_restante >= 0 else "inverse",
    )

st.markdown("---")

# Alerta Visual Condicional
if gasto_filtrado <= orcamento_total:
    st.success(
        f"✅ **Projeto dentro da meta!** Você ainda possui R$ {saldo_restante:,.2f} disponíveis no orçamento atual."
    )
else:
    excesso = abs(saldo_restante)
    st.error(
        f"⚠️ **Atenção!** O orçamento foi ultrapassado em R$ {excesso:,.2f}. Reveja os itens selecionados."
    )

# Layoutdividido para Gráfico e Tabela
col_grafico, col_tabela = st.columns(2)

with col_grafico:
    st.subheader("📊 Gastos por Categoria")
    if not df_filtrado.empty:
        # Agrupando dados para o gráfico nativo
        df_grouped = df_filtrado.groupby("Categoria")["Valor (R$)"].sum()
        st.bar_chart(df_grouped)
    else:
        st.info("Nenhuma categoria selecionada para exibir o gráfico.")

with col_tabela:
    st.subheader("📋 Detalhamento dos Itens")
    st.dataframe(df_filtrado, use_container_width=True, hide_index=True)
  
