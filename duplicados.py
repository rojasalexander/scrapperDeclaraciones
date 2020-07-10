import os, fnmatch

def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(name))
    return result

archivo = open("lista_duplicados.txt", "a")

pdfs = find('*.pdf', r'C:\Users\alxro\Desktop\Trabajo CDS\pdfs')

read = open("lista_duplicados.txt", "r")
almacenados = read.readlines()
read.close()

for almacenado in almacenados:
    almacenado = almacenado[:-1]

    for pdf in pdfs:
        if("(" in pdf and pdf not in almacenado):
            archivo.write(pdf)
            archivo.write("\n")

archivo.close()