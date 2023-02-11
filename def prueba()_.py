filename = 'correcto.txt'
list_commas= [',', '[','|', ']', ':', ';']
numbers = ['0','1', '2', '3', '4', '5', '6', '7', '8', '9']
coordinates = ['right', 'left', 'front', 'back']
directions = ['north', 'south', 'east', 'west']
objects = ['baloons', 'chips']
vars=[]
procs = ['assignto', 'goto', 'move', 'turn', 'face', 'put', 'pick', 
    'movetothe', 'moveindir', 'jumptothe', 'jumpindir', 'nop']
coditionals= ['facing', 'canput', 'canpick', 'canmoveindir', 'canjumpindir', 'canmovetothe', 'canjumptothe', 'not']

def open_file(filename):
    try:
        with open(filename, 'r') as f:
            text = f.read()
        return text
    except FileNotFoundError:
        raise Exception(f'Error: El archivo {filename} no existe')

def tratemos():

    text= open_file(filename)
    text= text.strip() #quita espacios en blanco al inicio y al final
    text=text.replace('\n', ' ').lower().replace('\t', '')
    #solo quitamos saltos de línea y mayúsculas

    list= text.split(' ')
    #texto se vuelve lista delimitado por espacios en blanco, algunos quedan con comas o paréntesis pero eso se maneja después
    #para probar print(list)

    state= 0

    while state!=4:
        #nos aseguramos que lo primero sea robot_r y lo quitamos
        if state==0 and list[0]=='robot_r':
            state+=1
            del list[0]

        #nos aseguramos que lo segundo sea vars y todo lo que está entre vars y procs son variables que se guardan en vars y se quitan de la lista
        elif state==1 and list[0]=='vars':
            x=list.index('procs')
            while len(vars)!=x:
                v= list.pop(0)
                vars.append(v)
            state+=1

        elif state==1 and list[0]=='procs':
            state+=1
        #nos aseguramos que la tercera línea sea procs y pasamos a la función que analiza los procs
        elif state== 2 and list[0]=='procs':
            del list[0]
            new= format(list)
            structure_blocks, structure_procs, positions= filter(new)
            value= identifyprocs(structure_procs, vars)
            state=4

        else:
            print('NO')


    return   value

def format(list):


    new=[]

    for i in list:
        x=''
        for j in i:
            if j not in list_commas:
                x=x+j

            elif x!='' and j in list_commas:
                new.append(x)
                x=''
                new.append(j)
            elif j in list_commas:
                new.append(j)

        if x!='':
            new.append(x)

    return new
         


def filter(list): 

    structure_blocks=[]
    structure_procs=[]
    positions=[]
    noms=[]

    if list[0]!= '[':
        noms.append(list[0])
        del list[0]

    else: 
        structure_blocks.append(list)

    for i in range(0,len(list)):
        if list[i]!=']' and list[i]!='[' and list[i-1]==']' and list[i+1]=='[':
            noms.append(list[i])
            positions.append(i)

        elif list[i]=='[' and list[i-1]==']':
            positions.append(i)


    for i in range(0, len(positions)):
        if positions[i]!= positions[-1]:
            chnk= list[positions[i]:positions[i+1]]
            structure_procs.append(chnk)

        elif positions[i]==positions[-1]:
            chnk= list[positions[i]:]
            structure_blocks.append(chnk)

    return structure_blocks, structure_procs, positions

