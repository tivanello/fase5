# app_risco_futuro.py
import streamlit as st
import pandas as pd
import joblib
import json

from pathlib import Path


# CONFIGURAÇÃO
# ======================

st.set_page_config(page_title="App Risco Futuro", page_icon="📊", layout="centered")

BASE_DIR = Path(__file__).resolve().parents[1]   # volta pra raiz do projeto
MODEL_PATH = BASE_DIR / "models" / "modelo_risco_futuro_c1.joblib"
COLUNAS_PATH = BASE_DIR / "models" / "colunas_modelo_risco_futuro_c1.json"
METADATA_PATH = BASE_DIR / "models" / "metadata_modelo_risco_futuro_c1.json"

st.markdown(
    "<style>div[role='listbox'] ul{background-color: #6e42ad};</style>",
    unsafe_allow_html=True
)

st.markdown(
    "<h1 style='text-align: center;'>Predição de Risco Futuro de Defasagem 📊</h1>",
    unsafe_allow_html=True
)

st.markdown("""
<div style="
    background-color: rgba(33,150,243,0.15);
    border-left: 6px solid rgba(33,150,243,1);
    padding: 12px 16px;
    border-radius: 6px;
    text-align: center;
">
    Envie sua base de alunos em <b>CSV</b> para analisar o risco futuro de defasagem.<br>
    O app irá identificar os alunos <b>com</b> e <b>sem previsão de defasagem</b>.
</div>
""", unsafe_allow_html=True)


# CARREGAMENTO DOS ARTEFATOS
# ======================

@st.cache_resource
def carregar_modelo(caminho):
    return joblib.load(caminho)

@st.cache_data
def carregar_json(caminho):
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)

try:
    model = carregar_modelo(MODEL_PATH)
    colunas_info = carregar_json(COLUNAS_PATH)
    metadata = carregar_json(METADATA_PATH)

    if isinstance(colunas_info, list):
        feature_columns = colunas_info
    elif isinstance(colunas_info, dict):
        feature_columns = colunas_info.get("colunas_modelo", [])
    else:
        raise TypeError("Formato inválido no arquivo de colunas.")

    threshold = float(metadata.get("threshold_final", 0.70))

except Exception as e:
    st.error(f"Erro ao carregar os artefatos do modelo.\n\n{e}")
    st.stop()


# FUNÇÕES AUXILIARES
# ======================

def validar_colunas(df, colunas_esperadas):
    faltando = [c for c in colunas_esperadas if c not in df.columns]
    extras = [c for c in df.columns if c not in colunas_esperadas]
    return faltando, extras

def preparar_dataframe(df, colunas_esperadas):
    df = df.copy()

    # mantém apenas as colunas esperadas e na ordem correta
    df = df[colunas_esperadas]

    colunas_numericas = [
        "ano_base",
        "IDA",
        "IEG",
        "IAA",
        "IPS",
        "IPP",
        "IPV",
        "idade_geral",
        "Ano ingresso",
        "Fase_num",
        "FaseIdeal_num",
        "target_defasagem_atual",
    ]

    for col in colunas_numericas:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "Gênero" in df.columns:
        df["Gênero"] = df["Gênero"].astype(str).str.strip()

    if "inst_ensino_cat" in df.columns:
        df["inst_ensino_cat"] = df["inst_ensino_cat"].astype(str).str.strip()

    return df


# ENTRADA DE DADOS
# ======================

aba1, aba2 = st.tabs(["Avaliação em grupo", "Avaliação individual"])

st.write("## Envio da base")

arquivo = st.file_uploader("Selecione o arquivo CSV", type=["csv"])

