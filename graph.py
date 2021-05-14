class Graph:
    """Klasse zur Darstellung von einem Graphen mit einer Adjazenzmatrix

    Beispiel
    g = Graph(6)
    kanten = [
        [0, 2],
        [0, 3],
        [0, 4],
        [1, 3],
        [1, 4],
        [1, 5],
    ]
    for kante in kanten:
        g.setze_kante_zwischen(kante[0],kante[1])
    print(g.nachbarn_von(0))
    g.adjazenzmatrix_drucken()

    Alternative:
    g = Graph(6)
    g.matrix_eingabe(matrix)
    """
    def __init__(self, anzahl_der_knoten):
        self.matrix = [[0 for x in range(anzahl_der_knoten)] for y in range(anzahl_der_knoten)]

    def setze_kante_zwischen(self, a, b):
        self.matrix[a][b] = 1
        self.matrix[b][a] = 1

    def nachbarn_von(self, a):
        nachbarn = []
        for index, value in enumerate(self.matrix[a]):
            if value == 1:
                nachbarn.append(index)
        return nachbarn

    def adjazenzmatrix_drucken(self):
        zeile_linie = "+---"+ ("+--") * (len(self.matrix) ) + "+"
        zeile_doppellinie = "+===" + ("+==") * (len(self.matrix) ) + "+"

        print(zeile_linie)
        print("|   ", end='')
        for spaltennummern in range(len(self.matrix)):
            print("|#" + str(spaltennummern), end='')
        print("|")
        for zeilen_index, zeile in enumerate(self.matrix):
            if zeilen_index == 0:
                print(zeile_doppellinie)
            else:
                print(zeile_linie)
            print("|#" + str(zeilen_index) + "|", end='')
            for wert in zeile:
                print("| " + str(wert), end='')
            print("|")
        print(zeile_linie)

    def matrix_eingabe(self, matrix):
        self.matrix = matrix

    def anzahl_der_knoten(self):
        return len(self.matrix)
