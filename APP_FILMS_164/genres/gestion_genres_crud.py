"""Gestion des "routes" FLASK et des données pour les genres.
Fichier : gestion_genres_crud.py
Auteur : NM 2022.03.16
"""
from pathlib import Path

from flask import redirect
from flask import request
from flask import session
from flask import url_for

from APP_FILMS_164.database.database_tools import DBconnection
from APP_FILMS_164.erreurs.exceptions import *
from APP_FILMS_164.genres.gestion_genres_wtf_forms import FormWTFAjouterDonneur
from APP_FILMS_164.genres.gestion_genres_wtf_forms import FormWTFDeleteDonneur
from APP_FILMS_164.genres.gestion_genres_wtf_forms import FormWTFUpdateDonneur

"""
    Auteur : OM 2021.03.16
    Définition d'une "route" /genres_afficher
    
    Test : ex : http://127.0.0.1:5005/genres_afficher
    
    Paramètres : order_by : ASC : Ascendant, DESC : Descendant
                id_donneur_sel = 0 >> tous les genres.
                id_donneur_sel = "n" affiche le genre dont l'id est "n"
"""


@app.route("/genres_afficher/<string:order_by>/<int:id_donneur_sel>", methods=['GET', 'POST'])
def genres_afficher(order_by, id_donneur_sel):
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                if order_by == "ASC" and id_donneur_sel == 0:
                    strsql_genres_afficher = """SELECT id_donneur, prenom, nom, adresse, mail, num_tel, date_naissance, groupe_sanguin from t_donneur ORDER BY id_donneur ASC"""
                    mc_afficher.execute(strsql_genres_afficher)
                elif order_by == "ASC":
                    # C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
                    # la commande MySql classique est "SELECT * FROM t_donneur"
                    # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
                    # donc, je précise les champs à afficher
                    # Constitution d'un dictionnaire pour associer l'id du genre sélectionné avec un nom de variable
                    valeur_id_genre_selected_dictionnaire = {"value_id_donneur_selected": id_donneur_sel}
                    strsql_genres_afficher = """SELECT id_donneur, prenom, nom, adresse, mail, num_tel, date_naissance, groupe_sanguin FROM t_donneur WHERE id_donneur = %(value_id_donneur_selected)s"""

                    mc_afficher.execute(strsql_genres_afficher, valeur_id_genre_selected_dictionnaire)
                else:
                    strsql_genres_afficher = """SELECT id_donneur, prenom, nom, adresse, mail, num_tel, date_naissance, groupe_sanguin FROM t_donneur ORDER BY id_donneur DESC"""

                    mc_afficher.execute(strsql_genres_afficher)

                data_genres = mc_afficher.fetchall()

                print("data_genres ", data_genres, " Type : ", type(data_genres))

                # Différencier les messages si la table est vide.
                if not data_genres and id_donneur_sel == 0:
                    flash("""La table "t_donneur" est vide. !!""", "warning")
                elif not data_genres and id_donneur_sel > 0:
                    # Si l'utilisateur change l'id_donneur dans l'URL et que le genre n'existe pas,
                    flash(f"Le genre demandé n'existe pas !!", "warning")
                else:
                    # Dans tous les autres cas, c'est que la table "t_donneur" est vide.
                    # OM 2020.04.09 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                    flash(f"Données des donneurs affichés !!", "success")

        except Exception as Exception_genres_afficher:
            raise ExceptionGenresAfficher(f"fichier : {Path(__file__).name}  ;  "
                                          f"{genres_afficher.__name__} ; "
                                          f"{Exception_genres_afficher}")

    # Envoie la page "HTML" au serveur.
    return render_template("genres/genres_afficher.html", data=data_genres)


