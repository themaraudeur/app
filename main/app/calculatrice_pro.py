import sys
import math
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLineEdit, QPushButton, QLabel,
    QVBoxLayout, QGridLayout, QTabWidget, QComboBox, QHBoxLayout, QSpinBox
)
from PyQt6.QtCore import Qt

# Fonctions géométriques
def aire_rectangle(l, L): return l * L
def perimetre_rectangle(l, L): return 2 * (l + L)
def aire_cercle(r): return math.pi * r ** 2
def perimetre_cercle(r): return 2 * math.pi * r
def aire_triangle(b, h): return 0.5 * b * h
def volume_cube(c): return c ** 3
def volume_cylindre(r, h): return math.pi * r ** 2 * h
def volume_sphere(r): return (4/3) * math.pi * r ** 3

class Calculatrice(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculatrice Scientifique & Géométrique")
        self.setFixedSize(500, 600)

        self.tabs = QTabWidget(self)
        self.calculatrice_tab = QWidget()
        self.geometrie_tab = QWidget()

        self.tabs.addTab(self.calculatrice_tab, "Calculatrice")
        self.tabs.addTab(self.geometrie_tab, "Géométrie")

        self.init_ui_calculatrice()
        self.init_ui_geometrie()

        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        self.setLayout(layout)

    def init_ui_calculatrice(self):
        layout = QVBoxLayout(self.calculatrice_tab)

        self.affichage = QLineEdit()
        self.affichage.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.affichage.setStyleSheet("font-size: 24px; padding: 10px;")
        layout.addWidget(self.affichage)

        boutons = QGridLayout()
        touches = [
            ("7", 0, 0), ("8", 0, 1), ("9", 0, 2), ("/", 0, 3),
            ("4", 1, 0), ("5", 1, 1), ("6", 1, 2), ("*", 1, 3),
            ("1", 2, 0), ("2", 2, 1), ("3", 2, 2), ("-", 2, 3),
            ("0", 3, 0), (".", 3, 1), ("=", 3, 2), ("+", 3, 3),
            ("(", 4, 0), (")", 4, 1), ("^", 4, 2), ("√", 4, 3),
            ("sin", 5, 0), ("cos", 5, 1), ("tan", 5, 2), ("log", 5, 3),
            ("exp", 6, 0), ("C", 6, 1, 1, 3),
        ]

        for bouton in touches:
            if len(bouton) == 3:
                text, row, col = bouton
                rowspan, colspan = 1, 1
            else:
                text, row, col, rowspan, colspan = bouton

            btn = QPushButton(text)
            btn.setStyleSheet("font-size: 18px; padding: 15px;")
            btn.clicked.connect(self.gerer_click)
            boutons.addWidget(btn, row, col, rowspan, colspan)

        layout.addLayout(boutons)

    def init_ui_geometrie(self):
        layout = QVBoxLayout(self.geometrie_tab)

        self.forme_box = QComboBox()
        self.forme_box.addItems([
            "Aire Rectangle", "Périmètre Rectangle", "Aire Cercle", "Périmètre Cercle",
            "Aire Triangle", "Volume Cube", "Volume Cylindre", "Volume Sphère"
        ])
        layout.addWidget(self.forme_box)

        self.inputs_layout = QHBoxLayout()
        self.input1 = QSpinBox(); self.input1.setMaximum(10000)
        self.input2 = QSpinBox(); self.input2.setMaximum(10000)

        self.inputs_layout.addWidget(self.input1)
        self.inputs_layout.addWidget(self.input2)

        layout.addLayout(self.inputs_layout)

        self.result_label = QLabel("Résultat : ")
        self.result_label.setStyleSheet("font-size: 20px; padding: 10px;")
        layout.addWidget(self.result_label)

        calculer_btn = QPushButton("Calculer")
        calculer_btn.setStyleSheet("font-size: 18px; padding: 10px;")
        calculer_btn.clicked.connect(self.calculer_geometrie)
        layout.addWidget(calculer_btn)

        self.forme_box.currentIndexChanged.connect(self.maj_inputs)

        self.maj_inputs()

    def maj_inputs(self):
        forme = self.forme_box.currentText()
        if "Rectangle" in forme:
            self.input1.setPrefix("l = ")
            self.input2.setPrefix("L = ")
            self.input2.show()
        elif "Cercle" in forme or "Sphère" in forme:
            self.input1.setPrefix("r = ")
            self.input2.hide()
        elif "Triangle" in forme:
            self.input1.setPrefix("base = ")
            self.input2.setPrefix("hauteur = ")
            self.input2.show()
        elif "Cylindre" in forme:
            self.input1.setPrefix("r = ")
            self.input2.setPrefix("h = ")
            self.input2.show()
        elif "Cube" in forme:
            self.input1.setPrefix("c = ")
            self.input2.hide()

    def keyPressEvent(self, event):
        key = event.text()
        if key in "0123456789+-*/().":
            self.affichage.setText(self.affichage.text() + key)
        elif event.key() == Qt.Key.Key_Backspace:
            self.affichage.backspace()
        elif event.key() in (Qt.Key.Key_Enter, Qt.Key.Key_Return):
            self.calculer()

    def gerer_click(self):
        texte = self.sender().text()
        if texte == "=":
            self.calculer()
        elif texte == "C":
            self.affichage.clear()
        elif texte == "√":
            self.affichage.setText(self.affichage.text() + "sqrt(")
        elif texte == "^":
            self.affichage.setText(self.affichage.text() + "**")
        else:
            self.affichage.setText(self.affichage.text() + texte)

    def calculer(self):
        try:
            expression = self.affichage.text()
            expression = expression.replace('sin', 'math.sin')
            expression = expression.replace('cos', 'math.cos')
            expression = expression.replace('tan', 'math.tan')
            expression = expression.replace('log', 'math.log10')
            expression = expression.replace('exp', 'math.exp')
            expression = expression.replace('sqrt', 'math.sqrt')
            expression = expression.replace('π', str(math.pi))
            resultat = eval(expression)
            self.affichage.setText(str(resultat))
        except Exception:
            self.affichage.setText("Erreur")

    def calculer_geometrie(self):
        forme = self.forme_box.currentText()
        a = self.input1.value()
        b = self.input2.value()

        try:
            match forme:
                case "Aire Rectangle": res = aire_rectangle(a, b)
                case "Périmètre Rectangle": res = perimetre_rectangle(a, b)
                case "Aire Cercle": res = aire_cercle(a)
                case "Périmètre Cercle": res = perimetre_cercle(a)
                case "Aire Triangle": res = aire_triangle(a, b)
                case "Volume Cube": res = volume_cube(a)
                case "Volume Cylindre": res = volume_cylindre(a, b)
                case "Volume Sphère": res = volume_sphere(a)
                case _: res = "Inconnu"
            self.result_label.setText(f"Résultat : {res:.4f}")
        except Exception as e:
            self.result_label.setText("Erreur : " + str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    fenetre = Calculatrice()
    fenetre.show()
    sys.exit(app.exec())
