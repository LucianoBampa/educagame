import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

st.set_page_config(
    page_title="EducaGames — Dashboard",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
<style>
    .metric-card {
        background: #1F3F73;
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .stMetric { background: #f8f9fa; border-radius: 10px; padding: 10px; }
    div[data-testid="stMetricValue"] { font-size: 2rem; color: #1F3F73; }
</style>
""", unsafe_allow_html=True)

API_URL = "http://127.0.0.1:8000/api/internal"
st_autorefresh(interval=15000, key="refresh")

# ---------------- API STATUS ----------------

def check_api():
    try:
        return requests.get(f"{API_URL}/health", timeout=2).status_code == 200
    except:
        return False

col1, col2 = st.sidebar.columns([3, 1])
with col1:
    if check_api():
        st.success("API Online")
    else:
        st.error("API Offline")
with col2:
    if st.button("↻"):
        st.rerun()

# ---------------- GET DATA ----------------

def get_data(endpoint):
    try:
        r = requests.get(f"{API_URL}/{endpoint}/")
        r.raise_for_status()
        data = r.json()
        return pd.DataFrame(data) if data else pd.DataFrame()
    except:
        st.error(f"Erro ao buscar {endpoint}")
        st.stop()

turmas  = get_data("turmas")
jogos   = get_data("jogos")
sessoes = get_data("sessoes")
alunos  = get_data("alunos")

if sessoes.empty:
    st.title("🎓 EducaGames — Dashboard do Professor")
    st.info("Nenhuma sessão registrada ainda. Jogue uma partida para ver os dados aqui!")
    st.stop()

# ---------------- PREPARAR DATAFRAMES ----------------

if alunos.empty:
    alunos = pd.DataFrame(columns=["id", "nome", "turma_id", "ra"])
if turmas.empty:
    turmas = pd.DataFrame(columns=["id", "ano", "turma"])
if jogos.empty:
    jogos = pd.DataFrame(columns=["id", "nome"])

alunos_df = alunos.rename(columns={"id": "aluno_id_ref", "nome": "aluno_nome"})
turmas_df = turmas.rename(columns={"id": "turma_id_ref"})
jogos_df  = jogos.rename(columns={"id": "jogo_id_ref", "nome": "jogo_nome"})

df = sessoes.merge(
    alunos_df[["aluno_id_ref", "aluno_nome", "turma_id", "ra"]],
    left_on="aluno_id", right_on="aluno_id_ref", how="left"
)
df = df.merge(
    turmas_df[["turma_id_ref", "ano", "turma"]],
    left_on="turma_id", right_on="turma_id_ref", how="left"
)
df = df.merge(
    jogos_df[["jogo_id_ref", "jogo_nome"]],
    left_on="jogo_id", right_on="jogo_id_ref", how="left"
)
df.drop(columns=["aluno_id_ref", "turma_id_ref", "jogo_id_ref"], inplace=True, errors="ignore")

df["data_execucao"] = pd.to_datetime(df["data_execucao"], format="mixed", errors="coerce")
df["tempo_segundos"] = pd.to_numeric(df["tempo_total"], errors="coerce").fillna(0)
df["acertos"]  = pd.to_numeric(df["acertos"],  errors="coerce").fillna(0)
df["erros"]    = pd.to_numeric(df["erros"],    errors="coerce").fillna(0)
df["pontuacao"] = pd.to_numeric(df["pontuacao"], errors="coerce").fillna(0)
df["total_tentativas"] = df["acertos"] + df["erros"]
df["aproveitamento"] = (df["acertos"] / df["total_tentativas"].replace(0, 1) * 100).round(1)

def segundos_para_mmss(s):
    try:
        s = int(s)
        return f"{s // 60:02d}:{s % 60:02d}"
    except:
        return "00:00"

df["tempo_fmt"] = df["tempo_segundos"].apply(segundos_para_mmss)

# ---------------- FILTROS ----------------

st.sidebar.title("🔍 Filtros")

data_min = df["data_execucao"].min().date()
data_max = df["data_execucao"].max().date()

periodo = st.sidebar.date_input("Período", value=(data_min, data_max),
                                 min_value=data_min, max_value=data_max)

ra_sel     = st.sidebar.text_input("RA do Aluno")
anos_sel   = st.sidebar.multiselect("Ano Letivo", sorted(df["ano"].dropna().unique()))
turma_sel  = st.sidebar.multiselect("Turma", sorted(df["turma"].dropna().unique()))
jogos_sel  = st.sidebar.multiselect("Jogo", sorted(df["jogo_nome"].dropna().unique()))
dif_sel    = st.sidebar.multiselect("Dificuldade", sorted(df["dificuldade"].dropna().unique()))

df_f = df.copy()

if isinstance(periodo, tuple) and len(periodo) == 2:
    df_f = df_f[(df_f["data_execucao"].dt.date >= periodo[0]) &
                (df_f["data_execucao"].dt.date <= periodo[1])]
if ra_sel:
    df_f = df_f[df_f["ra"].str.contains(ra_sel, case=False, na=False)]
if anos_sel:
    df_f = df_f[df_f["ano"].isin(anos_sel)]
if turma_sel:
    df_f = df_f[df_f["turma"].isin(turma_sel)]
if jogos_sel:
    df_f = df_f[df_f["jogo_nome"].isin(jogos_sel)]
if dif_sel:
    df_f = df_f[df_f["dificuldade"].isin(dif_sel)]

# ---------------- DOWNLOAD ----------------

@st.dialog("Exportar dados")
def download_dialog():
    st.download_button("📥 Baixar CSV",
        data=df_f.to_csv(index=False).encode("utf-8"),
        file_name=f"educagames_{datetime.now().strftime('%Y-%m-%d')}.csv",
        mime="text/csv")

st.sidebar.divider()
st.sidebar.button("📥 Exportar CSV", on_click=download_dialog)

# ════════════════════════════════════════════════════════════════
#  DASHBOARD
# ════════════════════════════════════════════════════════════════

st.title("🎓 EducaGames — Dashboard do Professor")
st.caption(f"Atualizado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}  |  {len(df_f)} sessões exibidas")

# ── KPIs ────────────────────────────────────────────────────────
k1, k2, k3, k4, k5, k6 = st.columns(6)
k1.metric("📋 Sessões",        len(df_f))
k2.metric("👥 Alunos únicos",  df_f["ra"].nunique())
k3.metric("🏫 Turmas",         df_f["turma"].nunique())
k4.metric("⏱️ Tempo Médio",    segundos_para_mmss(df_f["tempo_segundos"].mean() or 0))
k5.metric("✅ Acertos Totais", int(df_f["acertos"].sum()))
k6.metric("🎯 Aproveitamento", f"{df_f['aproveitamento'].mean():.1f}%")

st.divider()

# ── LINHA 1: Sessões por dia + Sessões por jogo ──────────────────
c1, c2 = st.columns([2, 1])

with c1:
    st.subheader("📅 Sessões por Dia")
    por_dia = df_f.groupby(df_f["data_execucao"].dt.date).size().reset_index(name="sessoes")
    fig = px.line(por_dia, x="data_execucao", y="sessoes",
                  markers=True, color_discrete_sequence=["#F28C28"])
    fig.update_layout(xaxis_title="Data", yaxis_title="Sessões",
                      plot_bgcolor="white", height=300)
    fig.update_xaxes(showgrid=True, gridcolor="#eee")
    fig.update_yaxes(showgrid=True, gridcolor="#eee")
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.subheader("🎮 Sessões por Jogo")
    por_jogo = df_f.groupby("jogo_nome").size().reset_index(name="total")
    fig = px.pie(por_jogo, values="total", names="jogo_nome",
                 color_discrete_sequence=["#1F3F73", "#F28C28", "#27AE60", "#E74C3C"])
    fig.update_layout(height=300, showlegend=True)
    st.plotly_chart(fig, use_container_width=True)

# ── LINHA 2: Aproveitamento por turma + por dificuldade ──────────
c3, c4 = st.columns(2)

with c3:
    st.subheader("🏫 Aproveitamento por Turma")
    por_turma = df_f.groupby("turma").agg(
        aproveitamento=("aproveitamento", "mean"),
        sessoes=("id", "count")
    ).reset_index().sort_values("aproveitamento", ascending=False)
    fig = px.bar(por_turma, x="turma", y="aproveitamento",
                 text="aproveitamento", color="aproveitamento",
                 color_continuous_scale=["#E74C3C", "#F28C28", "#27AE60"],
                 range_color=[0, 100])
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig.update_layout(yaxis_title="Aproveitamento (%)", xaxis_title="Turma",
                      plot_bgcolor="white", height=320, showlegend=False,
                      coloraxis_showscale=False)
    fig.update_yaxes(range=[0, 110], showgrid=True, gridcolor="#eee")
    st.plotly_chart(fig, use_container_width=True)

with c4:
    st.subheader("📊 Aproveitamento por Dificuldade")
    por_dif = df_f.groupby("dificuldade").agg(
        aproveitamento=("aproveitamento", "mean"),
        sessoes=("id", "count")
    ).reset_index().dropna(subset=["dificuldade"])

    ordem = {"facil": 1, "medio": 2, "normal": 3, "dificil": 4, "muito_dificil": 5, "chucknorris": 6}
    por_dif["ordem"] = por_dif["dificuldade"].map(ordem).fillna(99)
    por_dif = por_dif.sort_values("ordem")

    fig = px.bar(por_dif, x="dificuldade", y="aproveitamento",
                 text="aproveitamento", color="dificuldade",
                 color_discrete_map={
                     "facil": "#27AE60", "medio": "#F28C28", "normal": "#3498DB",
                     "dificil": "#E74C3C", "muito_dificil": "#8E44AD", "chucknorris": "#2C3E50"
                 })
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig.update_layout(yaxis_title="Aproveitamento (%)", xaxis_title="Dificuldade",
                      plot_bgcolor="white", height=320, showlegend=False)
    fig.update_yaxes(range=[0, 110], showgrid=True, gridcolor="#eee")
    st.plotly_chart(fig, use_container_width=True)

# ── LINHA 3: Ranking de alunos ───────────────────────────────────
st.subheader("🏆 Ranking de Alunos")

ranking = df_f.groupby(["ra", "aluno_nome"]).agg(
    sessoes      =("id",            "count"),
    pontuacao    =("pontuacao",     "sum"),
    aproveitamento=("aproveitamento","mean"),
    tempo_total  =("tempo_segundos","sum"),
    acertos      =("acertos",       "sum"),
    erros        =("erros",         "sum"),
).reset_index().sort_values("pontuacao", ascending=False).reset_index(drop=True)

ranking.index += 1
ranking["aproveitamento"] = ranking["aproveitamento"].round(1).astype(str) + "%"
ranking["tempo_total"]    = ranking["tempo_total"].apply(segundos_para_mmss)
ranking["aluno"] = ranking["aluno_nome"] + " (" + ranking["ra"] + ")"

st.dataframe(
    ranking[["aluno", "sessoes", "pontuacao", "aproveitamento", "acertos", "erros", "tempo_total"]]
    .rename(columns={
        "aluno":          "Aluno (RA)",
        "sessoes":        "Sessões",
        "pontuacao":      "Pontuação Total",
        "aproveitamento": "Aproveitamento",
        "acertos":        "Acertos",
        "erros":          "Erros",
        "tempo_total":    "Tempo Total",
    }),
    use_container_width=True,
    height=300
)

# ── LINHA 4: Tabela detalhada ────────────────────────────────────
st.divider()
st.subheader("📋 Dados Detalhados")

df_exibir = df_f.copy()
df_exibir["aluno_exibir"] = df_exibir["aluno_nome"] + " (" + df_exibir["ra"].fillna("") + ")"

st.dataframe(
    df_exibir[[
        "aluno_exibir", "ano", "turma", "jogo_nome", "palavra",
        "dificuldade", "tempo_fmt", "acertos", "erros",
        "aproveitamento", "pontuacao", "data_execucao"
    ]].rename(columns={
        "aluno_exibir":  "Aluno (RA)",
        "ano":           "Ano",
        "turma":         "Turma",
        "jogo_nome":     "Jogo",
        "palavra":       "Palavras",
        "dificuldade":   "Dificuldade",
        "tempo_fmt":     "Tempo",
        "acertos":       "Acertos",
        "erros":         "Erros",
        "aproveitamento":"Aproveit. %",
        "pontuacao":     "Pontuação",
        "data_execucao": "Data",
    }),
    use_container_width=True
)