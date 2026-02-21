import pandas as pd
import matplotlib.pyplot as plt
from raport import *
from datetime import datetime



def execute(fichier_entrer , fichier_sortie_ecxel="documents_rapport/data_cleaning.xlsx"):
    try :
   
    #ÉTAPE 1 — Nettoyer et préparer les données ******************************

        # read and clean data
        df = pd.read_excel(fichier_entrer)
        pd.set_option('display.max_columns' , None)
        df_A = df.drop_duplicates().dropna(subset=["ID_Règlement" ,"ID_Client" , "ID_Restaurant" , "ID_User" ]).copy()
        #clean columns Date_Heure
        df_A["Date_Règlement"] = pd.to_datetime(
            df_A["Date_Règlement"],
            format="%Y-%m-%d",
            errors="coerce"
        ) 
        df_A["Date_Sys"] = pd.to_datetime(
            df_A["Date_Sys"],
            format="%Y-%m-%d",
            errors="coerce"
        ) 
        df_A["Heure_Règlement"] = pd.to_datetime(
            df_A["Heure_Règlement"],
            format="%H:%M:%S",
            errors="coerce"
        ) 
        # extraction de annes mois semaine heur
        df_A["Année"] = df_A["Date_Règlement"].dt.year
        df_A["Mois"] = df_A["Date_Règlement"].dt.month
        df_A["Semaine"] = df_A["Date_Règlement"].dt.isocalendar().week
        df_A["Jour"] = df_A["Date_Règlement"].dt.day
        df_A["Heure"] = df_A["Heure_Règlement"].dt.hour
        # Conversion des montants en numérique
        c_montant = ["Montant_Rgl", "Montant_Rst", "Montant_Versé", "Solde_CPP"]
        for c in c_montant:
            new_col = []
            for x in df_A[c]:
                if isinstance(x, (pd.Timestamp, datetime)):
                    new_col.append(x.day + x.month / 100)
                elif isinstance(x, (int, float)):
                    new_col.append(float(x))
                elif isinstance(x, str):
                    if x.replace('.', '').isdigit():
                        new_col.append(float(x))
                    else:
                        new_col.append(pd.NA)  
                else:
                    new_col.append(pd.NA)  
            df_A[c] = new_col  
        # Drop rows == NaN 
        df_A = df_A.dropna(subset=c_montant).reset_index(drop=True)
        df_A = df_A.dropna(subset=["Date_Règlement" , "Date_Sys" , "Heure_Règlement"])



    #ÉTAPE 2 — Analyse des tendances ******************************

        # nomber des jeur et semaine et mois
        agregation = df_A.groupby("Date_Règlement").agg(
            Chiffre_journalier = ("Jour" , "sum"),
            Chiffre_hebdomadaire = ("Semaine" , "sum"),
            Chiffre_mensuel = ("Mois" , "sum")
        )
        # Analyse des Soldes des Cartes
        Analyse_Soldes_Cartes_Jeur = df_A.groupby("Jour")["Solde_CPP"].mean().reset_index()
        Analyse_Soldes_Cartes_Semaine = df_A.groupby("Semaine")["Solde_CPP"].mean().reset_index()
        Analyse_Soldes_Cartes_Mois = df_A.groupby("Mois")["Solde_CPP"].mean().reset_index()
        # classement des Soldes par Jeur , Semainne , Mois
        analyse_jeur = Analyse_Soldes_Cartes_Jeur.sort_values(by="Solde_CPP" , ascending=False)
        analyse_Semaine = Analyse_Soldes_Cartes_Semaine.sort_values(by="Solde_CPP" , ascending=False)
        analyse_Mois = Analyse_Soldes_Cartes_Mois.sort_values(by="Solde_CPP" , ascending=False)
        #graphe
        plt.figure()
        plt.plot( Analyse_Soldes_Cartes_Jeur["Jour"] , Analyse_Soldes_Cartes_Jeur["Solde_CPP"] , marker="o")
        plt.ylabel("Solde")
        plt.xlabel("Jour")
        plt.title("moyenne sold par jour")
        plt.xticks(rotation=40)
        plt.savefig("documents_rapport/Moyenne_solde_par_jeur.jpg")

        plt.figure()
        plt.plot(Analyse_Soldes_Cartes_Semaine["Semaine"] , Analyse_Soldes_Cartes_Semaine["Solde_CPP"]  , marker="o")
        plt.ylabel("Solde")
        plt.xlabel("Semaine")
        plt.title("moyenne sold par Semaine")
        plt.xticks(rotation=40)
        plt.savefig("documents_rapport/Moyenne_solde_par_Semaine.jpg")

        plt.figure()
        plt.plot(Analyse_Soldes_Cartes_Mois["Mois"] , Analyse_Soldes_Cartes_Mois["Solde_CPP"] , marker="o")
        plt.ylabel("Solde")
        plt.xlabel("Mois")
        plt.title("moyenne sold par Mois")
        plt.savefig("documents_rapport/Moyenne_solde_par_mois.jpg")



    #ÉTAPE 3 — Identifier les clients clés ******************************

        # afficher top 10 clients
        clients = df_A.groupby("ID_Client").agg(
            Total_dépensé = ("Montant_Rgl" , "sum") , 
            moyenne_transactions = ("Montant_Rgl", "mean"),
            Nombre_Transactions = ("ID_Règlement", "count"),
            solde_moyen = ("Solde_CPP", "mean"),
        ).reset_index()
        # classement des top clients 
        clients_10Tops = clients.sort_values(by="Total_dépensé" , ascending=False
        )[["ID_Client", "Total_dépensé" , "Nombre_Transactions", "solde_moyen"]]
        # On détecte les clients ayant des restes non réglés.
        Ayant_Non_Regles = df_A[df_A["Montant_Rst"] > 0]
        clients_Ayant_Non_Regles = Ayant_Non_Regles.groupby("ID_Client").agg(
            Sum_mantans_RST = ("Montant_Rst" , "sum") ,
            nomber_transaction = ("ID_Règlement","count"),
            moy_sold = ("Solde_CPP" , "mean") 
        )
   

    

    #ÉTAPE 4 — Performance des Restaurants & Heures de Pointe ******************************
 
        # Chiffre d’affaires par restaurant
        G_resturant = df_A.groupby("ID_Restaurant").agg(
            total_Rgl = ("Montant_Rgl" , "sum"),
            moy_Rgl = ("Montant_Rgl" , "mean"),
            nomber_transaction = ("ID_Règlement","count")
        )
        # Analyse du volume de transactions par tranche horaire
        G_heur = df_A.groupby("Heure").agg(
            total_Rgl = ("Montant_Rgl" , "sum") , 
            nomber_transaction = ("ID_Règlement","count")
        )
        # Classement des restaurant et Heur
        top_resturants = G_resturant.sort_values( by="total_Rgl" , ascending=False )
        top_heur = G_heur.sort_values(by="total_Rgl" , ascending=False)




    #ÉTAPE 5 — Détection des anomalies ******************************

        # calcule quantile 1 et 3
        Q1 = df_A["Montant_Rgl"].quantile(0.25)
        Q3 = df_A["Montant_Rgl"].quantile(0.75)
        # calcule IQR
        IQR = Q3 - Q1
        # calcule data anomalies
        lower_range = Q1 - 1.5 * IQR
        upper_range = Q3 + 1.5 * IQR
        df_Anormalis = df_A[
            (df_A["Montant_Rgl"] < lower_range) |
            (df_A["Montant_Rgl"] > upper_range)
        ][["ID_Règlement" , "ID_Client" , "ID_User" , "Montant_Rgl"]]
    


    #ÉTAPE 6 — Analyse des Performances des Caissiers ******************************

        G_User = df_A.groupby("ID_User").agg(
            Montant_total_traité = ("Montant_Versé" , "sum") ,
            Nombre_de_transactions = ('ID_Règlement' , "count")
        )
        # classement user
        s_User = G_User.sort_values(by="Montant_total_traité" , ascending=False)



    #ÉTAPE 7 — Corrélations et insights stratégiques ******************************

        # calculer la Corrélations entre column Solde_CPP et Montant_Rgl
        table = df_A[["Solde_CPP", "Montant_Rgl"]].copy()
        r = table.corr()
    


    #ÉTAPE 8 — Reporting et visualisation ******************************
        
        # export data to fichier excel
        df_A.to_excel(fichier_sortie_ecxel)
        # create rapport word
        create_report_word( agregation, analyse_jeur, analyse_Semaine, analyse_Mois, clients_10Tops, clients_Ayant_Non_Regles,
                        top_resturants, top_heur, df_Anormalis, s_User, r )
        # create rapport text
        rapport_text( agregation, analyse_jeur, analyse_Semaine, analyse_Mois, clients_10Tops, clients_Ayant_Non_Regles,
                        top_resturants, top_heur, df_Anormalis, s_User, r )
        




        




    except Exception as e :
        print("Erreur : ",e)    