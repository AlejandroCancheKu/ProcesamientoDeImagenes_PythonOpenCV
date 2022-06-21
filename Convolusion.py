import PySimpleGUI as sg
import cv2
import numpy as np

sg.theme('Topanga')      # Add some color to the window

# Very basic window.  Return values using auto numbered keys
bandera=False
datoLleno=False
def lecturaMatriz(values):
    filtro=[] 
    global datoLleno
    

    for i in range(3): 
            filtro.append([]) 
            for j in range(3): 
                if(values[i*3+j]!=''):
                    filtro[i].append(int(values[i*3+j]))
                    datoLleno=True
                else:
                    datoLleno=False
                    break
            if(datoLleno==False):
                break
    return filtro

def mostrarResultados():
    #MOSTRANDO LOS RESULTADOS 
    imgOriginal=cv2.imread(direccion) 
    imgNuevo=cv2.imread('ResultadoFiltro.jpg') 
    cv2.namedWindow("ORIGINAL",cv2.WINDOW_NORMAL) 
    cv2.namedWindow("FILTRO", cv2.WINDOW_NORMAL)
    cv2.imshow("ORIGINAL",imgOriginal) 
    cv2.imshow("FILTRO",imgNuevo)
    cv2.waitKey()

def convolusion(filtro,direccion):
    
    texto=''
    #FILTRO INTRODUCIDO
    print("\nFiltro introducido:")
    print()
    for fila in filtro:
        print("[", end=" ")
        texto=texto+"[ ";
        for elemento in fila:
            print("{}".format(elemento), end=" ")
            texto=texto+str(elemento)+" "
        texto=texto+"]\n"
        print("]")
    print()

    window['-MATRIZ-'].update(texto)

    img=cv2.imread(direccion) 
    kernel=np.array (filtro) 

    #aplicacion del filtro utilizando el kernel solicitado al usuario 
    dst = cv2.filter2D(img,-1,kernel)

    cv2.imwrite('ResultadoFiltro.jpg',dst)
    direccionNuevo = direccion.split(sep='/')
    print(direccionNuevo)
    direccionNuevo.pop()
    print(direccionNuevo)
    direccionResultado= '/'.join(direccionNuevo)
    direccionResultado=direccionResultado+'/ResultadoFiltro.jpg'
    print(direccionResultado)
    window['-ORIGINAL-'].update('Original: '+direccion)
    window['-NUEVO-'].update('Resultados: '+direccionResultado)
    global bandera
    bandera=True
    sg.popup_ok('Filtro Aplicado Correctamente',title=('Alerta'),font=("helvetica",14)) 
    
#Funciones de filtros basicos -------------
def deteccionBordes(direccion):
    filtro=[[0,1,0],
            [1,-4,1],
            [0,1,0]]    
    convolusion(filtro,direccion)

def sobel(direccion):
    filtro=[[-1,0,1],
            [-2,0,2],
            [-1,0,1]]    
    convolusion(filtro,direccion)

def desenfoque(direccion):
    filtro=[[1,1,1],
            [1,1,1],
            [1,1,1]]    
    convolusion(filtro,direccion)

def enfoque(direccion):
    filtro=[[0,-1,0],
            [-1,5,-1],
            [0,-1,0]]    
    convolusion(filtro,direccion)

def realzarBorde(direccion):
    filtro=[[0,0,0],
            [-1,1,0],
            [0,0,0]]    
    convolusion(filtro,direccion)

def repujado(direccion):
    filtro=[[-2,-1,0],
            [-1,1,1],
            [0,1,2]]    
    convolusion(filtro,direccion)

#Diseño de ventana -------------

