import os, fnmatch
import shutil

path_pdfs = r'C:\Users\alxro\Desktop\Trabajo CDS\pdfs'
path_searchable =  r"C:\Users\alxro\Desktop\Trabajo CDS\pdfs\searchable" #Requisito: crear ambas carpetas
path_non_searchable = r"C:\Users\alxro\Desktop\Trabajo CDS\pdfs\non_searchable" 

def find(pattern, path): #buscar los pdfs en el directorio
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(name))
    return result

def check(): #verificar si el pdf es searchable o no
    nombres = find('*.pdf', path_pdfs)
    for nombre in nombres:
        b=0
        aux = nombre
        aux = path_pdfs + f"\{aux}"
        nombre = nombre.replace('_', '')
        nombre = nombre.replace('-', '')
        for x in range(2014, 2021):
            if str(x) in nombre:
                b = 1
                
        if(b == 1):
            mover_searchable(aux)
        else:
            mover_non_searchable(aux)

def mover_searchable(aux): #mover el pdf a la carpeta searchable
    try:
        shutil.move(aux, path_searchable)
    except:
        print("Ya existe")

def mover_non_searchable(aux): #mover el pdf a la carpeta non_searchable
    try:
        shutil.move(aux, path_non_searchable)
    except:
        print("Ya existe")

check()