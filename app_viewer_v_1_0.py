# coding: utf-8

import os
import sys
import json
import sqlite3

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QDesktopWidget, QMessageBox
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from api_mat_v_2 import get_db_path
from api_mat_v_2 import get_stock_item_names, get_tech_stock_item_names
from api_mat_v_2 import get_one_stock_stockCount, get_one_tech_stock_stockCount
from api_mat_v_2 import get_one_stock_atelCount, get_one_tech_stock_atelCount
from api_mat_v_2 import get_nonull_atelCount_items, get_nonull_tech_atelCount_items
from api_mat_v_2 import get_prets_localisations, get_one_prets_type, get_one_prets_list, calculate_total_prets

CUR_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(CUR_DIR, "data")
ICON_FILE = os.path.join(DATA_DIR, "icone.png")
PATH_FILE = os.path.join(DATA_DIR, "db_path_viewer.json")

class App(QtWidgets.QTabWidget):
    def __init__(self, parent = None): # Initialisation de la fenêtre et des fonctions de départ
        super(App, self).__init__(parent)
        self.setWindowTitle("MATOSAURUS VIEWER  |  v.1.0 - Alpha")
        self.setStyleSheet("background-color: rgb(200, 200, 255)")
        self.setWindowIcon(QtGui.QIcon(ICON_FILE))

        self.tab_stock = QtWidgets.QWidget()
        self.tab_tech_stock = QtWidgets.QWidget()
        self.tab_pret = QtWidgets.QWidget()
        self.tab_atel = QtWidgets.QWidget()

        self.addTab(self.tab_stock," STOCK ")
        self.addTab(self.tab_tech_stock," STOCK TECHNIQUE ")
        self.addTab(self.tab_pret," PRETS DE MATERIEL ")
        self.addTab(self.tab_atel," ATELIER ")
        
        self.tabStockUI()
        self.tabTechStockUI()
        self.tabPretUI()
        self.tabAtelUI()
        self.setup_connections()
        self.setup_default()

        calculate_total_prets()

        self.populate_stock_lw()
        
        self.populate_tech_stock_lw()
        
        self.populate_prets_localisations_lw()
        
        self.populate_atel_ref_qty_lw()
        self.populate_atel_search_cbb()

    def tabStockUI(self): # Génération du Tab "STOCK"
        self.grid_layout = QtWidgets.QGridLayout(self)

        self.lw_stock_ref = QtWidgets.QListWidget()
        self.lw_stock_count = QtWidgets.QListWidget()
        self.lbl_stock_ref = QtWidgets.QLabel(" 🏷  REFERENCES")
        self.lbl_stock_qty = QtWidgets.QLabel(" 🧮  QUANTITES")
        self.btn_update_1 = QtWidgets.QPushButton("ACTUALISER")

        self.grid_layout.addWidget(self.lw_stock_ref, 1, 0, 8, 8)
        self.grid_layout.addWidget(self.lw_stock_count, 1, 8, 8, 2)
        self.grid_layout.addWidget(self.lbl_stock_ref, 0, 0, 1, 8)
        self.grid_layout.addWidget(self.lbl_stock_qty, 0, 8, 1, 1)
        self.grid_layout.addWidget(self.btn_update_1, 0, 9, 1, 1)

        self.lw_stock_ref.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.lw_stock_count.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.btn_update_1.setStyleSheet("background-color: rgb(200, 100, 100)")
        self.lw_stock_ref.setAlternatingRowColors(True)
        self.lw_stock_count.setAlternatingRowColors(True)

        ## Affichage du Tab

        self.setTabText(0," STOCK ")
        self.tab_stock.setLayout(self.grid_layout)

        self.sliderBarS1 = self.lw_stock_ref.verticalScrollBar()
        self.sliderBarS2 = self.lw_stock_count.verticalScrollBar()

        self.sliderBarS1.valueChanged.connect(self.move_stock_scrollbar)
        self.sliderBarS2.valueChanged.connect(self.move_stock_scrollbar)

    def move_stock_scrollbar(self, value): # Synchronisation des SliderBars des ListWidgets du Tab "Stock"
        self.sliderBarS1.setValue(value)
        self.sliderBarS2.setValue(value)

    def tabTechStockUI(self): # Génération du Tab "STOCK TECHNIQUE"
        self.grid_layout = QtWidgets.QGridLayout(self)

        self.lw_Tstock_ref = QtWidgets.QListWidget()
        self.lw_Tstock_count = QtWidgets.QListWidget()
        self.lbl_Tstock_ref = QtWidgets.QLabel(" 🏷  REFERENCES")
        self.lbl_Tstock_qty = QtWidgets.QLabel(" 🧮  QUANTITES")
        self.btn_update_2 = QtWidgets.QPushButton("ACTUALISER")

        self.grid_layout.addWidget(self.lw_Tstock_ref, 1, 0, 8, 8)
        self.grid_layout.addWidget(self.lw_Tstock_count, 1, 8, 8, 2)
        self.grid_layout.addWidget(self.lbl_Tstock_ref, 0, 0, 1, 8)
        self.grid_layout.addWidget(self.lbl_Tstock_qty, 0, 8, 1, 1)
        self.grid_layout.addWidget(self.btn_update_2, 0, 9, 1, 1)

        self.lw_Tstock_ref.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.lw_Tstock_count.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.btn_update_2.setStyleSheet("background-color: rgb(200, 100, 100)")
        self.lw_Tstock_ref.setAlternatingRowColors(True)
        self.lw_Tstock_count.setAlternatingRowColors(True)

        ## Affichage du Tab

        self.setTabText(1," STOCK TECHNIQUE ")
        self.tab_tech_stock.setLayout(self.grid_layout)

        self.sliderBarT1 = self.lw_Tstock_ref.verticalScrollBar()
        self.sliderBarT2 = self.lw_Tstock_count.verticalScrollBar()

        self.sliderBarT1.valueChanged.connect(self.move_Tstock_scrollbar)
        self.sliderBarT2.valueChanged.connect(self.move_Tstock_scrollbar)

    def move_Tstock_scrollbar(self, value): # Synchronisation des SliderBars des ListWidgets du Tab "Stock Technique"
        self.sliderBarT1.setValue(value)
        self.sliderBarT2.setValue(value)

    def tabPretUI(self): # Génération du Tab "PRETS DE MATERIEL"
        self.grid_layout = QtWidgets.QGridLayout(self)

        self.lbl_prets_local = QtWidgets.QLabel(" 📥  LOCALISATIONS")
        self.lbl_prets_matos = QtWidgets.QLabel(" 📋  MATERIEL")
        self.lbl_prets_legend = QtWidgets.QLabel("🟨 Prêts récurents - 🟩 Salles - 🟦 Assos & particuliers")
        self.lw_prets_local = QtWidgets.QListWidget()
        self.lw_prets_matos = QtWidgets.QListWidget()
        self.btn_update_3 = QtWidgets.QPushButton("ACTUALISER")

        self.grid_layout.addWidget(self.lbl_prets_local, 0, 0, 1, 8)
        self.grid_layout.addWidget(self.lbl_prets_matos, 0, 8, 1, 1)
        self.grid_layout.addWidget(self.btn_update_3, 0, 9, 1, 1)
        self.grid_layout.addWidget(self.lbl_prets_legend, 9, 0, 1, 8)
        self.grid_layout.addWidget(self.lw_prets_local, 1, 0, 8, 8)
        self.grid_layout.addWidget(self.lw_prets_matos, 1, 8, 8, 2)

        self.lw_prets_local.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.lw_prets_matos.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.btn_update_3.setStyleSheet("background-color: rgb(200, 100, 100)")
        self.lw_prets_matos.setAlternatingRowColors(True)

        for i in range(9) :
            self.grid_layout.setRowStretch(i, 4)
        self.grid_layout.setRowStretch(0, 1)
        self.grid_layout.setRowStretch(9, 1)

        ## Affichage du Tab

        self.setTabText(2," PRETS DE MATERIEL ")
        self.tab_pret.setLayout(self.grid_layout)

    def tabAtelUI(self): # Génération du Tab "ATELIER"
        self.grid_layout = QtWidgets.QGridLayout(self)

        self.lbl_atel_ref = QtWidgets.QLabel(" 🏷  REFERENCES")
        self.lbl_atel_qty = QtWidgets.QLabel(" 🧮  QUANTITES")
        self.lbl_atel_search = QtWidgets.QLabel(" 🔍  Rechercher une Réference")
        self.btn_update_4 = QtWidgets.QPushButton("ACTUALISER")
        self.lw_atel_ref = QtWidgets.QListWidget()
        self.lw_atel_qty = QtWidgets.QListWidget()
        self.lw_atel_search = QtWidgets.QListWidget()
        self.cbb_atel_ref = QtWidgets.QComboBox()
        self.btn_database = QtWidgets.QPushButton("BASE DE DONNEES")

        self.grid_layout.addWidget(self.lbl_atel_ref, 0, 0, 1, 5)
        self.grid_layout.addWidget(self.lbl_atel_qty, 0, 5, 1, 1)
        self.grid_layout.addWidget(self.lbl_atel_search, 0, 6, 1, 4)
        self.grid_layout.addWidget(self.btn_update_4, 0, 9, 1, 2)
        self.grid_layout.addWidget(self.lw_atel_ref, 1, 0, 9, 5)
        self.grid_layout.addWidget(self.lw_atel_qty, 1, 5, 9, 1)
        self.grid_layout.addWidget(self.lw_atel_search, 2, 6, 8, 5)
        self.grid_layout.addWidget(self.cbb_atel_ref, 1, 6, 1, 3)
        self.grid_layout.addWidget(self.btn_database, 1, 9, 1, 2)

        for i in range(10) :
            self.grid_layout.setRowStretch(i, 4)
        self.grid_layout.setRowStretch(0, 1)
        self.grid_layout.setRowStretch(9, 1)
        for i in range(11) :
            self.grid_layout.setColumnStretch(i, 2)
        self.grid_layout.setColumnStretch(5, 1)

        self.lw_atel_ref.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.lw_atel_qty.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.lw_atel_search.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.cbb_atel_ref.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.btn_update_4.setStyleSheet("background-color: rgb(200, 100, 100)")
        self.btn_database.setStyleSheet("background-color: rgb(255, 255, 150)")
        self.lw_atel_ref.setAlternatingRowColors(True)
        self.lw_atel_qty.setAlternatingRowColors(True)
        self.lw_atel_search.setAlternatingRowColors(True)

        ## Affichage du Tab

        self.setTabText(3," ATELIER ")
        self.tab_atel.setLayout(self.grid_layout)

        self.sliderBarA1 = self.lw_atel_ref.verticalScrollBar()
        self.sliderBarA2 = self.lw_atel_qty.verticalScrollBar()

        self.sliderBarA1.valueChanged.connect(self.move_atel_scrollbar)
        self.sliderBarA2.valueChanged.connect(self.move_atel_scrollbar)

    def move_atel_scrollbar(self, value): # Synchronisation des SliderBars des ListWidgets du Tab "Atelier"
        self.sliderBarA1.setValue(value)
        self.sliderBarA2.setValue(value)

    def setup_connections(self): # Initialisation des connections Widgets - Fonctions
        self.lw_prets_local.itemClicked.connect(self.populate_prets_lists_lw)
        self.cbb_atel_ref.activated.connect(self.populate_atel_search_lw)
        self.btn_database.clicked.connect(self.get_database)

        self.btn_update_1.clicked.connect(self.update_app)
        self.btn_update_2.clicked.connect(self.update_app)
        self.btn_update_3.clicked.connect(self.update_app)
        self.btn_update_4.clicked.connect(self.update_app)

    def setup_default(self): # Définition des valeurs de Widget par défaut
        pass

