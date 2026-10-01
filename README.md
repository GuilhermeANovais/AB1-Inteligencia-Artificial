# Atividade de Inteligência Artificial - Lista 1 (2026.2)

Este repositório contém as resoluções das atividades avaliativas da disciplina de Inteligência Artificial (Lista 1).

## Q1 - Árvores de Decisão Manuais (ID3, C4.5 e CART)

Implementação manual de árvores de decisão para análise de risco de crédito, a partir de uma base ampliada para 30 exemplos e 6 atributos (`Historia de Credito`, `Divida`, `Garantia`, `Renda`, `Idade`, `Emprego_Fixo`).

- A base de dados gerada encontra-se em `data/dataset_ampliado.csv`.
- A construção passo-a-passo teórica das árvores ID3, C4.5 e CART, a extração de regras e a justificativa técnica da melhor abordagem (C4.5) podem ser encontradas detalhadamente no documento **`q1/resolucao_q1.md`**.

---

## Q2 - Implementação com Bibliotecas (ID3, C4.5 e CART)

**Biblioteca Utilizada:** `scikit-learn` (Python), associada à biblioteca `pandas` para pré-processamento via One-Hot Encoding e `matplotlib` para visualização gráfica da árvore de decisão.

O código-fonte da solução está na pasta `q2/`.

### Resultados Obtidos
A árvore gerou altíssima assertividade sobre os dados propostos.
- O gráfico da árvore resultante foi gerado e salvo em `q2/output/arvore_q2.png`.
- As regras textuais lógicas foram geradas e salvas em `q2/output/regras_q2.txt`.

Para rodar:
```bash
cd q2
pip install -r requirements.txt
python main.py
```

---

## Q3 - Dataset Kaggle e Métricas de Avaliação

**Dataset:** Mushroom Classification (Kaggle / UCI Machine Learning Repository)
**Objetivo:** Prever a classe dos cogumelos (0 = comestível/edible, 1 = venenoso/poisonous).

Foi utilizada uma árvore de decisão baseada no algoritmo CART otimizado do `scikit-learn` (com `max_depth=5` para mitigar *overfitting*), operando sob atributos categorizados via One-Hot Encoding.

O código-fonte e resultados encontram-se na pasta `q3/`. O dataset baixado automaticamente e utilizado para o treinamento está em `data/dataset_kaggle_mushroom.csv`.

### Métricas de Avaliação
Obtivemos um resultado excepcionalmente preciso, indicando o forte padrão nas características morfológicas dos cogumelos e o ótimo funcionamento do classificador:
- **Acurácia:** 0.9996 (99.96%)
- **Precisão:** 0.9992
- **Recall:** 1.0000
- **F1-Score:** 0.9996

---

## Q4 - Geração Direta de Regras (Algoritmo Simulação PRISM)

Como o ecossistema Python e o Scikit-Learn não possuem nativamente algoritmos dedicados exclusivamente à indução de regras modulares (como o PRISM original), foi simulada a geração direta de regras genéricas utilizando uma extrema restrição na Árvore de Decisão (`max_depth=3`, `min_samples_leaf=20`) utilizando a mesma base de dados de cogumelos da Q3.

### Métricas de Avaliação (Regras Restritas)
Mesmo forçando a extração de regras limitadas para evitar crescimento de árvores, o forte poder discriminatório dos dados resultou em excelentes predições:
- **Acurácia:** 0.9820 (98.20%)
- **F1-Score:** 0.9817

O código encontra-se em `q4/main.py` e as regras extraídas de forma legível estão em `q4/output/regras_q4.txt`.

---

## Q5 - Shell Genérico de Sistema Baseado em Conhecimento (SBC)

**Arquitetura Implementada:** Base de Conhecimento $\rightarrow$ Motor de Inferência $\rightarrow$ Explicação $\rightarrow$ Interface interativa via Terminal.

A ferramenta foi totalmente desenvolvida em Python de forma **genérica** e modular, localizada em `q5/shell_gen.py`. O sistema não detém conhecimento prévio, permitindo que o usuário interaja via linha de comando para popular fatos e regras em linguagem natural.

### Exemplo de Interação:
```bash
python q5/shell_gen.py
SBC> add fato chove
✔ Fato 'chove' registrado no sistema.
SBC> add regra R1 IF chove,frio THEN gripado
✔ Regra R1 inserida com sucesso.
SBC> add fato frio
✔ Fato 'frio' registrado no sistema.

SBC> fc
>>> Iniciando Motor de Inferência (Forward Chaining)...
[Engine] Fato inferido (Forward): 'gripado' através da regra R1

SBC> como gripado
O fato 'gripado' foi inferido usando a regra [R1].
Isso ocorreu porque os seguintes fatos eram verdadeiros: ['chove', 'frio']
```

O Shell interativo suporta:
- **Encadeamento para Frente** (Forward Chaining - `fc`)
- **Encadeamento para Trás** (Backward Chaining - `bc <objetivo>`)
- **Módulo COMO** (`como <fato>`) - Trilha de inferência.
- **Módulo POR QUÊ** (`pq <fato>`) - Justificativa para a busca de premissas.
