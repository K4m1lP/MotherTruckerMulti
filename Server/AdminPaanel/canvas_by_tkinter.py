
'''Klasy:
CanvasClass - główne płótno programu. Wspiera metody działające bezpośrednio na widgecie canvas
    metody:
    siatka - tworzy siatkę
    usun_klik_bezpośredni - usuwa obiekt na ktory kliknięto lpm

DrawObject - klasa bazowa dla wszystkich obiektów rysunkowych
    metody:
    nazwa - tworzy nazwe obiektu
    press - wywoływana po wcisnieciu lpm, zczytuje aktualną pozycje kursora i zapisuje do list_of_kliks
    rysuj - tworzy obiekt rysunkowy
    contin - określa procedury po zakonczeniu wprowadzania obiektu
    dodawanie - dodaje obiekt do przestrzeni

Line - tworzy linie
Prostokat - tworzy prostokaty'''
from tkinter import *



class CanvasClass:

    def __init__(self, menu, window):
        self.main_menu = menu
        self.window = window
        self.canvas_window = Canvas(window, bg="#142727")
        self.canvas_window.pack(fill=BOTH, expand=YES)
        self.__kolor = 'white'
        self.__grubosc = 1
        self.__dash = None

    def clear_canvas(self):
        self.canvas_window.delete(ALL)


    def siatka(self, skok=50, kolor="#142710"):
        '''Tworzy siatke. Obiekty nie są przyciągane'''
        start_val = 0
        end_val = 5000
        for x in range(start_val, end_val, skok):
            self.canvas_window.create_line(x, 0, x, end_val, fill=kolor, tags='canv_mesh')
            self.canvas_window.create_line(0, x, end_val, x, fill=kolor, tags='canv_mesh')



    @property
    def kolor(self):
        return self.__kolor

    @kolor.setter
    def kolor(self, kolor):
        self.__kolor = kolor

    @property
    def grubosc(self):
        return self.__grubosc

    @grubosc.setter
    def grubosc(self, grubosc):
        self.__grubosc = grubosc

    @property
    def dash(self):
        return self.__dash

    @dash.setter
    def dash(self, dash):
        if dash == 0:
            self.__dash = None
        else:
            self.dash = dash



