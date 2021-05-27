# Créé par Léo, le 25/05/2021 en Python 3.4
# Créé par Léo, le 21/05/2021 en Python 3.4
# Créé par Léo, le 20/05/2021 en Python 3.4
import os
import xlrd
import matplotlib.pyplot as plt
import numpy as np
import pylab


#fonctions utile

#lissage de courbe problème cette fonction ne fait pas que une moyenne elle modififie un peu l'allure générale de la courbe COMMENT NE PAS LA MODIFIER ?
def moyenne(L,j=3):

    n=len(L)
    for l in range(n-j):
        somme=0
        for ll in range(j):
            somme+=L[l+ll]
        L[l]=somme/j
    return L


def recherche0(liste):#pour que les courbes commencent au même moment
    i=0
##    print(len(liste))
    while  i<len(liste)-1 and (liste[i]>0 and liste[i+1]>0 or liste[i]<0):#il y a forcément une fin à la fonction while car la fonction est sinusoïdale
        i+=1
    if i>len(liste)*0.7:
        return 0
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

#determination d'amplitude à partir d'une liste d'extremum

def moyenne_amplitude(liste_indice,liste):
    somme=0
    n=len(liste_indice)
    for indice in liste_indice[1:-2]:#car les première et les dernières valeurs sont souvent fausse
        somme+=abs(liste[indice])#comme il y a des valeurs négative on travail tout en positif
    if n==0:
        print("c'est la merde")
        return 1
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
            temps=np.linspace(0,echantillonage*n,n)
##            indice_extr_min=indice_des_extremun_negatif_liste(element,temps)
##            indice_extr_max=indice_des_extremun_positif_liste(element,temps)
            (indice_extr_min,indice_extr_max)=extremum(element)


            liste_frequence.append(frequence(indice_extr_min,temps))
            Xm_pour_chaque_frequence.append(Xm(Amplitude(indice_extr_min,indice_extr_max,element),frequence(indice_extr_min,temps)))

        #on trace la fonction
##        plt.plot(liste_frequence,Xm_pour_chaque_frequence)#ne marche pas pour l'instant


        if num==0:
            for i in range (len(liste_frequence)):
                plt.plot(liste_frequence[i],Xm_pour_chaque_frequence[i],marker="o",color="red",label ="eau fixe")
        else :
            for i in range (len(liste_frequence)):
                plt.plot(liste_frequence[i],Xm_pour_chaque_frequence[i],marker="o",color="green",label ="eau qui bouge")
        num+=1

    plt.xlabel("frequence en Hz")
    plt.ylabel("Xm(f)")
    plt.title(nom+"\n en rouge l'eau fixe en vert l'eau qui bouge")
##    plt.legend()
    plt.show()

    return

#pour visualiser les courbes et savoir ce que le programme fait
def extremum(liste):
    indice_min=[]
    indice_max=[]
    for i in range(len(liste)-2):

        difference1=liste[i]-liste[i+1]
        difference2=liste[i+1]-liste[i+2]

        if difference1>0 and difference2<=0 and liste[i+1]<0:
            indice_min.append(i+1)
        if difference1<0 and difference2>=0 and liste[i+1]>0:
            indice_max.append(i+1)
    i=0
    while i <len(indice_min)-1:
        if indice_min[i+1]-indice_min[i]<5 :

            valeur1,valeur2=liste[indice_min[i]],liste[indice_min[i+1]]
            if valeur1<valeur2:
                del(indice_min[i+1])

            else:

                del(indice_min[i])
                i-=1
        i+=1
    i=0
    while i <len(indice_max)-1:
        if indice_max[i+1]-indice_max[i]<5 :

            valeur1,valeur2=liste[indice_max[i]],liste[indice_max[i+1]]
            if valeur1>valeur2:
                del(indice_max[i+1])

            else:

                del(indice_max[i])
                i-=1
        i+=1


    return (indice_min,indice_max)


