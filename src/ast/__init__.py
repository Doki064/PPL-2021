__all__ = [
    "programTree",
    "blockTree",
    "declrTree",
    "funcDeclTree",
    "funcHeadTree",
    "typeTree",
    "idTree",
    "numberTree",
    "stringTree",
    "assignTree",
    "ifTree",
    "whileTree",
    "returnTree",
    "callTree",
    "relOPTree",
    "addOPTree",
    "multOPTree",
]

from abc import ABC as _ABC


class _AST(_ABC):
    """ A simple Abstract Syntax Tree structure.

    Contains the root label and children ASTs.

    Attributes:
        nodeCount (static int): How many nodes in the program tree.
        _kids (list): List of immediate children AST.
        _label (str): Label of the root node.
        _nodeNum (int): The index of the root node in the program tree.
    """

    nodeCount = 0

    def __init__(self, label):
        """AST constructor.

        Args:
            label (int): The root node's label.
        """

        super().__init__()
        self._kids = []
        _AST.nodeCount += 1
        self._nodeNum = _AST.nodeCount
        self._label = label

    def getKid(self, idx):
        """Return the child AST at the given index.

        Args:
            idx (int): The index of the child AST.

        Returns:
            (AST) The child AST if exists, None if index out of bounds.
        """
        if idx <= 0 or idx > self.kidCount():
            return None
        return self._kids[idx - 1]

    def getKids(self):
        """Return a list containing the children ASTs of the root node.
        
        Returns:
            (List) List of children ASTs.
        """
        return self._kids

    def kidCount(self):
        """Return the number of children ASTs of the root node.

        Returns:
            (int) The number of children ASTs.
        """
        return len(self._kids)

    def addKid(self, kidAST):
        """Add an AST to the children list of the root node.

        Args:
            kidAST (AST): The child AST to be added

        Returns:
            (AST) The AST of the root node.
        """
        self._kids.append(kidAST)
        return self

    def setLabel(self, label):
        """Set the label of the root node.

        Args:
            label (str): The label to be set.

        Returns:
            None
        """
        self._label = label

    def getLabel(self):
        """Return the label of the AST's root node.

        Returns:
            (str) The label of the AST's root node.
        """
        return self._label

#                      GRAMMAR NOTES                                  #
# --------------------------------------------------------------------#
#               Children trees are noted by '*'                       #
#                   [] stands for a list of                           #
class programTree(_AST):
    """ An AST for the program structure.

        GRAMMAR:
            program    :-   class *id *block
    """
    def __init__(self):
        super().__init__('Program/Class')


class blockTree(_AST):
    """ An AST for a codeblock structure.

        GRAMMAR:
            block   :-  { [*statements] }
    """
    def __init__(self):
        super().__init__('Code block')


class declrTree(_AST):
    """ An AST for a declaration statement structure.

        GRAMMAR:
            declr   :-  *type *id = *expr ; 
                        *type *id ;
                        *type *id 
    """
    def __init__(self):
        super().__init__('Declaration')


class funcDeclTree(_AST):
    """ An AST for a function declaration structure.

        GRAMMAR:
            funcDeclr   :-  *type *id *funcHead *block
    """
    def __init__(self):
        super().__init__('Function Declaration')


class funcHeadTree(_AST):
    """ An AST for a function header structure.

        GRAMMAR:
            funcHead   :-   ()               #   void
                            ( [*declr] )     #   params / list of declr
    """
    def __init__(self):
        super().__init__('Function header')

class typeTree(_AST):
    """ An AST for a type structure.
        ATOMIC/LEAF

        GRAMMAR:
            type   :-   type

        Args:
            isList (bool): whether the type is for a single or a list/array of variables.
                            E.g: String vs String[]
    """
    def __init__(self, isList=False):
        super().__init__('Type')
        self.isArray = isList

    def setArray(self):
        """ Set the value of isList to True

        Returns:
            None
        """
        self.isArray = True

    def isArray(self):
        """ Return the value of isList.

        Returns:
            (bool) whether the type is an array or not.
        """
        return self.isArray


