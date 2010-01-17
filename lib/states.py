from os import environ
import sys
from screens import *

class BaseState(object):
    """The base state that all other states subclass."""

    def __init__(self, window=None):
        self.window = window
        self.clock = pygame.time.Clock()

    def run(self):
        """The main game loop that listens for events and draws the screen."""

        while True:
            self.clock.tick(FRAME_RATE)
            self.state.show_debug(int(self.clock.get_fps()))
            self.state.check_events()
            self.state.screen.draw()

    def switch(self, state):
        self.state = state
        self.run()

    def show_debug(self, fps):
        """Print debugging info to console."""

        if SHOW_FRAME_RATE:
            print 'Framerate: %f/%f' % (fps, FRAME_RATE)

    def exit(self):
        pygame.quit()
        sys.exit(0)


class InitState(Screen, BaseState):
    """State used to initialize the game and switch to the title screen."""

    def __init__(self):
        environ['SDL_VIDEO_CENTERED'] = '1'
        Screen.__init__(self)
        del environ['SDL_VIDEO_CENTERED']
        BaseState.__init__(self, self.window)
        self.switch(TitleState())


class TitleState(BaseState):
    """A game state for the title screen."""

    def __init__(self):
        BaseState.__init__(self)
        self.screen = TitleScreen()

    def check_events(self):
        """
        Title screen events:
        Esc:    exit game
        N:      new game
        """

        for event in pygame.event.get():
            if event.type == QUIT: self.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE: self.exit()
                elif event.key == K_n:
                    self.screen.destroy()
                    self.switch(WorldState(STARTING_MAP))


class WorldState(BaseState):
    """A game state for the main world screen."""

    def __init__(self, map_name):
        BaseState.__init__(self)
        self.map_name = map_name
        self.screen = WorldScreen(self.map_name)
        self.player = self.screen.party.list['hero']

    def check_events(self):
        """Check for user input on the world screen."""

        self.move_keys = self.player.move_keys
        for event in pygame.event.get():
            if event.type == QUIT: self.exit()
            elif event.type == KEYDOWN:
                if event.key == GAME_QUIT: self._exit()
                elif event.key == K_d:
                    pygame.time.set_timer(DIALOG_EVENT, 100)

                # An example of adding and removing a test character to the
                # party.
                elif event.key == K_a:
                    self.screen.party.add("test")
                elif event.key == K_z:
                    self.screen.party.remove("test")

                elif event.key in (
                    HERO_MOVE_DOWN,
                    HERO_MOVE_UP,
                    HERO_MOVE_LEFT,
                    HERO_MOVE_RIGHT):
                        self.player_input(True, pygame.key.name, event.key)
            elif event.type == KEYUP:
                if event.key in (
                    HERO_MOVE_DOWN,
                    HERO_MOVE_UP,
                    HERO_MOVE_LEFT,
                    HERO_MOVE_RIGHT):
                        self.player_input(False, pygame.key.name, event.key)
            elif event.type == BATTLE_EVENT:
                self.player.move_keys = []
                self.player.stop = True
                self.switch(BattleState(self))
            elif event.type == DIALOG_EVENT:
                self.player.move_keys = []
                self.player.stop = True
                self.switch(DialogState(self))

    def player_input(self, moving, name, key):
        """Controls key input to the player character."""

        if moving:
            self.move_keys.append(name(key))
            self.player.direction = self.move_keys[-1]
            self.player.stop = False
        else:
            if len(self.move_keys) > 0:
                keyid = self.move_keys.index(name(key))
                del self.move_keys[keyid]
                if len(self.move_keys) != 0:
                    self.player.direction = (self.move_keys[-1])
                else: self.player.stop = True

    def show_debug(self, fps):
        BaseState.show_debug(self, fps)
        if SHOW_RECTS:
            self.screen.map.layers['terrain'].image.fill(
                (0,0,0), self.player.collide_rect)
            for rect in (self.screen.map.nowalk):
                self.screen.map.layers['terrain'].image.fill(
                    (255,255,255), rect)
        if SHOW_TERRAIN:
            print "Current terrain: " + self.player.current_terrain
        if SHOW_REGION:
            print "Current region: " + self.player.current_region

    def destroy(self):
        """Cleanup some objects before we leave this state."""

        self.screen.destroy()
        self.player = None

    def _exit(self):
        """Quit the main game screen returning to the title screen."""

        self.destroy()
        self.switch(TitleState())


class BattleState(BaseState):
    """A game state for a battle scene."""

    def __init__(self, prevstate):
        BaseState.__init__(self)
        self.screen = BattleScreen(prevstate.screen)
        self.prevstate = prevstate
        self.prev_screen = self.prevstate.screen.all_sprites

    def check_events(self):
        """Title screen events"""

        for event in pygame.event.get():
            if event.type == QUIT: self.exit()
            elif event.type == KEYDOWN:
                if event.key == GAME_QUIT: self._exit()

    def _exit(self):
        """Quits the battle screen returning to the world screen."""

        pygame.time.set_timer(BATTLE_EVENT, 0)
        for sprite in self.prev_screen:
            sprite.dirty = 1
        self.screen.destroy()
        self.switch(self.prevstate)


class DialogState(BaseState):
    """A game state for a battle scene."""

    def __init__(self, prevstate):
        BaseState.__init__(self)
        self.prevstate = prevstate
        self.screen = prevstate.screen
        self.dialog = DialogWindow(self.screen.dialog_text)
        self.screen.layers.add(self.dialog)
        for sprite in self.screen.all_sprites:
            sprite.dirty = 1

    def check_events(self):
        """Title screen events"""

        for event in pygame.event.get():
            if event.type == QUIT: self.exit()
            elif event.type == KEYDOWN:
                if event.key == DIALOG_CLOSE: self._exit()
                elif event.key == DIALOG_SCROLL_UP:
                    self.dialog.text.scroll("up")
                elif event.key == DIALOG_SCROLL_DOWN:
                    self.dialog.text.scroll("down")

    def _exit(self):
        """Quits the battle screen returning to the world screen."""

        pygame.time.set_timer(DIALOG_EVENT, 0)
        self.dialog.destroy()
        self.switch(self.prevstate)
