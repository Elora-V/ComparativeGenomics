import os
import glob
import argparse

parser=argparse.ArgumentParser()
parser.add_argument("-d","--dirBlast",help="chemin vers les fichiers output blast",type=str,required=True)
args=parser.parse_args()



genomhit={}


for blast in glob.iglob(args.dirBlast+"*"):

    # recupérer les noms des genomes query et subject
    filename=os.path.basename(blast)
    listGenom=filename.strip(".bl").split("-vs-")
    queryGenom=listGenom[0]
    subjectGenom=listGenom[1]

    # ajout de la clé du genome query
    if queryGenom not in genomhit.keys() : # si c'est la première fois qu'on a ce genome en query
        genomhit[queryGenom]={} # on crée un dico associé au query genome

    genomhit[queryGenom][subjectGenom]=[] # on crée une liste associé au genome subjet dans le genome query

        

    # ouverture fichier
    with open(blast) as file : 
        l=1
        nbquery=0
        for line in file:
            if line.startswith("# BLASTP"):
                l=1 # première ligne de commentaire 
                nbquery += 1
            else :
                l+=1 # on a avancé d'une ligne
                

        print(nbquery)
        file.close 



    break