class idTree(_AST):
    """ An AST for a identifier or name.
        ATOMIC/LEAF

        GRAMMAR:
            id   :-   id/name

        Args:
            name (str): name of the identifier.
    """
    def __init__(self, name):
        super().__init__('id')
        self.name = name

    def getName(self):
        """ Return the value of id's name.

        Returns:
            (str) name of the id.
        """
        return self.name


class numberTree(_AST):
    """ An AST for a literal number.
        ATOMIC/LEAF

        GRAMMAR:
            num   :-    <int>
                        <float>
     
        Args:
            value (str): value of the literal number.
    """
    def __init__(self, value):
        super().__init__('literal number')
        self.value = value

    def getValue(self):
        """ Return the value of literal number.

        Returns:
            (str) value of the number.
        """
        return self.value


class stringTree(_AST):
    """ An AST for a literal string.
        ATOMIC/LEAF

        GRAMMAR:
            string  :-  string
     
        Args:
            value (str): value of the literal string.
    """
    def __init__(self, value):
        super().__init__('literal string')
        self.value = value

    def getValue(self):
        """ Return the value of literal string.

        Returns:
            (str) value of the string.
        """
        return self.value


class assignTree(_AST):
    """ An AST for a assignment structure.

        GRAMMAR:
            assignment  :-  *id assign_op *expr ;
     
        Args:
            assignToken (str): the assignment operator token name.
    """
    def __init__(self, assignToken):
        super().__init__('Assignment')
        self.assignToken = assignToken

    def getToken(self):
        """ Return the assignment operator token name.

        Returns:
            (str) the assignment operator token name.
        """
        return self.assignToken


class ifTree(_AST):
    """ An AST for a ifStatement structure.

        GRAMMAR:
            ifStatement  :-  if ( *expr ) *block
                             if ( *expr ) *block else *block
    """
    def __init__(self):
        super().__init__('if statement')
        

class whileTree(_AST):
    """ An AST for a whileStatement structure.

        GRAMMAR:
            whileStatement  :-  while ( *expr ) *block
    """
    def __init__(self):
        super().__init__('while statement')


class returnTree(_AST):
    """ An AST for a returnStatement structure.

        GRAMMAR:
            returnStatement  :-  return expr ;
    """
    def __init__(self):
        super().__init__('return statement')


class callTree(_AST):
    """ An AST for a function call structure.

        GRAMMAR:
            funcCall  :-  *id ()
                          *id ( [*expr] )
    """
    def __init__(self):
        super().__init__('function call')


class relOPTree(_AST):
    """ An AST for a relation operation structure.

        GRAMMAR:
            relOp   :-  *expr rel_op *expr

        Args:
            relToken (str): the relational operator token name.
    """
    def __init__(self, relToken):
        super().__init__('Relational Operation')
        self.relToken = relToken

    def getToken(self):
        """ Return the relation operator token name.

        Returns:
            (str) the relation operator token name.
        """
        return self.relToken


class addOPTree(_AST):
    """ An AST for a addition operation structure.

        GRAMMAR:
            addOp   :-  *expr rel_op *expr
            
        Args:
            addToken (str): the addition operator token name.
    """
    def __init__(self, addToken):
        super().__init__('Additional Operation')
        self.addToken = addToken

    def getToken(self):
        """ Return the addition operator token name.

        Returns:
            (str) the addition operator token name.
        """
        return self.addToken


class multOPTree(_AST):
    """ An AST for a multiplication operation structure.

        GRAMMAR:
            addOp   :-  *expr rel_op *expr
                        
        Args:
            multToken (str): the multiplication operator token name.
    """
    def __init__(self, multToken):
        super().__init__('Multiplication Operation')
        self.multToken = multToken

    def getToken(self):
        """ Return the multiplication operator token name.

        Returns:
            (str) the multiplication operator token name.
        """
        return self.multToken
