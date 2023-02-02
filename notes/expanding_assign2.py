# <exp> ::= 0 | 1 | 2
# <exp> ::= '👍' | '👎'
# <exp> ::= (<Operator> <exp> <exp>)
# <exp> ::= ('|' <exp> <exp) | ('&' <exp> <exp>) | ('❗' <exp>)
# <numericalOperator> ::= '+' | '-' | '*' | '/'
# <booleanOperator> ::= '|' | '&' | '❗' 


import random

def tokenize(string):
  #inputs a string containing a Delta expression
  #returns a list of atoms of the language
  return string.replace('(', ' ( ').replace(')', ' )').split()

def parse(tokenList):
  #inputs a list of tokens
  #returns a parse tree, represented as a nested list structure
  token = tokenList.pop(0)
  if token[0].isdigit():
    return int(token)
  # just a terminal
  if token[0] != '(':
    return token
  #  <exp> can be (<operator> <exp>) or (<operator> <exp> <exp>) or (<operator> followed by any number of expressions
  ans = [tokenList.pop(0)]
  while tokenList[0] != ')':
    ans.append(parse(tokenList)) 
  tokenList.pop(0) # to get rid of the ')'
  return ans

# print(parse(tokenize(deltaCode)))

#check that the parentheses balance
def balanced(tokenList):
  count = 0
  for token in tokenList:
    if token == '(':
      count+= 1
    if token == ')':
      count-= 1
    if count < 0:
      return False
  return count == 0

# print(balanced(tokenize(deltaCode)))

def prettyPrint(exp, depth = 0):
  if isinstance(exp,int):
    print(" "*3*depth + str(exp))
  else:
    print(" "*3*depth + "(" + str(exp[0]))
    prettyPrint(exp[1], depth+1)
    prettyPrint(exp[2], depth+1)
    print(" "*3*depth + ")")

# prettyPrint(parse(tokenize(deltaCode)))

def run(program):
  global UserFunctions
  UserFunctions = {}
  # input string, output the execution of the Delta program
  tokens = tokenize(program)  
  codeList = []
  while tokens != []:
    codeList.append(parse(tokens))
#   print(codeList) # DEBUG
  for code in codeList:
    print(evalDelta(code))

def evalDelta(exp, stackFrames = []):
  # atoms, primitives
  if isinstance(exp, int):
    return exp
  if exp == '👍':
    return True
  if exp == '👎':
    return False
  # user defined variable
  if not isinstance(exp, list):
    for frame in stackFrames:
      # TODO IMPLEMENT -------------------------------------
      pass
  # <exp>'s
  # logical operators
  if exp[0] == '❗':
    return not evalDelta(exp[1])
  if exp[0] == '|':
    return '👍' if evalDelta(exp[1]) or evalDelta(exp[2]) else '👎'
  if exp[0] == '&':
    return '👍' if evalDelta(exp[1]) and evalDelta(exp[2]) else '👎'
  # mathmatical operators
  if exp[0] == '+':
    return evalDelta(exp[1]) + evalDelta(exp[2])
  if exp[0] == '-':
    return evalDelta(exp[1]) - evalDelta(exp[2])
  if exp[0] == '/':
    return evalDelta(exp[1]) // evalDelta(exp[2])
  if exp[0] == '*':
    return evalDelta(exp[1]) * evalDelta(exp[2])
  # logical operators of integers
  if exp[0] == '==':
    return '👍' if evalDelta(exp[1]) == evalDelta(exp[2]) else '👎'
  if exp[0] == '<':
    return '👍' if evalDelta(exp[1]) < evalDelta(exp[2]) else '👎'
  # conditionals
  if exp[0] == 'if':
    # try blocks for catching nested conditionals
    if evalDelta(exp[1]):
      try: return evalDelta(exp[2])
      except: return '👍'
    else:
      try: return evalDelta(exp[3])
      except: return '👎'
  # user functions
  # define
  if exp[0] == "fun":
    UserFunctions[exp[1]] = exp[2:]
    return
  # execute
  if exp[0] in UserFunctions.keys():
    (formalParameters, functioBody) = UserFunctions[exp[0]]
    # setup parameters
    variableValues = {}
    for (parameter, actual) in zip(formalParameters, exp[1:]):
        variableValues[parameter] = evalDelta(actual)
    # run function
    return evalDelta(functioBody, [variableValues] + stackFrames)

# random program genereator
def randPG(programType):
  if programType == "boolean":
    return generateBoolean()
  elif programType == "numerical":
    return "(" + generateOperator("numerical") + " " + generateExp("numerical") + " " + generateExp("numerical") + ")"
  elif programType == "conditional":
    return "(if " + randPG("boolean") + " " + randPG("numerical") + " " + randPG("numerical") + ") "
  else:
    return "ERROR: INVALID PROGRAM TYPE REQUESTED"

def generateBoolean():
  operator = generateOperator("boolean")
  output = "(" + operator + " "
  if operator in ["<"]: # List of all boolean binary operators that compare numbers 
    output += generateExp("numerical") + " " + generateExp("numerical")
  else:
    output += generateExp("boolean")
    if operator not in  ["❗"]: # List of all boolean unary operators
      output +=  " " + generateExp("boolean")
  return output + ")"

def generateExp(expType):
  if random.random() < 0.75: # arbitrary numbers, determines how often exp are recursive 0.75 = 75% of the time the call is non recursive
    # recursive call for more exp
    if expType == "numerical":
      return randPG("numerical")
    elif expType == "boolean":
      return randPG("boolean")
  else:
    # non recursive call, returns a value
    if expType == "numerical":
      return str(random.randint(0, 1000)) # Arbitrary numbers, chose small numbers to increase readability
    elif expType == "boolean":
      return '👍' if random.choice([True, False]) else '👎'

def generateOperator(expType):
  if expType == "numerical":
    return random.choice(["+", "-", "*", "/"]) # Numerical Operators
  elif expType == "boolean":
    return random.choice(["==", "<", "|", "&", "❗"]) # Boolean Operators


# print("examples of '==' '<' and 'if")
# print("(== 👍 1):\t" + run("(== 👍 1)"))
# print("(== 0 0):\t" + run("(== 0 0)"))
# print("(< 79 80):\t" + run("(< 79 80)"))
# print("(< 81 80):\t" + run("(< 81 80)"))
# print("(< 80 80):\t" + run("(< 80 80)"))
# print("(if (< 81 80) 4 5):\t" + str(run("(if (< 81 80) 4 5)")))
# print("(if (== 80 80) 4 5):\t" + str(run("(if (== 80 80) 4 5)")))

# print("\nexamples of randPG")
# print(randPG("numerical"))
# print(randPG("boolean"))
# print(randPG("conditional"))

code = "(+ 1 2) (* 5 6)"
run(code)