if arquivo is not None:
    try:
        df_input = pd.read_csv(arquivo)
    except Exception as e:
        st.error(f"Erro ao ler o arquivo CSV.\n\n{e}")
        st.stop()

    st.write("## Pré-visualização da base enviada")
    st.dataframe(df_input.head())

    faltando, extras = validar_colunas(df_input, feature_columns)

    if faltando:
        st.error(f"Faltam colunas exigidas pelo modelo: {faltando}")
        st.stop()

    if extras:
        if extras == ["RA"] or "RA" in extras:
            st.success(
                "Coluna de identificação detectada (RA). "
                "Ela não é usada pelo modelo, mas será mantida no resultado para identificar os alunos."
            )
        else:
            st.info(
                f"Colunas adicionais encontradas: {extras}. "
                "Essas colunas não entram no cálculo do modelo, mas serão preservadas na saída."
            )

    X_novo = preparar_dataframe(df_input, feature_columns)

    if st.button("Avaliar"):
        try:
            if not hasattr(model, "predict_proba"):
                st.error("O modelo não possui predict_proba(). Verifique o artefato salvo.")
                st.stop()

            probas = model.predict_proba(X_novo)[:, 1]
            preds = (probas >= threshold).astype(int)

            df_resultado = df_input.copy()
            df_resultado["prob_risco_futuro"] = probas
            df_resultado["classe_risco_futuro"] = preds

            qtd_risco = int(df_resultado["classe_risco_futuro"].sum())
            qtd_sem_risco = int((df_resultado["classe_risco_futuro"] == 0).sum())
            perc_risco = (df_resultado["classe_risco_futuro"].mean() * 100) if len(df_resultado) > 0 else 0

            df_com_risco = df_resultado[df_resultado["classe_risco_futuro"] == 1].copy()
            df_sem_risco = df_resultado[df_resultado["classe_risco_futuro"] == 0].copy()

            df_com_risco = df_com_risco.sort_values("prob_risco_futuro", ascending=False)
            df_sem_risco = df_sem_risco.sort_values("prob_risco_futuro", ascending=False)

            if qtd_risco > 0:
                st.warning(f"### Resultado: {qtd_risco} aluno(s) com previsão de defasagem")
            else:
                st.success("### Resultado: nenhum aluno foi classificado com previsão de defasagem")

            st.write("---")
            st.write("## Resumo")

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total de registros", len(df_resultado))
            with col2:
                st.metric("Com previsão de defasagem", qtd_risco)
            with col3:
                st.metric("Sem previsão de defasagem", qtd_sem_risco)

            st.caption(f"Threshold usado: {threshold:.2f}  (proba ≥ threshold => 1)")
            st.caption(f"Percentual com previsão de defasagem: {perc_risco:.1f}%")

            st.write("## Alunos com previsão de defasagem")
            if len(df_com_risco) > 0:
                st.dataframe(df_com_risco, use_container_width=True)
            else:
                st.success("Nenhum aluno foi classificado com previsão de defasagem.")

            st.write("## Alunos sem previsão de defasagem")
            if len(df_sem_risco) > 0:
                st.dataframe(df_sem_risco, use_container_width=True)
            else:
                st.info("Não há alunos classificados sem previsão de defasagem.")

            st.write("## Base completa")
            st.dataframe(df_resultado, use_container_width=True)

            csv_completo = df_resultado.to_csv(index=False).encode("utf-8")
            csv_com_risco = df_com_risco.to_csv(index=False).encode("utf-8")
            csv_sem_risco = df_sem_risco.to_csv(index=False).encode("utf-8")

            st.download_button(
                label="Baixar base completa",
                data=csv_completo,
                file_name="predicao_risco_futuro_completa.csv",
                mime="text/csv"
            )

            st.download_button(
                label="Baixar alunos com previsão de defasagem",
                data=csv_com_risco,
                file_name="alunos_com_previsao_defasagem.csv",
                mime="text/csv"
            )

            st.download_button(
                label="Baixar alunos sem previsão de defasagem",
                data=csv_sem_risco,
                file_name="alunos_sem_previsao_defasagem.csv",
                mime="text/csv"
            )

            with st.expander("Ver arquivo original enviado"):
                st.caption("Esta é a base exatamente como foi enviada pelo usuário, incluindo colunas extras como RA.")
                st.dataframe(df_input, use_container_width=True)

            with st.expander("Ver base utilizada pelo modelo"):
                st.caption("Esta é a base após seleção das colunas exigidas pelo modelo para realizar a predição.")
                st.dataframe(X_novo, use_container_width=True)

        except Exception as e:
            st.error(f"Erro ao gerar predições.\n\n{e}")
            st.stop()

else:
    st.info("""
O arquivo CSV deve conter, no mínimo, as seguintes colunas do modelo:

ano_base, IDA, IEG, IAA, IPS, IPP, IPV, idade_geral, Gênero,
Ano ingresso, inst_ensino_cat, Fase_num, FaseIdeal_num, target_defasagem_atual.

Você também pode incluir colunas extras, como RA, para identificação dos alunos.
""")
    
