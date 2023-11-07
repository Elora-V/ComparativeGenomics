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
                    if query not in genomhit[queryGenom].keys():
                        genomhit[queryGenom][query]=[] # on crée une liste associé à la sequence query : on aura les best hits pour chaque genome

                if l == 4 and line.startswith("# 0 hits") :
                    # si on a pas de hit 
                     genomhit[queryGenom][query].append(None) # on ajoute un none


                elif l == 6 : # premier hit s'il y en a un

                    # on recupère les informations
                    dataline=line.split("\t")
                    subject=dataline[1]
                    identity= float(dataline[2])
                    evalue=float(dataline[11])
                    cov=float(dataline[3])/float(dataline[13]) *100 # coverage : longueur alignement sur longueur query
                    
                    # ajout du best hit
                    genomhit[queryGenom][query].append(subject)
                    

        print(genomhit['Escherichia_coli_umn026']['Eco13_4407'])

        file.close 



    break
