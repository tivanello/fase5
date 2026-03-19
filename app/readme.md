# App Streamlit – Predição de Risco Futuro de Defasagem Escolar

Este app foi desenvolvido em **Streamlit** para consumir o modelo treinado de predição de risco futuro de defasagem escolar e retornar a probabilidade estimada de um aluno entrar em defasagem ou agravar a defasagem no período seguinte.

O app permite dois tipos de análise:

- **Avaliação em grupo**: análise de vários alunos a partir de um arquivo
- **Avaliação individual**: análise de um único aluno com preenchimento manual

---

## Como funciona

1. O usuário escolhe o tipo de avaliação desejada.
2. Na **avaliação em grupo**, o usuário envia uma base em **CSV, XLSX ou XLS**.
3. Na **avaliação individual**, o usuário preenche manualmente os dados do aluno.
4. O app organiza os dados no formato esperado pelo modelo.
5. A base é ajustada conforme a **ordem exata das colunas** usadas no treinamento.
6. O modelo calcula a probabilidade de risco futuro de defasagem.
7. A classificação final é feita com base no limiar definido no metadata do modelo.

---

## Modelo utilizado

Foi adotado como modelo final:

- **Regressão Logística conservadora C1**
- **sem IAN**
- **threshold final = 0,70**

Objetivo do modelo:

- prever alunos com risco de:
  - entrar em defasagem
  - ou agravar a defasagem no ano seguinte

---

## Arquivos utilizados pelo app

O app carrega os seguintes arquivos:

- **models/modelo_risco_futuro_c1.joblib**
- **models/colunas_modelo_risco_futuro_c1.json**
- **models/metadata_modelo_risco_futuro_c1.json**

### Observação importante

O arquivo **colunas_modelo_risco_futuro_c1.json** está salvo como **lista pura**.

Por isso, o app trata corretamente tanto lista quanto dicionário ao carregar as colunas esperadas pelo modelo.

---

## Colunas esperadas pelo modelo

A base enviada deve conter as colunas obrigatórias do modelo:

- ano_base
- IDA
- IEG
- IAA
- IPS
- IPP
- IPV
- idade_geral
- gênero
- ano_ingresso
- inst_ensino_cat
- fase_num
- faseIdeal_num
- target_defasagem_atual

Além disso, o app aceita colunas extras, como:

- RA
- ID do aluno
- Matrícula

Essas colunas adicionais não entram no cálculo do modelo, mas são preservadas na saída para facilitar a identificação do aluno.

---

## Como executar localmente

A partir da raiz do projeto:

```bash
pip install -r requirements.txt
streamlit run app/app_risco_futuro.py