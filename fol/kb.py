from fol.rule import Rule

class KnowledgeBase:
    def __init__(self):
        self.facts = set()
        self.rules = []
        self.agenda = []
        self.index = {}

    def add_fact(self, fact):
        if fact not in self.facts:
            self.facts.add(fact)
            self.agenda.append(fact)

    def add_rule(self, rule):
        self.rules.append(rule)
        rule.count = len(rule.premises)   

        for p in rule.premises:
            if p not in self.index:
                self.index[p] = []
            self.index[p].append(rule)

    def copy(self):
        new_kb = KnowledgeBase()
        new_kb.facts = set(self.facts)
        new_kb.agenda = list(self.agenda) # copy mutable list

        # 1️⃣ copy rules
        new_kb.rules = []
        for r in self.rules:
            new_rule = Rule(r.premises, r.conclusion)
            new_rule.count = r.count
            new_kb.rules.append(new_rule)

        # 2️⃣ rebuild index trỏ rule mới
        new_kb.index = {}
        for r in new_kb.rules:
            for p in r.premises:
                if p not in new_kb.index:
                    new_kb.index[p] = []
                new_kb.index[p].append(r)

        return new_kb