def identifyprocs(procslist, vars):
    # procslist es una lista de todos los procs de la función
    # vars es una lista que contiene todas las vars definidas al inicio del programa
    procs = ['assignto', 'goto', 'move', 'turn', 'face', 'put', 'pick',
    'movetothe', 'moveindir', 'jumptothe', 'jumpindir', 'nop']
    numbers = ['0','1', '2', '3', '4', '5', '6', '7', '8', '9']
    coordinates = ['right', 'left', 'front', 'back']
    directions = ['north', 'south', 'east', 'west']
    objects = ['baloons', 'chips']
    numbers_and_vars = numbers + vars
    controls = ['while', 'if', 'repeat']
    procs_controls = procs + controls
    conditions = ['facing', 'canput', 'canpick', 'canmoveindir', 'canjumpindir', 'canmovetothe', 'canjumptothe', 'not']

    procsnames = []
    #procsnames es una lista con los nombres de todos los procedures definitions
    counter = -1
    state = True
    
    #se toma como estado inicial true, es decir que el programa es correcto hasta que se prueba lo contrario
    while state is True or counter < len(procslist)-1:
        counter+=1
        proc = procslist[counter]
        # proc representa cada procedure definition
        procsnames.append(proc[0])
        del proc[0]
        #como cada definition empieza con su nombre, se agrega el nombre a la lista de procsnames y se elimina
        
        #si el primer elemento después del nombre no es [ y el último no es ], es incorrecto.
        if proc[0] != '[' or proc[-1] != ']':
            state = False
            
        #si las variables no están encerradas en |, es incorrecto.
        if proc.count('|') != 2:
            state = False
        pos = proc.index('|')
        del proc[0:pos+1]
        
        #se eliminan los valores hasta la primera | y se meten los nombres en la lista procsnames
        i = 0
        comma = 0
        names = 0
        while proc[i] != '|':
            if proc[i] == ',':
                comma+=1
            else:
                procsnames.append(proc[i])
                names+=1
            i+=1
         #Si hay comas adicionales, es incorrecto
        #Se elimina todo lo que sea parámetro
        del proc[0:i+1]
        if names != comma+1:
            state = False
        
        #Se verifica que lo siguiente que siga sea un command o un control structur
        #En caso de no serlo, false
        if proc[0] not in procs_controls or proc[1] != ':':
            state = False
        
        #Si está presente, se verifica que el estado sea true 
        if proc[0] in procs:
            state = True
            while len(proc) != 0:
                if proc[0] in procs and proc[1] == ':':
                    name = proc[0]
                    if name == 'assignto':
                        if proc[2] not in numbers or proc[3] != ',' or proc[4] not in vars:
                            state = False
                            del proc[0:5]
                        else:
                            del proc[0:5]
                    elif name == 'goto':
                        if proc[2] not in numbers_and_vars or proc[3] != ',' or proc[4] not in numbers_and_vars:
                            state = False
                            del proc[0:5]
                        else:
                            del proc[0:5]
                    elif name == 'move':
                        if proc[2] not in numbers_and_vars:
                            state = False
                            del proc[0:3]
                        else:
                            del proc[0:3]
                    elif name == 'turn':
                        if proc[2] not in coordinates:
                            state = False
                            del proc[0:3]
                        else:
                            del proc[0:3]
                    elif name == 'face': 
                        if proc[2] not in directions:
                            state = False
                            del proc[0:3]
                        else:
                            del proc[0:3]
                    elif name == 'put':
                        if proc[2] not in numbers_and_vars or proc[3] != ',' or proc[4] not in objects:
                            state = False
                            del proc[0:5]
                        else:
                            del proc[0:5]
                    elif name == 'pick':
                        if proc[2] not in numbers_and_vars or proc[3] != ',' or proc[4] not in objects:
                            state = False
                            del proc[0:5]
                        else:
                            del proc[0:5]
                    elif name == 'movetothe':
                        if proc[2] not in numbers_and_vars or proc[3] != ',' or proc[4] not in coordinates:
                            state = False
                            del proc[0:5]
                        else:
                            del proc[0:5]
                    elif name == 'moveindir':
                        if proc[2] not in numbers_and_vars or proc[3] != ',' or proc[4] not in directions:
                            state = False
                            del proc[0:5]
                        else:
                            del proc[0:5]
                    elif name == 'jumptothe':
                        if proc[2] not in numbers_and_vars or proc[3] != ',' or proc[4] not in coordinates:
                            state = False
                            del proc[0:5]
                        else:
                            del proc[0:5]
                    elif name == 'jumpindir':
                        if proc[2] not in numbers_and_vars or proc[3] != ',' or proc[4] not in directions:
                            state = False
                            del proc[0:5]
                        else:
                            del proc[0:5]

                    if proc[0] != ';' or proc[0] != ']' and len(proc) != 0:
                        state = False
               
                        del proc[0]
                        if len(proc) == 0:
                            break

                    if proc[0] == ';' or proc[0] == ']':
                        state = True
                        if len(proc) == 0:
                            break
                        del proc[0]
                    

        elif proc[0] in controls:
            # SI PROC[0] ES REPEAT
            if proc[0] == 'repeat' and proc[1] == ':':
                if proc[2] not in numbers_and_vars:
                    state = False
                elif proc[2] in numbers_and_vars:
                    del proc[0:3]
                    if isblock(proc, procsnames, vars) == False:
                        state = False

            if proc[0] == 'if' or proc[0] == 'while' and proc[1] == ':':
                if proc[2] not in conditions:
                    state = False
                    del proc[0:3]
                elif proc[2] in conditions:
                    del proc[0:3]
                    condition = proc[0]
                    if proc[1] != ':':
                        state = False
                    if condition == 'facing':
                        if proc[2] not in directions:
                            state = False
                            del proc[0:3]
                        else:
                            del proc[0:3]
                    elif condition == 'canput' or condition == 'canpick':
                        if proc[2] not in numbers_and_vars or proc[3] != ',' or proc[4] not in objects:
                            state = False
                            del proc[0:5]
                        else:
                            del proc[0:5]
                    elif condition == 'canmoveindir' or condition == 'canjumpindir':
                        if proc[2] not in numbers_and_vars or proc[3] != ',' or proc[4] not in directions:
                            state = False
                            del proc[0:5]
                        else:
                            del proc[0:5]
                    elif condition == 'canmovetothe' or condition == 'canjumptothe':
                        if proc[2] not in numbers_and_vars or proc[3] != ',' or proc[4] not in coordinates:
                            state = False
                            del proc[0:5]
                        else:
                            del proc[0:5]
                    elif condition == 'not':
                        if proc[2] not in conditions:
                            state = False
                            del proc[0:3]
                        else:
                            del proc[0:3]

       #SE COMPROBÓ QUE DESPUÉS DEL CONDICIONAL O EL CICLO ESTÉ LA CONDICIÓN CORRECTAMENTE
        #SE ELIMINÓ LA CONDICIÓN HASTA EL DO O EL THEN             
                    if proc[0] != 'do' or proc[0] != 'then' or proc[1] != ':':
                        state = False
                    elif proc[0] == 'do':
                        begins = proc.index['[']
                        ends = proc.index[']']
                        if isblock(proc[begins, ends+1], procsnames, vars) == False:
                            state = False

                        elif isblock(proc[begins, ends+1], procsnames, vars) == True:
                            del proc[0:ends+1]
                        if proc[0] != 'od' or proc[1] != ']':
                            state = False
                            del proc[0]

                    elif proc[0] == 'then':
                        if '[' in proc and ']' in proc:
                            begins = proc.index['[']
                            ends = proc.index[']']
                        if '[' not in proc or ']' not in proc:
                            state = False
                        if isblock(proc[begins, ends+1], procsnames, vars) == False:
                            state = False

                        elif isblock(proc[begins, ends+1], procsnames, vars) == True:
                            del proc[0:ends+1]

                        if proc[0] != 'else' or proc[1] != ':':
                            state = False
                        elif proc[0] == 'else' and proc[1] == ':':
                            if '[' in proc and ']' in proc:
                                begins = proc.index['[']
                                ends = proc.index[']']
                            if '[' not in proc or ']' not in proc:
                                state = False
                        if isblock(proc[begins, ends+1], procsnames, vars) == False:
                            state = False

                        elif isblock(proc[begins, ends+1], procsnames, vars) == True:
                            del proc[0:ends+1]
                        if proc[0] != ']':
                            state = False
                            del proc[0]
                        if proc[0] == ']':
                            del proc[0]
        else:
            del proc[0]

    return state

