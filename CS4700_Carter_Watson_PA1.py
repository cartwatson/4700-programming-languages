# programs
legal1 = "(+ (+ (+ 5 6) 6) 7)"
legal2 = "(+ (- (+ 5 1) 6) 7)"
legal3 = "(- (- (- 9 6) 1) 2)"
illegal1 = "(= 5 5)"
illegal2 = "(+ 5 5 5)"
illegal3 = "(- 5 5"

# -- starter code --
def tokenize(string):
  #inputs a string containing a Delta expression
  #returns a list of atoms of the language
  return string.replace('(', ' ( ').replace(')', ' )').split()

def parser(tokenList):
  #inputs a list of tokens
  #returns a parse tree, represented as a nested list structure
  token = tokenList.pop(0)
  if token[0].isdigit():
    return int(token)
  # assumes <exp> is (<operator> <exp> <exp>)
  ans = [tokenList.pop(0)] + [parser(tokenList)] + [parser(tokenList)]
  tokenList.pop(0) # to get rid of the ')'
  return ans
# -- end starter code -- 

# balanced
#check that the parentheses balance
def balanced(tokenList):
  openParantheses = 0
  closedParantheses = 0
  # check for equal numbers of parantheses
  for i in range(len(tokenList)):
    if tokenList[i] == '(':
      openParantheses += 1
    if tokenList[i] == ')':
      closedParantheses += 1 
  return closedParantheses == openParantheses

# prettyPrint
#print an expression readably
def prettyPrint(parsed, spacing=0):
  # iterate through parsed input
  for i in range(len(parsed)):
    if type(parsed[i]) == type([]):
      spacing += 1
      prettyPrint(parsed[i], spacing)
    
    if parsed[i] == '+' or parsed[i] == '-':
      print(spacing * "  " + '(' + parsed[i])
    elif type(parsed[i]) == type(1):
      print((spacing + 1) * "  " + str(parsed[i]))
    else:
      print(spacing * "  " + ')')
      spacing -= 1
  if spacing == 0:
    print(')')

# main
def runProgram(input):
  tokenList = tokenize(input)
  if (balanced(tokenList)):
    print("-- Legal Program --")
    parsed = parser(tokenList)
    print(parsed)
    prettyPrint(parsed)
  else:
    print("-- Illegal Program --")
    print("Operations not performed")

# run programs
print("--- Legal Programs ---")
runProgram(legal1)
runProgram(legal2)
runProgram(legal3)
print("--- Illegal Programs ---")
runProgram(illegal1)
runProgram(illegal2)
runProgram(illegal3)