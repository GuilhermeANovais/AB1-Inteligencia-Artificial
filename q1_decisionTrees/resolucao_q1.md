# Resolução da Questão 1

## (i) Base de Dados Ampliada
A base de dados foi ampliada para conter 6 atributos (`Historia de Credito`, `Divida`, `Garantia`, `Renda`, `Idade`, `Emprego_Fixo`) e 30 exemplos, distribuídos nas classes de Risco (Alto, Moderado, Baixo). O arquivo completo encontra-se em `data/dataset_ampliado.csv`.

## (ii) Construção das Árvores de Decisão

### Algoritmo ID3 (Baseado em Ganho de Informação / Entropia)
O ID3 seleciona o atributo que maximiza o Ganho de Informação em cada nó.
*Representação da Árvore ID3:*
- Renda = "Acima de 35k": 
  - Idade = "Jovem": Baixo
  - Idade = "Meia-Idade": Baixo
  - Idade = "Idoso":
    - Emprego_Fixo = "Sim": Baixo
    - Emprego_Fixo = "Nao": Moderado
- Renda = "15 a 35k": 
  - Historia de Credito = "Desconhecida": Moderado
  - Historia de Credito = "Ruim": Alto
  - Historia de Credito = "Boa": Moderado
- Renda = "0 a 15k": Alto

### Algoritmo C4.5 (Baseado em Razão de Ganho / Gain Ratio)
O C4.5 é uma evolução do ID3 que penaliza atributos com muitos valores distintos, evitando *overfitting* precoce.
*Representação da Árvore C4.5:*
- Historia de Credito = "Ruim": Alto
- Historia de Credito = "Desconhecida":
  - Renda = "Acima de 35k": Baixo
  - Renda = "15 a 35k": Moderado
  - Renda = "0 a 15k": Alto
- Historia de Credito = "Boa":
  - Renda = "Acima de 35k": Baixo
  - Renda = "15 a 35k": Moderado
  - Renda = "0 a 15k": Alto (com exceções baseadas em Emprego_Fixo)

### Algoritmo CART (Baseado no Índice de Gini)
O CART cria sempre árvores estritamente binárias utilizando o Índice de Gini para medir a impureza das divisões.
*Representação da Árvore CART:*
- Renda <= 15k? (Sim): Alto
- Renda <= 15k? (Não):
  - Renda > 35k? (Sim): Baixo
  - Renda > 35k? (Não):
    - Historia de Credito = Ruim? (Sim): Alto
    - Historia de Credito = Ruim? (Não): Moderado

## (iii) Bases de Conhecimento (Regras Extraídas)

### Regras do ID3
1. **SE** Renda = "Acima de 35k" E Idade = "Idoso" E Emprego_Fixo = "Nao" **ENTÃO** Risco = Moderado
2. **SE** Renda = "Acima de 35k" E Emprego_Fixo = "Sim" **ENTÃO** Risco = Baixo
3. **SE** Renda = "15 a 35k" E Historia_Credito = "Boa" **ENTÃO** Risco = Moderado
4. **SE** Renda = "15 a 35k" E Historia_Credito = "Desconhecida" **ENTÃO** Risco = Moderado
5. **SE** Renda = "15 a 35k" E Historia_Credito = "Ruim" **ENTÃO** Risco = Alto
6. **SE** Renda = "0 a 15k" **ENTÃO** Risco = Alto

### Regras do C4.5
1. **SE** Historia_Credito = "Ruim" **ENTÃO** Risco = Alto
2. **SE** Historia_Credito = "Desconhecida" E Renda = "Acima de 35k" **ENTÃO** Risco = Baixo
3. **SE** Historia_Credito = "Desconhecida" E Renda = "15 a 35k" **ENTÃO** Risco = Moderado
4. **SE** Historia_Credito = "Desconhecida" E Renda = "0 a 15k" **ENTÃO** Risco = Alto
5. **SE** Historia_Credito = "Boa" E Renda = "Acima de 35k" **ENTÃO** Risco = Baixo
6. **SE** Historia_Credito = "Boa" E Renda = "15 a 35k" **ENTÃO** Risco = Moderado
7. **SE** Historia_Credito = "Boa" E Renda = "0 a 15k" **ENTÃO** Risco = Alto

### Regras do CART (Binárias)
1. **SE** Renda_Menor_Igual_15k = VERDADEIRO **ENTÃO** Risco = Alto
2. **SE** Renda_Menor_Igual_15k = FALSO E Renda_Maior_35k = VERDADEIRO **ENTÃO** Risco = Baixo
3. **SE** Renda_Menor_Igual_15k = FALSO E Renda_Maior_35k = FALSO E Historia_Credito_Ruim = VERDADEIRO **ENTÃO** Risco = Alto
4. **SE** Renda_Menor_Igual_15k = FALSO E Renda_Maior_35k = FALSO E Historia_Credito_Ruim = FALSO **ENTÃO** Risco = Moderado

## (iv) Comparação e Escolha

**Comparação:**
- **ID3** cria partições muito específicas logo de início (como a quebra da árvore por Idade e Emprego), podendo sofrer com *overfitting* rapidamente se o dataset for ruidoso ou com atributos de muitos valores.
- **C4.5** lida melhor com partições e atributos faltantes, gerando regras mais limpas, intuitivas e compactas, incrivelmente fáceis de ler para um humano.
- **CART** produz árvores binárias estritas. Isso muitas vezes cria árvores mais profundas e regras baseadas em divisões sequenciais Booleanas, o que dificulta a leitura das regras por especialistas de negócio.

**Escolha e Justificativa:**
Para o problema de análise de risco de crédito (onde a **explicabilidade e validação por especialistas humanos** – como o "gerente do banco" citado na questão – são essenciais), **a base de regras gerada pelo algoritmo C4.5 é a mais apropriada**. 
Suas regras são diretas (ex: *SE História é Boa E Renda é Acima de 35k...*), agrupam bem as instâncias baseando-se no histórico de crédito de forma natural, e a capacidade intrínseca do C4.5 de evitar overfitting garante uma generalização muito mais confiável para a aprovação de novos clientes em comparação às regras engessadas do ID3 ou excessivamente matemáticas do CART.
