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

def run(program):
  # input string, multiple expressions.
  # tokenize and parse all,
  # then evaluate each Delta program
   global UserFunctions
   UserFunctions = {}
   tokens = tokenize(program)
   codeList = []
   while tokens != []:
     codeList.append(parse(tokens))
   print(codeList)
   for code in codeList:
     print(evalDelta(code))

def debugHelper(exp, depth=0):
  print("   |" * depth, end="")

#print(UserFunctions)
def evalDelta(exp, stackFrames = [], DEBUG=False, depth=0):
  if DEBUG:
    debugHelper(exp, depth)
  # input a parsed expression, list of stack frames
  if isinstance(exp, int):
    return exp
  if exp == '👍':
    return True
  if exp == '👎':
    return False
  if not isinstance(exp, list):
    #user defined variable, look it up
    for frame in stackFrames:
      if exp in frame:
        return frame[exp]
  if exp[0] == 'fun':
    # user defined function, remember
     UserFunctions[exp[1]] = exp[2:]
     return 
  if exp[0] == '❗':
    return not evalDelta(exp[1], stackFrames)
  if exp[0] == '|':
    return evalDelta(exp[1], stackFrames) or evalDelta(exp[2], stackFrames)
  if exp[0] == '&':
    return evalDelta(exp[1], stackFrames) and evalDelta(exp[2], stackFrames)
  #know [<operator> <exp> <exp>]
  if exp[0] == '+':
    return evalDelta(exp[1], stackFrames) + evalDelta(exp[2], stackFrames)
  if exp[0] == '-':
    return evalDelta(exp[1], stackFrames) - evalDelta(exp[2], stackFrames)
  if exp[0] == '/':
    return evalDelta(exp[1], stackFrames) // evalDelta(exp[2], stackFrames)
  if exp[0] == '*':
    return evalDelta(exp[1], stackFrames) * evalDelta(exp[2], stackFrames)
  if exp[0] == '==':
    return evalDelta(exp[1], stackFrames) == evalDelta(exp[2], stackFrames)
  if exp[0] == '<':
    return evalDelta(exp[1], stackFrames) < evalDelta(exp[2], stackFrames)
  if exp[0] == 'if':
    if evalDelta(exp[1], stackFrames): 
       return evalDelta(exp[2], stackFrames)
    return evalDelta(exp[3], stackFrames) 
  #must be a user defined function
  (formalParameters, functionBody) = UserFunctions[exp[0]]
  variableValues = {} # use a dictionary to map formal parameters to actual parameters
  for (parameter, actual) in zip(formalParameters, exp[1:]):
    variableValues[parameter] = evalDelta(actual, stackFrames)
  return evalDelta(functionBody, [variableValues] + stackFrames)

code = "(fun plus1 (x) (+ 1 x)) (plus1 (plus1 7))"
run(code)

codeFactorial='FILL IN'
codeFibonacci='FILL IN'