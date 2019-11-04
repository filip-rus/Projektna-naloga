import json
import requests
import re
import csv
import json
import os
import sys

vzorec = (
    r'<td  width="85" align="left" valign="top"><font face="Arial" size="2"><A HREF=".*.htm">'
    r'(?P<datum>.*)' #zajamemo datum nesreče
    r'</a></td>'
    r'\s+'
    r'<td  align="left"valign="top"><font face="Arial" size="2">'
    r'(?P<kraj>.*)' #zajamemo kraj nesreče
    r'<br>'
    r'(?P<operator>.*)' #zajamemo letalsko druzbo/operatorja letala 
    r'\s+</td>'
    r'\s+<td  align="left" valign="top"><font face="Arial" size="2">'
    r'(?P<model>.*)' #zajamemo model letala
    r'<br>'
    r'(?P<registracija>.*)' #zajamemo registracijo letala
    r'</td>'
    r'\s+'
    r'<td  width="1"align="right" valign="top"><font face="Arial" size="2">'
    r'(?P<stevilo_mrtvih>.*)' #zajamemo stevilo mrtvih glede na stevilo potnikov
    r'</td>' 
)

nesreče = []
for leto in range(1920, 1921):
    url = "http://www.planecrashinfo.com/{število}/{število}.htm".format(število=leto)
    r = requests.get(url)
    vsebina = r.text
    for zadetek in re.finditer(vzorec, vsebina):
        nesreče.append(zadetek.groupdict())

with open("nesrece.json", "w") as j:
    json.dump(nesreče, j)

def pripravi_imenik(ime_datoteke):
    '''Če še ne obstaja, pripravi prazen imenik za dano datoteko.'''
    imenik = os.path.dirname(ime_datoteke)
    if imenik:
        os.makedirs(imenik, exist_ok=True)

def zapisi_csv(slovarji, imena_polj, ime_datoteke):
    '''Iz seznama slovarjev ustvari CSV datoteko z glavo.'''
    pripravi_imenik(ime_datoteke)
    with open(ime_datoteke, 'w', encoding='utf-8') as csv_datoteka:
        writer = csv.DictWriter(csv_datoteka, fieldnames=imena_polj)
        writer.writeheader()
        for slovar in slovarji:
            writer.writerow(slovar)

zapisi_csv(nesreče, ["datum", "kraj", "operator", "model", "registracija", "stevilo_mrtvih"], "csv_datoteka.csv")