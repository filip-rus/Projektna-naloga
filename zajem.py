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
    r'\s+<td  align="left" valign="top"><font face="Arial" size="2">\s*'
    r'(?P<model>.*)' #zajamemo model letala
    r'<br>'
    r'(?P<registracija>.*)' #zajamemo registracijo letala
    r'</td>'
    r'\s+'
    r'<td  width="1"align="right" valign="top"><font face="Arial" size="2">'
    r'(?P<stevilo_mrtvih>.*)' #zajamemo stevilo mrtvih glede na stevilo potnikov
    r'</td>' 
)

vzorec_datum = (
    r'<td  width="85" align="left" valign="top"><font face="Arial" size="2"><A HREF=".*.htm">'
    r'(?P<datum>.*)' #zajamemo samo datum nesreče
    r'</a></td>'
)
vzorec_kraj = (
    r'<td  align="left"valign="top"><font face="Arial" size="2">(.|\n)*?'
    r'(?P<kraj>.*)' #zajamemo samo kraj nesreče
    r'<br>'
    )

vzorec_družba = (
    r'<td  align="left"valign="top"><font face="Arial" size="2">(.|\n)*?' 
    r'<br>'
    r'(?P<družba>.*)' #zajamemo samo letalsko druzbo/operatorja letala 
    r'\s+</td>'
)
vzorec_družba = (
    r'<td  width="1"align="right" valign="top"><font face="Arial" size="2">'
    r'(?P<stevilo_mrtvih>.*)/(?P<potniki>.*)' #zajamemo stevilo mrtvih glede na stevilo potnikov z umrlimi na tleh
    r'</td>'
)
vzorec_brez_tal = (
    r'<td  width="1"align="right" valign="top"><font face="Arial" size="2">'
    r'(?P<stevilo_mrtvih>.*)/(?P<potniki>.*)\(' #zajamemo stevilo mrtvih glede na stevilo potnikov brez umrlih na tleh
)

vzorec_mesec = (
    r'<td  width="85" align="left" valign="top"><font face="Arial" size="2"><A HREF=".*.htm">'
    r'\d\d (?P<mesec>.*) ' #zajamemo samo mesec
    )
vzorec_leto = (
    r'<td  width="85" align="left" valign="top"><font face="Arial" size="2"><A HREF=".*.htm">'
    r'\d\d ... (?P<leto>....)<' #zajamemo samo leto
    )
    
nesreče = []
for leto in range(1920, 2019):
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

zapisi_csv(nesreče, ["datum", "kraj", "družbe", "model", "registracija", "žrtve/potniki"], "vsi.csv")


števec = 1920
while števec < 2019:
    print("04 Apr", števec)  #izpis vseh 4. Aprilov od leta 1920
    števec += 1

seznam = []
with open("kraj.json", "r", encoding="utf-8") as j:
    vsebina = json.load(j)
    for slovar in vsebina:
        for place in slovar.values():
            while place.count(",") != 0: #znebimo se specifičnih regij nesreče, tako da nam ostane le država
                place = place[1:]
            seznam.append(place)

with open("datoteka.txt", "w", encoding="utf-8") as d:
    for država in seznam:                      #ustvarimo datoteko z državami
        d.write("%s\n" % država)
    
