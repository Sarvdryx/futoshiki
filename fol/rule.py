class Rule:
    def __init__(self, premises, conclusion):
        # self.premises = list(premises)    # for debugging 
        self.premises = set(premises)   
        self.conclusion = conclusion

    def __repr__(self):
        return f"{self.premises} => {self.conclusion}"