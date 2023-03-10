# -*- coding: utf-8 -*-
"""Delta User Functions.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/15L0oeLNu2vJbXoAPc5ZG3aWJfZyEjz_X

Delta Language Inperpreter
"""

def run(program, debug = True):
  # input string, multiple expressions.
  # tokenize and parse all, then evaluate each Delta program 
   global UserFunctions, Debug
   Debug = debug
   UserFunctions = {}
   tokens = tokenize(program)
   codeList = []
   while tokens != []:
     codeList.append(parse(tokens))
   #print(codeList)
   for code in codeList:
     evalDeltaShow(code)

def tokenize(string):
  #inputs a string containing a Delta expression
  #returns a list of atoms of the language
  tokenList = string.replace('(', ' ( ').replace(')', ' )').replace('::=', ' ').replace('[', ' ( ').replace(']', ' ) ').split()
  return tokenList
  
def parse(tokenList):
  #inputs a list of tokens
  #returns a parse tree, represented as a nested list structure
  token = tokenList.pop(0)
  if token[0].isdigit(): #terminal
    return int(token)
  if token[0] != '(': #terminal
    return token
  #  <exp> can be (<operator> <exp>) or (<operator> <exp> <exp>) or (<operator> followed by any number of expressions
  ans = [tokenList.pop(0)]
  while tokenList[0] != ')':
    ans.append(parse(tokenList)) 
  tokenList.pop(0) # to get rid of the ')'
  return ans

def evalDeltaShow(exp, stackFrames = [], depth = 0):
  if Debug:
    print("   |"*depth + "-> " + str(exp))
  result = evalDelta(exp, stackFrames, depth + 1)
  if Debug:
    print("   |"*depth + "-< " + str(result))
  return result

def evalDelta(exp, stackFrames = [], depth = 0):
  # input a parsed expression, list of stack frames
  if not isinstance(exp, list):
    return evalDeltaAtom(exp, stackFrames, depth)
  if exp[0] == 'fun': # user defined function, remember (formal parameters, body)
     UserFunctions[exp[1]] = exp[2:]
     return None
  if exp[0] == '❗':
    return not evalDeltaShow(exp[1], stackFrames, depth)
  if exp[0] == '|':
    return evalDeltaShow(exp[1], stackFrames, depth) or evalDeltaShow(exp[2], stackFrames, depth)
  if exp[0] == '&':
    return evalDeltaShow(exp[1], stackFrames, depth) and evalDeltaShow(exp[2], stackFrames, depth)
  if exp[0] == '+':
    return evalDeltaShow(exp[1], stackFrames, depth) + evalDeltaShow(exp[2], stackFrames, depth)
  if exp[0] == '-':
    return evalDeltaShow(exp[1], stackFrames, depth) - evalDeltaShow(exp[2], stackFrames, depth)
  if exp[0] == '/':
    return evalDeltaShow(exp[1], stackFrames, depth) // evalDeltaShow(exp[2], stackFrames, depth)
  if exp[0] == '*':
    return evalDeltaShow(exp[1], stackFrames, depth) * evalDeltaShow(exp[2], stackFrames, depth)
  if exp[0] == '==':
    return evalDeltaShow(exp[1], stackFrames, depth) == evalDeltaShow(exp[2], stackFrames, depth)
  if exp[0] == '<':
    return evalDeltaShow(exp[1], stackFrames, depth) < evalDeltaShow(exp[2], stackFrames, depth)
  if exp[0] == 'if':
    if evalDeltaShow(exp[1], stackFrames, depth): 
       return evalDeltaShow(exp[2], stackFrames, depth)
    return evalDeltaShow(exp[3], stackFrames, depth) 
  #must be a user defined function
  return evalDeltaUserCall(exp, stackFrames, depth)

def evalDeltaAtom(exp, stackFrames, depth):
  # exp is an atom in Delta
  if isinstance(exp, int):
    return exp
  if exp == '👍':
    return True
  if exp == '👎':
    return False
  #user defined variable, look up its value 
  for frame in stackFrames:
    if exp in frame:
      return frame[exp]

def evalDeltaUserCall(exp, stackFrames, depth):
  #must be a user defined function
  (formalParameters, functionBody) = UserFunctions[exp[0]]
  variableValues = {} # use a dictionary to map formal parameters to actual parameters (values)
  for (parameter, actual) in zip(formalParameters, exp[1:]):
    variableValues[parameter] = evalDeltaShow(actual, stackFrames, depth)
  return evalDeltaShow(functionBody, [variableValues] + stackFrames, depth)



#code = "(fun fact (x) (if (== x 0) 1 (* x (fact (- x 1))))) (fact 2)"
code = "(fun fib (x) (if (| (== x 0) (== x 1)) 1 (+ (fib (- x 1)) (fib (- x 2))))) (fib 10)"

#code = "(fun plus1 (x) (+ 1 x)) (fun divide (a b) (/ a b)) (plus1 (divide# (plus1 7) 22))"
run(code)