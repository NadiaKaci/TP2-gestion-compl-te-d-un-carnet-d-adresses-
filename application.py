import sys
import sqlite3
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QTableWidget, QTableWidgetItem, QHBoxLayout

# ==========================
# FONCTIONS BASE DE DONNÉES
# ==========================

def connect_db():
    """Ouvre ou crée la base SQLite carnet.db"""
    return sqlite3.connect("carnet.db")

def create_table():
    """Crée la table 'contacts' si elle n'existe pas"""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT,
            prenom TEXT,
            telephone TEXT,
            email TEXT
        )
    """)
    conn.commit()
    conn.close()

def get_contacts():
    """Retourne tous les contacts"""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contacts")
    data = cursor.fetchall()
    conn.close()
    return data

def add_contact(nom, prenom, telephone, email):
    """Ajoute un nouveau contact"""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO contacts (nom, prenom, telephone, email) VALUES (?, ?, ?, ?)",
        (nom, prenom, telephone, email)
    )
    conn.commit()
    conn.close()

def delete_contact(contact_id):
    """Supprime un contact par son id"""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
    conn.commit()
    conn.close()

def update_contact(contact_id, nom, prenom, telephone, email):
    """Modifie un contact existant"""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE contacts
        SET nom = ?, prenom = ?, telephone = ?, email = ?
        WHERE id = ?
    """, (nom, prenom, telephone, email, contact_id))
    conn.commit()
    conn.close()

# ==========================
# INTERFACE GRAPHIQUE
# ==========================

# Variables globales
selected_id = None
nom_input = None
prenom_input = None
tel_input = None
email_input = None
table = None

# --- Fonctions d'interface ---

def load_table():
    """Charge tous les contacts dans le tableau"""
    global table, selected_id
    selected_id = None
    table.setRowCount(0)
    contacts = get_contacts()
    for contact in contacts:
        row_pos = table.rowCount()
        table.insertRow(row_pos)
        table.setItem(row_pos, 0, QTableWidgetItem(str(contact[0])))
        table.setItem(row_pos, 1, QTableWidgetItem(contact[1]))
        table.setItem(row_pos, 2, QTableWidgetItem(contact[2]))
        table.setItem(row_pos, 3, QTableWidgetItem(contact[3]))
        table.setItem(row_pos, 4, QTableWidgetItem(contact[4]))

def select_contact():
    """Quand on clique sur un contact, remplir les champs"""
    global selected_id
    row = table.currentRow()
    if row >= 0:
        selected_id = int(table.item(row, 0).text())
        nom_input.setText(table.item(row, 1).text())
        prenom_input.setText(table.item(row, 2).text())
        tel_input.setText(table.item(row, 3).text())
        email_input.setText(table.item(row, 4).text())

def clear_fields():
    """Vide les champs et réinitialise la sélection"""
    global selected_id
    nom_input.clear()
    prenom_input.clear()
    tel_input.clear()
    email_input.clear()
    selected_id = None

def add_btn_clicked():
    """Ajouter un contact"""
    add_contact(nom_input.text(), prenom_input.text(), tel_input.text(), email_input.text())
    clear_fields()
    load_table()

def delete_btn_clicked():
    """Supprimer le contact sélectionné"""
    global selected_id
    if selected_id:
        delete_contact(selected_id)
        clear_fields()
        load_table()

def update_btn_clicked():
    """Modifier le contact sélectionné"""
    global selected_id
    if selected_id:
        update_contact(selected_id, nom_input.text(), prenom_input.text(), tel_input.text(), email_input.text())
        clear_fields()
        load_table()

# ==========================
# CREATION DE LA FENETRE
# ==========================

create_table()

app = QApplication(sys.argv)
fenetre = QWidget()
fenetre.setWindowTitle("Carnet d'adresses")
fenetre.setGeometry(100, 100, 700, 400)

# Layout principal vertical
layout = QVBoxLayout()

# Champs de saisie
nom_input = QLineEdit()
nom_input.setPlaceholderText("Nom")
prenom_input = QLineEdit()
prenom_input.setPlaceholderText("Prénom")
tel_input = QLineEdit()
tel_input.setPlaceholderText("Téléphone")
email_input = QLineEdit()
email_input.setPlaceholderText("Email")

layout.addWidget(nom_input)
layout.addWidget(prenom_input)
layout.addWidget(tel_input)
layout.addWidget(email_input)

# Boutons CRUD dans un layout horizontal
h_layout = QHBoxLayout()
btn_add = QPushButton("Ajouter")
btn_add.clicked.connect(add_btn_clicked)
btn_update = QPushButton("Modifier")
btn_update.clicked.connect(update_btn_clicked)
btn_delete = QPushButton("Supprimer")
btn_delete.clicked.connect(delete_btn_clicked)

h_layout.addWidget(btn_add)
h_layout.addWidget(btn_update)
h_layout.addWidget(btn_delete)
layout.addLayout(h_layout)

# Tableau pour afficher les contacts
table = QTableWidget()
table.setColumnCount(5)
table.setHorizontalHeaderLabels(["ID", "Nom", "Prénom", "Téléphone", "Email"])
table.cellClicked.connect(select_contact)
layout.addWidget(table)

fenetre.setLayout(layout)

load_table()  # Charger les contacts dès le démarrage

fenetre.show()
sys.exit(app.exec())
