from enum import Enum, auto

class TokenCategory(Enum):
  # Variable Names
  varName = auto()

  # Primitives Types
  typeInt = auto()
  typeFloat = auto()
  typeBool = auto()
  typeChar = auto()
  typeString = auto()
  typeVoid = auto()

  # Accepted Values by the Primitives Types
  boolVal = auto()
  intVal = auto()
  floatVal = auto()
  charVal = auto()
  stringVal = auto()

  # Conditional Structure Commands
  cmdIf = auto()
  cmdElsif = auto()
  cmdElse = auto()

  # Repetition Structure Commands
  cmdFor = auto()
  cmdWhile = auto()

  # Logics Operators
  opTrue = auto()
  opFalse = auto()
  opNot = auto()
  opOr = auto()
  opAnd = auto()

  # Relationals Operators
  opEqual = auto()
  opNotEqual = auto()
  opGtrThan = auto()
  opLessThan = auto()
  opGtrEqual = auto()
  opLessEq = auto()

  # Mathematics Operators
  opAttr = auto()
  opAdd = auto()
  opSub = auto()
  opMult = auto()
  opDiv = auto()
  opMod = auto()
  opUnaryNeg = auto()
  opUnaryPos = auto()

  # Concatenation Operator 
  opConcat = auto()

  # Program Start Execution Point
  main = auto()

  # Terminal 
  semicolon = auto()

  # Separators
  commaSep = auto()

  # Functions
  fnDecl = auto()
  fnRtn = auto()

  # Input/Output
  fnRead = auto()
  fnWrite = auto()

  # One-Dimensional Arrays
  arrayBegin = auto()
  arrayEnd = auto()

  # Params Delimiters
  paramBegin = auto()
  paramEnd = auto()

  # Scope Delimiters
  scopeBegin = auto()
  scopeEnd = auto()

  # Tokens not defined
  tokenNotDefined = auto()

  # End Of File
  EOF = auto()

print(TokenCategory.opConcat.value)