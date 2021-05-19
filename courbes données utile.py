import os
import xlrd
import matplotlib.pyplot as plt
import numpy as np
import pylab

#définition de quelques fonctions qui vont être utiles

#lissage de courbe problème cette fonction ne fait pas que une moyenne elle modififie un peu l'allure générale de la courbe COMMENT NE PAS LA MODIFIER ?
def moyenne(L,j=8):

    n=len(L)
    for l in range(n-j):
        somme=0
        for ll in range(j):
            somme+=L[l+ll]
        L[l]=somme/j
    return L

#détermination d'une fréquence à partir d'une liste contennant les indices des extremun min d'une fonction et d'une liste contant les temps de l'expérience

def frequence(Liste,temps):#on prend pas les première ni les dernières valeur car surement fausse
    freq = (temps[Liste[-2]]-temps[Liste[1]])/len(Liste[1:-2])
    return 1/freq

#détermination du premier indice d'une liste coupant l'axe des abscices

def recherche0(liste):#pour que les courbes commencent au même moment
    i=0
    while liste[i]>0 and liste[i+1]>0 or liste[i]<0:#il y a forcément une fin à la fonction while car la fonction est sinusoïdale
        i+=1
    return i

#pour que les listes aient la meme durée

def synchroniser(liste1,liste2,temps):
    n=min(len(liste1),len(liste2),len(temps))
    return liste1[:n],liste2[:n],temps[:n]

#pour trouver les extremums min d'une fonction

def indice_des_extremun_negatif_liste(Liste,temps):

    n=len(Liste)
    indice_aproxi=[]
    #déterminations des extremums possibles
    for i in range (n-2):
        derive1= (Liste[i+1]-Liste[i])/(temps[i+1]-temps[i])
        derive2= (Liste[i+2]-Liste[i+1])/(temps[i+2]-temps[i+1])


        if (derive1<0 and derive2>0 and Liste[i]<0):
            indice_aproxi.append(i)
    #première filtration des résultats
    i=0
    indice_mauvais=[]
    while i <len(indice_aproxi)-2:
##        deriv=[]
##        for j in range(5):
##            deriv.append( (Liste[indice_aproxi[i+1]]-Liste[indice_aproxi[i]])/(temps[indice_aproxi[i+1]]-temps[indice_aproxi[i]]))
##        derive_avg=m

        if indice_aproxi[i+1]-indice_aproxi[i]<20 :

            valeur1,valeur2=Liste[indice_aproxi[i]],Liste[indice_aproxi[i+1]]
            if valeur1<valeur2:
                del(indice_aproxi[i+1])
                i-=1
        i+=1
    #deuxième filtration des résultats je comprends pas pourquoi ca marche comme ca mais j'ai essayer de nombreux moyen différents et celui-ci marche mieux que les autres solutions
    i=0
    while i <len(indice_aproxi)-1:
        if indice_aproxi[i+1]-indice_aproxi[i]<20 :

            valeur1,valeur2=Liste[indice_aproxi[i]],Liste[indice_aproxi[i+1]]
            if valeur1<valeur2:
                del(indice_aproxi[i+1])

            else:

                del(indice_aproxi[i])
                i-=1
        i+=1
    return indice_aproxi

#fonction pour déterminer des rapports en régime forcé
#pas finis car pour l'instant elle marche que si il y a le même nombre d'extremun

def rapport_dif_des_max_en_forcé(indicesmax_B,indicesmax_F,liste_B,liste_F):
    if len(indicesmax_B)==len(indicesmax_F):
        n=len(indicesmax_B)
        somme_B=0
        somme_F=0
        for i in range(n):
            somme_B+=liste_B[indicesmax_B[i]]
            somme_F+=liste_F[indicesmax_F[i]]
        moyenne_B=somme_B/n
        moyenne_F=somme_F/n
        rapport =moyenne_B/moyenne_F
        return rapport
    return 0

#création de diagramme baton
def plot_diag_baton(liste,nom,titre,name_axeY):
    n=len(liste)
    X=[i for i in range(1,n+1)]
    width=0.1
    plt.bar(X,liste,width)
    plt.scatter([i+width/2.0 for i in X],liste)

    plt.xlim(0,n+1)
    plt.ylim(0,max(liste)+min(liste)/2)
    plt.ylabel(name_axeY)
    plt.title(titre)

    pylab.xticks(X,nom,rotation=40)

    plt.show()

#ouverture du premier document contenant les adresses de tout les autres ainsi que des informations particulières aux epériences et aux mesures

document1 = xlrd.open_workbook("donnees_utiles.xlsx")
feuille = document1.sheet_by_index(0)
rows1 = feuille.nrows
nom,experience,experience_name=[],[],[]

#on récupère dans un document excel toute les adresses des document à utilser, on creer une liste contenant leur adresse et l'autre leur type

