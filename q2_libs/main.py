import pandas as pd
from sklearn.tree import DecisionTreeClassifier, export_text
# pyrefly: ignore [missing-import]
import matplotlib.pyplot as plt
from sklearn import tree
import os

def main():
    print("Resolvendo a questão 2")
    
    # Garantir que a pasta de output existe
    os.makedirs('output', exist_ok=True)
    
    # 1. Carregar os dados
    dataset_path = '../data/dataset_ampliado.csv'
    df = pd.read_csv(dataset_path)
    
    # 2. Pré-processamento: Codificação de variáveis categóricas
    # A maioria dos modelos do sklearn exige que as categorias sejam numéricas
    df_encoded = pd.get_dummies(df.drop('Risco', axis=1))
    X = df_encoded
    y = df['Risco']
    
    # 3. Treinar Árvore de Decisão
    # O scikit-learn usa uma versão otimizada do CART
    clf = DecisionTreeClassifier(criterion='entropy', random_state=42)
    clf.fit(X, y)
    
    # 4. Exportar regras
    tree_rules = export_text(clf, feature_names=list(X.columns))
    with open('output/regras_q2.txt', 'w') as f:
        f.write(tree_rules)
    print("Regras salvas em output/regras_q2.txt")
    
    # 5. Plotar árvore
    plt.figure(figsize=(20,10))
    tree.plot_tree(clf, feature_names=list(X.columns), class_names=clf.classes_, filled=True, rounded=True)
    plt.savefig('output/arvore_q2.png')
    print("Gráfico da árvore salvo em output/arvore_q2.png")

if __name__ == "__main__":
    main()
