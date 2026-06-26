import flet as ft


class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model

    def handleCreaGrafo(self, e):
        self._view.txt_result.controls.clear()
        minInput = self._view._txt_min.value
        maxInput = self._view._txt_max.value
        if minInput > maxInput:
            self._view.create_alert("Il minimo deve essere minore del massimo")
            return
        if minInput ==  "" or maxInput == "":
            self._view.create_alert("Seleziona entrambi i valori")
            return
        try:
            minInt = int(minInput)
            maxInt = int(maxInput)
        except ValueError:
            self._view.create_alert("Scrivi valori numerici")
            return
        genere = self._view._dd_genere.value
        if genere is None:
            self._view.create_alert("Seleziona un genere")
            return
        min, max = self._model.getMaxMinByGenre(genere)
        if minInt < min or maxInt > max:
            self._view.create_alert(f"Per il genere selezionato, il valore minimo è {min} e il massimo è {max}. Inserisci valori in questo range.")
            return
        self._model.buildGraph(genere, minInt, maxInt)
        nNodes, nEdges = self._model.getGraphDetails()
        self._view.txt_result.controls.append(ft.Text(f"Nodi: {nNodes} - Archi: {nEdges}"))
        connessa = self._model.getInfoConnessa()
        self._view.txt_result.controls.append(ft.Text(""))
        for dimensione, numP in connessa:
            self._view.txt_result.controls.append(ft.Text(f"Componente con {dimensione}, inseriti in {numP} playlist."))
        self._view.update_page()


    def handlePlaylist(self, e):
        self._view.txt_result.controls.clear()
        m = self._view._txt_dTot.value
        if m == "":
            self._view.create_alert("Scrivi un valore")
            return
        try:
            minuti = float(m)
        except ValueError:
            self._view.create_alert("Inserisci un valore numerico")
            return
        playlist = self._model.getPlaylist(minuti)
        for p in playlist:
            self._view.txt_result.controls.append(ft.Text(f"{p}"))
        self._view.update_page()


    def fillDDGeneri(self):
        generi = self._model.getAllGeneri()
        for g in generi:
            self._view._dd_genere.options.append(ft.dropdown.Option(g))
        self._view.update_page()