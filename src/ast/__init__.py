from abc import ABC

class AST(ABC):
    nodeCount = 0

    def __init__(self):
        super().__init__()
        self._kids = []
        AST.nodeCount += 1
        self._nodeNum = AST.nodeCount
        self._label = ""

    def getKid(self, idx):
        if idx <= 0 or idx > kidCount():
            return None
        return _kids[idx - 1]

    def getKids(self):
        return self._kids

    def kidCount(self):
        return len(self._kids)

    def addKid(self, kidAST):
        self._kids.add(kidAST)

    def setLabel(self, label):
        self.label = label

    def getLabel(self):
        return self._label