### "STOCK" TAB METHODS ###############################################################

    def populate_stock_lw(self): # Peuplement des ListWidgets du Tab "Stock"
        try :
            self.lw_stock_ref.clear()
            self.lw_stock_count.clear()

            stock_item_names = get_stock_item_names()
            for item_name in sorted(stock_item_names) :
                self.lw_stock_ref.addItem(item_name)
                item_stockCount = get_one_stock_stockCount(item_name)
                self.lw_stock_count.addItem(str(item_stockCount))
        except TypeError :
            pass

### "STOCK TECHNIQUE" TAB METHODS #####################################################

    def populate_tech_stock_lw(self): # Peuplement des ListWidgets du Tab "Stock Technique"
        try :    
            self.lw_Tstock_ref.clear()
            self.lw_Tstock_count.clear()

            tech_stock_item_names = get_tech_stock_item_names()
            for item_name in sorted(tech_stock_item_names) :
                self.lw_Tstock_ref.addItem(item_name)
                tech_item_stockCount = get_one_tech_stock_stockCount(item_name)
                self.lw_Tstock_count.addItem(str(tech_item_stockCount))
        except TypeError :
            pass

### "PRETS DE MATERIEL" TAB METHODS ###################################################

    def populate_prets_localisations_lw(self): # Peuplement du ListWidget de Localisations du Tab "Prets de Matériel"
        try :
            self.lw_prets_local.clear()
            prets_localisations = get_prets_localisations()

            for localisation in sorted(prets_localisations) :
                localisation_type = get_one_prets_type(localisation)

                if localisation_type == 1 :
                    localisation = """🟡 %s""" %(localisation)
                    item = QtWidgets.QListWidgetItem(localisation)
                    self.lw_prets_local.addItem(item)

            for localisation in sorted(prets_localisations) :
                localisation_type = get_one_prets_type(localisation)

                if localisation_type == 2 :
                    localisation = """🟢 %s""" %(localisation)
                    item = QtWidgets.QListWidgetItem(localisation)
                    self.lw_prets_local.addItem(item)

            for localisation in sorted(prets_localisations) :
                localisation_type = get_one_prets_type(localisation)

                if localisation_type == 3 :
                    localisation = """🟣 %s""" %(localisation)
                    item = QtWidgets.QListWidgetItem(localisation)
                    self.lw_prets_local.addItem(item)
        except TypeError :
            pass

    def populate_prets_lists_lw(self): # Peuplement du ListWidget de Listes du Tab "Prets de Matériel"
        try :    
            self.lw_prets_matos.clear()

            if not self.lw_prets_local.selectedItems() :
                return False

            for selected_name in self.lw_prets_local.selectedItems() :
                selected_local_name = selected_name.text()

            if selected_local_name.startswith("🟡") :
                selected_localisation = selected_local_name.lstrip("🟡 ")
            if selected_local_name.startswith("🟢") :
                selected_localisation = selected_local_name.lstrip("🟢 ")
            if selected_local_name.startswith("🟣") :
                selected_localisation = selected_local_name.lstrip("🟣 ")

            local_total_list = get_one_prets_list(selected_localisation)
            if local_total_list == None :
                return False
            else :
                local_list = local_total_list.split("\n")

                for item in local_list :
                    self.lw_prets_matos.addItem(item)
        except TypeError :
            pass

