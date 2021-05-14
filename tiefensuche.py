class Tiefensuche:
    """Erstellt zu einem Graphen einen aufspannenden Baum

    Beispiel:
    suche = Tiefensuche(graph)
    suche.start(startknoten)
    weg = suche.weg_zu(zielknoten)
    """
    def __init__(self, graph):
        self.graph = graph
        self.baum = [None for x in range(self.graph.anzahl_der_knoten())]
        self.startknoten = None
        # Knotenliste speichert die Knoten in der Reihenfolge, wie sie besucht werden
        self.knotenliste = []

    def start(self, startknoten):
        self.reset()
        self.startknoten = startknoten
        self.baum[startknoten] = startknoten
        self.schritt(startknoten)

    def knoten_abfolge(self, startknoten):
        """Fuehrt die Tiefensuche durch, gibt zusaetzlich den Weg der Tiefensuche zurueck."""
        self.start(startknoten)
        return self.knotenliste

    def schritt(self, knoten):
        self.knotenliste.append(knoten)
        nachbarn = self.graph.nachbarn_von(knoten)
        nachbarn.reverse()
        for nachbar in nachbarn:
            if self.baum[nachbar] is None:
                self.baum[nachbar] = knoten
                self.schritt(nachbar)
                self.knotenliste.append(knoten)

    def reset(self):
        self.baum = [None for x in range(self.graph.anzahl_der_knoten())]
        self.startknoten = None

    def gib_baum(self):
        return self.baum

    def weg_zu(self, a):
        """Erstellt einen Weg vom startknoten zu a im aufspannenden Baum"""
        if self.startknoten is None:
            print("Erst die Tiefensuche durchführen")
            return None
        else:
            weg = [a]
            while weg[0] != self.startknoten:
                weg.insert(0, self.baum[weg[0]])
        return weg

