from selenium.webdriver import Chrome, ChromeOptions 
from time import sleep
import os, fnmatch

opts = ChromeOptions()
opts.binary_location = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

prefs = {'download.default_directory' : r'C:\Users\alxro\Desktop\Trabajo CDS\pdfs'}
opts.add_experimental_option('prefs', prefs)

driver = Chrome(options=opts)

def get_file_data(file_name): #saca ci, nombre, año y version del link y nombre del archivo
    
    cleaned = file_name \
                .replace('PERDOMO2016_1', 'PERDOMO_2016_1') \
                .replace('SOSARIELLA_216', 'SOSARIELLA_2016') \
                .replace('221.035', '221035') \
                .replace('991712_8', '991712#8') \
                .replace("_.pdf", "") \
                .replace("_pdf", "") \
                .replace(".pdf", "") \
                .strip() \
                .replace("\n", "") \
                .replace("-", "_") \
                .replace(" ", "_") \
                .replace(".", "_")

    parts = cleaned.split("_")
    document = parts[0]

    name = ''
    last = 'name'
    year = ''
    version = ''
    for part in parts[1:]:
        if last == 'name':
            if part.isdigit():
                last = 'year'
                year = part
            else:
                name += ' ' + part
        if last == 'year' and len(part) == 1:
            version = part

    if year == '216':
        year = '2016'

    return {
            'file_name': file_name.replace("\n", ""),
            'document': document,
            'name': name.strip(),
            'year': year,
            'version': version
           }

def find(pattern, path): #busca todos los pdfs del directorio
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(name))
    return result
  
def get_pdfs(my_url): #guarda todos los links de la pagina contraloria en una lista
    links = []
    driver.get(my_url)

    el = driver.find_element_by_id("limit")
    for option in el.find_elements_by_tag_name('option'):
        if option.text == 'Todo':
            option.click() # select() in earlier versions of webdriver
            break

    a = driver.find_elements_by_tag_name('a')
    buttons = driver.find_elements_by_css_selector(".pd-button-download [href]")

    for link in buttons:
        current_link = link.get_attribute('href')
        print(current_link)
        links.append(current_link)

    return links

def check(links): #verificar si es que el archivo ya existe
    c = 0
    for link in links:
        c += 1
        b = 0
        guion = link.find('-') + 1
        plbrlink = link[guion:]
        plbrlink = plbrlink.replace('-', '_')
        plbrlink = get_file_data(plbrlink)
        nombres = find('*.pdf', r'C:\Users\alxro\Desktop\Trabajo CDS\pdfs') #Agarra todos los pdfs del directorio
        for nombre in nombres:
            nombre = get_file_data(nombre)
            if(nombre["document"] == plbrlink["document"] and nombre["year"] == plbrlink["year"] and nombre["version"] == plbrlink["version"]):
                print("El archivo ya existe: ", c)
                b = 1
        if(b != 1):
            descargar(link)

def descargar(link): #descargar el pdf
    try:
        print("Descargando: "+ link)
        driver.get(link)
        driver.implicitly_wait(0)
        button = driver.find_element_by_id('pdlicensesubmit')
        button.click()
        sleep(2)
    except:
        print ("Error")

def main():
    my_url = "https://djbpublico.contraloria.gov.py/index.php"
    links = get_pdfs(my_url)
    check(links)

main()