### "ATELIER" TAB METHODS #############################################################

    def populate_atel_ref_qty_lw(self): # Peuplement des ListWidgets "Références" et "Quantité" du Tab "Atelier"
        try :
            self.lw_atel_ref.clear()
            self.lw_atel_qty.clear()

            atel_stock_item_names = get_stock_item_names()
            for item_name in sorted(atel_stock_item_names) :
                self.lw_atel_ref.addItem(item_name)
                item_atelCount = get_one_stock_atelCount(item_name)
                self.lw_atel_qty.addItem(str(item_atelCount))

            atel_tech_stock_item_names = get_tech_stock_item_names()
            for item_name in sorted(atel_tech_stock_item_names) :
                self.lw_atel_ref.addItem(item_name)
                item_atelCount = get_one_tech_stock_atelCount(item_name)
                self.lw_atel_qty.addItem(str(item_atelCount))
        except TypeError :
            pass

    def populate_atel_search_cbb(self): # Peuplement du ComboBox "Recherche" du Tab "Atelier"
        try :
            self.cbb_atel_ref.clear()
            atel_search_items = [""]

            stock_item_names = get_stock_item_names()
            for item_name in sorted(stock_item_names) :
                atel_search_items.append(item_name)

            tech_stock_item_names = get_tech_stock_item_names()
            for item_name in sorted(tech_stock_item_names) :
                atel_search_items.append(item_name)

            self.cbb_atel_ref.addItems(atel_search_items)
        except TypeError :
            pass

    def populate_atel_search_lw(self): # Peuplement du ListWidget de Recherche d'items du Tab "Atelier"
        try :
            self.lw_atel_search.clear()
            item_searched = self.cbb_atel_ref.currentText()
            item_list = []

            if item_searched == "" :
                return False

            # Récupération des items de l'Atelier

            stock_items = get_stock_item_names()
            tech_stock_items = get_tech_stock_item_names()

            for item in stock_items :
                if item == item_searched :
                    atel_count = get_one_stock_atelCount(item_searched)
                    if atel_count != 0 :
                        atel_formated_count = f"Atelier : {int(atel_count)}"
                        item_list.append(atel_formated_count)
                    elif atel_count == 0 :
                        pass

            for item in tech_stock_items :
                if item == item_searched :
                    atel_tech_count = get_one_tech_stock_atelCount(item_searched)
                    if atel_tech_count != 0 :
                        atel_formated_count = f"Atelier : {int(atel_tech_count)}"
                        item_list.append(atel_formated_count)
                    elif atel_tech_count == 0 :
                        pass

            # Récupération des items dans Prets

            prets_localisations = get_prets_localisations()
            for pret_localisation in prets_localisations :
                pret_list_unformated = get_one_prets_list(pret_localisation)

                if pret_list_unformated != None :
                    pret_list = pret_list_unformated.split("\n")

                    for pret_item in pret_list :
                        if pret_item.split(" : ")[0] == item_searched :
                            item_qty = pret_item.split(" : ")[1]
                            pret_formated_count = """%s : %s""" %(pret_localisation, item_qty)
                            item_list.append(pret_formated_count)

            # Ecriture du ListWidget de Recherche d'Item

            if item_list == [] :
                empty_item = "Cet élément n'est pas en stock"
                self.lw_atel_search.addItem(empty_item)
            else :
                for item in item_list :
                    self.lw_atel_search.addItem(item)
        except TypeError :
            pass

    def get_database(self): # Pop Up de recherche du chemin vers la base de données partagée.
        raw_path = QtWidgets.QFileDialog.getOpenFileName(self, "Choisir la base de données partagée", "*.db")
        path = {"path" : raw_path[0]}
        with open(PATH_FILE, 'w', encoding='utf8') as f :
            json.dump(path, f)
        f.close()

### GENERAL METHODS ###################################################################

    def update_app(self): # BTN - Actualiser - Mise à jour des Widgets
        get_db_path()
        self.populate_stock_lw()
        self.populate_tech_stock_lw()
        self.populate_prets_localisations_lw()
        self.populate_atel_ref_qty_lw()
        self.populate_atel_search_cbb()

### END OF App CLASS ##################################################################

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())


