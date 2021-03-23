# -*- coding: utf-8 -*-

import os
import json
import sqlite3
import textwrap

CUR_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(CUR_DIR, "data")
PATH_FILE = os.path.join(DATA_DIR, "db_path_viewer.json")

with open(PATH_FILE, "r", encoding='utf8') as f :
    raw_path = json.load(f)
f.close()
path = raw_path["path"]

def get_db_path():
    global path
    with open(PATH_FILE, "r", encoding='utf8') as f :
        raw_path = json.load(f)
    f.close()
    path = raw_path["path"]

## LECTURE DE LA TABLE STOCK :

def _get_all_stock_values() : # Récupere la table "Stock" intégralement
    try :
        conn = sqlite3.connect(path)
        c = conn.cursor()
        sql = "SELECT * FROM Stock"
        c.execute(sql)
        all_stock_values = c.fetchall()
        conn.close()
        return all_stock_values
    except sqlite3.OperationalError :
        pass

def get_stock_item_names() : # Récupere les Item Names de "Stock"
    try :
        stock_item_names = []
        all_stock_values = _get_all_stock_values()
        for value in all_stock_values :
            stock_item_names.append(value[0])
        return stock_item_names
    except TypeError :
        pass

def get_stock_stockCount() : # Récupere les Stock Counts de "Stock"
    try :
        stock_stockCount = []
        all_stock_values = _get_all_stock_values()
        for value in all_stock_values :
            stock_stockCount.append(value[1])
        return stock_stockCount
    except TypeError :
        pass

def get_one_stock_stockCount(name) : # Récupere le Stock Count d'un Item de "Stock"
    try :
        item_row = get_item_row(name)
        item_stockCount = item_row[0][1]
        return item_stockCount
    except TypeError :
        pass

def get_one_stock_atelCount(name) : # Récupere le Atel Count d'un Item de "Stock"
    try :
        item_row = get_item_row(name)
        item_atelCount = item_row[0][3]
        return item_atelCount
    except TypeError :
        pass

def get_stock_pretsCount() : # Récupere les Prets Counts de "Stock"
    try :
        stock_pretsCount = []
        all_stock_values = _get_all_stock_values()
        for value in all_stock_values :
            stock_pretsCount.append(value[2])
        return stock_pretsCount
    except TypeError :
        pass

def get_stock_atelCount() : # Récupere les Atelier Counts de "Stock"
    try :
        stock_atelCount = []
        all_stock_values = _get_all_stock_values()
        for value in all_stock_values :
            stock_atelCount.append(value[3])
        return stock_atelCount
    except TypeError :
        pass

def get_item_row(name) : # Récupere la ligne de la table "Stock" correspondante à "name"
    try :    
        conn = sqlite3.connect(path)
        c = conn.cursor()
        sql = """SELECT * FROM Stock WHERE Item = ("%s")""" %(name)
        c.execute(sql)
        item_row = c.fetchall()
        conn.close()
        return item_row
    except sqlite3.OperationalError :
        pass

def get_nonull_atelCount_items() : # Récupere la liste des Items de "Stock" dont AtelCount est non-nul
    try :    
        conn = sqlite3.connect(path)
        c = conn.cursor()
        sql = """SELECT * FROM Stock WHERE AtelCount != 0"""
        c.execute(sql)
        nonull_atel_items = c.fetchall()
        conn.close()
        return nonull_atel_items
    except sqlite3.OperationalError :
        pass

## LECTURE DE LA TABLE STOCK TECHNIQUE :

def _get_all_tech_stock_values() : # Récupere la table "Tech_Stock" intégralement
    try :    
        conn = sqlite3.connect(path)
        c = conn.cursor()
        sql = "SELECT * FROM Tech_Stock"
        c.execute(sql)
        all_tech_stock_values = c.fetchall()
        conn.close()
        return all_tech_stock_values
    except sqlite3.OperationalError :
        pass

def get_tech_stock_item_names() : # Récupere les Item Names de "Tech_Stock"
    try :
        tech_stock_item_names = []
        all_tech_stock_values = _get_all_tech_stock_values()
        for value in all_tech_stock_values :
            tech_stock_item_names.append(value[0])
        return tech_stock_item_names
    except TypeError :
        pass

