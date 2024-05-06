import os
import ast

# Get current working directory
CWD = os.getcwd()
FilesList = os.listdir(CWD)
print('\n\nFiles Names In The Current Directory : ', FilesList)

FileName = input("\nEnter The Name Of The File That You Want Compile:\n--> ") 
SourceCode = open(FileName, 'r').read() #Read The File Content        

def lexer(x):

    operators=['+','-', "/", '*', '%', '=', '&','|','^','~']
    punctuations=[':' , ',' , ';', '.','[', '{', '(',']', '}', ')']

    MyStr=''

    for i in range (len(x)):
        try:
            # If the character is an operator and both the previous and next characters are also operators
            if x[i] in operators and x[i+1] in operators and x[i-1] not in operators:
                MyStr+=' '+x[i]

            # If the character is an operator and either the previous or next character (or both) are not operators
            elif x[i] in operators and x[i+1] not in operators and x[i-1] not in operators :
                MyStr+=' '+x[i]+' '

            elif x[i] in operators and x[i+1] not in operators and x[i-1] in operators:
                MyStr+=x[i]+' '

            # If the character is a punctuation mark, it appends the punctuation mark with surrounding spaces
            elif x[i] in punctuations:
                MyStr+=' '+x[i] + ' ' 

            # Otherwise, it appends the character unchanged
            else:
                MyStr+=x[i]

        except:
                MyStr+=x[i]


#  Removing any empty strings or spaces from the end of a list:
    #EXAMPLE:
    # print ( 'x = 10' )       # My Code
    # print ( 'x=10' )         # Correct 

    LexemesList=[]
    for x in MyStr.split(" "):
        LexemesList.extend(x.split("\n"))


    i = len(LexemesList)-1
    while i > 0: 
        if LexemesList[i] == ' ' or LexemesList[i] == '':
            LexemesList.pop(i)
        i-=1

    return LexemesList                


def tokener(x):
    keywords=['False' ,'await','else' ,'import','pass','None','break','except','in','raise',
    'True','class','finally','is','return','and','continue','for','lambda','try','as','def',
    'from','while','assert','del','global','not','with','async','elif','if','or',
    'yield', 'print' ]

    tokens=[]

    for i in x:
        if i.isdigit():
            tokens.append('number')
        elif i == '':
            x.remove(i)  
        elif i in ['+','-','*','/','%','//','**','!=','==','>=','<=','<>','<','>','=']:
            tokens.append('Operator')
        elif i in [']', '}', ')','[', '{', '(']:
            tokens.append('Parenthes')
        elif i in keywords:
            tokens.append('Keyword')
        elif i == ';':
            tokens.append('semicolon') 
        elif i == '.':
            tokens.append('Dot')
        elif i in ["'" , '"', '~']:
            tokens.append('Punctuation')
        elif i == ',':
            tokens.append('comma')
        elif i == ':':
            tokens.append('Double Dot')
        elif (str(i).startswith("'") and str(i).endswith("'")) or (str(i).startswith('"') and str(i).endswith('"')):
            tokens.append('string')
        else:
            tokens.append('Identfier')

    return tokens

#=============( Symbol Table )=================

def symbol_table(tokens, lexemes):
    table = []
    cnt = 0 #Count the identifier
    pos = 0 #Memory Position
    i = 0
    while i < len(tokens):
         # Check if the current token is an identifier and the next token is an assignment operator
        if tokens[i] == "Identfier" and i + 1 < len(tokens) and lexemes[i + 1] == "=":
            table.append((cnt, lexemes[i], type(i).__name__ , pos)) # Id, Name, Type, Memory Pos
            pos += 2
            cnt += 1 
        i += 1 # Move to next token
    return table

def LexicalAnalyzer(x):      

    lexemesList=lexer(x)    
    tokenslist=tokener(lexemesList)
    symboltable=symbol_table(tokenslist, lexemesList)


    # Combines the list of lexemes and the list of tokens into a list of tuples
    LexemesTokensList= [x for x in ( zip(lexemesList,tokenslist) ) ]
    print ('lexeme',15*' ',':token')
    for i in LexemesTokensList:
        n=15-len(i[0])
        print(i[0], n*' ',':\t', i[1])

    return lexemesList, tokenslist, symboltable

lexemes,tokens, symboltable = LexicalAnalyzer(SourceCode)

print()
print("Symbol Table")
print("Id", "Name", "Type", "Memory Position", sep="\t") #sep="\t" To Print With Taps
for item in symboltable:
    print(*item, sep="\t")

# ===================================================================================
# Check For Errors
has_error = True
cnt = 0 # balance of parentheses
wait_for_colon = False #currently expecting a colon
errors_list = [] #list of errors

for lexeme in lexemes:
    # Check if the lexeme is a newline character & if we are currently expecting a colon
    if lexeme == "\n":
        if wait_for_colon:
            errors_list.append("Error Expected A Colon")
            continue
    lexeme = lexeme.strip("\n").strip()
    if lexeme == ":":
        if not wait_for_colon: 
            errors_list.append("Unexpected Colon")
        wait_for_colon = False
    elif lexeme in ["if", "elif", "else", "def", "class"]:
        wait_for_colon = True
    elif lexeme == "(":
        cnt += 1
    elif lexeme == ")":
        cnt -= 1

if cnt != 0:
    errors_list.append("Error, Parentheses Don't Match")


for er in errors_list:
    print("\nErrors: ")
    print(er)

if len(errors_list) == 0:
    print("\nNo Errors Found")
    has_error = False

# ===================================================================================
# SourceCode To Parse Tree
if len(errors_list) == 0 :
    
    def parse(x):
        tree = ast.parse(x) #Parses the string
        print("\nParse The Python Code Into An Abstract Syntax Tree (AST): \n")
        print(ast.dump(tree)) #Prints a textual representation of the AST
        parse(SourceCode)



    def GenerateParseTree(x):
        try:
            parse_tree = ast.parse(x)
            identifiers = []
            expressions = []
            for node in ast.walk(parse_tree): #Traverses the AST to visit each node
                if isinstance(node, ast.Name):  #Isinstance => bool (True,False)
                    identifiers.append(node.id)
                elif isinstance(node, ast.Expr):
                    expressions.append(node.value)
            return {"parse_tree": ast.dump(parse_tree), "identifiers": identifiers, "expressions": expressions}
        except SyntaxError as e:
            print("SyntaxError:", e)
            return None
        except Exception as e:
            print("Run Time Error:", e)
            return None


        print("\n\nGenerate Parse Tree With Dictionary (Identifiers - Expressions) : \n")

        tree = print(GenerateParseTree(SourceCode))

if len(errors_list) != 0:
    print("\nThere are errors in the code, so it cannot be parsed into an AST")

# =====================================
# By : Hossam Elbesh (Computer Science)
# =====================================