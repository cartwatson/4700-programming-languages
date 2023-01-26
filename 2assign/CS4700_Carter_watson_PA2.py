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
  # input string, output the execution of the Delta program
  return evalDelta(parse(tokenize(program)))

def evalDelta(exp):
  if isinstance(exp, int):
    return exp
  if exp == '👍':
    return True
  if exp == '👎':
    return False
  if exp[0] == '❗':
    return not evalDelta(exp[1])
  if exp[0] == '|':
    return evalDelta(exp[1]) or evalDelta(exp[2])
  if exp[0] == '&':
    return evalDelta(exp[1]) and evalDelta(exp[2])
  #know [<operator> <exp> <exp>]
  if exp[0] == '+':
    return evalDelta(exp[1]) + evalDelta(exp[2])
  if exp[0] == '-':
    return evalDelta(exp[1]) - evalDelta(exp[2])
  if exp[0] == '/':
    return evalDelta(exp[1]) // evalDelta(exp[2])
  if exp[0] == '*':
    return evalDelta(exp[1]) * evalDelta(exp[2])
  if exp[0] == '==':
    return evalDelta(exp[1]) == evalDelta(exp[2])
  if exp[0] == '<':
    return evalDelta(exp[1]) < evalDelta(exp[2])
  if exp[0] == 'if':
    if evalDelta(exp[1]):
      try:
        return evalDelta(exp[2])
      except:
        return True
    else:
      try:
        return evalDelta(exp[3])
      except:
        return True

# random program genereator
def randPG(programType):
  if programType == "boolean":
    return generateBoolean()
  elif programType == "numerical":
    return generateNumerical()
  elif programType == "conditional":
    return generateConditional()
  else:
    return "ERROR: INVALID PROGRAM TYPE REQUESTED"

def generateBoolean():
  output = "("
  operator = generateOperatorHelper("boolean") + " " 
  output += generateOperatorHelper("boolean") + " "
  output += generateBooleanHelper()
  if "❗" not in operator:
    output +=  " " + generateBooleanHelper()
  return output + ")"

def generateBooleanHelper():
  if random.choice([True, False, False]):
    return generateBoolean()
  else:
    return '👍' if random.randint(0, 1) else '👎'

def generateNumerical():
  output = "("
  output += generateOperatorHelper("numerical") + " "
  output += generateNumericalHelper() + " "
  output += generateNumericalHelper()
  return output + ")"

def generateNumericalHelper():
  if random.choice([True, False, False]):
    return generateNumerical()
  else:
    return str(random.randint(0, 1000)) # Arbitrary numbers, chose small numbers to increase readability

def generateOperatorHelper(type):
  booleanOperators   = ["==", "<", "|", "&", "❗"]
  numericalOperators = ["+", "-", "*", "/"]
  if type == "boolean":
    return random.choice(booleanOperators)
  elif type == "numerical":
    return random.choice(numericalOperators)

def generateConditional():
  output = "(if "
  output += generateBoolean() + " "
  output += generateNumerical() + " "
  output += generateNumerical()
  return output + ") "


deltaCode = "(if (< 81 80) 4 5)"
# deltaCode = ""
print(run(deltaCode))
print(randPG("numerical"))
print(randPG("boolean"))
print(randPG("conditional"))