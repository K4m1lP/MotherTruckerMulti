import pygame
import pygame_menu
import Network

from time import time_ns as get_time, time

from RenderSystem import RenderSystem

menu = None
SCR_WIDTH, SCR_HEIGHT = 1900, 1000
client = Network.Client()
DISCONNECT_MSG = "!DISCONNECT"


def login_function(menu, nick_id, password_id):
    print(client.pos)
    if client.pos is not None:
        nick = pygame_menu.Menu.get_widget(menu, widget_id=nick_id).get_value()
        password = pygame_menu.Menu.get_widget(menu, widget_id=password_id).get_value()
        IS_LOGGED = client.login(nick, password)
        if IS_LOGGED:
            menu.close()


def create_login_view(game_window):
    menu = pygame_menu.Menu('Mother Trucker', SCR_WIDTH, SCR_HEIGHT,
                            theme=pygame_menu.themes.THEME_DARK)
    nick_id = menu.add.text_input('Nick :', default='').get_id()
    password_id = menu.add.text_input('Password :', default='', password=True).get_id()
    menu.add.button('Login', login_function, menu, nick_id, password_id)
    menu.add.button('Quit', pygame_menu.events.EXIT)
    menu.mainloop(game_window)
    return menu


if __name__ == '__main__':
    pygame.init()
    game_window = pygame.display.set_mode((SCR_WIDTH, SCR_HEIGHT))
    pygame.display.set_caption("MotherTracker")
    should_close = False
    dt = 1 / 60
    end_time = 0
    start_time = get_time()
    menu = create_login_view(game_window)
    print("elooo")
    if client.is_log():
        # create world
        render_system = RenderSystem(game_window)
        while not should_close:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    should_close = True
            key_pressed = pygame.key.get_pressed()
            to_draw = client.send_obj(key_pressed)
            if not to_draw or to_draw == DISCONNECT_MSG:
                pass
            render_system.update(dt, to_draw)
            end_time = get_time()
            dt = (end_time - start_time) * 1e-9
            start_time = get_time()
    pygame.quit()
    quit()
