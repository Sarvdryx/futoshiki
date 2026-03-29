import itertools

class Sentence:
    def evaluate(self, model):
        raise Exception("Nothing to evaluate")

    def formula(self):
        return ""

    def symbols(self):
        return set()

    @classmethod
    def validate(cls, sentence):
        if not isinstance(sentence, Sentence):
            raise TypeError("Must be a logical sentence")

    @classmethod
    def parenthesize(cls, s):
        def balanced(s):
            count = 0
            for c in s:
                if c == "(":
                    count += 1
                elif c == ")":
                    if count <= 0:
                        return False
                    count -= 1
            return count == 0

        if not len(s) or s.isalpha() or (
            s[0] == "(" and s[-1] == ")" and balanced(s[1:-1])
        ):
            return s
        return f"({s})"


# =========================
# SYMBOL
# =========================
class Symbol(Sentence):
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return isinstance(other, Symbol) and self.name == other.name

    def __hash__(self):
        return hash(("symbol", self.name))

    def __repr__(self):
        return self.name

    def evaluate(self, model):
        if self.name not in model:
            raise Exception(f"{self.name} not in model")
        return bool(model[self.name])

    def formula(self):
        return self.name

    def symbols(self):
        return {self.name}


# =========================
# NOT
# =========================
class Not(Sentence):
    def __init__(self, operand):
        Sentence.validate(operand)
        self.operand = operand

    def __repr__(self):
        return f"¬{self.operand}"

    def evaluate(self, model):
        return not self.operand.evaluate(model)

    def formula(self):
        return "¬" + Sentence.parenthesize(self.operand.formula())

    def symbols(self):
        return self.operand.symbols()
    
    def __eq__(self, other):
        return isinstance(other, Not) and self.operand == other.operand

    def __hash__(self):
        return hash(("not", self.operand))


# =========================
# AND
# =========================
class And(Sentence):
    def __init__(self, *conjuncts):
        for c in conjuncts:
            Sentence.validate(c)
        self.conjuncts = list(conjuncts)

    def add(self, conjunct):
        Sentence.validate(conjunct)
        self.conjuncts.append(conjunct)

    def __repr__(self):
        return " ∧ ".join(str(c) for c in self.conjuncts)

    def evaluate(self, model):
        return all(c.evaluate(model) for c in self.conjuncts)

    def formula(self):
        return " ∧ ".join(
            Sentence.parenthesize(c.formula()) for c in self.conjuncts
        )

    def symbols(self):
        return set.union(*[c.symbols() for c in self.conjuncts]) if self.conjuncts else set()

    def __eq__(self, other):
        return isinstance(other, And) and set(self.conjuncts) == set(other.conjuncts)

    def __hash__(self):
        return hash(("and", tuple(sorted(self.conjuncts, key=hash))))

# =========================
# OR
# =========================
class Or(Sentence):
    def __init__(self, *disjuncts):
        for d in disjuncts:
            Sentence.validate(d)
        self.disjuncts = list(disjuncts)

    def __repr__(self):
        return " ∨ ".join(str(d) for d in self.disjuncts)

    def evaluate(self, model):
        return any(d.evaluate(model) for d in self.disjuncts)

    def formula(self):
        return " ∨ ".join(
            Sentence.parenthesize(d.formula()) for d in self.disjuncts
        )

    def symbols(self):
        return set.union(*[d.symbols() for d in self.disjuncts])

    def __eq__(self, other):
        return isinstance(other, Or) and set(self.disjuncts) == set(other.disjuncts)

    def __hash__(self):
        return hash(("or", tuple(sorted(self.disjuncts, key=hash))))

# =========================
# IMPLICATION
# =========================
class Implication(Sentence):
    def __init__(self, antecedent, consequent):
        Sentence.validate(antecedent)
        Sentence.validate(consequent)
        self.antecedent = antecedent
        self.consequent = consequent

    def __repr__(self):
        return f"({self.antecedent} => {self.consequent})"

    def evaluate(self, model):
        return (not self.antecedent.evaluate(model)) or self.consequent.evaluate(model)

    def formula(self):
        return f"{Sentence.parenthesize(self.antecedent.formula())} => {Sentence.parenthesize(self.consequent.formula())}"

    def symbols(self):
        return self.antecedent.symbols().union(self.consequent.symbols())
    
    def __eq__(self, other):
        return (
            isinstance(other, Implication)
            and self.antecedent == other.antecedent
            and self.consequent == other.consequent
        )

    def __hash__(self):
        return hash(("imp", self.antecedent, self.consequent))


# =========================
# MODEL CHECKING
# =========================
def model_check(knowledge, query):
    """
    Checks if KB entails query
    """

    def check_all(knowledge, query, symbols, model):
        if not symbols:
            if knowledge.evaluate(model):
                return query.evaluate(model)
            return True

        remaining = symbols.copy()
        p = remaining.pop()

        model_true = model.copy()
        model_true[p] = True

        model_false = model.copy()
        model_false[p] = False

        return (
            check_all(knowledge, query, remaining, model_true)
            and check_all(knowledge, query, remaining, model_false)
        )

    symbols = knowledge.symbols().union(query.symbols())
    return check_all(knowledge, query, symbols, {})