for i in range (1,rows1):
    nom+=[feuille.cell_value(rowx=i, colx=0)]
    experience+=[feuille.cell_value(rowx=i, colx=1)]
    if int(experience[i-1])==0:
        experience_name+=["oscillation forcée"]
    else:
        experience_name+=["amortissement"]

#données précisant l'échantillonnage

échantillonage=float(feuille.cell_value(rowx=1, colx=2))
acc,accligne=feuille.cell_value(rowx=1, colx=3),feuille.cell_value(rowx=1, colx=4)

#vérification de la récupération des adresses des documments

print(nom)

#Variables globales pour le diagramme baton

rapport_regime_force=[]
nom_regime_force=[]

#pour chaque document on regarde ses données
#chaque document possede 14 collonnes de données les 7 premières pour l'exprience ou l'eau bouge et les 7 autres quand l'eau est stable  dans les mêmes conditions

for k in range (len(nom)):
    document = xlrd.open_workbook(nom[k])
    feuille_1 = document.sheet_by_index(0)
    cols = feuille_1.ncols
    rows = feuille_1.nrows
    X = []
    Liste_valeurs_eau_mouvante= []
    Liste_valeurs_eau_fixe=[]
    t=0
    for r in range(2, rows):
        valeur_eau_mouvante=feuille_1.cell_value(rowx=r, colx=int(accligne))
        valeur_eau_stable=feuille_1.cell_value(rowx=r, colx=7+int(accligne))
        t+=échantillonage #étape de création de la liste des abscises suremment des erreurs dans les données car l'échantillonage n'est pas précis à la miliseconde près ce qui nous interresse ici donc peut induire un décalage irréversible
        X+= [t]
        if valeur_eau_mouvante:#car la donnee peut ne pas exister pour des raisons d'indice
            Liste_valeurs_eau_mouvante+= [int(valeur_eau_mouvante)]
        if valeur_eau_stable:#car la donnee peut ne pas exister pour des raisons d'indice
            Liste_valeurs_eau_fixe+=[int(valeur_eau_stable)]

    #réalisation d'une moyenne pour lisser la courbe

    Liste_valeurs_eau_mouvante=moyenne(moyenne(moyenne(Liste_valeurs_eau_mouvante)))
    Liste_valeurs_eau_fixe=moyenne(moyenne(moyenne(Liste_valeurs_eau_fixe)))
##
##    Liste_valeurs_eau_mouvante=moyenneY(Liste_valeurs_eau_mouvante)
##    Liste_valeurs_eau_fixe=moyenneY(Liste_valeurs_eau_fixe)
##    print("i=",i)
    #on commence les deux listes au même point (faut faire attention car il y a les courbes en ammortissement et celles en oscilation forcés)

    if int(experience[k])==0:#si oscillation forcée
        i=recherche0(Liste_valeurs_eau_mouvante)
        j=recherche0(Liste_valeurs_eau_fixe)
    else:#si ammortissement
        i=Liste_valeurs_eau_mouvante.index(min(Liste_valeurs_eau_mouvante))
        j=Liste_valeurs_eau_fixe.index(min(Liste_valeurs_eau_fixe))

    #créeation de liste

    Liste_B=Liste_valeurs_eau_mouvante[i:]
    Liste_F=Liste_valeurs_eau_fixe[j:]
    temps=X[:len(Liste_valeurs_eau_mouvante)-min(i,j)]

    #synchronisation

    Liste_B,Liste_F,temps=synchroniser(Liste_B,Liste_F,temps)

    #valeur des extremuns

    indice_B=indice_des_extremun_negatif_liste(Liste_B,temps)
    indice_F=indice_des_extremun_negatif_liste(Liste_F,temps)

    #fréquence des courbes

    freq_B=frequence(indice_B,temps)
    freq_F=frequence(indice_F,temps)

    #modification des variables globales pour le diagramme baton

    if int(experience[k])==0:#si oscillation forcée
        nom_regime_force.append(nom[k][:-12])
        rapport_regime_force.append(rapport_dif_des_max_en_forcé(indice_B[1:-2],indice_F[1:-2],Liste_B,Liste_F))

    #on créer les courbes


    plt.plot(temps, Liste_B,label="eau mouvante "+"freq "+str(freq_B)[:6]+" Hz")
    plt.plot(temps,Liste_F,label="eau fixe "+"freq "+str(freq_F)[:6]+" Hz")
    plt.title(experience_name[k]+" : "+nom[k][:-5])
    plt.xlabel("Temps (en secondes)")


    #tracer les points des extremums min

    for j in indice_B:
        plt.plot(temps[j],Liste_B[j],marker="o",color="red")
    for j in indice_F:
        plt.plot(temps[j],Liste_F[j],marker="o",color="green")

    plt.ylabel(acc)
    plt.legend()
    plt.show()

#tracer le diagramme baton des rapport à modifier

plot_diag_baton(rapport_regime_force,nom_regime_force,"régime forcé","accélération")