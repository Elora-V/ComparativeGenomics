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



# on parcours tous les outputs de blast
files=sorted(glob.glob(args.dirBlast+"/*"))

all_auto_hits={}

for blast in files:

    # recupérer les noms des genomes query et subject
    filename=os.path.basename(blast)
    listGenom=filename.strip(".bl").split("-vs-")
    queryGenom=listGenom[0]
    subjectGenom=listGenom[1]

    if(queryGenom == subjectGenom) : # si blast contre lui meme

        all_auto_hits[queryGenom]={}
        print("Recherche auto-hits de "+queryGenom)

        # ouverture fichier
        with open(blast) as file : 
            l=1
            for line in file :
                if line.startswith("# BLAST"):
                    l=1 # première ligne de commentaire d'une seq query

                else :
                    l+=1 # on a avancé d'une ligne

                    if l == 2 :
                        # on recupère le nom de la sequence query
                        query=line.strip("# Query:").strip()
                        # ajout clé query si necessaire
                        if query not in all_auto_hits[queryGenom].keys():
                            all_auto_hits[queryGenom][query]=[] # on crée une liste associé à la sequence query : on aura les best hits pour chaque genome

                    # if l == 4 and line.startswith("# 0 hits") :
                    #     # si on a pas de hit 
                    #     all_auto_hits[queryGenom][query].append(None) # on ajoute un none


                    elif l >= 6 : # premier hit s'il y en a un

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
                            all_auto_hits[queryGenom][query].append(subject)
                        # else :
                        #     genomhit[queryGenom][query].append(None)
                        

            #file.close()
    

# Verifier reciprocité et comptage gène dupli
geneDupli={}
pourcentDupli={}

for genom in all_auto_hits.keys():
    
    dupli=0
    for query in all_auto_hits[genom].keys(): # pr chaque query

        nbhit=len(all_auto_hits[genom][query] )
        
        if nbhit>=2 :
            newhit_query=[]
            for i in range(nbhit): # pr chaque hit d'une query regarde si reciproque
                hit=all_auto_hits[genom][query][i]
                if hit != query :
                    hits_of_hit=all_auto_hits[genom][hit]
                    if query in hits_of_hit: # si  reciproque
                        # on veut ajouter hit de la liste de query 
                        newhit_query.append(hit)
                else:
                    newhit_query.append(hit)
            # replace nouvelle liste reciproque ds dico
            all_auto_hits[genom][query]=newhit_query
            if len(newhit_query)>=2 : # regarde nouvelle taille
                dupli+=1

    geneDupli[genom]=dupli
    pourcentDupli[genom]=round(dupli/len(all_auto_hits[genom])*100,2)

print(geneDupli)
print(str(sum(geneDupli.values())/len(geneDupli))+ " gene dupli en moyenne")
print(str(sum(geneDupli.values()))+ " gene dupli au total")
print(pourcentDupli)
print(str(round(sum(pourcentDupli.values())/len(pourcentDupli),2))+ " % gene dupli en moyenne")

# on ecrit le dictionnaire dans un fichier json
with open( args.json , 'w') as fichier_json:
    json.dump(all_auto_hits, fichier_json)
