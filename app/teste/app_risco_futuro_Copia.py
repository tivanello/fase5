from PIL import Image
import streamlit as st
import pandas as pd
import joblib
import json
from pathlib import Path

# ==============================================================
# CONFIGURAÇÃO
# ==============================================================

st.set_page_config(
    page_title="App Risco Futuro",
    page_icon="📉",
    layout="centered"
)

BASE_DIR = Path(__file__).resolve().parents[1]   # volta pra raiz do projeto
MODEL_PATH = BASE_DIR / "models" / "modelo_risco_futuro_c1.joblib"
COLUNAS_PATH = BASE_DIR / "models" / "colunas_modelo_risco_futuro_c1.json"
METADATA_PATH = BASE_DIR / "models" / "metadata_modelo_risco_futuro_c1.json"

st.markdown(
    """
    <style>
    div[role='radiogroup'] {
        display: flex;
        justify-content: center;
        gap: 1rem;
    }
    div[role='radiogroup'] label {
        background-color: rgba(33,150,243,0.08);
        padding: 0.45rem 0.9rem;
        border-radius: 10px;
        border: 1px solid rgba(33,150,243,0.18);
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    "<h1 style='text-align: center;'>📉 Predição de Risco Futuro de Defasagem Escolar</h1>",
    unsafe_allow_html=True
)

st.markdown(
    """
    <div style="
        background-color: rgba(33,150,243,0.15);
        border-left: 6px solid rgba(33,150,243,1);
        padding: 12px 16px;
        border-radius: 6px;
        margin-bottom: 18px;
    ">
        <b>Escolha o tipo de avaliação desejada:</b>
        <ul style="margin-top: 8px; margin-bottom: 0;">
            <li><b>Avaliação em grupo:</b> envie uma base com vários alunos.</li>
            <li><b>Avaliação individual:</b> preencha os dados de um único aluno.</li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True
)

# ==============================================================
# CARREGAMENTO DOS ARTEFATOS
# ==============================================================

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

# ==============================================================
# FUNÇÕES AUXILIARES
# ==============================================================

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

def ler_arquivo_upload(arquivo):
    nome = arquivo.name.lower()

    if nome.endswith(".csv"):
        return pd.read_csv(arquivo)
    if nome.endswith((".xlsx", ".xls")):
        return pd.read_excel(arquivo)

    raise ValueError("Formato de arquivo não suportado.")

# ============================================================
# ENTRADA DE DADOS
# ============================================================

st.markdown("<h2 style='text-align: center;'>✏️ Tipo de avaliação</h2>", unsafe_allow_html=True)

col_esq, col_centro, col_dir = st.columns([1, 2, 1])

with col_centro:
    tipo_avaliacao = st.radio(
        "Selecione uma opção",
        ["Avaliação em grupo", "Avaliação individual"],
        index=None,
        horizontal=True,
        label_visibility="collapsed"
    )

if tipo_avaliacao is None:
    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    st.info("Selecione o tipo de avaliação desejada.")
    st.stop()


# ============================================================
# ABA 1 — AVALIAÇÃO EM GRUPO
# ============================================================

