filename = 'correcto.txt'
#filename = 'incorrecto.txt'

status = 0 # Part of the program that is being parsed
# 0: expects robot_r keyword
# 1: expects vars keyword
# 2: expects procs keyword
# 3: instructions
# 10: excepts vars declaration
# 20: expects procedure name 
# 21: [
# 22: expects parameter
# 23: 
# COMPLETAR

exceptions = {0: 'Error: Se esperaba la palabra reservada ROBOT_R', 
              1: 'Error: Se esperaba la palabra reservada VARS',
              10: 'Error: Nunca se completó la declaración de variables',
              11: 'Error: Se esperaba el nombre de una variable pero se econtró un punto y coma',
              2: 'Error: Se esperaba la palabra reservada PROCS', }

status_tokens = {0:'robot_r', 1:'vars', 2:'procs'}
procs = ['assignto', 'goto', 'move', 'turn', 'face', 'put', 'pick', 
'movetothe', 'moveindir', 'jumptothe', 'jumpindir', 'nop']

def open_file(filename):
    try:
        with open(filename, 'r') as f:
            text = f.read()
        return text
    except FileNotFoundError:
        raise Exception(f'Error: El archivo {filename} no existe')

def parse(text, status):
    text = text.replace(' ', '').replace('\t', '').replace('\n', '').lower()
    pointer = 0 # Pointer to the current character
    current = str() # Command that is being parsed

    while pointer < len(text):
        current += text[pointer]

        if status == 0 and current==status_tokens[0]:
            current = str()
            status = 1 
        elif status == 1 and current==status_tokens[1]:
            current = str()
            status = 10
            user_vars = list()
        elif status == 10 and current[-1] == ',':
            user_vars.append(current[:-1])
            current = str()
            status = 10 # Does nothing, just to be explicit
        elif status == 10 and current[-1] == ';': 
            if ';' != current:
                user_vars.append(current[:-1])
            else:
                if len(user_vars) != 0:
                    raise(Exception(exceptions[10]))
            current = str()    
            status = 2
        elif status == 2 and current==status_tokens[2]:
            current+=pointer
        
        pointer += 1
    
    if status in exceptions:
        raise(Exception(exceptions[status]))
    

def main():
    text = open_file(filename)
    parse(text, status)
    print('El archivo fue parseado correctamente')




def prueba(text):
    open= 0
    closed=0
    count=0

    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

    txt=text
    positions= []
    intern= []

    for i in range(0,len(txt)):
        if txt[i]=='[' and txt[i-1]==':':
            pos_f= txt.find(']',i)
            positions.append(i)
            positions.append(pos_f)

    while len(positions)>0:
        zero= positions[0]
        one= positions[1]
        cuted= txt[zero+1:one]
        intern.append(cuted)
        positions= positions[2:]

    if len(intern)!=0:
        for i in intern:
            txt= txt.replace('['+i+']',"")
            
    return txt, intern



print(prueba("goWest[||if:canMoveInDir:1,westthen:[MoveInDir:1,west]else:nop:]"))