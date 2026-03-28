from fol.logic import Symbol

def Val(i, j, v):
    return Symbol(f"Val_{i}_{j}_{v}")

def Given(i, j, v):
    return Symbol(f"Given_{i}_{j}_{v}")

def LessH(i, j):
    return Symbol(f"LessH_{i}_{j}")

def GreaterH(i, j):
    return Symbol(f"GreaterH_{i}_{j}")

def LessV(i, j):
    return Symbol(f"LessV_{i}_{j}")

def GreaterV(i, j):
    return Symbol(f"GreaterV_{i}_{j}")

def Less(i, j):
    return Symbol(f"Less_{i}_{j}")

def NotVal(i, j, v):
    return Symbol(f"NotVal_{i}_{j}_{v}")