def get_tech_stock_stockCount() : # Récupere les Stock Counts de "Tech_Stock"
    try :
        tech_stock_stockCount = []
        all_tech_stock_values = _get_all_tech_stock_values()
        for value in all_tech_stock_values :
            tech_stock_stockCount.append(value[1])
        return tech_stock_stockCount
    except TypeError :
        pass

def get_one_tech_stock_stockCount(name) : # Récupere le Stock Count d'un Item de "Tech_Stock"
    try :
        tech_item_row = get_tech_item_row(name)
        tech_item_stockCount = tech_item_row[0][1]
        return tech_item_stockCount
    except TypeError :
        pass

def get_tech_stock_pretsCount() : # Récupere les Prets Counts de "Tech_Stock"
    try :
        tech_stock_pretsCount = []
        all_tech_stock_values = _get_all_tech_stock_values()
        for value in all_tech_stock_values :
            tech_stock_pretsCount.append(value[2])
        return tech_stock_pretsCount
    except TypeError :
        pass

def get_tech_stock_atelCount() : # Récupere les Atelier Counts de "Tech_Stock"
    try :
        tech_stock_atelCount = []
        all_tech_stock_values = _get_all_tech_stock_values()
        for value in all_tech_stock_values :
            tech_stock_atelCount.append(value[3])
        return tech_stock_atelCount
    except TypeError :
        pass

def get_one_tech_stock_atelCount(name) : # Récupere le Atel Count d'un Item de "Tech_Stock"
    try :
        tech_item_row = get_tech_item_row(name)
        tech_item_atelCount = tech_item_row[0][3]
        return tech_item_atelCount
    except TypeError :
        pass

def get_tech_item_row(name) : # Récupere la ligne de la table "Tech_Stock" correspondante à "name"
    try :    
        conn = sqlite3.connect(path)
        c = conn.cursor()
        sql = """SELECT * FROM Tech_Stock WHERE Item = ("%s")""" %(name)
        c.execute(sql)
        tech_item_row = c.fetchall()
        conn.close()
        return tech_item_row
    except sqlite3.OperationalError :
        pass

def get_nonull_tech_atelCount_items() : # Récupere la liste des Items de "Stock" dont AtelCount est non-nul
    try :
        conn = sqlite3.connect(path)
        c = conn.cursor()
        sql = """SELECT * FROM Tech_Stock WHERE AtelCount != 0"""
        c.execute(sql)
        nonull_tech_atel_items = c.fetchall()
        conn.close()
        return nonull_tech_atel_items
    except sqlite3.OperationalError :
        pass

## LECTURE DE LA TABLE PRETS :

def _get_all_prets_values() : # Récupere la table "Prets" intégralement
    try :    
        conn = sqlite3.connect(path)
        c = conn.cursor()
        sql = "SELECT * FROM Prets"
        c.execute(sql)
        all_prets_values = c.fetchall()
        conn.close()
        return all_prets_values
    except sqlite3.OperationalError :
        pass

def get_prets_localisations() : # Récupere les Localisations de "Prets"
    try :
        prets_localisations = []
        all_prets_values = _get_all_prets_values()
        for value in all_prets_values :
            prets_localisations.append(value[0])
        return prets_localisations
    except TypeError :
        pass

def get_prets_types() : # Récupere les Types de "Prets"
    try :
        prets_types = []
        all_prets_values = _get_all_prets_values()
        for value in all_prets_values :
            prets_types.append(value[1])
        return prets_types
    except TypeError :
        pass

def get_prets_row(localisation) : # Récupere la ligne de la table "Prets" correspondante à "localisation"
    try :    
        conn = sqlite3.connect(path)
        c = conn.cursor()
        sql = """SELECT * FROM Prets WHERE Localisation = ("%s")""" %(localisation)
        c.execute(sql)
        prets_row = c.fetchall()
        conn.close()
        return prets_row
    except sqlite3.OperationalError :
        pass

def get_one_prets_type(localisation) :  # Récupere le Type d'une Localisation de "Prets"
    try :
        prets_row = get_prets_row(localisation)
        prets_type = prets_row[0][1]
        return prets_type
    except TypeError :
        pass

