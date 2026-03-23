# fase5

🏫 Sobre a Associação Passos Mágicos
A Associação Passos Mágicos possui 32 anos de atuação, transformando a vida de crianças e jovens de baixa renda e ampliando suas oportunidades por meio da educação.

A iniciativa começou em 1992, idealizada por Michelle Flues e Dimetri Ivanoff, atuando inicialmente em orfanatos no município de Embu-Guaçu.

Em 2016, após anos de atuação, o programa foi ampliado para alcançar mais jovens, consolidando-se como um projeto social e educacional. A fórmula de transformação inclui:

Educação de qualidade

Apoio psicológico e psicopedagógico

Ampliação da visão de mundo

Desenvolvimento do protagonismo juvenil

A missão da associação é usar a educação como ferramenta para mudar as condições de vida de crianças e jovens em vulnerabilidade social.

📁 Sobre o Desafio do Datathon
Com base em um dataset de pesquisa extensiva sobre o desenvolvimento educacional nos anos 2022, 2023 e 2024, o desafio consiste em:

Aplicar técnicas de Data Analytics aprendidas no curso

Responder às dores de negócio apresentadas

Construir uma narrativa analítica (storytelling)

Desenvolver um modelo preditivo de risco de defasagem

Entregar uma solução final com insights e recomendações

❓ Perguntas a serem respondidas na análise

1. Adequação do nível (IAN)
Qual é o perfil geral de defasagem dos alunos e como ele evolui ao longo do ano?
Exemplo: quantos alunos estão moderadamente ou severamente defasados?

2. Desempenho acadêmico (IDA)
O desempenho acadêmico médio está melhorando, estagnado ou caindo ao longo das fases e anos?

3. Engajamento nas atividades (IEG)
O grau de engajamento tem relação direta com o desempenho (IDA) e com o ponto de virada (IPV)?

4. Autoavaliação (IAA)
As percepções dos alunos sobre si mesmos são coerentes com seu desempenho real (IDA) e engajamento (IEG)?

5. Aspectos psicossociais (IPS)
Existem padrões psicossociais que antecedem quedas de desempenho ou engajamento?

6. Aspectos psicopedagógicos (IPP)
As avaliações psicopedagógicas confirmam ou contradizem a defasagem identificada pelo IAN?

7. Ponto de virada (IPV)
Quais comportamentos — acadêmicos, emocionais ou de engajamento — mais influenciam o IPV ao longo do tempo?

8. Multidimensionalidade dos indicadores
Quais combinações de indicadores (IDA + IEG + IPS + IPP) elevam mais a nota global do aluno (INDE)?

9. Previsão de risco com Machine Learning
Quais padrões permitem identificar alunos em risco antes da queda no desempenho ou aumento da defasagem?
Criar um modelo preditivo que estime a probabilidade de risco.

10. Efetividade do programa
Os indicadores mostram melhora consistente ao longo do ciclo nas fases Quartzo, Ágata, Ametista e Topázio?

11. Insights adicionais
Trazer análises extras, sugestões e oportunidades de melhoria para a Passos Mágicos.

📦 Entregáveis do Projeto
A entrega deve conter:

✔️ 1. Repositório GitHub
Com todos os códigos de limpeza, análise e preparação dos dados.

✔️ 2. Apresentação (PPT ou PDF)
Storytelling completo, respondendo às perguntas e mostrando insights.

✔️ 3. Notebook Python
Com o modelo preditivo, incluindo:

Feature engineering

Split treino/teste

Modelagem

Avaliação

✔️ 4. Aplicação Streamlit
Disponibilizando o modelo preditivo para uso pela Passos Mágicos.
O deploy deve ser feito no Community Cloud.

✔️ 5. Vídeo de até 5 minutos
Apresentando:

Storytelling

Principais descobertas

Modelo preditivo


According to o documento **“POSTECH - DTAT - Datathon - Fase 5”**, sua entrega tem 4 peças obrigatórias: **GitHub com códigos**, **apresentação (PPT/PDF) com storytelling**, **notebook do modelo preditivo (feature engineering → treino/teste → modelagem → avaliação)** e **app em Streamlit com deploy no Community Cloud**, além de **vídeo de até 5 min** apresentando tudo. 

Abaixo vai um plano de ação bem “pé no chão”, e depois o bloco de Colab + os ajustes do seu `df_fase5`.

---

## 1) Plano de ação para entregar o desafio (do jeito que a banca espera)

### Etapa A — Estruturar o repositório (GitHub)

1. Pasta padrão:

