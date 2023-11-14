import os
import glob
import argparse
import json

parser=argparse.ArgumentParser()
parser.add_argument("-d","--dirBlast",help="chemin vers les fichiers output blast",type=str,required=True)
parser.add_argument("-e","--evalue",help="evalue max",type=float,required=False)
parser.add_argument("-cov","--coverage",help="coverage min",type=float,required=False)
parser.add_argument("-id","--identity",help="identity min",type=float,required=False)
parser.add_argument("-j","--json",help="name json output",type=str,required=True)

args=parser.parse_args()



genomhit_all={}

# on parcours tous les outputs de blast
files=sorted(glob.glob(args.dirBlast+"/*"))

queryGenom=""
genomhit={}

for blast in files:

    # recupérer les noms des genomes query et subject
    filename=os.path.basename(blast)
    listGenom=filename.strip(".bl").split("-vs-")
    newqueryGenom=listGenom[0]
    subjectGenom=listGenom[1]

    # ajout de la clé du genome query
    if newqueryGenom != queryGenom  and queryGenom != "": 
        genomhit_all[queryGenom]=genomhit # ajoute le dico de genom d'avant
        genomhit={} # le temporaire
    elif queryGenom == "" :
        genomhit_all[newqueryGenom]={} # le grand dico
        genomhit={} # le temporaire
    

    queryGenom=newqueryGenom

    # ouverture fichier
    with open(blast) as file : 
        l=1
        
        for line in file:
            if line.startswith("# BLASTP"):
                l=1 # première ligne de commentaire d'une seq query

            else :
                l+=1 # on a avancé d'une ligne

                if l == 2 :
                    # on recupère le nom de la sequence query
                    query=line.strip("# Query:").strip()
                    # ajout clé query si necessaire
                    if query not in genomhit.keys():
                        genomhit[query]=[] # on crée une liste associé à la sequence query : on aura les best hits pour chaque genome

                if l == 4 and line.startswith("# 0 hits") :
                    # si on a pas de hit 
                     genomhit[query].append(None) # on ajoute un none


                elif l == 6 : # premier hit s'il y en a un

                    # on recupère les informations
                    dataline=line.split("\t")
                    subject=dataline[1]
                    identity= float(dataline[2])
                    evalue=float(dataline[11])
                    cov=float(dataline[3])/float(dataline[13]) *100 # coverage : longueur alignement sur longueur query

                    
                    # applications filtres
                    add= True # on dit qu'on va ajouter
                    # on regarde si une des conditions n'est pas validé
                    if (args.identity is not None and identity<args.identity) or \
                    (args.evalue is not None and evalue > args.evalue) or \
                    (args.coverage is not None and cov<args.coverage)  :
                        add=False


                    # ajout du best hit
                    if add == True :
                        genomhit[query].append(subject)
                    else :
                        genomhit[query].append(None)
                    

        file.close 
    
    if blast == files[len(files)-1]: # si c'était le dernier fichier, faut ajouter
        genomhit_all[queryGenom]=genomhit 
    

    # on ecrit le dictionnaire dans un fichier json
    with open( args.json , 'w') as fichier_json:
        json.dump(genomhit_all, fichier_json)
