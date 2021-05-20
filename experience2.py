# Créé par Léo, le 20/05/2021 en Python 3.4
import os
import xlrd
import matplotlib.pyplot as plt
import numpy as np
import pylab


#fonctions utile

#lissage de courbe problème cette fonction ne fait pas que une moyenne elle modififie un peu l'allure générale de la courbe COMMENT NE PAS LA MODIFIER ?
def moyenne(L,j=8):

    n=len(L)
    for l in range(n-j):
        somme=0
        for ll in range(j):
            somme+=L[l+ll]
        L[l]=somme/j
    return L


def recherche0(liste):#pour que les courbes commencent au même moment
    i=0
    while liste[i]>0 and liste[i+1]>0 or liste[i]<0:#il y a forcément une fin à la fonction while car la fonction est sinusoïdale
        i+=1
    return i


def recherche_nombre_composante_max(liste_de_liste):#fonction pour déterminer au final la longueur de la liste temps
    dimension=[]
    for liste in liste_de_liste:
        dimension.append(len(liste))
    return max(dimension)

#détection de la fréquence à partir d'une liste de la position des extremums d'une liste
def frequence(Liste,temps):#on prend pas les première ni les dernières valeur car surement fausse
    freq = (temps[Liste[-2]]-temps[Liste[1]])/len(Liste[1:-2])
    return 1/freq

#détection des extremums
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

#meme chose pour les extremum positifs

def indice_des_extremun_positif_liste(Liste,temps):

    n=len(Liste)
    indice_aproxi=[]
    #déterminations des extremums possibles
    for i in range (n-2):
        derive1= (Liste[i+1]-Liste[i])/(temps[i+1]-temps[i])
        derive2= (Liste[i+2]-Liste[i+1])/(temps[i+2]-temps[i+1])


        if (derive1>0 and derive2<0 and Liste[i]>0):
            indice_aproxi.append(i)
    #première filtration des résultats
    i=0
    indice_mauvais=[]
    while i <len(indice_aproxi)-2:

        if indice_aproxi[i+1]-indice_aproxi[i]<20 :

            valeur1,valeur2=Liste[indice_aproxi[i]],Liste[indice_aproxi[i+1]]
            if valeur1>valeur2:
                del(indice_aproxi[i+1])
                i-=1
        i+=1
    #deuxième filtration des résultats je comprends pas pourquoi ca marche comme ca mais j'ai essayer de nombreux moyen différents et celui-ci marche mieux que les autres solutions
    i=0
    while i <len(indice_aproxi)-1:
        if indice_aproxi[i+1]-indice_aproxi[i]<20 :

            valeur1,valeur2=Liste[indice_aproxi[i]],Liste[indice_aproxi[i+1]]
            if valeur1>valeur2:
                del(indice_aproxi[i+1])

            else:

                del(indice_aproxi[i])
                i-=1
        i+=1
    return indice_aproxi

#determination d'amplitude à partir d'une liste d'extremum

def moyenne_amplitude(liste_indice,liste):
    somme=0
    n=len(liste_indice[1:-1])
    for indice in liste_indice[1:-2]:#car les première et les dernières valeurs sont souvent fausse
        somme+=abs(liste[indice])#comme il y a des valeurs négative on travail tout en positif
    return somme/n


#détermination d'une amplitude
def Amplitude(indice_min,indice_max,liste):
    amplitude_min=moyenne_amplitude(indice_min,liste)
    amplitude_max=moyenne_amplitude(indice_max,liste)
    res=(amplitude_min+amplitude_max)/2
    return res

#détermination de Xm
def Xm(amplitude,freq):
    return (amplitude/((2*np.pi*freq)**2))


#méthode de comparaison de la profde physique


def methode_comparaison_tout_en_un_villas(liste__de_liste,nom):

    num=0
    for liste in liste__de_liste:
        liste_frequence=[]
        Xm_pour_chaque_frequence=[]
        for element in liste:
            n=len(element)
            temps=np.linspace(0,échantillonage*n,n)
            indice_extr_min=indice_des_extremun_negatif_liste(element,temps)
            indice_extr_max=indice_des_extremun_positif_liste(element,temps)


            liste_frequence.append(frequence(indice_extr_min,temps))
            Xm_pour_chaque_frequence.append(Xm(Amplitude(indice_extr_min,indice_extr_max,element),frequence(indice_extr_min,temps)))

        #on trace la fonction
