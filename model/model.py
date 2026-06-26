import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._tracks = []
        self._idMapT = {}
        self._playlist = []

    def getPlaylist(self, minuti):
        self._playlist = []
        componenti = nx.connected_components(self._graph)
        largest = list(max(componenti, key=len))  # lista, non set, per poter indicizzare
        parziale = []
        self._ricorsione(parziale, largest, minuti, 0, 0)
        return self._playlist

    def _ricorsione(self, parziale, largest, minuti, somma, start):
        if len(parziale) > len(self._playlist):
            self._playlist = list(parziale)
        for i in range(start, len(largest)):
            track = largest[i]
            nuova_somma = track.Milliseconds/6000 + somma
            if nuova_somma <= minuti:
                parziale.append(track)
                self._ricorsione(parziale, largest, minuti, nuova_somma, i + 1)
                parziale.pop()

    def getAllGeneri(self):
        return DAO.getAllGeneri()

    def getMaxMinByGenre(self, genere):
        for min, max in DAO.getMaxMinByGenre(genere):
            return min, max

    def buildGraph(self, genere, min, max):
        self._graph.clear()
        self._tracks = DAO.getAllTracks(genere, min, max)
        for track in self._tracks:
            self._idMapT[track.TrackId] = track
        self._graph.add_nodes_from(self._tracks)
        allEdges = DAO.getAllEdges(genere, min, max, self._idMapT)
        for e in allEdges:
            self._graph.add_edge(e[0], e[1])

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getInfoConnessa(self):
        risultati = []
        componenti = nx.connected_components(self._graph) #[ {Track10, Track11, Track13}, {Track12, Track14} ]
        for comp in componenti:
            comp = list(comp) # [Track10, Track11, Track13]
            numVertici = len(comp)
            numPlaylist = comp[0].NumP #prendiamo un nodo qualsiasi e verifichiamo il numero di playlist
            risultati.append((numVertici, numPlaylist))
        return risultati