def isblock(lst, procsnames, vars):
    #procsnames son los nombres de las funciones que se definen al inicio
    procs = ['assignto', 'goto', 'move', 'turn', 'face', 'put', 'pick',
    'movetothe', 'moveindir', 'jumptothe', 'jumpindir', 'nop']
    instructions = procsnames + procs
    numbers = ['0','1', '2', '3', '4', '5', '6', '7', '8', '9']
    coordinates = ['right', 'left', 'front', 'back']
    directions = ['north', 'south', 'east', 'west']
    objects = ['baloons', 'chips']
    numbers_and_vars = numbers + vars
    controls = ['while', 'if', 'repeat']
    procs_controls = procs + controls
    conditions = ['facing', 'canput', 'canpick', 'canmoveindir', 'canjumpindir', 'canmovetothe', 'canjumptothe', 'not']
    state = True

    counter = -1
    while state is True and counter < len(lst):
        counter+=1
        if lst[0] != '[' or lst[-1] != ']':
            state = False

        if lst[0] == '[':
            del lst[0]
            if lst[0] not in instructions:
                state = False
            elif lst[0] in instructions and lst[1] == ':':
                if lst[0] == 'assignto':
                    if lst[2] not in numbers or lst[3] != ',' or lst[4] not in vars:
                        state = False
                        del lst[0:5]
                    else:
                        del lst[0:5]
                elif lst[0] == 'goto':
                    if lst[2] not in numbers_and_vars or lst[3] != ',' or lst[4] not in numbers_and_vars:
                        state = False
                        del lst[0:5]
                    else:
                        del lst[0:5]
                elif lst[0] == 'move':
                    if lst[2] not in numbers_and_vars:
                        state = False
                        del lst[0:3]
                    else:
                        del lst[0:3]
                elif lst[0] == 'turn':
                    if lst[2] not in coordinates:
                        state = False
                        del lst[0:3]
                    else:
                        del lst[0:3]
                elif lst[0] == 'face': 
                    if lst[2] not in directions:
                        state = False
                        del lst[0:3]
                    else:
                        del lst[0:3]
                elif lst[0] == 'put':
                    if lst[2] not in numbers_and_vars or lst[3] != ',' or lst[4] not in objects:
                        state = False
                        del lst[0:5]
                    else:
                        del lst[0:5]
                elif lst[0] == 'pick':
                    if lst[2] not in numbers_and_vars or lst[3] != ',' or lst[4] not in objects:
                        state = False
                        del lst[0:5]
                    else:
                        del lst[0:5]
                elif lst[0] == 'movetothe':
                    if lst[2] not in numbers_and_vars or lst[3] != ',' or lst[4] not in coordinates:
                        state = False
                        del lst[0:5]
                    else:
                        del lst[0:5]
                elif lst[0] == 'moveindir':
                    if lst[2] not in numbers_and_vars or lst[3] != ',' or lst[4] not in directions:
                        state = False
                        del lst[0:5]
                    else:
                        del lst[0:5]
                elif lst[0] == 'jumptothe':
                    if lst[2] not in numbers_and_vars or lst[3] != ',' or lst[4] not in coordinates:
                        state = False
                        del lst[0:5]
                    else:
                        del lst[0:5]
                elif lst[0] == 'jumpindir':
                    if lst[2] not in numbers_and_vars or lst[3] != ',' or lst[4] not in directions:
                        state = False
                        del lst[0:5]
                    else:
                        del lst[0:5]
                else:
                    del lst[0]

        # FALTAN LAS FUNCIONES AGREGADAS MANUALMENTE CON SUS PARÁMETROS
        else:
            del lst[0]
        return state
                        

            

print(tratemos())




