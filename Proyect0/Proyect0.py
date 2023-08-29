import re

def wordTokinezer():

    txt = 'Ejemplo.txt'
    with open(txt, 'r') as file:
        instructions = file.read()


    pattern = r'\w+|[.,!?;(){}\[\]]'

    tokens = re.findall(pattern, instructions)

    print(tokens)

#putCB está pegado, necesito que el tokinezer lo analice separado 

wordTokinezer()