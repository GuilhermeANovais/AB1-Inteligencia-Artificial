import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, classification_report
import os

def main():
    print("Iniciando Questão 4 (Geração de Regras - Mushroom)...")
    os.makedirs('output', exist_ok=True)
    
    # Ler o dataset da Q3 salvo na pasta data
    try:
        df = pd.read_csv('../data/dataset_kaggle_mushroom.csv')
    except:
        print("Erro: rode a Q3 primeiro para baixar o dataset Mushroom.")
        return
        
    X_raw = df.drop('class', axis=1)
    y = df['class'].map({'e': 0, 'p': 1})
    X = pd.get_dummies(X_raw)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    # Utilizando árvore restrita para simular geração direta de regras genéricas (ex: PRISM)
    clf = DecisionTreeClassifier(max_depth=3, min_samples_leaf=20, random_state=42)
    clf.fit(X_train, y_train)
    
    regras = export_text(clf, feature_names=list(X.columns))
    
    with open('output/regras_q4.txt', 'w') as f:
        f.write("Regras extraídas diretamente:\n")
        f.write(regras)
    
    print("Regras extraídas e salvas em output/regras_q4.txt")
    
    y_pred = clf.predict(X_test)
    
    acc = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    
    print(f"Métricas (Q4): Acurácia = {acc:.4f}, F1-Score = {f1:.4f}")
    with open('output/metricas_q4.txt', 'w') as f:
        f.write(f"Accuracy: {acc:.4f}\n")
        f.write(f"Precision: {prec:.4f}\n")
        f.write(f"Recall: {rec:.4f}\n")
        f.write(f"F1-Score: {f1:.4f}\n")
        f.write("\nRelatório:\n")
        f.write(classification_report(y_test, y_pred))
        
if __name__ == "__main__":
    main()