if tipo_avaliacao == "Avaliação em grupo":
    st.markdown("<h2 style='text-align: center;'>📥 Upload da base de alunos</h2>", unsafe_allow_html=True)


    arquivo = st.file_uploader(
    "Selecione ou arraste o arquivo da base de alunos",
    type=["csv", "xlsx", "xls"],
    key="upload_grupo"
)

    if arquivo is not None:
        try:
            df_input = pd.read_csv(arquivo)
        except Exception as e:
            st.error(f"Erro ao ler o arquivo CSV.\n\n{e}")
            st.stop()

        st.write("## Pré-visualização do arquivo enviado")
        st.dataframe(df_input.head(), use_container_width=True)

        faltando, extras = validar_colunas(df_input, feature_columns)

        if faltando:
            st.error("O arquivo enviado não contém todas as colunas obrigatórias do modelo.")
            st.write("**Colunas faltantes:**", faltando)
            st.write("**Colunas obrigatórias esperadas:**", feature_columns)
            st.stop()

        if extras:
            if "RA" in extras:
                st.success(
                    "Coluna de identificação detectada (RA). "
                    "Ela será mantida no resultado para facilitar a identificação dos alunos."
                )

            extras_sem_ra = [col for col in extras if col != "RA"]
            if extras_sem_ra:
                st.info(
                    f"Colunas adicionais encontradas: {extras_sem_ra}. "
                    "Essas colunas não são usadas pelo modelo, mas serão preservadas na saída."
                )

        X_novo = preparar_dataframe(df_input, feature_columns)

        if st.button("Avaliar base", key="botao_grupo"):
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
                    mime="text/csv",
                    key="download_completo"
                )

                st.download_button(
                    label="Baixar alunos com previsão de defasagem",
                    data=csv_com_risco,
                    file_name="alunos_com_previsao_defasagem.csv",
                    mime="text/csv",
                    key="download_com_risco"
                )

                st.download_button(
                    label="Baixar alunos sem previsão de defasagem",
                    data=csv_sem_risco,
                    file_name="alunos_sem_previsao_defasagem.csv",
                    mime="text/csv",
                    key="download_sem_risco"
                )

                with st.expander("Ver arquivo original enviado"):
                    st.caption("Esta é a base exatamente como foi enviada pelo usuário, incluindo colunas extras como RA.")
                    st.dataframe(df_input, use_container_width=True)

                with st.expander("Ver base utilizada pelo modelo"):
                    st.caption("Esta é a base após seleção das colunas exigidas pelo modelo para realizar a predição.")
                    st.dataframe(X_novo, use_container_width=True)

                with st.expander("Como esta análise foi feita"):
                    st.write("""
                Esta análise foi construída a partir de um modelo preditivo treinado com dados históricos de alunos.

                O modelo observa padrões em indicadores educacionais e na trajetória escolar, como desempenho, engajamento, fase atual, fase ideal e situação de defasagem no momento.

                Com base nesses dados, ele estima a probabilidade de o aluno entrar em defasagem ou agravar uma defasagem já existente no período seguinte.

                Importante: este resultado é um apoio para análise e acompanhamento. Ele não deve ser usado sozinho como decisão final.
                """)

            except Exception as e:
                st.error(f"Erro ao gerar predições.\n\n{e}")
                st.stop()

    else:
        st.info("""
A avaliação em grupo recebe um arquivo CSV, XLSX e XLS com a base de alunos.
    
Colunas obrigatórias do modelo: ano_base; IDA; IEG; IAA; IPS; IPP; IPV; idade_geral; gênero; 
ano_ingresso; inst_ensino_cat; fase_num; faseIdeal_num; target_defasagem_atual.  

Você também deve incluir coluna(s) extra(s), como RA, ID do aluno, Matricula.
Essas informações são necessárias para que identifique o aluno, para identificação dos alunos.
                
Abaixo você poderá baixar um arquivo modelo para entender o formato esperado.
                
IMPORTANTE: O modelo de predição foi treinado com dados organizados nesse formato, então é importante seguir a estrutura para que as predições sejam geradas corretamente. 
        """)

from io import BytesIO

# ============================================================
# ARQUIVO MODELO PARA DOWNLOAD
# ============================================================
df_modelo = pd.DataFrame([
    {
        "ano_base": 2024,
        "IDA": 7.5,
        "IEG": 8.1,
        "IAA": 7.8,
        "IPS": 6.9,
        "IPP": 7.2,
        "IPV": 6.8,
        "idade_geral": 12,
        "gênero": "Masculino",
        "ano_ingresso": 2022,
        "inst_ensino_cat": "Pública",
        "fase_num": 5,
        "faseIdeal_num": 5,
        "target_defasagem_atual": 0,
        "RA": "123456"
    }
])

buffer = BytesIO()
with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
    df_modelo.to_excel(writer, index=False, sheet_name="modelo_base")

arquivo_modelo = buffer.getvalue()

