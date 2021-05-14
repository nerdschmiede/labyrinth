import tkinter as tk
from kruskal import Kruskal
from graph import Graph
from tiefensuche import Tiefensuche


class GUILabyrinth(tk.Frame):
    """Erstellt mit tkinter eine GUI für die Tiefensuche in einem Labyrinth"""

    def __init__(self):
        self.master = tk.Tk()
        super().__init__(self.master)
        self.master.title("Labyrinth")
        self.BREITE = 700
        self.HOEHE = 700
        self.RAND = 10
        self.zeilen = 20
        self.spalten = 20
        self.ungeloest = True
        self.lab_maker = Kruskal()
        self.lab_maker.labyrinth_erstellen(self.zeilen, self.spalten)
        self.waende = self.lab_maker.spielbrett_waende()
        self.suche = None

        # Einfuegen der tkinter Objekte
        self.pack()

        self.menuleiste = tk.Frame(self)
        self.menuleiste.pack(side="top")
        self.quit = tk.Button(self.menuleiste, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="left")
        self.next = tk.Button(self.menuleiste, text="Next", command=self.naechstes_labyrinth)
        self.next.pack(side="left")
        self.solve = tk.Button(self.menuleiste, text="Solve", command=self.loesen)
        self.solve.pack(side="left")
        self.create = tk.Button(self.menuleiste, text="Create", command=self.aufbau)
        self.create.pack(side="left")
        self.label_zeilen = tk.Label(self.menuleiste, text="Zeilen:")
        self.label_zeilen.pack(side="left")
        self.zeilen_eingabe = tk.Entry(self.menuleiste, width=3)
        self.zeilen_eingabe.insert(0, str(self.zeilen))
        self.zeilen_eingabe.pack(side="left")
        self.label_spalten = tk.Label(self.menuleiste, text="Spalten:")
        self.label_spalten.pack(side="left")
        self.spalten_eingabe = tk.Entry(self.menuleiste, width=3)
        self.spalten_eingabe.insert(0, str(self.spalten))
        self.spalten_eingabe.pack(side="left")
        self.label_arrow = tk.Label(self.menuleiste, text="Arrow")
        self.label_arrow.pack(side="left")
        self.pfeile_eingabe = tk.IntVar()
        self.pfeile_checkbutton = tk.Checkbutton(self.menuleiste, variable=self.pfeile_eingabe)
        self.pfeile_checkbutton.pack(side="left")
        self.label_slider = tk.Label(self.menuleiste, text="Speed:")
        self.label_slider.pack(side="left")
        self.slider = tk.Scale(self.menuleiste, from_=1, to=1000, orient=tk.HORIZONTAL)
        self.slider.set(1)
        self.slider.pack()

        self.zeichenbrett = tk.Canvas(self,
                                      width=self.BREITE + 2 * self.RAND,
                                      height=self.HOEHE + 2 * self.RAND)
        self.zeichenbrett.pack(side="bottom")
        self.aktueller_knoten = None

        self.master.bind('q', lambda event: self.master.destroy())
        self.master.bind('n', lambda event: self.naechstes_labyrinth())
        self.master.bind('s', lambda event: self.loesen())

        self.zeichne()

        self.master.mainloop()

    def zeichne(self):
        self.zeichenbrett.delete("all")
        self.zeichenbrett.focus_set()
        # Mit spielfeld ist ein Feld gemeint
        spielfeld_breite = self.BREITE / self.spalten
        spielfeld_hoehe = self.HOEHE / self.zeilen

        x = self.RAND + spielfeld_breite / 2
        y = self.RAND + spielfeld_hoehe / 2
        self.aktueller_knoten = self.zeichenbrett.create_oval(
                                x-2, y-2, x+2, y+2, width=0, fill='red')

        # Umrandung mit Ausgaengen
        self.zeichenbrett.create_line(self.RAND + spielfeld_breite, self.RAND,
                                      self.BREITE + self.RAND, self.RAND)
        self.zeichenbrett.create_line(self.BREITE + self.RAND, self.RAND,
                                      self.BREITE + self.RAND, self.HOEHE + self.RAND)
        self.zeichenbrett.create_line(self.BREITE + self.RAND - spielfeld_breite, self.HOEHE + self.RAND,
                                      self.RAND, self.HOEHE + self.RAND)
        self.zeichenbrett.create_line(self.RAND, self.HOEHE + self.RAND,
                                      self.RAND, self.RAND)

        # Waende zeichnen
        for wand in self.waende:
            # Eine Kante besteht aus zwei Knoten
            # Ein Knoten besteht aus einer x und y Koordinate auf dem Spielbrett
            knoten_1 = wand[0]
            knoten_2 = wand[1]
            # Startkoordinaten berechnen
            start_x = self.RAND + spielfeld_breite * knoten_2[1]
            start_y = self.RAND + spielfeld_hoehe * knoten_2[0]
            # Frage ob es eine waagerechte Kante ist
            if knoten_1[0] + 1 == knoten_2[0]:
                self.zeichenbrett.create_line(start_x, start_y,
                                              start_x + spielfeld_breite, start_y)
            else:
                self.zeichenbrett.create_line(start_x, start_y,
                                              start_x, start_y + spielfeld_hoehe)

    def naechstes_labyrinth(self):
        if self.next['state'] == 'normal':
            self.solve['state'] = 'normal'
            self.create['state'] = 'normal'
            self.ungeloest = True
            self.zeilen = int(self.zeilen_eingabe.get())
            self.spalten = int(self.spalten_eingabe.get())
            self.lab_maker.labyrinth_erstellen(self.zeilen, self.spalten)
            self.waende = self.lab_maker.spielbrett_waende()
            self.zeichne()

    def loesen(self):
        self.solve['state'] = 'disabled'
        self.create['state'] = 'disabled'
        if self.ungeloest:
            # Graph auslesen und speichern
            matrix = self.lab_maker.matrix()
            graph = Graph(len(matrix))
            graph.matrix_eingabe(matrix)

            # Tiefensuche
            self.suche = Tiefensuche(graph)
            self.suche.start(0)
            self.ungeloest = False
        weg = self.suche.weg_zu(self.zeilen * self.spalten - 1)
        if self.pfeile_eingabe.get() == 1:
            weg.reverse()

        # Weg einzeichnen
        self.weg_zeichnen(weg, 'red')

    def aufbau(self):
        self.create['state'] = 'disabled'
        self.ungeloest = False
        # Graph auslesen und speichern
        matrix = self.lab_maker.matrix()
        graph = Graph(len(matrix))
        graph.matrix_eingabe(matrix)

        # Tiefensuche
        self.suche = Tiefensuche(graph)
        baum = self.suche.knoten_abfolge(0)

        # Weg einzeichnen
        self.aufbau_zeichnen(baum, 'gold', 'blue')

    def spielfeld_koordinaten(self, nummer):
        """Berechnet zu einer Spielfeldnummer die Koordinaten

        Das Spielfeld ist durchnummeriert. Bei 3 Zeilen und 4 Spalten
        0   1   2   3
        4   5   6   7
        8   9   10  11
        So kann man zwischen Zeilen/Spalten und Matrix hin un her wechseln
        """
        zeile = nummer // self.spalten
        spalte = nummer % self.spalten
        x = self.RAND + (spalte + 0.5) * self.BREITE / self.spalten
        y = self.RAND + (zeile + 0.5) * self.HOEHE / self.zeilen
        return x, y

    def weg_zeichnen(self, weg, color):
        if self.next['state'] == 'normal':
            self.next['state'] = 'disabled'
            self.weg_schritt(weg, 0, color)

    def weg_schritt(self, weg, i, color):
        if i < len(weg) - 1:
            startknoten = weg[i]
            zielknoten = weg[i+1]
            start_x, start_y = self.spielfeld_koordinaten(startknoten)
            ziel_x, ziel_y = self.spielfeld_koordinaten(zielknoten)
            arrow_value = None
            if self.pfeile_eingabe.get() == 1:
                arrow_value = tk.LAST
            self.zeichenbrett.create_line(start_x, start_y,
                                          ziel_x, ziel_y, 
                                          fill=color, arrow=arrow_value, width=5)
            self.zeichenbrett.coords(self.aktueller_knoten,
                                     ziel_x-2, ziel_y-2, ziel_x+2, ziel_y+2)
            self.after(self.slider.get(), self.weg_schritt, weg, i+1, color)
        else:
            self.next['state'] = 'normal'

    # TODO: Die naechsten zwei Methoden sind zu nah an den bisherigen zwei Methoden und sollten umgeschrieben werden
    def aufbau_zeichnen(self, weg, color_1, color_2):
        if self.next['state'] == 'normal':
            self.next['state'] = 'disabled'
            besuchte_knoten = set()
            besuchte_knoten.add(weg[0])
            self.aufbau_schritt(weg, 0, color_1, color_2, besuchte_knoten)

    def aufbau_schritt(self, weg, i, color_1, color_2, besuchte_knoten):
        if i < len(weg) - 1:
            startknoten = weg[i]
            zielknoten = weg[i+1]
            start_x, start_y = self.spielfeld_koordinaten(startknoten)
            ziel_x, ziel_y = self.spielfeld_koordinaten(zielknoten)
            arrow_value = None
            if zielknoten in besuchte_knoten:
                color = color_2
                if self.pfeile_eingabe.get() == 1:
                    arrow_value = tk.LAST
            else:
                color = color_1
                besuchte_knoten.add(zielknoten)
            self.zeichenbrett.create_line(start_x, start_y,
                                          ziel_x, ziel_y,
                                          fill=color, arrow=arrow_value, width=3)
            self.zeichenbrett.coords(self.aktueller_knoten,
                                     ziel_x-2, ziel_y-2, ziel_x+2, ziel_y+2)
            self.after(self.slider.get(), self.aufbau_schritt, weg, i + 1, color_1, color_2, besuchte_knoten)
        else:
            self.next['state'] = 'normal'


if __name__ == '__main__':
    gui = GUILabyrinth()
