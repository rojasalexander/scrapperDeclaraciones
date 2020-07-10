import PyPDF4
import re
import io
import os, fnmatch
import fitz
from PIL import Image 
import pytesseract 
from pdf2image import convert_from_path 

def find(pattern, path):

    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(name))
    return result

def hacerOCR(path):
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    # Path of the pdf 
    PDF_file = path
    pages = convert_from_path(PDF_file, 500)
    image_counter = 1
    for page in pages: 
        filename = "page_"+str(image_counter)+".jpg"
        page.save(filename, 'JPEG')
        image_counter = image_counter + 1
    filelimit = image_counter - 1
    outfile = "textoPDF.txt"
    f = open(outfile, "a")
    for i in range(1, filelimit + 1):
        filename = "page_"+str(i)+".jpg"
        text = str(((pytesseract.image_to_string(Image.open(filename))))) 
        text = text.replace('-\n', '')     
        f.write(text) 
    f.close() 

def verificar_existentes(path):
    b = 0
    read = open("datosFuncionarios.txt", "r")#VERIFICAR
    lines= read.readlines()
    for line in lines:
        line = line[:-1]
        if(os.path.basename(path) in line):
            print("EL PDF YA FUE SCRAPEADO")
            b = 1
    read.close()#VERIFICAR
    return b
        
def sacar_datos_fitz(path, text):
    ta, tp, pn = '', '', ''
    doc = fitz.open(path)#sacar datos fitz
    for page in doc:
        text+=(page.getText())
    
    txt = open('pdfactual.txt', 'w')
    try: 
        txt.write(text)
        txt.close()
        c = 0
        txt = open('pdfactual.txt', 'r+')
        lines = txt.readlines()
        txt.truncate(0)
        txt.close()
        for line in lines:
            line = line.replace(' ', '')
            line = line.strip()

            if(line == "TOTALACTIVO"):  #scrapear el pdf que son searchable
                ta = lines[c+3]
                ta = ta[:-1]
            elif(line == "TOTALPASIVO"):
                tp = lines[c+2]
                tp = tp[:-1]
            elif(line == "PATRIMONIONETO"):
                pn = lines[c - 1]
                pn = pn[:-1]
                break
            c += 1
    except:
        print("error")  #sacar datos fitz 
    return text, ta, tp, pn 

def sacar_datos_ocr(text, path):
    textoPDF = open("textoPDF.txt", 'r+')#SACAR DATOS
    lines = textoPDF.readlines()
    textoPDF.truncate(0)
    textoPDF.close()
    b=0
    ta, tp, pn = '', '', ''
    datos = []
    for line in lines:
        if("TOTAL ACTIVO" in line):
            b = 1

        if(b == 1 and not"TOTAL ACTIVO" in line ):
            if(any(i.isdigit() for i in line[:10])):
                datos = line[:-1].split(" ")
                c = 0
                while(c < len(datos)):
                    aux = datos[c].replace(".", "")
                    if(not aux.isdigit()):
                        datos.remove(datos[c])
                        c -= 1 
                    c += 1
                print("datos despues: ", datos, "\narchivo: ", os.path.basename(path))
                if(len(datos) == 3):
                    ta, tp, pn = datos[0], datos[1], datos[2]
                b = 0
            
            elif(re.search('[a-zA-Z]', line)):#SACAR DATOS
                b = 0
    return ta,tp,pn

def guardar(b, path):
    if not(re.search('[a-zA-Z]', ta)) and b == 0:    
        archivo.write(ta + "," + tp + "," + pn + "," + os.path.basename(path) + "\n")

archivo = open("datosFuncionarios.txt", "a")
nombres = find('*.pdf', r'C:\Users\alxro\Desktop\Trabajo CDS\pdfs\searchable') 
ta, tp, pn = '', '', ''

#MAIN
def main():
    for nombre in nombres:
        path = (r'C:\Users\alxro\Desktop\Trabajo CDS\pdfs\searchable' + f"\{nombre}")
        text=""
        b = verificar_existentes(path)
        
        if(b == 0 and not"(" in os.path.basename(path)):
            text, ta, tp, pn = sacar_datos_fitz(path, text)
    
            if(text == ""): #scrapear pdf que no sean searchable
                s = 0
                hacerOCR(path)
                ta, tp, pn = sacar_datos_ocr(text, path)

                if ((re.search('[a-zA-Z]', ta)) or (re.search('[a-zA-Z]', tp)) or (re.search('[a-zA-Z]', pn)) or ta == '' or tp == ''or pn == ''):#PARA GUARDAR
                    print('Error, no se encontraron total activo, total pasivo, y patrimonio neto')
                    archivo.write("No se scrapeo exitosamente: "+ os.path.basename(path) + "\n")
                else:
                    guardar(b, path)
                    print("TOTAL ACTIVO: ",ta, "TOTAL PASIVO: ",tp, "PATRIMONIO NETO: ",pn, "PATH: ", os.path.basename(path), " exitosamente OCR")
            
            else:
                if ((re.search('[a-zA-Z]', ta)) or (re.search('[a-zA-Z]', tp)) or (re.search('[a-zA-Z]', pn)) or ta == '' or tp == ''or pn == ''):
                    print('Error, no se encontraron total activo, total pasivo, y patrimonio neto')
                    archivo.write("No se scrapeo exitosamente: "+ os.path.basename(path) + "\n")    
                else:   
                    guardar(b, path)
                    print("TOTAL ACTIVO: ",ta, "TOTAL PASIVO: ",tp, "PATRIMONIO NETO: ",pn, "PATH: ", os.path.basename(path))#PARA GUARDAR

main()
archivo.close()