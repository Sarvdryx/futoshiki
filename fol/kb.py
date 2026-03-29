class KnowledgeBase:
    def __init__(self):
        self.facts = set()
        self.rules = []

    def add_fact(self, fact):
        self.facts.add(fact)

    def add_rule(self, rule):
        self.rules.append(rule)

    def copy(self):
        new_kb = KnowledgeBase()
        new_kb.facts = set(self.facts)   # copy set
        new_kb.rules = list(self.rules)  # copy list
        return new_kb