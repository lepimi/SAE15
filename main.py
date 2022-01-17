file = open('data.txt', 'r') #ouvre le fichier 
Lines = file.readlines()

import csv
import markdown
from mdtable import MDTable
import os

def getAfter(text, word):  # recupere le mot apres un mot choisi.
	splited = text.split(word,1)
	if len(splited) > 0:
		return text.split(word,1)[1].strip().split(' ')[0].strip()
	else:
		return ''

def remove_empty_lines(filename): # enleve les lignes vides du fichier
    if not os.path.isfile(filename):
        print("{} does not exist ".format(filename))
        return
    with open(filename) as filehandle:
        lines = filehandle.readlines()

    with open(filename, 'w') as filehandle:
        lines = filter(lambda x: x.strip(), lines)
        filehandle.writelines(lines)

class request:  
	def __init__(self, hour, source, dest, flag, length, protocol):  #definition des variables
		self.hour = hour
		self.source = source
		self.dest = dest
		self.flag = flag
		self.length = length
		self.protocol = protocol
 
requests = []
lines = []
for line in Lines:
	if not line.startswith((' ', '\t')) and "Flags" in line:  #si la ligne ne commence pas par une tabulation ou si elle ne contient pas le mot flag, elle n'est pas compté
		requests.append(request(line.strip().split(' ')[0],  #heure
			getAfter(line, line.strip().split(' ')[1]),  # protocol
			getAfter(line, ">").replace(':', ''),  # adresse destination
			getAfter(line, "Flags").replace('[', '').replace('],', ''), # le flag et supprime les crochets et la virgule
			getAfter(line, "length").replace(':', ''), # la taille et supprime les deux points
			line.strip().split(' ')[1]))

with open('result.csv', 'w', encoding='UTF8') as f:  #creer le fichier result.csv avec les resultats dedans
	writer = csv.writer(f)
	writer.writerow(['Hour', 'Source', 'Destination', 'Flag', 'Length', 'Protocol'])
	for req in requests:
		writer.writerow([req.hour, req.source, req.dest, req.flag, req.length, req.protocol])

remove_empty_lines("result.csv")  #enleve les lignes vides du fichier csv

markdown_string_table = MDTable('result.csv').get_table()  # creer un tableau markdown a partir du fichier csv
f = open("result.md", "w")
f.write(markdown_string_table)
f.close()

with open("result.md",'r') as f: # creer une page html a partir du tableau markdown.
    text=f.read()
    html=markdown.markdown(text,extensions=['tables']).replace("<table>", '<table class="table table-striped">')
    with open('index.html','w') as f:
        f.write("""<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Oui</title>
            <style>
                .bonjour{
                    animation-name: rotate;
                    animation-duration: 3s;
                    animation-timing-function: linear;
                    animation-iteration-count: infinite;
					border-radius: 100%;
					box-shadow: rgb(85, 91, 255) 0px 0px 0px 3px, rgb(31, 193, 27) 0px 0px 0px 6px, rgb(255, 217, 19) 0px 0px 0px 9px, rgb(255, 156, 85) 0px 0px 0px 12px, rgb(255, 85, 85) 0px 0px 0px 15px;
                }
				.bonjour:hover{
					animation-play-state: paused;
				}
                @keyframes rotate {
                from {
                    transform: rotate(0deg);
                }

                to {
                    transform: rotate(359deg);
                }
            }
            </style>
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
        </head>
        <body>"""+html+"""<div style="width: 100%; display: flex; justify-content:center;align-items:center"><img onclick="window.scrollTo(0,0)" class="bonjour" src="https://i.ibb.co/BPL6372/16112777-131412247365155-290713036321863328-o.jpg"/></div></body>
        
		</html>""")