"""
    Auteur : OM 2021.03.22
    Définition d'une "route" /genres_ajouter
    
    Test : ex : http://127.0.0.1:5005/genres_ajouter
    
    Paramètres : sans
    
    But : Ajouter un genre pour un film
    
    Remarque :  Dans le champ "name_genre_html" du formulaire "genres/genres_ajouter.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@app.route("/genres_ajouter", methods=['GET', 'POST'])
def genres_ajouter_wtf():
    form = FormWTFAjouterDonneur()
    if request.method == "POST":
        try:
            if form.validate_on_submit():
                name_prenom_wtf = form.nom_prenom_wtf.data
                name_prenom = name_prenom_wtf

                name_nom_wtf = form.nom_nom_wtf.data
                name_nom = name_nom_wtf

                name_adresse_wtf = form.nom_adresse_wtf.data
                name_adresse = name_adresse_wtf

                name_mail_wtf = form.nom_mail_wtf.data
                name_mail = name_mail_wtf

                name_num_tel_wtf = form.nom_num_tel_wtf.data
                name_num_tel = name_num_tel_wtf

                name_date_naissance_wtf = form.nom_date_naissance_wtf.data
                name_date_naissance = name_date_naissance_wtf

                name_groupe_sanguin_wtf = form.nom_groupe_sanguin_wtf.data
                name_groupe_sanguin = name_groupe_sanguin_wtf



                valeurs_insertion_dictionnaire = {"value_name_prenom": name_prenom,
                                                  "value_name_nom": name_nom,
                                                  "value_name_adresse": name_adresse,
                                                  "value_name_mail": name_mail,
                                                  "value_name_num_tel": name_num_tel,
                                                  "value_name_date_naissance": name_date_naissance,
                                                  "value_name_groupe_sanguin": name_groupe_sanguin

                                                  }

                print("valeurs_insertion_dictionnaire ", valeurs_insertion_dictionnaire)

                strsql_insert_genre = """INSERT INTO t_donneur (id_donneur, prenom, nom, adresse, mail, num_tel, date_naissance, groupe_sanguin) VALUES (NULL,%(value_name_prenom)s,%(value_name_nom)s,%(value_name_adresse)s,%(value_name_mail)s,%(value_name_num_tel)s,%(value_name_date_naissance)s,%(value_name_groupe_sanguin)s )"""
                # strsql_insert_genre = """INSERT INTO t_donneur (id_donneur, prenom, nom, adresse, mail, num_tel, date_naissance) VALUES (NULL,%(value_name_prenom)s,%(value_name_nom)s,%(value_name_adresse)s,%(value_name_mail)s,%(value_name_num_tel)s,%(value_name_date_naissance)s )"""

                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_genre, valeurs_insertion_dictionnaire)

                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")

                # Pour afficher et constater l'insertion de la valeur, on affiche en ordre inverse. (DESC)
                return redirect(url_for('genres_afficher', order_by='DESC', id_donneur_sel=0))

        except Exception as Exception_genres_ajouter_wtf:
            raise ExceptionGenresAjouterWtf(f"fichier : {Path(__file__).name}  ;  "
                                          f"{genres_ajouter_wtf.__name__} ; "
                                          f"{Exception_genres_ajouter_wtf}")

    return render_template("genres/genres_ajouter_wtf.html", form=form)

"""
    Auteur : OM 2021.03.29
    Définition d'une "route" /genre_update
    
    Test : ex cliquer sur le menu "genres" puis cliquer sur le bouton "EDIT" d'un "genre"
    
    Paramètres : sans
    
    But : Editer(update) un genre qui a été sélectionné dans le formulaire "genres_afficher.html"
    
    Remarque :  Dans le champ "nom_genre_update_wtf" du formulaire "genres/genre_update_wtf.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@app.route("/genre_update", methods=['GET', 'POST'])
