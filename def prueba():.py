filename = 'correcto.txt'

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
    text=text.replace('\n', ' ').lower()
    #solo quitamos saltos de línea y mayúsculas

    list= text.split(' ')
    #texto se vuelve lista delimitado por espacios en blanco, algunos quedan con comas o paréntesis pero eso se maneja después
    #para probar print(list)

    vars=[]
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
        #nos aseguramos que la tercera línea sea procs y pasamos a la función que analiza los procs
        elif state== 2 and list[0]=='procs':
            del list[0]
            #sorting_hat(list)
            state=4

        else:
            print('NO')


    return list

def sorting_hat(lst):

    procs = ['assignto', 'goto', 'move', 'turn', 'face', 'put', 'pick', 
    'movetothe', 'moveindir', 'jumptothe', 'jumpindir', 'nop']

    coditionals= ['facing', 'canput', 'canpick', 'canmoveindir', 'canjumpindir', 'canmovetothe', 'canjumptothe', 'not']

    list_commas= [',', '[','|', ']', ':', ';']

    value=0
    #condicional que mantiene valor bool 1 como True mientras los elementos de la lista se encuentre en alguno de
    #los diccionarios. Si no se encuentran, vemos si tiene pegado algún símbolo y se analizan por separado. Si tampoco se encuentra,
    # vemos si está seguido de un [, lo que indicaría que es el nombre de una variable. La idea es poner condiciones necesarias que, si no se cumples, cambia el valor value a 0 y lo devolvemos como False
    for i in lst:
        if i in list_commas:
            value= 1

        elif i in procs:
            value=1

        elif i in coditionals:
            value=1

#hacer variable sin la primera posición, sin la última y sin las dos para analizarlas.


print(tratemos())


    