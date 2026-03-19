## Orientações para uso do modelo treinado no Streamlit

O modelo salvo foi a versão final da **Regressão Logística conservadora C1**, treinada para prever **risco futuro de agravamento da defasagem**.

### Arquivos que devem ser carregados no app

O Streamlit deverá ler os três arquivos salvos em **models**:

- **modelo_risco_futuro_c1.joblib**  
  contém o pipeline completo já treinado, incluindo pré-processamento e modelo

- **colunas_modelo_risco_futuro_c1.json**  
  contém a lista exata das colunas esperadas pelo modelo

- **metadata_modelo_risco_futuro_c1.json**  
  contém informações auxiliares, incluindo o limiar final de decisão

### Lógica de uso no Streamlit

O app não deve treinar novamente o modelo.  
Ele deve apenas:

1. carregar os artefatos salvos  
2. receber um dataframe de entrada  
3. garantir que o dataframe possua as colunas esperadas  
4. aplicar o pipeline carregado  
5. calcular a probabilidade de risco futuro  
6. aplicar o limiar de decisão para gerar a classe final

### Variável alvo prevista pelo modelo

O modelo prevê:

- **target_risco_futuro**

Interpretação:

- **0** = não houve alerta de agravamento no ano seguinte
- **1** = há alerta de agravamento no ano seguinte

### Limiar final de decisão

O limiar adotado no modelo foi:

- **0,70**

Regra de classificação:

- probabilidade **maior ou igual a 0,70** → classe **1**
- probabilidade **menor que 0,70** → classe **0**

### Colunas que o Streamlit deverá fornecer ao modelo

O dataframe de entrada deve conter exatamente estas colunas:

- **ano_base**
- **IDA**
- **IEG**
- **IAA**
- **IPS**
- **IPP**
- **IPV**
- **idade_geral**
- **Gênero**
- **Ano ingresso**
- **inst_ensino_cat**
- **Fase_num**
- **FaseIdeal_num**
- **target_defasagem_atual**

### Tipo esperado de cada campo

#### Campos numéricos
Devem ser enviados como número:

- **ano_base**
- **IDA**
- **IEG**
- **IAA**
- **IPS**
- **IPP**
- **IPV**
- **idade_geral**
- **Ano ingresso**
- **Fase_num**
- **FaseIdeal_num**
- **target_defasagem_atual**

#### Campos categóricos
Devem ser enviados como texto:

- **Gênero**
- **inst_ensino_cat**

### Valores esperados para os campos categóricos

#### Gênero
Usar apenas:

- **Feminino**
- **Masculino**

#### inst_ensino_cat
Usar apenas:

- **Pública**
- **Privada**
- **Outras**

### Observação sobre valores ausentes

O pipeline do modelo já possui tratamento interno para nulos:

- variáveis numéricas → imputação pela mediana
- variáveis categóricas → imputação pelo valor mais frequente

Mesmo assim, o ideal é que o Streamlit envie os dados o mais completos possível.

### Como calcular a saída no app

O Streamlit deverá gerar dois campos principais no resultado:

- **prob_risco_futuro**  
  probabilidade estimada de agravamento futuro

- **classe_risco_futuro**  
  classe final obtida com base no limiar 0,70

### Interpretação sugerida no app

Sugestão de leitura para o usuário:

- **classe 0** → sem alerta de risco elevado
- **classe 1** → aluno com risco elevado de agravamento futuro

### Ponto de atenção importante

A coluna **IAN** não deve ser enviada ao modelo, porque ela foi removida na versão final C1.

### Resumo prático

Para usar o modelo no Streamlit, basta:

1. carregar os três arquivos salvos  
2. montar um dataframe com as 14 colunas exigidas  
3. aplicar **predict_proba**  
4. comparar a probabilidade com o limiar **0,70**  
5. devolver a probabilidade e a classe final