def get_prets_lists() : # Récupere les Listes de "Prets"
    try :
        prets_lists = []
        all_prets_values = _get_all_prets_values()
        for value in all_prets_values :
            prets_lists.append(value[2])
        return prets_lists
    except TypeError :
        pass

def get_one_prets_list(localisation) :  # Récupere la Liste d'une Localisation de "Prets"
    try :
        prets_row = get_prets_row(localisation)
        prets_list = prets_row[0][2]
        return prets_list
    except TypeError :
        pass

## MODIFICATIONS DE LA TABLE PRETS DE MATERIEL :

def update_pret_list(localisation, item_list) : # Modification de ItemList de Row de "Prets"
    try :
        sql = """UPDATE Prets SET ItemLists = ("%s") WHERE Localisation = ("%s")""" %(item_list, localisation)
        conn = sqlite3.connect(path)
        c = conn.cursor()
        c.execute(sql)
        conn.commit()
        conn.close()
    except sqlite3.OperationalError :
        pass

def empty_total_prets() : # RAZ du total des prets pour nouveau calcul
    try :
        item_names = get_stock_item_names()
        item_tech_names = get_tech_stock_item_names()
        for name in item_names :
            conn = sqlite3.connect(path)
            sql = """UPDATE Stock SET PretsCount = ("%s") WHERE Item = ("%s")""" %(0, name)
            c = conn.cursor()
            c.execute(sql)
            conn.commit()
            conn.close()

        for name in item_tech_names :
            conn = sqlite3.connect(path)
            sql = """UPDATE Tech_Stock SET PretsCount = ("%s") WHERE Item = ("%s")""" %(0, name)
            c = conn.cursor()
            c.execute(sql)
            conn.commit()
            conn.close()
    except sqlite3.OperationalError :
        pass
    except TypeError :
        pass

def calculate_total_prets() : # Calcule de la quantité totale de chaque Item prété
    try :    
        empty_total_prets()
        set_to_none()

        stock_items = get_stock_item_names()
        tech_stock_items = get_tech_stock_item_names()

        total_lists = get_prets_lists()
        total_lists_unformated = []
        total_list_separated = []
        items_list = []

        for liste in total_lists :
            if liste != None :
                total_lists_unformated.append(liste)

        for liste in total_lists_unformated :
            total_list_separated.append(liste.split("\n"))

        for i in range(len(total_list_separated)) :
            for item in total_list_separated[i] :
                items_list.append(item)

        for item in items_list :
            item_name = (item.split(" : ")[0])
            item_qty = (item.split(" : ")[1])

            if item_name in stock_items :
                conn = sqlite3.connect(path)
                c = conn.cursor()
                sql = """SELECT * FROM Stock WHERE Item = ("%s")""" %(item_name)
                c.execute(sql)
                item_data = c.fetchall()
                item_old_qty = item_data[0][2]

                item_qty = int(item_qty) + int(item_old_qty)
                sql = """UPDATE Stock SET PretsCount = ("%s") WHERE Item = ("%s")""" %(item_qty, item_name)
                c = conn.cursor()
                c.execute(sql)
                conn.commit()
                conn.close()

            elif item_name in tech_stock_items :
                conn = sqlite3.connect(path)
                c = conn.cursor()
                sql = """SELECT * FROM Tech_Stock WHERE Item = ("%s")""" %(item_name)
                c.execute(sql)
                item_data = c.fetchall()
                item_old_qty = item_data[0][2]

                item_qty = int(item_qty) + int(item_old_qty)
                sql = """UPDATE Tech_Stock SET PretsCount = ("%s") WHERE Item = ("%s")""" %(item_qty, item_name)
                c = conn.cursor()
                c.execute(sql)
                conn.commit()
                conn.close()
    except sqlite3.OperationalError :
        pass
    except TypeError :
        pass

def set_to_none() : # Transforme une liste vide en élément nul
    try :
        conn = sqlite3.connect(path)
        sql = """UPDATE Prets SET ItemLists = NULL WHERE ItemLists = ("%s")""" %("")
        c = conn.cursor()
        c.execute(sql)
        conn.commit()
        conn.close()
    except sqlite3.OperationalError :
        pass
