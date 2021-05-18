from abc import ABC

class AST(ABC):
    nodeCount = 0

    def __init__(self):
        super().__init__()
        self.kids = []
        AST.nodeCount += 1
        self.nodeNum = AST.nodeCount
        self.label = ""

    def getKid(self, idx):
        if idx <= 0 or idx > kidCount():
            return None
        return kids[idx - 1]

    def getKids(self):
        return self.kids

    def kidCount(self):
        return len(self.kids)

    def addKid(self, kidAST):
        self.kids.add(kidAST)

    def setLabel(self, label):
        self.label = label

    def getLabel(self):
        return self.label