* `data/raw/` (seu xlsx)
* `data/processed/` (parquet/csv limpo)
* `notebooks/` (EDA + modelo)
* `src/` (funções reutilizáveis: limpeza, features, treino)
* `app/` (Streamlit)
* `README.md` (como rodar tudo)

2. README já com:

* objetivo do desafio
* como baixar dados
* como rodar notebook
* como rodar app local
* link do deploy

(Entrega exige link do GitHub com códigos.)

---

### Etapa B — Entender o problema e “amarrar” as perguntas do storytelling

O documento pede responder **perguntas 1 a 11** e contar história com dados, incluindo **um modelo para prever risco de defasagem**. 

Checklist do storytelling (páginas/chapters da apresentação):

1. Contexto do programa + base
2. Qualidade dos dados (nulos, tipos, consistência)
3. Análises pedidas (1–8 e 10–11)
4. Definição do “risco” (target) e por quê
5. Modelo + métricas + interpretação
6. Recomendação prática (como usar no dia a dia)

---

### Etapa C — Preparação de dados (o básico bem feito)

1. Padronizar nomes de colunas (sem acento, sem espaço, snake_case) e alinhar com o dicionário.
2. Tipos corretos: booleano onde é booleano, numérico onde é numérico.
3. Tratar faltantes com regra (não no “achismo”):

* colunas de notas: imputar ou remover? (decisão documentada)
* textos de recomendações/destaques: `""` ou `NaN` (e depois pipeline de texto trata)

4. Salvar base limpa em `data/processed/base_limpa.parquet`.

---

### Etapa D — Features (incluindo “técnicas das aulas”, só onde faz sentido)

Você tem bastante texto em:

* `Rec Av1..4`, `Rec Psicologia`, `Destaque IEG/IDA/IPV`
  Aqui cabem as técnicas de NLP: normalização, tokenização, stopwords, stemming/lemmatização, vetorização (TF-IDF) e/ou embeddings. (Aula 2 fala de normalização/lematização/stemming e redução de espaço de características.)

Estratégia simples e efetiva:

* **Baseline rápido:** TF-IDF nos textos + modelo clássico (LogReg/LinearSVC/RandomForest/XGBoost se usar).
* **Upgrade:** embeddings (se quiser) só para os campos de texto, concatenando com variáveis numéricas.

---

### Etapa E — Modelo preditivo (pergunta 9)

A pergunta 9 é explícita: **um modelo que devolva probabilidade do aluno entrar em risco de defasagem**. 

O que fazer na prática:

1. Definir target (ex.: “risco” = defasagem alta / IAN baixo / mudança ruim de um ano para outro).
   *Aqui você precisa decidir com base nas colunas disponíveis no seu arquivo final.*
2. Separar treino/teste (estratificado).
3. Pipeline:

* pré-processamento numérico (imputer + scaler se necessário)
* categóricos (one-hot)
* texto (TF-IDF)
* modelo

4. Métricas: AUC, F1, recall (recall costuma ser importante para “risco”)
5. Explicabilidade: feature importance / SHAP (se der tempo)

(Entrega exige demonstrar essas etapas no notebook.)

---

### Etapa F — Streamlit + Deploy (obrigatório)

1. `app.py` com:

* upload/entrada de dados de 1 aluno (ou selecionar por RA)
* botão “prever risco”
* output: probabilidade + top fatores

2. Deploy no **Streamlit Community Cloud** (obrigatório).

---

### Etapa G — Vídeo (até 5 min)

Roteiro rápido:

1. Dor do negócio e o que é risco
2. 2 insights fortes do EDA
3. Como definiu o target
4. Resultado do modelo (métrica + como interpretar)
5. Demonstração do Streamlit

(Obrigatório.)

---

## 2) Bloco Python (Colab) para carregar o XLSX do seu GitHub em `df_fase5`

> Como o Colab não “lê pasta do Git” direto, você usa a URL **raw** do arquivo.

```python
import pandas as pd

# URL RAW do GitHub (ajuste se o nome do arquivo/pasta mudar)
url = "https://raw.githubusercontent.com/tivanello/fase5/main/data/raw/BASE%20DE%20DADOS%20PEDE%202024%20-%20DATATHON.xlsx"

df_fase5 = pd.read_excel(url)

print(df_fase5.shape)
df_fase5.head()
```

Se der erro por tamanho/timeout, alternativa robusta:

```python
import requests
from pathlib import Path
import pandas as pd

url = "https://raw.githubusercontent.com/tivanello/fase5/main/data/raw/BASE%20DE%20DADOS%20PEDE%202024%20-%20DATATHON.xlsx"
local_path = Path("BASE_DE_DADOS_PEDE_2024_DATATHON.xlsx")

r = requests.get(url, timeout=120)
r.raise_for_status()
local_path.write_bytes(r.content)

df_fase5 = pd.read_excel(local_path)
print(df_fase5.shape)
```