def verification_visuelle(liste,temps):

    plt.plot(temps,liste,label="données filtrées frequence"+str(frequence(extremum(liste)[0],temps))[:4]+"Hz")
    for j in extremum(liste)[0]:
        plt.plot(temps[j],liste[j],marker="o",color="green")

    for j in extremum(liste)[1]:
        plt.plot(temps[j],liste[j],marker="o",color="red")

    plt.title("vérification visuelle des emplacements des extremums\n en rouge extremum positif en vert négatif")
    plt.xlabel("temps en seconde")
    plt.ylabel("accélération")
    plt.legend()
    plt.show()
    return


#on se place dans le fichier contenant les expériences


fichier_contenant_les_experiences='comparaison'
os.chdir(fichier_contenant_les_experiences)
List_nom_experiences=os.listdir(".")
adress_depart=os.getcwd()

#variables globales

accligne=2 #la colonne qui nous interesse dans chaque doc excel
echantillonage=0.035911602#échantillonnage en seconde


#on regarde les expériences présentent dans tout les fichiers
for nom_experience in List_nom_experiences:
    print("nom de l'experience :",nom_experience," \n fichier en traitement :")
    os.chdir(nom_experience)
    Liste_experiences=os.listdir(".")
    print(Liste_experiences ,"\n ...")

    #Liste des composante pour chaque experience

    Liste_de_Liste_des_2_experiences=[]#eau fixe et eau qui bouge

    #ouverture de chaques documents

    for experience in Liste_experiences :#le premier doc sera l'eau fixe et le deuxième l'eau qui bouge

        print("expérience en cours =",experience)



        document = xlrd.open_workbook(experience)
        feuille_1 = document.sheet_by_index(0)
        cols = feuille_1.ncols
        rows = feuille_1.nrows

        #quelques variables utiles

        Liste_valeur__experience=[]

        #on parcours toute les données
        numeros_experience=1
        for colonne in range(accligne,cols,7):
            liste_expe_pour_une_meme_expe=[]

            print("expérience numéros :",numeros_experience)
            numeros_experience+=1
            for ligne in range(2, rows):


                valeur=feuille_1.cell_value(rowx=ligne, colx=colonne)

                if type (valeur)==float :#car la donnee peut ne pas exister pour des raisons d'indice
                    liste_expe_pour_une_meme_expe.append(float(valeur))

            if len(liste_expe_pour_une_meme_expe)>0:# pour l'exp

                liste_expe_pour_une_meme_expe=moyenne(moyenne(moyenne(liste_expe_pour_une_meme_expe)))#on lisse en meme temps les données , 335 car nombre de données pendant 12 s

                i=recherche0(liste_expe_pour_une_meme_expe)


                Liste_valeur__experience.append(liste_expe_pour_une_meme_expe[i:279+i])#on se place au meme début pour chaque courbe

##                verification_visuelle(liste_expe_pour_une_meme_expe[i:279+i],np.linspace(0,echantillonage*len(liste_expe_pour_une_meme_expe[i:279+i]),len(liste_expe_pour_une_meme_expe[i:279+i])))

        #on ajoute les experiences dans la liste contenant les deux experiences

        Liste_de_Liste_des_2_experiences.append(Liste_valeur__experience)

    # après avoir ouvert les documents et enregistrer les valeur avec et sans mouvement sous forme de liste dans les variables

    # création de la liste temps :

    nombre_composante_max=max(recherche_nombre_composante_max(Liste_de_Liste_des_2_experiences[0]),recherche_nombre_composante_max(Liste_de_Liste_des_2_experiences[1]))
    temps=np.linspace(0,echantillonage*nombre_composante_max,nombre_composante_max)


    print("nom_experience :",nom_experience, ", shape liste eau fixe :",np.shape(Liste_de_Liste_des_2_experiences[0]),", shape liste eau qui bouge :", np.shape(Liste_de_Liste_des_2_experiences[1]),"\n")

    #visualisation et comparaison des résultats

    methode_comparaison_tout_en_un_villas(Liste_de_Liste_des_2_experiences,nom_experience)




    #on revient à l'adresse d'avant
    os.chdir(adress_depart)





