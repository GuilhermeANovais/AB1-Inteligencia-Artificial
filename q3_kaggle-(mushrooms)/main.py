import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, classification_report
import os

def main():
    print("Resolvendo a questão 3")
    os.makedirs('output', exist_ok=True)
    
    # Dataset Mushroom Classification do UCI / Kaggle
    url = "https://archive.ics.uci.edu/ml/machine-learning-databases/mushroom/agaricus-lepiota.data"
    columns = [
        'class', 'cap-shape', 'cap-surface', 'cap-color', 'bruises', 'odor',
        'gill-attachment', 'gill-spacing', 'gill-size', 'gill-color',
        'stalk-shape', 'stalk-root', 'stalk-surface-above-ring', 'stalk-surface-below-ring',
        'stalk-color-above-ring', 'stalk-color-below-ring', 'veil-type', 'veil-color',
        'ring-number', 'ring-type', 'spore-print-color', 'population', 'habitat'
    ]
    print(f"Baixando dataset de: {url}")
    df = pd.read_csv(url, names=columns)
    
    # Salvar o dataset localmente na pasta data
    df.to_csv('../data/dataset_kaggle_mushroom.csv', index=False)
    
    # Separa features e target (class: e=edible, p=poisonous)
    X_raw = df.drop('class', axis=1)
    # Codifica 'e' como 0 e 'p' como 1
    y = df['class'].map({'e': 0, 'p': 1})
    
    # One-Hot Encoding para as features categóricas
    X = pd.get_dummies(X_raw)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    # Treinando a Árvore de Decisão
    clf = DecisionTreeClassifier(max_depth=5, random_state=42)
    clf.fit(X_train, y_train)
    
    # Gerando as Regras
    regras = export_text(clf, feature_names=list(X.columns))
    with open('output/regras_q3.txt', 'w') as f:
        f.write(regras)
    print("Regras extraídas e salvas em output/regras_q3.txt")
    
    # Avaliando
    y_pred = clf.predict(X_test)
    
    acc = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    
    with open('output/metricas_q3.txt', 'w') as f:
        f.write(f"Accuracy: {acc:.4f}\n")
        f.write(f"Precision: {prec:.4f}\n")
        f.write(f"Recall: {rec:.4f}\n")
        f.write(f"F1-Score: {f1:.4f}\n\n")
        f.write(classification_report(y_test, y_pred))
        
    print(f"Métricas avaliadas e salvas em output/metricas_q3.txt")
    print(f"Acurácia: {acc:.4f} | F1-Score: {f1:.4f}")

if __name__ == "__main__":
    main()
