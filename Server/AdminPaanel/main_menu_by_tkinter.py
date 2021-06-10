from AdminPaanel.canvas_by_tkinter import *

slownik_obiektow = {}
ikony = []
width = 800
height = 500


class MainWindow:
    def __init__(self):
        self.window = Tk()
        self.window.title("Admin Panel")
        self.x_coord, self.y_coord = (0, 0)
        self.window.geometry("%dx%d+%d+%d" % (width, height, self.x_coord, self.y_coord))
        self.menu()

        '''
        top_frame = Frame(self.window, bg="dark slate gray", width=450, height=50)
        top_frame.grid(row=0, sticky="ew")

        center = Frame(self.window, bg='gray2', width=50, height=40)
        center.grid(row=1, sticky="nsew")
        center.grid_rowconfigure(0, weight=1)
        center.grid_columnconfigure(1, weight=1)

        self.window.grid_rowconfigure(1, weight=1)
        self.window.grid_columnconfigure(0, weight=1)


        rysuj_container = Frame(top_frame, width=50, height=50, padx=3)
        rysuj_container.grid(row=0, column=0)
        modyfikuj_container = Frame(top_frame, width=50, height=50)
        modyfikuj_container.grid(row=0, column=1)
        ustawienia_container = Frame(top_frame, width=50, height=50, padx=3)
        ustawienia_container.grid(row=0, column=2)
        test_container = Frame(top_frame, width=50, height=50, padx=3)
        test_container.grid(row=0, column=3)

        self.ctr_left = Frame(center, bg='black')
        self.ctr_mid = Frame(center, bg='black', width=250, height=190)
        self.ctr_right = Frame(center, bg='black', width=100, height=190)
        self.ctr_left.grid(row=0, column=0, sticky="ns")
        self.ctr_mid.grid(row=0, column=1, sticky="nsew")
        self.ctr_right.grid(row=0, column=2, sticky="ns")

        self.pos_label = Label(self.ctr_right, text='pozycja', width=10)

        # self.button_bars()
        # self.pos_label = Label(self.ctr_right, text='pozycja', width=10)

        # self.temporairy_conainer = None
        # self.prop_top = None
        # self.window.bind('<Motion>', self.motion)
        '''
    @staticmethod
    def change_val(button, val1):
        """Obsługuje włączanie i wyłączanie przycisku
        button - cel
        getter - funkcja, powinna zwracać bool
        setter - funkcja zmienia wartość argumentu typu bool na przeciwną """
        if val1:
            val1 = 1
            button.config(fg='gray74')

        else:
            val1 = True
            button.config(fg='black')

    @staticmethod  # TODO dekorator jak chuj
    def check_window(window, funkcja_window, funkcja_cont=None):
        """Sprawdza czy dany atrybut już istnieje i zapobiega 
        jego wielokrotnemu wywołaniu i nakładaniu"""
        try:
            if window.winfo_exists():
                pass
            else:
                window = funkcja_window()
        except:
            window = funkcja_window()
        finally:
            temp = funkcja_cont

    def motion(self, event):
        x, y = event.x, event.y
        self.pos_label.config(text='x={}, y={}'.format(x, y))
        return x, y

    def auto_butt(self, frame, tuptus):
        """automatycznie tworzy przyciski z listy tuptus w ramce frame"""

        def foo(se):
            return eval('se.' + butt[0])

        for widget in frame.winfo_children():
            widget.destroy()
        for butt in tuptus:
            x = foo(self)
            ttub = Button(frame, text=butt[0], width=10, command=x)
            ttub.grid(row=butt[1], column=butt[2])

    def menu(self):
        menubar = Menu(self.window)
        self.window.config(menu=menubar)
        file_menu = Menu(menubar)
        edit_menu = Menu(menubar)
        paint_menu = Menu(menubar)
        elem_menu = Menu(paint_menu)

        file_menu.add_command(label="Zapisz", underline=0)
        file_menu.add_command(label="Zapisz jako", underline=0)
        file_menu.add_command(label="Otworz", underline=0)
        file_menu.add_command(label="Nowy", underline=0)
        file_menu.add_command(label="Drukuj", underline=0)

        edit_menu.add_command(label="owtorz")
        edit_menu.add_command(label="cofnij")
        edit_menu.add_separator()
        edit_menu.add_command(label="kopiuj")
        edit_menu.add_command(label="wklej")
        edit_menu.add_command(label="wytnij")

        paint_menu.add_cascade(label="elementy rysunkowe", menu=elem_menu)
        paint_menu.add_command(label="siatka")

        elem_menu.add_command(label="linia")
        elem_menu.add_cascade(label="okrąg")
        elem_menu.add_cascade(label="prostokąt")

        menubar.add_cascade(label="plik", menu=file_menu)
        menubar.add_cascade(label="edycja", menu=edit_menu)
        menubar.add_cascade(label='rysuj', menu=paint_menu)

    def button_bars(self):
        przyciski_rysuj = ()

        def mp(self, button):
            if self.przestrzen.magnet_points:
                button.config(fg='gray74')
            else:
                button.config(fg='black')

        r1 = Button(self.ctr_right, text='przyciągaj', width=10,
                    command=lambda: mp(self, r1))
        r1.grid(row=0, column=0)

        def str(self, button):
            if self.przestrzen.straight:
                button.config(fg='gray74')
            else:
                button.config(fg='black')

        r2 = Button(self.ctr_right, text='proste', width=10, fg='gray74',
                    command=lambda: str(self, r2))
        r2.grid(row=1, column=0, )

        self.pos_label.grid(row=2, column=0)
        self.auto_butt(self.ctr_left, przyciski_rysuj)

    def właściwości_r(self):
        self.prop_top = Toplevel()
        width, height = 100, 100
        x_coord, y_coord = self.x_coord - width - 20, height
        self.prop_top.geometry("%dx%d+%d+%d" % (width, height, x_coord, y_coord))
        self.prop_top.title("Właściwości")

        kolor = Label(self.prop_top, text='kolor:')
        kolor.grid(row=0, column=0, sticky=E)

        grubosc = Label(self.prop_top, text='grubość:')
        grubosc.grid(row=1, column=0, sticky=E)

        self.grubosc_button.grid(row=1, column=1)

        rodzaj = Label(self.prop_top, text='przerwy')
        rodzaj.grid(row=2, column=0, sticky=E)

        return self.prop_top

    def grubosc(self):
        self.grubosc_button.destroy()
        e = Entry(self.prop_top)
        e.grid(row=1, column=1)
        self.grubosc_OK = Button(self.prop_top, text="Ok", command=lambda: self.butt(e))
        self.grubosc_OK.grid(row=1, column=2)

    def butt(self, e):
        self.temporairy_conainer = e.get()
        e.destroy()
        self.grubosc_OK.destroy()
        self.grubosc_button = Button(self.prop_top, text=self.obiekt_canvas.grubosc,
                                     width=2, height=1, command=self.grubosc)
        self.grubosc_button.grid(row=1, column=1)


main_menu = MainWindow()
mainloop()
