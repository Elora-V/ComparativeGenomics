import os
import glob
import argparse
import json

parser=argparse.ArgumentParser()
parser.add_argument("-d","--dirBlast",help="chemin vers les fichiers output blast",type=str,required=True)
parser.add_argument("-ecds","--evaluecds",help="evalue max",type=float,required=False)
parser.add_argument("-covcds","--coveragecds",help="coverage min",type=float,required=False)
parser.add_argument("-idcds","--identitycds",help="identity min",type=float,required=False)
parser.add_argument("-eigorf","--evalueigorf",help="evalue max",type=float,required=False)
parser.add_argument("-covigorf","--coverageigorf",help="coverage min",type=float,required=False)
parser.add_argument("-idigorf","--identityigorf",help="identity min",type=float,required=False)
parser.add_argument("-jcds","--jsoncds",help="name json output",type=str,required=True)
parser.add_argument("-jigorf","--jsonigorf",help="name json output",type=str,required=True)

args=parser.parse_args()



genomhit_cds={}
genomhit_igorf={}

# on parcours tous les outputs de blast
files=sorted(glob.glob(args.dirBlast+"/*.bl"))


for blast in files:

    # recupérer les noms des genomes query et subject
    filename=os.path.basename(blast)
    listGenom=filename.strip(".bl").split("_vs_")
    queryGenom=listGenom[0]
    subjectGenom=listGenom[1]

    # add key genom
    if queryGenom not in genomhit_cds.keys():
        print("Genome "+queryGenom)
        genomhit_cds[queryGenom]={}
    if queryGenom not in genomhit_igorf.keys():
        genomhit_igorf[queryGenom]={}

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
                    isCDS=len(query.split('_'))<=3

                    # ajout clé query si necessaire
                    if isCDS and query not in genomhit_cds[queryGenom].keys():
                        genomhit_cds[queryGenom][query]=[] # on crée une liste associé à la sequence query : on aura les best hits pour chaque genome
                    elif not isCDS and query not in genomhit_igorf[queryGenom].keys():
                        genomhit_igorf[queryGenom][query]=[]

                if l == 4 and line.startswith("# 0 hits") :
                    # si on a pas de hit 
                    if isCDS :
                        genomhit_cds[queryGenom][query].append(None) # on ajoute un none
                    else :
                        genomhit_igorf[queryGenom][query].append(None)

                elif l == 6 : # premier hit s'il y en a un

                    # on recupère les informations
                    dataline=line.split("\t")
                    subject=dataline[1]
                    identity= float(dataline[2])
                    evalue=float(dataline[11])
                    cov=float(dataline[3])/float(dataline[13]) *100 # coverage : longueur alignement sur longueur query

                    isHitCDS=len(subject.split('_'))<=3
                    # applications filtres
                    add= True # on dit qu'on va ajouter
                    # on regarde si une des conditions n'est pas validé
                    if isCDS and isHitCDS : # si cds

                        if (args.identitycds is not None and identity<args.identitycds) or \
                        (args.evaluecds is not None and evalue > args.evaluecds) or \
                        (args.coveragecds is not None and cov<args.coveragecds)  :
                            add=False
                    elif not isCDS and not isHitCDS : # si igorf

                        if (args.identityigorf is not None and identity<args.identityigorf) or \
                        (args.evalueigorf is not None and evalue > args.evalueigorf) or \
                        (args.coverageigorf is not None and cov<args.coverageigorf)  :
                            add=False


                    # ajout du best hit
                    if add == True :
                        if isCDS:
                            genomhit_cds[queryGenom][query].append(subject)
                        else :
                            genomhit_igorf[queryGenom][query].append(subject)

                    else :
                        if isCDS:
                            genomhit_cds[queryGenom][query].append(None)
                        else :
                            genomhit_igorf[queryGenom][query].append(None)
                    

        #file.close()

    


# on ecrit le dictionnaire dans un fichier json
with open( args.jsoncds , 'w') as fichier_json:
    json.dump(genomhit_cds, fichier_json)
with open( args.jsonigorf , 'w') as fichier_json:
    json.dump(genomhit_igorf, fichier_json)