#Columna izquierda de la ventana
left_col = [

    [sg.Text('Datos De Procesamiento',size=(30, 1),justification='center',font=("Helvetica", 14))],
    [sg.Text('Nombre Del Archivo',font=("Helvetica", 12))],
    [sg.Input(key='-ARCHIVO-', enable_events=True), sg.FileBrowse("Buscar")],
    [sg.Text('')],

    [sg.Text('Filtros Basicos',font=("Helvetica", 12))],
    [sg.Button('Deteccion De Bordes'),sg.Button('Sobel'),sg.Button('Desenfoque')],
    [sg.Button('Enfoque'),sg.Button('Realce De Bordes'),sg.Button('Repujado')],

    [sg.Text('')],
    [sg.Text('MATRIZ DE CONVOLUSION',size=(30, 1),justification='center',font=("Helvetica", 14))],
    [sg.InputText(size=(15, 1)) for col in range(3)],
    [sg.InputText(size=(15, 1)) for col in range(3)],
    [sg.InputText(size=(15, 1)) for col in range(3)],
    [sg.Text(' ')],
    [sg.Button("Procesar"), sg.Button('Salir')]
]

# Columna derecha de la ventana
right_col = [
    [sg.Text('INFORMACION DE PROCESAMIENTO',size=(44, 1),justification='center',font=("Helvetica", 14))],
    [sg.Text('Matriz De Convolusion:',size=(25,1),justification='center',font=("Helvetica", 12))],
    [sg.Text('Ninguna',size=(10, 3),key='-MATRIZ-',justification='center',font=("Helvetica", 32))],
    [sg.Text('')],
    [sg.Text('Direccion De Las Imagenes',size=(26, 1),justification='center',font=("Helvetica", 14))],
    [sg.Text('Original: ',size=(50, 2),key='-ORIGINAL-',justification='left',font=("Helvetica", 11))],
    [sg.Text('Resultados: ',size=(50, 2),key='-NUEVO-',justification='left',font=("Helvetica", 11))],
    [sg.Button('Mostar Resultados')]
]

layout = [
    [sg.Text('Programa De Aplicacion De Filtros',size=(57, 1),justification='center', font=("Helvetica", 21), relief=sg.RELIEF_RIDGE)],
    [sg.Text('')],
    [sg.Column(left_col, element_justification='c'), sg.VSeperator(),sg.Column(right_col, element_justification='c')],
    
]

#Ejecucion de la ventana -------------
window = sg.Window('Convolusion De Imagenes', layout)

direccion=''
while True:       
    event, values = window.read()       
    if event == sg.WIN_CLOSED or event== 'Salir':
        break
    
    if event == '-ARCHIVO-':
        direccion = values['-ARCHIVO-']
    
    if event =='Deteccion De Bordes':
        if(direccion!=''):
            deteccionBordes(direccion)
        else:
            sg.popup_ok('No se ha especificado ninguna direccion',title=('Alerta'),font=("helvetica",14))

    if event =='Sobel':
        if(direccion!=''):
            sobel(direccion)
        else:
            sg.popup_ok('No se ha especificado ninguna direccion',title=('Alerta'),font=("helvetica",14))
    
    if event =='Desenfoque':
        if(direccion!=''):
            desenfoque(direccion)
        else:
            sg.popup_ok('No se ha especificado ninguna direccion',title=('Alerta'),font=("helvetica",14))
    
    if event == 'Enfoque':
        if(direccion!=''):
            enfoque(direccion)
        else:
            sg.popup_ok('No se ha especificado ninguna direccion',title=('Alerta'),font=("helvetica",14))
    
    if event =='Realce De Bordes':
        if(direccion!=''):
            realzarBorde(direccion)
        else:
            sg.popup_ok('No se ha especificado ninguna direccion',title=('Alerta'),font=("helvetica",14))

    if event =='Repujado':
        if(direccion!=''):
            repujado(direccion)
        else:
            sg.popup_ok('No se ha especificado ninguna direccion',title=('Alerta'),font=("helvetica",14))

    if event == 'Procesar':
        if(direccion!=''):
            filtro=lecturaMatriz(values)
            if(datoLleno):
                convolusion(filtro,direccion)
            else:
                sg.popup_ok('Verifique que la matriz este llenada',title=('Alerta'),font=("helvetica",14))
        else:
            sg.popup_ok('No se ha especificado ninguna direccion',title=('Alerta'),font=("helvetica",14))
    
    if(event=='Mostar Resultados'):
        if(bandera):
            mostrarResultados()
        else:
            sg.popup_ok('No se ha aplicado filtro',title=('Alerta'),font=("helvetica",14)) 

    

window.close()