st.download_button(
    label="📥 Baixar arquivo modelo em XLSX",
    data=arquivo_modelo,
    file_name="modelo_base_alunos.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# ============================================================
# ABA 2 — AVALIAÇÃO INDIVIDUAL
# ============================================================
if tipo_avaliacao == "Avaliação individual":
    st.write("## 🎓 Dados do aluno")
    st.caption("Preencha os dados do aluno para realizar uma avaliação individual.")

    opcoes_fase = [f"Fase {i}" for i in range(10)]
    mapa_fase = {f"Fase {i}": i for i in range(10)}

    OP_NAO = "Não - Aluno não está em defasagem"
    OP_SIM = "Sim - Aluno está em defasagem"
    OP_SEM_INFO = "Não avaliado / sem informação"

    target_defasagem_txt = st.selectbox(
        "Defasagem atual",
        ["", OP_NAO, OP_SIM, OP_SEM_INFO]
    )

    if target_defasagem_txt == "":
        st.info("Selecione a situação de defasagem atual para continuar.")

    elif target_defasagem_txt == OP_SEM_INFO:
        st.warning(
            "A avaliação individual não pode prosseguir sem a informação de defasagem atual. "
            "O modelo final depende dessa variável para realizar a predição."
        )

    else:
        with st.form("form_individual"):
            col1, col2 = st.columns(2)

            with col1:
                ra = st.text_input("RA (opcional)", value="")
                ano_base = st.text_input("Ano base", value="")
                IDA = st.text_input("IDA", value="")
                IEG = st.text_input("IEG", value="")
                IAA = st.text_input("IAA", value="")
                IPS = st.text_input("IPS", value="")
                IPP = st.text_input("IPP", value="")
                IPV = st.text_input("IPV", value="")

            with col2:
                idade_geral = st.text_input("Idade", value="")
                genero = st.selectbox("Gênero", ["", "Feminino", "Masculino"])
                ano_ingresso = st.text_input("Ano ingresso", value="")
                inst_ensino_cat = st.selectbox("Instituição de ensino", ["", "Pública", "Privada", "Outras"])
                fase_num_txt = st.selectbox("Fase atual", [""] + opcoes_fase)
                fase_ideal_num_txt = st.selectbox("Fase ideal", [""] + opcoes_fase)

            submit_individual = st.form_submit_button("Avaliar aluno")

        if submit_individual:
            try:
                campos_obrigatorios = {
                    "Ano base": ano_base,
                    "IDA": IDA,
                    "IEG": IEG,
                    "IAA": IAA,
                    "IPS": IPS,
                    "IPP": IPP,
                    "IPV": IPV,
                    "Idade": idade_geral,
                    "Gênero": genero,
                    "Ano ingresso": ano_ingresso,
                    "Instituição de ensino": inst_ensino_cat,
                    "Fase atual": fase_num_txt,
                    "Fase ideal": fase_ideal_num_txt,
                    "Defasagem atual": target_defasagem_txt,
                }

                faltando = [campo for campo, valor in campos_obrigatorios.items() if str(valor).strip() == ""]
                if faltando:
                    st.error(f"Preencha todos os campos obrigatórios. Campos faltantes: {faltando}")
                    st.stop()

                linha = {
                    "ano_base": int(ano_base),
                    "IDA": float(IDA),
                    "IEG": float(IEG),
                    "IAA": float(IAA),
                    "IPS": float(IPS),
                    "IPP": float(IPP),
                    "IPV": float(IPV),
                    "idade_geral": int(idade_geral),
                    "Gênero": genero,
                    "Ano ingresso": int(ano_ingresso),
                    "inst_ensino_cat": inst_ensino_cat,
                    "Fase_num": mapa_fase[fase_num_txt],
                    "FaseIdeal_num": mapa_fase[fase_ideal_num_txt],
                    "target_defasagem_atual": 1 if target_defasagem_txt == OP_SIM else 0,
                }

                X_individual = pd.DataFrame([linha])
                X_individual = preparar_dataframe(X_individual, feature_columns)

                if not hasattr(model, "predict_proba"):
                    st.error("O modelo não possui predict_proba(). Verifique o artefato salvo.")
                    st.stop()

                proba = float(model.predict_proba(X_individual)[:, 1][0])
                pred = 1 if proba >= threshold else 0

                st.write("---")
                st.write("## Resultado da avaliação individual")

                if pred == 1:
                    st.markdown("""
                    <div style="
                        background-color: rgba(244,67,54,0.12);
                        border-left: 6px solid rgba(244,67,54,1);
                        padding: 14px 16px;
                        border-radius: 6px;
                        margin-bottom: 12px;
                    ">
                        <b style="font-size: 24px; color: #b00020;">Resultado: há previsão de defasagem</b><br>
                        <span style="font-size: 17px;">
                            Com os dados informados, o aluno foi classificado com previsão de defasagem
                            e merece acompanhamento com maior atenção.
                        </span>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div style="
                        background-color: rgba(76,175,80,0.12);
                        border-left: 6px solid rgba(76,175,80,1);
                        padding: 14px 16px;
                        border-radius: 6px;
                        margin-bottom: 12px;
                    ">
                        <b style="font-size: 24px; color: #1b5e20;">Resultado: sem previsão de defasagem</b><br>
                        <span style="font-size: 17px;">
                            Com os dados informados, o aluno não foi classificado com previsão de defasagem
                            neste momento.
                        </span>
                    </div>
                    """, unsafe_allow_html=True)

                st.metric(
                    "Probabilidade estimada de entrar ou agravar a defasagem",
                    f"{proba * 100:.1f}%"
                )

                if pred == 1:
                    st.write("**Situação prevista:** Com previsão de defasagem")
                else:
                    st.write("**Situação prevista:** Sem previsão de defasagem")

                if target_defasagem_txt == OP_SIM:
                    st.write("**Situação atual informada:** aluno já está em defasagem no momento.")
                elif target_defasagem_txt == OP_NAO:
                    st.write("**Situação atual informada:** aluno não está em defasagem no momento.")

                if ra.strip():
                    st.write(f"**RA informado:** {ra}")

                st.progress(min(max(proba, 0.0), 1.0))

                with st.expander("Ver dados enviados ao modelo"):
                    df_exibicao = X_individual.copy()
                    if ra.strip():
                        df_exibicao.insert(0, "RA", ra)
                    st.dataframe(df_exibicao, use_container_width=True)

                with st.expander("Como esta análise foi feita"):
                    st.write("""
                Esta análise foi construída a partir de um modelo preditivo treinado com dados históricos de alunos.

                O modelo observa padrões em indicadores educacionais e na trajetória escolar, como desempenho, engajamento, fase atual, fase ideal e situação de defasagem no momento.

                Com base nesses dados, ele estima a probabilidade de o aluno entrar em defasagem ou agravar uma defasagem já existente no período seguinte.

                Importante: este resultado é um apoio para análise e acompanhamento. Ele não deve ser usado sozinho como decisão final.
                """)

            except ValueError:
                st.error("Verifique os campos numéricos. Há valores inválidos ou não preenchidos corretamente.")
            except Exception as e:
                st.error(f"Erro ao gerar a avaliação individual.\n\n{e}")
                st.stop()