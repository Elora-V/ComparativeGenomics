import json
import argparse

parser=argparse.ArgumentParser()
parser.add_argument("-f","--filejson",help="chemin vers le fichier dictionnaire best hits",type=str,required=True)
args=parser.parse_args()



with open(args.filejson) as file:
    genomhit = json.load(file)



listClique=[]

genom1=list(genomhit.keys())[1]
queries1=genomhit[genom1].keys()


for q1 in queries1 : # pour chaque gène/query du genome 1
    hit1=genomhit[genom1][q1] # les best hit du genome 1 query q
    if None not in hit1: # si il manque 1 best hit : pas clique
    # donc fait que si pas none la verification des comparaisons

        flag=True # on suppose que clique

        for i in range( len(list((genomhit.keys()))) ) : # pour chaque best hits, verif si ces hits ont les mêmes listes (i de 0 à 20)
            if flag==True: # si clique possible

                genom=list((genomhit.keys()))[i] # recup clé du genome i
                query=hit1[i] # recup le ieme hit
                
                listHit=genomhit[genom][query]

                if listHit!=hit1 : # si la liste des hits est différente de celle obtenu dans le genome 1
                    flag=False # arrete

        # on a verifié pour chaque besthit si csa liste de best hit est pareil
        # si flag tjrs vrai : clique
        if flag==True:
            listClique.append(hit1) # ajoute la clique

print(len(listClique))
            





