# fase5

**Sobre a Associação Passos Mágicos**
A Associação Passos Mágicos possui 32 anos de atuação, transformando a vida de crianças e jovens de baixa renda por meio da educação.

A iniciativa começou em 1992, idealizada por Michelle Flues e Dimetri Ivanoff, atuando inicialmente em orfanatos no município de Embu-Guaçu.

Em 2016, o programa foi ampliado, consolidando-se como um projeto social e educacional baseado em:

- Educação de qualidade  
- Apoio psicológico e psicopedagógico  
- Ampliação da visão de mundo  
- Desenvolvimento do protagonismo juvenil  

A missão da associação é utilizar a educação como ferramenta de transformação social.

---

Sobre o Desafio do Datathon  

Com base em um dataset educacional dos anos de 2022, 2023 e 2024, o desafio consiste em:

- Aplicar técnicas de Data Analytics  
- Responder às perguntas de negócio  
- Construir uma narrativa analítica (storytelling)  
- Desenvolver um modelo preditivo de risco de defasagem  
- Entregar uma solução com insights e recomendações  

---

Perguntas a serem respondidas  

(1 a 11 mantidas exatamente como você já colocou — estão corretas)

---

Entregáveis do Projeto  

A entrega deve conter **5 itens obrigatórios**:

✔️ 1. Repositório GitHub  
Contendo:
- Código de tratamento de dados  
- Análises  
- Modelagem  
- Aplicação  

✔️ 2. Apresentação (PPT ou PDF)  
Com storytelling completo:
- Respostas às perguntas  
- Insights  
- Recomendações  

✔️ 3. Notebook Python (Modelo Preditivo)  
Incluindo:
- Feature engineering  
- Divisão treino/teste  
- Treinamento  
- Avaliação  

✔️ 4. Aplicação em Streamlit  
- Interface para uso do modelo  
- Deploy no Streamlit Community Cloud  

✔️ 5. Vídeo (até 5 minutos)  
Apresentando:
- Contexto do problema  
- Principais insights  
- Modelo preditivo  
- Demonstração da aplicação  

---

Plano de Execução do Projeto  

### Etapa 1 — Entendimento do problema
- Leitura do documento do Datathon  
- Compreensão das perguntas de negócio  

### Etapa 2 — Estrutura do projeto
- Criação do repositório GitHub  
- Organização das pastas:

FASE5/
├── app/
│   ├── app_risco_futuro.py
│   └── README.md
├── data/
│   ├── raw/
│   ├── processed/
│   └── README.md
├── models/
│   ├── modelo_risco_futuro_c1.joblib
│   ├── colunas_modelo_risco_futuro_c1.json
│   ├── metadata_modelo_risco_futuro_c1.json
│   └── README.md
├── notebooks/
│   ├── Entrega_DATATHON_Fase5.ipynb
│   └── README.md
├── Paineis/
│   ├── dashboard.pbix
│   └── README.md
├── reports/
│   ├── apresentacao_final.pdf
│   └── README.md
├── src/
│   ├── data_prep.py
│   ├── features.py
│   ├── train.py
│   └── README.md
├── .gitignore
├── requirements.txt
├── runtime.txt
└── README.md



---

### Etapa 3 — Aquisição dos dados
- Download da base **PEDE 2024**  
- Download do **dicionário de dados**  

---

### Etapa 4 — Preparação e análise dos dados
- Tratamento da base  
- Padronização de colunas  
- Tratamento de valores nulos  
- Geração de datasets analíticos  

➡️ Utilizado para responder:
- Perguntas **1 a 8 e 10**

---

### Etapa 5 — Storytelling e visualização
- Construção dos painéis no Power BI  
- Criação da narrativa analítica  

---

### Etapa 6 — Modelagem preditiva
- Definição do target (risco de defasagem)  
- Engenharia de features  
- Treinamento do modelo  
- Avaliação (métricas)  

➡️ Relacionado à:
- Pergunta **9**

---

### Etapa 7 — Desenvolvimento da aplicação
- Criação do app **app_risco_futuro.py**  
- Testes locais com Streamlit  
- Criação de arquivos de entrada para teste  

---

### Etapa 8 — Deploy
- Publicação do app no Streamlit Cloud  
- (Opcional) Publicação dos painéis no Power BI Service  

---

### Etapa 9 — Consolidação do projeto
- Organização final do GitHub  
- Inclusão de instruções de uso  
- Garantia de reprodutibilidade  

---

### Etapa 10 — Apresentação final
- Criação do PPT/PDF  
- Inclusão da pergunta 11 (insights adicionais)  

---

### Etapa 11 — Vídeo
- Gravação de apresentação (até 5 minutos)  

---

### Etapa 12 — Submissão
- Envio dos artefatos na plataforma da pós  

---

📌 Observação importante  

- As perguntas **1 a 8 e 10** são respondidas via análise exploratória e dashboards  
- A pergunta **9** é respondida via modelo preditivo  
- A pergunta **11** é respondida com insights estratégicos e recomendações  

Tech Challenge – Fase 05 | Data Analytics (Pos Tech)

Desenvolvimento de uma solução analítica e preditiva para identificação antecipada de alunos em risco de defasagem educacional, utilizando dados do programa Passos Mágicos.

A solução integra análise de dados, modelagem preditiva e visualização, permitindo transformar indicadores educacionais em apoio à tomada de decisão.

Principais componentes:

* Pipeline de dados estruturado e reprodutível
* Modelagem preditiva de risco futuro
* Aplicação interativa para simulação de cenários
* Dashboard analítico com insights estratégicos

Links da entrega:

Tech Challenge – Fase 05 | Data Analytics (Pos Tech)

Solução completa de Machine Learning aplicada à saúde para estimar tendência à obesidade com base em hábitos e contexto. 

O projeto inclui pipeline reprodutível (EDA + feature engineering + treino e avaliação), modelo persistido (.joblib), aplicação Streamlit publicada e dashboard Power BI com insights.

Links da entrega:

1. App Streamlit: [https://app-risco-defasagem.streamlit.app/]

2. Dashboard Power BI: [https://app.powerbi.com/view?r=eyJrIjoiMGNkNWNjZjQtMDczMS00YzA0LTg0NTMtODJmZDAwNThkNWI1IiwidCI6IjhhZjNmN2Y1LTUzYTQtNDcxYS1hMWI1LWI2N2E5YzQ4YTI1NCJ9&pageName=1b07d33989e06b696b79link]

3. Repositório GitHub: [https://github.com/tivanello/fase5]

4. Vídeo: [https://youtu.be/M6LLq6O6rJ4] 