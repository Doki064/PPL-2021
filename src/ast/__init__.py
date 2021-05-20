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
    def __init__(self):
        super().__init__('Program/Class')


class blockTree(AST):
    def __init__(self):
        super().__init__('Code block')


class declrTree(AST):
    def __init__(self):
        super().__init__('Declaration')


class declTreeWithAssign(AST):
    def __init__(self):
        super().__init__('Declaration with Assignment')


class funcDeclTree(AST):
    def __init__(self):
        super().__init__('Function Declaration')


class funcHeadTree(AST):
    def __init__(self):
        super().__init__('Function header')

class typeTree(AST):
    def __init__(self):
        super().__init__('Type')


class idTree(AST):
    def __init__(self, name):
        super().__init__('id')
        self.name = name

    def getName(self):
        return self.name
class assignTree(AST):
    def __init__(self, assignToken):
        super().__init__('Assignment')
        self.assignToken = assignToken

    def getAssignToken(self):
        return self.assignToken


class ifTree(AST):
    def __init__(self):
        super().__init__('if statement')
        

class whileTree(AST):
    def __init__(self):
        super().__init__('while statement')


class returnTree(AST):
    def __init__(self):
        super().__init__('return statement')