def genre_update_wtf():
    # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "id_donneur"
    id_donneur = request.values['id_donneur_btn_edit_html']

    # Objet formulaire pour l'UPDATE
    form_update = FormWTFUpdateDonneur()
    try:
        print(" on submit ", form_update.validate_on_submit())
        if form_update.validate_on_submit():
            # Récup la valeur du champ depuis "genre_update_wtf.html" après avoir cliqué sur "SUBMIT".
            # Puis la convertir en lettres minuscules.
            name_prenom_update = form_update.nom_prenom_update_wtf.data

            name_nom_update = form_update.nom_nom_update_wtf.data
            #
            name_adresse_update = form_update.nom_adresse_update_wtf.data
            #
            name_mail_update = form_update.nom_mail_update_wtf.data
            #
            name_num_tel_update = form_update.nom_num_tel_update_wtf.data
            #
            name_date_naissance_update = form_update.nom_date_naissance_update_wtf.data
            #
            name_groupe_sanguin_update = form_update.nom_groupe_sanguin_update_wtf.data




            valeur_update_dictionnaire = {"value_id_donneur": id_donneur,
                                          "value_name_prenom": name_prenom_update,
                                          "value_name_nom" : name_nom_update,
                                          "value_name_adresse": name_adresse_update,
                                          "value_name_mail" : name_mail_update,
                                          "value_name_num_tel": name_num_tel_update,
                                          "value_name_date_naissance": name_date_naissance_update,
                                          "value_name_groupe_sanguin": name_groupe_sanguin_update
                                          }
            print("valeur_update_dictionnaire ", valeur_update_dictionnaire)

            # str_sql_update_intitulegenre = """UPDATE t_donneur SET prenom, nom, adresse, mail, num_tel, date_naissance, groupe_sanguin = %(value_name_prenom)s WHERE id_donneur = %(value_id_donneur)s"""
            # str_sql_update_intitulegenre = """UPDATE t_donneur SET prenom = %(value_name_prenom)s, nom = %(value_name_nom)s, adresse = %(value_name_adresse)s, mail = %(value_name_mail)s, num_tel = %(value_name_num_tel)s, date_naissance = %(value_name_date_naissance)s, groupe_sanguin = %(value_name_groupe_sanguin)s WHERE id_donneur = %(value_id_donneur)s"""
            str_sql_update_intitulegenre = """UPDATE t_donneur SET prenom = %(value_name_prenom)s, nom = %(value_name_nom)s, adresse = %(value_name_adresse)s,  mail = %(value_name_mail)s, num_tel = %(value_name_num_tel)s, date_naissance = %(value_name_date_naissance)s, groupe_sanguin = %(value_name_groupe_sanguin)s WHERE id_donneur = %(value_id_donneur)s"""
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_intitulegenre, valeur_update_dictionnaire)

            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            # afficher et constater que la donnée est mise à jour.
            # Affiche seulement la valeur modifiée, "ASC" et l'"id_donneur"
            return redirect(url_for('genres_afficher', order_by="ASC", id_donneur_sel=0))
        elif request.method == "GET":
            # Opération sur la BD pour récupérer "id_donneur" et "intitule_genre" de la "t_donneur"
            # str_sql_id_genre = "SELECT id_donneur, prenom, nom, adresse, mail, num_tel, date_naissance, groupe_sanguin FROM t_donneur WHERE id_donneur = %(value_id_donneur)s"
            str_sql_id_genre = "SELECT id_donneur, prenom, nom, adresse, mail, num_tel, date_naissance, groupe_sanguin FROM t_donneur WHERE id_donneur = %(value_id_donneur)s"

            valeur_select_dictionnaire = {"value_id_donneur": id_donneur}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_genre, valeur_select_dictionnaire)
            # Une seule valeur est suffisante "fetchone()", vu qu'il n'y a qu'un seul champ "nom genre" pour l'UPDATE
            data_nom_prenom = mybd_conn.fetchone()
            print("data_nom_prenom ", data_nom_prenom, " type ", type(data_nom_prenom), " genre ",
                  data_nom_prenom["prenom"])

            # Afficher la valeur sélectionnée dans le champ du formulaire "genre_update_wtf.html"
            form_update.nom_prenom_update_wtf.data = data_nom_prenom["prenom"]
            form_update.nom_nom_update_wtf.data = data_nom_prenom["nom"]
            form_update.nom_adresse_update_wtf.data = data_nom_prenom["adresse"]
            form_update.nom_mail_update_wtf.data = data_nom_prenom["mail"]
            form_update.nom_num_tel_update_wtf.data = data_nom_prenom["num_tel"]
            form_update.nom_date_naissance_update_wtf.data = data_nom_prenom["date_naissance"]
            form_update.nom_groupe_sanguin_update_wtf.data = data_nom_prenom["groupe_sanguin"]


    except Exception as Exception_genre_update_wtf:
        raise ExceptionGenreUpdateWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{genre_update_wtf.__name__} ; "
                                      f"{Exception_genre_update_wtf}")

    return render_template("genres/genre_update_wtf.html", form_update=form_update)


"""
    Auteur : OM 2021.04.08
    Définition d'une "route" /genre_delete
    
    Test : ex. cliquer sur le menu "genres" puis cliquer sur le bouton "DELETE" d'un "genre"
    
    Paramètres : sans
    
    But : Effacer(delete) un genre qui a été sélectionné dans le formulaire "genres_afficher.html"
    
    Remarque :  Dans le champ "nom_genre_delete_wtf" du formulaire "genres/genre_delete_wtf.html",
                le contrôle de la saisie est désactivée. On doit simplement cliquer sur "DELETE"
"""


