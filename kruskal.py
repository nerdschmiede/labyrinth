from random import shuffle


class Kruskal:
    """ Erzeugt die Waende von  ein Labyrinth der Groesse zeilen und spalten


    Idee: http://weblog.jamisbuck.org/2011/1/3/maze-generation-kruskal-s-algorithm
    Die Spielfelder haben die Koordinaten [zeile][spalte]
    Die Waende sind im Format [[zeile_1,spalte_1][zeile_2,spalte_2]]

    Beispiel:
    zeilen = 4
    spalten = 5
    k = Kruskal()
    k.labyrinth_erstellen(zeilen, spalten)
    waende = k.spielbrett_waende()
    graph = k.matrix()
    """
    def __init__(self):
        """Intern wird mit einem Spielbrett in Zeilen und Spalten gearbeitet"""
        self.zeilen = None
        self.spalten = None
        self.spielbrett = []
        self.verbrauchte_kanten = []
        self.waende = []
        self.anzahl_der_mengen = 0

    def startwerte_setzen(self):
        """Initialisierung der Startwerte"""
        self.spielbrett = []
        self.verbrauchte_kanten = []
        self.waende = []

        for zeile in range(self.zeilen):
            self.spielbrett.append([])
            for spalte in range(self.spalten):
                # Jedes Spielfeld erhaelt seine Koordinaten als Inhalt
                self.spielbrett[zeile].append([zeile, spalte])

                # Waende nach rechts und unten setzen
                if spalte != self.spalten - 1:
                    self.waende.append([[zeile, spalte], [zeile, spalte + 1]])
                if zeile != self.zeilen - 1:
                    self.waende.append([[zeile, spalte], [zeile + 1, spalte]])

        shuffle(self.waende)
        # Die zusammenhaengenden Gebiete werden als Mengen interpretiert
        # Zum Start mit allen Waenden gibt es so viele Menge wie Felder
        self.anzahl_der_mengen = self.zeilen * self.spalten

    def spielbrett_ausgeben(self):
        for zeile in self.spielbrett:
            print(zeile)

    def finde_die_wurzel(self, knoten):
        """Findet zu einem Spielfeld die repraesentative Wurzel"""
        zeile, spalte = knoten
        # Falls auf dem Spielbrett immer noch der eigene Name steht
        if self.spielbrett[zeile][spalte] == [zeile, spalte]:
            # Wurzel gefunden
            return knoten
        else:
            # sonst geh zu dem notierten Feld
            return self.finde_die_wurzel(self.spielbrett[zeile][spalte])

    def vereinen(self, kante):
        """Vereinigung der Baeume

        Idee: https://de.wikipedia.org/wiki/Union-Find-Struktur
        Alle Knoten, die untereinander erreicht werden koennen, besitzen die gleiche Wurzel.
        Beim Entfernen einer Kante müssen die Namen aktualisiert werden.
        """
        # Zerlege die Kante und finde die Wurzeln
        baum_1 = self.finde_die_wurzel(kante[0])
        baum_2 = self.finde_die_wurzel(kante[1])

        # Wenn die Baeume unterschiedlich sind,
        if baum_1 != baum_2:
            # ändere Wurzel 2 zu 1
            zeile_1, spalte_1 = baum_1
            zeile_2, spalte_2 = baum_2
            self.spielbrett[zeile_2][spalte_2] = [zeile_1, spalte_1]

            self.anzahl_der_mengen -= 1

        # Zusatz, damit das Labyrinth schleifenfrei ist.
        else:
            self.verbrauchte_kanten.append(kante)

    def schritt(self):
        # Kante auswaehlen
        kante = self.waende.pop()

        # Teilbaeume wenn noetig vereinen
        self.vereinen(kante)

    def labyrinth_erstellen(self, zeilen, spalten):
        self.zeilen = zeilen
        self.spalten = spalten
        self.startwerte_setzen()
        while self.anzahl_der_mengen > 1:
            self.schritt()

        self.waende += self.verbrauchte_kanten

    def spielbrett_waende(self):
        return self.waende

    def spielbrett_zu_knoten(self, zeile, spalte):
        return zeile * self.spalten + spalte

    def matrix(self):
        """Wandelt das Spielbrett in eine Adjazenzmatrix um.

                         | 1  2  3  4  5  6
        +-+-+-+         -+-----------------
        |1 2|3|         1| 0  1  0  0  0  0
        +-+ +-+   =>    2| 1  0  0  0  1  0
        |4|5 6|         3| 0  0  0  0  0  0
        +-+-+-+         4| 0  0  0  0  0  0
                        5| 0  1  0  0  0  1
                        6| 0  0  0  0  1  0
        """
        knoten_zahl = self.spalten * self.zeilen
        adjazenzmatrix = [[0 for x in range(knoten_zahl)] for y in range(knoten_zahl)]
        # Spielbrett durchgehen und Verbindungen setzen
        for zeile in range(self.zeilen):
            for spalte in range(self.spalten):
                knoten = self.spielbrett_zu_knoten(zeile, spalte)
                if zeile + 1 != self.zeilen and [[zeile, spalte], [zeile + 1, spalte]] not in self.waende:
                    adjazenzmatrix[knoten][knoten + self.spalten] = 1
                    adjazenzmatrix[knoten + self.spalten][knoten] = 1
                if spalte + 1 != self.spalten and [[zeile, spalte], [zeile, spalte + 1]] not in self.waende:
                    adjazenzmatrix[knoten][knoten + 1] = 1
                    adjazenzmatrix[knoten + 1][knoten] = 1
        return adjazenzmatrix

    def spielbrett_drucken(self):
        print("+" + "-+" * (len(self.spielbrett)))
        for zeile in range(self.zeilen):
            druck_1 = "|"
            druck_2 = "+"
            for spalte in range(self.spalten):
                if spalte != self.spalten - 1:
                    if [[zeile, spalte], [zeile, spalte + 1]] in self.waende:
                        druck_1 += " |"
                    else:
                        druck_1 += "  "
                else:
                    druck_1 += " |"
                if zeile != self.zeilen - 1:
                    if [[zeile, spalte], [zeile + 1, spalte]] in self.waende:
                        druck_2 += "-+"
                    else:
                        druck_2 += " +"
                else:
                    druck_2 += "-+"
            print(druck_1)
            print(druck_2)

