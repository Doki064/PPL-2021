from abc import ABC


class AST(ABC):
    nodeCount = 0

    def __init__(self, label):
        super().__init__()
        self._kids = []
        AST.nodeCount += 1
        self._nodeNum = AST.nodeCount
        self._label = label

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
        return self

    def setLabel(self, label):
        self.label = label

    def getLabel(self):
        return self._label


class programTree(AST):
    def __init__(self, label):
        super().__init__(label)


class blockTree(AST):
    def __init__(self, label):
        super().__init__(label)


class declrTree(AST):
    def __init__(self, label):
        super().__init__(label)


class declTreeWithAssign(AST):
    def __init__(self, label):
        super().__init__(label)


class funcDeclTree(AST):
    def __init__(self, label):
        super().__init__(label)


class funcHeadTree(AST):
    def __init__(self, label):
        super().__init__(label)

class typeTree(AST):
    def __init__(self, label):
        super().__init__(label)


class idTree(AST):
    def __init__(self, label, name):
        super().__init__(label)
        self.name = name

    def getName(self):
        return self.name
class assignTree(AST):
    def __init__(self, label):
        super().__init__(label)


class ifTree(AST):
    def __init__(self, label):
        super().__init__(label)
        

class whileTree(AST):
    def __init__(self, label):
        super().__init__(label)


class returnTree(AST):
    def __init__(self, label):
        super().__init__(label)