@app.route("/genre_delete", methods=['GET', 'POST'])
def genre_delete_wtf():
    data_films_attribue_genre_delete = None
    btn_submit_del = None
    # L'utilisateur vient de cliquer sur le bouton "DELETE". Récupère la valeur de "id_donneur"
    id_donneur_delete = request.values['id_donneur_btn_delete_html']

    # Objet formulaire pour effacer le genre sélectionné.
    form_delete = FormWTFDeleteDonneur()
    try:
        print(" on submit ", form_delete.validate_on_submit())
        if request.method == "POST" and form_delete.validate_on_submit():

            if form_delete.submit_btn_annuler.data:
                return redirect(url_for("genres_afficher", order_by="ASC", id_genre_sel=0))

            if form_delete.submit_btn_conf_del.data:
                # Récupère les données afin d'afficher à nouveau
                # le formulaire "genres/genre_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                data_films_attribue_genre_delete = session['data_films_attribue_genre_delete']
                print("data_films_attribue_genre_delete ", data_films_attribue_genre_delete)

                flash(f"Effacer le genre de façon définitive de la BD !!!", "danger")
                # L'utilisateur vient de cliquer sur le bouton de confirmation pour effacer...
                # On affiche le bouton "Effacer genre" qui va irrémédiablement EFFACER le genre
                btn_submit_del = True

            if form_delete.submit_btn_del.data:
                valeur_delete_dictionnaire = {"value_id_donneur": id_donneur_delete}
                print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)


                str_sql_delete_idgenre = """DELETE FROM t_donneur WHERE id_donneur = %(value_id_donneur)s"""
                # Manière brutale d'effacer d'abord la "fk_genre", même si elle n'existe pas dans la "t_genre_film"
                # Ensuite on peut effacer le genre vu qu'il n'est plus "lié" (INNODB) dans la "t_genre_film"
                with DBconnection() as mconn_bd:

                    mconn_bd.execute(str_sql_delete_idgenre, valeur_delete_dictionnaire)

                flash(f"Genre définitivement effacé !!", "success")
                print(f"Genre définitivement effacé !!")

                # afficher les données
                return redirect(url_for('genres_afficher', order_by="ASC", id_genre_sel=0))

        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_donneur": id_donneur_delete}
            print(id_donneur_delete, type(id_donneur_delete))

            # Requête qui affiche tous les films_genres qui ont le genre que l'utilisateur veut effacer
            str_sql_genres_films_delete = """SELECT id_donneur, prenom, nom, adresse, mail, num_tel, date_naissance, groupe_sanguin FROM t_donneur WHERE id_donneur = %(value_id_donneur)s"""

            with DBconnection() as mydb_conn:
                mydb_conn.execute(str_sql_genres_films_delete, valeur_select_dictionnaire)
                data_films_attribue_genre_delete = mydb_conn.fetchall()
                print("data_films_attribue_genre_delete...", data_films_attribue_genre_delete)

                # Nécessaire pour mémoriser les données afin d'afficher à nouveau
                # le formulaire "genres/genre_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                session['data_films_attribue_genre_delete'] = data_films_attribue_genre_delete

                # Opération sur la BD pour récupérer "id_donneur" et "intitule_genre" de la "t_donneur"
                str_sql_id_genre = "SELECT id_donneur, prenom, nom, adresse, mail, num_tel, date_naissance, groupe_sanguin FROM t_donneur WHERE id_donneur = %(value_id_donneur)s"

                mydb_conn.execute(str_sql_id_genre, valeur_select_dictionnaire)
                # Une seule valeur est suffisante "fetchone()",
                # vu qu'il n'y a qu'un seul champ "nom genre" pour l'action DELETE
                data_nom_donneur = mydb_conn.fetchone()
                print("data_nom_donneur ", data_nom_donneur, " type ", type(data_nom_donneur), "prenom",
                      data_nom_donneur["prenom"])

            # Afficher la valeur sélectionnée dans le champ du formulaire "genre_delete_wtf.html"
            form_delete.nom_prenom_delete_wtf.data = data_nom_donneur["prenom"]
            form_delete.nom_nom_delete_wtf.data = data_nom_donneur["prenom"]
            form_delete.nom_adresse_delete_wtf.data = data_nom_donneur["prenom"]
            form_delete.nom_mail_delete_wtf.data = data_nom_donneur["prenom"]
            form_delete.nom_num_tel_delete_wtf.data = data_nom_donneur["prenom"]
            form_delete.nom_date_naissance_delete_wtf.data = data_nom_donneur["prenom"]
            form_delete.nom_groupe_sanguin_delete_wtf.data = data_nom_donneur["prenom"]
            # form_delete.nom_prenom_delete_wtf.data = data_nom_donneur["Prénom"]
            # form_delete.nom_nom_delete_wtf.data = data_nom_donneur["Nom"]
            # form_delete.nom_adresse_delete_wtf.data = data_nom_donneur["Adresse"]
            # form_delete.nom_mail_delete_wtf.data = data_nom_donneur["Mail"]
            # form_delete.nom_num_tel_delete_wtf.data = data_nom_donneur["Numéro de Téléphone"]
            # form_delete.nom_date_naissance_delete_wtf.data = data_nom_donneur["Date de Naissance"]
            # form_delete.nom_groupe_sanguin_delete_wtf.data = data_nom_donneur["Groupe Sanguin"]


            # Le bouton pour l'action "DELETE" dans le form. "genre_delete_wtf.html" est caché.
            btn_submit_del = False

    except Exception as Exception_genre_delete_wtf:
        raise ExceptionGenreDeleteWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{genre_delete_wtf.__name__} ; "
                                      f"{Exception_genre_delete_wtf}")

    return render_template("genres/genre_delete_wtf.html",
                           form_delete=form_delete,
                           btn_submit_del=btn_submit_del,
                           data_films_associes=data_films_attribue_genre_delete)
