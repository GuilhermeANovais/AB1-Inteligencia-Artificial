import sys

class Rule:
    def __init__(self, name, premises, conclusion):
        self.name = name
        self.premises = premises  # lista de strings (fatos)
        self.conclusion = conclusion  # string (fato alvo)

class KnowledgeBase:
    def __init__(self):
        self.rules = []
        self.facts = set()

    def add_rule(self, rule):
        self.rules.append(rule)

    def add_fact(self, fact):
        self.facts.add(fact)
        
    def remove_fact(self, fact):
        if fact in self.facts:
            self.facts.remove(fact)

    def clear(self):
        self.rules = []
        self.facts = set()

class InferenceEngine:
    def __init__(self, kb):
        self.kb = kb
        self.explanation_how = {} # fato -> tupla(nome_da_regra, premissas_usadas)

    def forward_chaining(self):
        inferred = True
        new_facts = set()
        
        while inferred:
            inferred = False
            for rule in self.kb.rules:
                if rule.conclusion not in self.kb.facts and rule.conclusion not in new_facts:
                    # Verifica se TODAS as premissas são conhecidas
                    if all(p in self.kb.facts or p in new_facts for p in rule.premises):
                        new_facts.add(rule.conclusion)
                        self.explanation_how[rule.conclusion] = (rule.name, rule.premises)
                        inferred = True
                        print(f"[Engine] Fato inferido (Forward): '{rule.conclusion}' através da regra {rule.name}")
                        
        self.kb.facts.update(new_facts)
        if not new_facts:
            print("[Engine] Nenhum fato novo pôde ser inferido com as regras atuais.")
        return new_facts

    def backward_chaining(self, goal, depth=0):
        indent = "  " * depth
        if goal in self.kb.facts:
            print(f"{indent}[Engine] '{goal}' já é um fato conhecido.")
            return True
            
        print(f"{indent}[Engine] Objetivo não resolvido: provar '{goal}'...")
        for rule in self.kb.rules:
            if rule.conclusion == goal:
                print(f"{indent}[Engine] -> Tentando aplicar a regra {rule.name} (Requer: {rule.premises})")
                all_premises_true = True
                for p in rule.premises:
                    if not self.backward_chaining(p, depth + 1):
                        all_premises_true = False
                        break
                if all_premises_true:
                    self.kb.add_fact(goal)
                    self.explanation_how[goal] = (rule.name, rule.premises)
                    print(f"{indent}[Engine] => SUCESSO! '{goal}' foi provado via {rule.name}!")
                    return True
        print(f"{indent}[Engine] => Falha ao provar '{goal}'.")
        return False
        
    def how(self, fact):
        """ Explanação de COMO um fato foi derivado (Trilha de inferência) """
        if fact not in self.explanation_how:
            if fact in self.kb.facts:
                print(f"O fato '{fact}' foi inserido diretamente pelo usuário (conhecimento a priori).")
            else:
                print(f"O fato '{fact}' não é conhecido pelo sistema.")
        else:
            rule_name, premises = self.explanation_how[fact]
            print(f"O fato '{fact}' foi inferido usando a regra [{rule_name}].")
            print(f"Isso ocorreu porque os seguintes fatos eram verdadeiros: {premises}")
            
    def why(self, fact):
        """ Explanação de POR QUE o sistema se importa com um fato """
        used_in = [r.name for r in self.kb.rules if fact in r.premises]
        if used_in:
            print(f"O fato '{fact}' é necessário porque ele é premissa para avaliar as regras: {used_in}")
        else:
            print(f"O fato '{fact}' no momento não serve de premissa para nenhuma regra cadastrada.")

def main():
    print("="*60)
    print(" SHELL GENÉRICO DE SISTEMA ESPECIALISTA (Baseado em Regras)")
    print("="*60)
    
    kb = KnowledgeBase()
    engine = InferenceEngine(kb)
    
    print("Comandos disponíveis (Diálogo Natural):")
    print("  add fato <texto>                     - Insere um fato na base")
    print("  add regra <nome> IF <f1,f2> THEN <c> - Insere uma regra (separe premissas com virgula)")
    print("  fc                                   - Executa Encadeamento para Frente (Forward)")
    print("  bc <objetivo>                        - Executa Encadeamento para Trás (Backward)")
    print("  como <fato>                          - Módulo de Explicação: COMO provou o fato?")
    print("  pq <fato>                            - Módulo de Explicação: POR QUE o fato é útil?")
    print("  status                               - Exibe Memória de Trabalho e Base de Regras")
    print("  sair                                 - Encerra o sistema")
    print("-" * 60)
    
    while True:
        try:
            cmd_line = input("\nSBC> ").strip()
        except EOFError:
            break
            
        if not cmd_line: continue
        parts = cmd_line.split()
        cmd = parts[0].lower()
        
        if cmd == "sair":
            print("Encerrando Shell Genérico...")
            break
            
        elif cmd == "add" and len(parts) >= 3:
            tipo = parts[1].lower()
            if tipo == "fato":
                fato = " ".join(parts[2:])
                kb.add_fact(fato)
                print(f"Fato '{fato}' registrado no sistema.")
            elif tipo == "regra":
                # Exemplo: add regra R1 IF chove,frio THEN gripado
                try:
                    nome = parts[2]
                    idx_if = parts.index("IF")
                    idx_then = parts.index("THEN")
                    premises = "".join(parts[idx_if+1:idx_then]).split(",")
                    conclusion = " ".join(parts[idx_then+1:])
                    
                    kb.add_rule(Rule(nome, premises, conclusion))
                    print(f"Regra {nome} inserida com sucesso.")
                except ValueError:
                    print("Sintaxe inválida! Formato correto: add regra NOME IF fato1,fato2 THEN conclusao")
                    
        elif cmd == "fc":
            print("Iniciando Motor de Inferência (Forward Chaining)...")
            engine.forward_chaining()
            
        elif cmd == "bc" and len(parts) > 1:
            objetivo = " ".join(parts[1:])
            print(f"Iniciando Motor de Inferência (Backward Chaining) buscando '{objetivo}'...")
            engine.backward_chaining(objetivo)
            
        elif cmd == "como" and len(parts) > 1:
            fato = " ".join(parts[1:])
            engine.how(fato)
            
        elif cmd == "pq" and len(parts) > 1:
            fato = " ".join(parts[1:])
            engine.why(fato)
            
        elif cmd == "status":
            print("\n--- STATUS DO SISTEMA ---")
            print("FATOS CONHECIDOS:")
            if not kb.facts:
                print("  (Nenhum fato na memória de trabalho)")
            else:
                for f in kb.facts: print(f"  • {f}")
                
            print("\nBASE DE REGRAS:")
            if not kb.rules:
                print("(Nenhuma regra cadastrada)")
            else:
                for r in kb.rules:
                    print(f"  [{r.name}] SE {r.premises} ENTÃO {r.conclusion}")
            print("-------------------------")
            
        else:
            print("Comando não reconhecido. Use 'status', 'add', 'fc', 'bc', 'como', 'pq' ou 'sair'.")

if __name__ == "__main__":
    main()