---

## 3) Avaliação do dicionário x seu `df_fase5`: o que ajustar

### 3.1. Principal ajuste: nomes de colunas (padronização)

Seu dataframe está com nomes “humanos” (com espaço, acento e “22”), mas o dicionário está no padrão `*_2022`.

Exemplos de mapeamento (dicionário → seu df):

* `FASE_2022` → `Fase`
* `TURMA_2022` → `Turma`
* `ANO_INGRESSO_2022` → `Ano ingresso`
* `PEDRA_2022` → `Pedra 22` (e “Pedra 20/21” parecem ser anos anteriores)
* `INDE_2022` → `INDE 22`
* `CG_2022 / CF_2022 / CT_2022` → `Cg / Cf / Ct`
* `QTDE_AVAL_2022` → `Nº Av`
* `REC_AVAL_1_2022..4` → `Rec Av1..4`
* `REC_PSICO_2022` → `Rec Psicologia`
* `NOTA_MAT_2022 / NOTA_PORT_2022 / NOTA_ING_2022` → `Matem / Portug / Inglês`
* `INDICADO_BOLSA_2022` → `Indicado` (deveria ser booleano)
* `PONTO_VIRADA_2022` → `Atingiu PV` (deveria ser booleano)
* `DESTAQUE_IEG_2022 / DESTAQUE_IDA_2022 / DESTAQUE_IPV_2022` → `Destaque IEG/IDA/IPV`

**Ajuste recomendado:** criar um dicionário de renomeação e converter tudo para o padrão do dicionário. Isso evita dor de cabeça no pipeline e no Streamlit.

---

### 3.2. Tipos errados (o seu `info()` entrega 2 suspeitos claros)

No dicionário:

* `INDICADO_BOLSA_2022` é **booleano**
* `PONTO_VIRADA_2022` é **booleano**

No seu df:

* `Indicado` = `object`
* `Atingiu PV` = `object`

**Ajuste:** normalizar para `True/False` (ou `0/1`) a partir de valores do tipo “Sim/Não”, “S/N”, “1/0”, etc.

---

### 3.3. Campos de texto: ok serem `object`, mas prepare para NLP

Esses aqui são “texto útil” e você tem bastante nulo:

* `Rec Av4` (296 non-null)
* `Avaliador4` (310 non-null)
* `Avaliador3` (534 non-null)
* `Inglês` (283 non-null)
* `Pedra 20/21` bem incompletos

**Ajuste:** decidir regra:

* “AvaliadorX” provavelmente é identificador/nome → eu tiraria do modelo (risco de vazamento e pouca utilidade).
* “Rec AvX / Rec Psicologia / Destaques” → usar NLP (TF-IDF) e preencher nulos com string vazia para o vetorizador.

---

### 3.4. “Pedra 20” e “Pedra 21” — confirmar se o desafio pede série temporal

O dicionário mostra claramente `PEDRA_2022`.
Seu df tem `Pedra 20`, `Pedra 21`, `Pedra 22`. Isso é ótimo para “evolução ao longo do tempo”, mas:

* você precisa **confirmar** se “20/21” = 2020/2021 mesmo (pelo nome parece, mas vale checar no arquivo/dicionário completo).
* se for isso, dá para criar features de tendência (ex.: mudou de pedra? piorou? melhorou?).

---

### 3.5. Colunas “Nome” e “RA”

* `Nome`: eu não usaria no modelo (risco de overfit e não agrega).
* `RA`: manter como chave/ID (para rastrear aluno), mas não entra como feature.

---

## 4) Onde entram “as técnicas das aulas” (só no que couber)

* NLP clássico nos textos (normalização + stopwords + stemming/lemmatização + TF-IDF) para recomendações/destaques. Isso é exatamente o tipo de transformação citada na aula de processamento de texto. 
* Se quiser dar um charme: comparar baseline TF-IDF vs embeddings só nos textos (mas não inventa moda se o prazo estiver curto).

---

Se você quiser, eu já te devolvo **um bloco único** que faz:

1. renomeia colunas para o padrão `*_2022`,
2. converte `Indicado` e `Atingiu PV` pra boolean,
3. prepara textos (nulos → “”),
4. e salva `parquet` em `data/processed/`.

Só me diga se você quer manter os nomes originais no df (bonitos) ou migrar de vez pro padrão do dicionário (o mais prático).