##        plt.plot(liste_frequence,Xm_pour_chaque_frequence)#ne marche pas pour l'instant


        if num==0:
            for i in range (len(liste_frequence)):
                plt.plot(liste_frequence[i],Xm_pour_chaque_frequence[i],marker="o",color="red")
        else :
            for i in range (len(liste_frequence)):
                plt.plot(liste_frequence[i],Xm_pour_chaque_frequence[i],marker="o",color="green")
        num+=1

    plt.xlabel("frequence en Hz")
    plt.ylabel("Xm(f)")
    plt.title(nom)
    plt.show()

    return

#on se place dans le fichier contenant les expériences


fichier_contenant_les_experiences='experience_deuxieme_partie_regime_force'
os.chdir(fichier_contenant_les_experiences)
List_nom_experiences=os.listdir(".")
adress_depart=os.getcwd()

#variables globales

accligne=2 #la colonne qui nous interesse dans chaque doc excel
échantillonage=0.003#échantillonnage en seconde


#on regarde les expériences présentent dans tout les fichiers
for nom_experience in List_nom_experiences:
    print("nom de l'experience :",nom_experience," \n fichier en traitement :")
    os.chdir(nom_experience)
    Liste_experiences=os.listdir(".")
    print(Liste_experiences ,"\n ...")

    #Liste des composante pour chaque experience

    Liste_eau_mouvante=[]
    Liste_eau_fixe=[]

    #ouverture de chaques documents

    for experience in Liste_experiences :


        document = xlrd.open_workbook(experience)
        feuille_1 = document.sheet_by_index(0)
        cols = feuille_1.ncols
        rows = feuille_1.nrows

        #quelques variables utiles

        Liste_valeurs_eau_mouvante= []#eau mouvante abrégé en M
        Liste_valeurs_eau_fixe=[]#eau fixe abrégé en F

        #indices extremum

        indices_extremun_max_M,indices_extremun_min_M=[],[]
        indices_extremun_max_F,indices_extremun_min_F=[],[]

        for r in range(2, rows):


            valeur_eau_mouvante=feuille_1.cell_value(rowx=r, colx=accligne)
            if cols > 7:# car il se peut que l'experience d'eau stable n'ai pas pu se faire
                valeur_eau_stable=feuille_1.cell_value(rowx=r, colx=7+accligne)
            else :
                valeur_eau_stable=False

            if valeur_eau_mouvante:#car la donnee peut ne pas exister pour des raisons d'indice
                Liste_valeurs_eau_mouvante+= [int(valeur_eau_mouvante)]

            if valeur_eau_stable:#car la donnee peut ne pas exister pour des raisons d'indice
                Liste_valeurs_eau_fixe+=[int(valeur_eau_stable)]

        if len(Liste_valeurs_eau_mouvante)>0:# pour l'eau qui bouge

            Liste_valeurs_eau_mouvante=moyenne(moyenne(moyenne(Liste_valeurs_eau_mouvante)))#on lisse en meme temps les données
            i=recherche0(Liste_valeurs_eau_mouvante)

            Liste_eau_mouvante.append(Liste_valeurs_eau_mouvante[i:])#on se place au meme début pour chaque courbe



        if len(Liste_valeurs_eau_fixe)>0: #pour l'eau fixe meme chose

            Liste_valeurs_eau_fixe=moyenne(moyenne(moyenne(Liste_valeurs_eau_fixe)))
            j=recherche0(Liste_valeurs_eau_fixe)

            Liste_eau_fixe.append(moyenne(moyenne(moyenne(Liste_valeurs_eau_fixe))))#on lisse en meme temps les données

            #detection des extremums



    # après avoir ouvert les documents et enregistrer les valeur avec et sans mouvement sous forme de liste dans les variables :Liste_eau_fixe et Liste_eau_mouvante :

    # création de la liste temps :
    nombre_composante_max=max(recherche_nombre_composante_max(Liste_eau_fixe),recherche_nombre_composante_max(Liste_eau_mouvante))
    temps=np.linspace(0,échantillonage*nombre_composante_max,nombre_composante_max)


    print("nom_experience :",nom_experience, ", shape liste eau fixe :",np.shape(Liste_eau_fixe),", shape liste eau qui bouge :", np.shape(Liste_eau_mouvante),"\n")

    #visualisation et comparaison des résultats

    methode_comparaison_tout_en_un_villas([Liste_eau_fixe,Liste_eau_mouvante],nom_experience)




    #on revient à l'adresse d'avant
    os.chdir(adress_depart)



