r"""
Music Player - Python Arcade
Source code for arcade.sound:
https://arcade.academy/_modules/arcade/sound.html
=======================

UNABLE TO CONVERT TO EXE (Missing Files In Cloud)
----------------------------------------------------------------------------

Missing Feature:
----------------------
Arcade Sound Module does not seem to have:
music.set_stream_position(current_player)
as a counterpart to:
music.get_stream_position(current_player)
so that song play position could respond to dragging of
progress bar by mouse.
"""
import arcade
import time, os
import arcade_udf as af

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 560
SCREEN_TITLE = "Background Music Example"
FPS = 30  # Frames/sec
BACK_COLOR = (250, 245, 254)
BTN_COLOR = (210, 190, 190)

class GamePlay(arcade.Window):
    """ Main application class. """

    def __init__(self):
        super().__init__(
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            SCREEN_TITLE, update_rate=1/FPS)

        self.current_player = None
        self.music = None
        self.button_list = arcade.SpriteList()
        self.text_list = arcade.SpriteList()
        
        self.current_song_index = 0
        self.lastValueFile = "LastValue.txt"
        self.sideMargin = 30
        self.buttonTop = 100        
        self.volume = 0.5
        self.volTrackWd = 300
        self.volTrackLeft = SCREEN_WIDTH/2 - self.volTrackWd/2
        self.volTrackTop = self.buttonTop - 50        
        self.length = 10     # Length of music track in sec - Nominal Value.
        self.position = 0   # Time Elapsed in sec
        self.progTrackWd = SCREEN_WIDTH - 2 * self.sideMargin
        self.progTrackLeft = self.sideMargin
        self.progTrackTop = self.buttonTop + 25

        # Relevant to scrolling sprites:
        self.txt = ""
        self.txtDx = -0.8
        self.txtDy = -0.4
        self.songBottomY = self.buttonTop + 150
        self.totSongs = 0
        self.songSpriteHt = 25

    def resetForFreshStart(self):
        # Get the index for last played song, from text file
        if os.path.exists(self.lastValueFile):
            with open(self.lastValueFile) as f:
                v = f.read()
                if len(v) > 0:
                    self.current_song_index = int(v)
                else:
                    self.current_song_index = 0
        else:
            self.current_song_index = 0
            with open(self.lastValueFile, "w+") as f:
                f.write("0")

        # List of music
        self.file_name_list = af.listFiles_by_scandir(
            "Music", ".mp3")[0]
        self.music_list = af.listFiles_by_scandir(
            "Music", ".mp3")[1]
        self.totSongs = len(self.file_name_list)
        
        if self.current_song_index < 0:
            self.current_song_index = self.totSongs - 1
        if self.current_song_index > (self.totSongs - 1):
            self.current_song_index = 0

        self.volKnob = None
        self.volBar = None
        self.volClick = False
        self.volTrack = None
        self.volLabel = None
        self.volValue = None
        self.progKnob = None
        self.progBar = None
        self.progClick = False
        self.progTrack = None
        self.bottomMaskSprite = None
        self.currentSongSprite = None
        self.songSpriteList = arcade.SpriteList()
        self.bar_list = arcade.SpriteList()
        arcade.set_background_color(BACK_COLOR)

    def makeCurrentSongSprite(self):
        """
        Boolean Parameters for bold & italic are not yet effective
        Inclusion of Bold or Italic property within font name
        (if permissible) results in getting desired results.

        width argument in arcade.draw_text() method can be
        omitted while creating a sprite object. However, it is
        needed for direct draw.
        """
        if not len(self.music_list) > 0:
            return
        
        start_x = 0
        start_y = self.buttonTop + 70
        fontSize = 26
        fontName = "GARA BOLD"
        
        txt = "Now Playing: " + str(1 + self.current_song_index) \
            + "-" + self.file_name_list[self.current_song_index]

        self.currentSongSprite = arcade.draw_text(
            txt, start_x, start_y, (0,0,255),
            font_size=fontSize, font_name=fontName,
            align="center")

        self.currentSongSprite.center_x = SCREEN_WIDTH / 2
        self.currentSongSprite.center_y = self.buttonTop + 80

    def makeSongSprites(self):
        """
        Set up scrolling text sprites for song names, duly numbered.
        """
        if not len(self.music_list) > 0:
            return
        
        n = 0
        y = SCREEN_HEIGHT
        for txt in self.file_name_list:
            sp = arcade.draw_text(
                str(n + 1) + "-" + txt, 0,
                SCREEN_HEIGHT - 60, (0,0,0),
                font_size=12, align="center")
            sp.guid = n + 1
            sp.height = self.songSpriteHt
            sp.center_x = SCREEN_WIDTH/2
            sp.center_y = self.songBottomY + n * 40
            self.songSpriteList.append(sp)
            n = n + 1

    def play_next_track(self):
        self.current_song_index += 1
        if self.current_song_index > len(self.music_list) - 1:
            self.current_song_index = 0
        self.play_song()
        self.makeCurrentSongSprite()

    def play_prev_track(self):
        self.current_song_index -= 1
        if self.current_song_index < 0:
            self.current_song_index = len(self.music_list) - 1
        self.play_song()
        self.makeCurrentSongSprite()

    def play_song(self):
        if not len(self.music_list) > 0:
            return
        
        # Stop what is currently playing.
        if self.music and self.current_player:
            self.music.stop(self.current_player)

        """
        Create an object instance of arcade.Sound() class
        class Sound:
            def __init__(self, file_name, streaming=False):
        """
        self.music = arcade.Sound(
            self.music_list[self.current_song_index],
            streaming=True)

        """
        Play the song. Sample def within arcade Sound class:
            def play(self, volume: float = 1.0,
                pan: float = 0.0, loop: bool = False) -> media.Player:

        This method returns an object of type arcade media.Player
        """
        self.current_player = self.music.play(self.volume)

        self.makeCurrentSongSprite()

        # Store song index in text file:
        with open("LastValue.txt", "w+") as f:
            f.write(str(self.current_song_index))
        
        # This is a quick delay. If we don't do this, our elapsed time is 0.0
        # and on_update will think the music is over and advance us to the next
        # song before starting this one.
        time.sleep(0.03)

    def toggle_play_pause(self):
        if not len(self.music_list) > 0:
            return

        if self.current_player:
            if self.current_player.playing:
                self.current_player.pause()
            else:
                self.current_player.play()

    def volume_up(self):
        self.volume = self.volume + 0.1
        if self.volume > 1:
            self.volume = 1
        self.current_player.volume = self.volume
        self.volBar.width = self.volume * self.volTrackWd
        self.volBar.left = self.volTrackLeft
        self.volKnob.center_x = self.volBar.right

    def volume_down(self):
        self.volume = self.volume - 0.1
        # Prevent zero value for self.volume - To avoid zero divn error
        # Min 2 out of 300 pixels (self.volBarMaxWd)
        if self.volume < 0.007:
            self.volume = 0.007
        self.current_player.volume = self.volume
        self.volBar.width = self.volume * self.volTrackWd
        self.volBar.left = self.volTrackLeft
        self.volKnob.center_x = self.volBar.right

    """
    stop method call within arcade.Sound class:
        def stop(self, player: media.Player) -> None:
            # Stop a currently playing sound.
            player.pause()
            player.delete()
            media.Source._players.remove(player)
    """

    def stop_play(self):
        if (len(self.music_list) > 0
                    and self.music
                    and self.current_player):
            self.music.stop(self.current_player)

    def pause_play(self):
        if len(self.music_list) > 0 and self.current_player:
            self.current_player.pause()

    def resume_play(self):
        if len(self.music_list) > 0 and self.current_player:
            self.current_player.play()

    def make_btnSprite(
                self, btn_x, btn_y, btn_wd=140, btn_ht=35,
                btn_clr=BTN_COLOR):
        sp = arcade.SpriteSolidColor(btn_wd, btn_ht, btn_clr)
        sp.left = btn_x
        sp.top = btn_y

        return sp

    # This text stripe function is meant for buttons
    def make_txtSprite(
                self, txt, txt_x, txt_y, label_width=140, 
                txt_clr=(0, 0, 0), fontSize=18):
        sp = arcade.draw_text(
                    txt, txt_x, txt_y, txt_clr, fontSize, 
                    width=label_width, align="center")
        return sp

    def setup(self):
        self.resetForFreshStart()
        
        self.makeSongSprites()

        self.makeCurrentSongSprite()

        # Make bottom mask sprite
        wd = SCREEN_WIDTH
        ht = 95
        self.bottomMaskSprite = arcade.SpriteSolidColor(
            wd, ht, (220,220,220))
        self.bottomMaskSprite.center_x = SCREEN_WIDTH/2
        self.bottomMaskSprite.center_y = self.songBottomY

        # Make bottom mask text stripe
        totSongs = len(self.file_name_list)
        start_x = 0
        start_y = self.songBottomY
        fontSize = 12
        fontName = "GARA BOLD"
        
        txt = "(Tot Tracks: " + str(len(self.file_name_list)) + ")  "
        txt = txt + "Play starts at the last song of prev session"
        txt = txt + "\nClick Any Of The Scrolling Songs - To Play It Out Of Turn"
        txt = txt + "\nClick Load Button For Adding Your "
        txt = txt + "Own Collection Of mp3 Files."
        txt = txt + "\nClick Clear Button To Empty Current List. "
        txt = txt + "Click Reset Button To Re-Load Original List."
        txt = txt + "\nKey Controls: Space Bar: Play/Pause, "
        txt = txt + "Up/Dn Arrow: Vol Up/Dn, Left/Right Arrow: "
        txt = txt + "Prev/Next Track"

        # width argument in arcade.draw_text() method can be
        # omitted while creating a sprite object. However, it is
        # needed for direct draw.
        self.bottomMaskTxtSprite = arcade.draw_text(
            txt, start_x, start_y, arcade.color.PURPLE,
            font_size=fontSize, font_name=fontName,
            align="center")

        self.bottomMaskTxtSprite.center_x = \
            self.bottomMaskSprite.center_x
        self.bottomMaskTxtSprite.center_y = \
            self.bottomMaskSprite.center_y

        """
        Create 7 button & text sprites for:
        Play/Pause,  Next, Prev, Load Files, Exit,
        Clear Music, Reset Music
        """
        self.textTop = self.buttonTop - 30
        spacing = 2 + (SCREEN_WIDTH - 2 * self.sideMargin) / 5
        bx = self.sideMargin
        by, ty = self.buttonTop, self.textTop
        
        sp = self.make_btnSprite(bx, by)
        sp.guid = "PP_Btn"
        self.button_list.append(sp)

        sp = self.make_txtSprite(
                "Play/Pause", bx, ty, txt_clr=(0,0,255))
        sp.guid = "PP_Txt"
        self.button_list.append(sp)

        sp = self.make_btnSprite(bx, by - 40)
        sp.guid = "Clear_Btn"
        self.button_list.append(sp)

        sp = self.make_txtSprite(
                "Clear Music", bx, ty - 40, txt_clr=(255,0,0))
        sp.guid = "Clear_Txt"
        self.button_list.append(sp)

        bx = bx + spacing        
        sp = self.make_btnSprite(bx, by)
        sp.guid = "Prev_Btn"
        self.button_list.append(sp)

        sp = self.make_txtSprite(
                "<< Prev", bx, ty)
        sp.guid = "Prev_Txt"
        self.button_list.append(sp)

        bx = bx + spacing        
        sp = self.make_btnSprite(bx, by)
        sp.guid = "Next_Btn"
        self.button_list.append(sp)

        sp = self.make_txtSprite(
                "Next >>", bx, ty)
        sp.guid = "Next_Txt"
        self.button_list.append(sp)

        bx = bx + spacing        
        sp = self.make_btnSprite(bx, by)
        sp.guid = "Files_Btn"
        self.button_list.append(sp)

        sp = self.make_txtSprite(
                "Load Songs", bx, ty)
        sp.guid = "Files_Txt"
        self.button_list.append(sp)

        bx = bx + spacing        
        sp = self.make_btnSprite(bx, by)
        sp.guid = "Exit_Btn"
        self.button_list.append(sp)

        sp = self.make_txtSprite(
                "<< Exit >>", bx, ty, txt_clr=(255,0,0))
        sp.guid = "Exit_Txt"
        self.button_list.append(sp)

        sp = self.make_btnSprite(bx, by - 40)
        sp.guid = "Reset_Btn"
        self.button_list.append(sp)

        sp = self.make_txtSprite(
                "Reset Music", bx, ty - 40, txt_clr=(0,0,255))
        sp.guid = "Reset_Txt"
        self.button_list.append(sp)

        # Make volume track sprite
        wd = self.volTrackWd
        ht = 10
        self.volTrack = arcade.SpriteSolidColor(
            wd, ht, (200,200,200))
        self.volTrack.left = self.volTrackLeft
        self.volTrack.top = self.volTrackTop
        self.bar_list.append(self.volTrack)

        # Make volume bar sprite
        wd = int(self.volume * self.volTrackWd)
        self.volBar = arcade.SpriteSolidColor(
            wd, ht, (100,100,100))
        self.volBar.center_x = self.volTrackLeft + wd/2
        self.volBar.top = self.volTrackTop
        self.bar_list.append(self.volBar)

        # Make volume knob sprite (radius: 10, color: Blue):
        radius = 10
        self.volKnob = arcade.SpriteCircle(radius, (0,0,255))
        self.volKnob.center_x = self.volBar.right
        self.volKnob.center_y = self.volTrack.center_y
        self.bar_list.append(self.volKnob)

        # Make volume label stripe:
        txt = "Vol:"
        labelWd = 120
        txt_x = self.volTrack.left - labelWd
        txt_y = self.volTrack.bottom
        txt_clr = (0,0,0)
        fontSize = 18
        self.volLabel = arcade.draw_text(
                    txt, txt_x, txt_y, txt_clr, fontSize, 
                    width=labelWd, align="right")
        self.volLabel.right = self.volTrackLeft - 2
        self.volLabel.center_y = self.volTrack.center_y
        self.bar_list.append(self.volLabel)

        # Make progress track sprite
        wd = self.progTrackWd
        ht = 10
        self.progTrack = arcade.SpriteSolidColor(
            wd, ht, (200,200,200))
        self.progTrack.left = self.progTrackLeft
        self.progTrack.top = self.progTrackTop
        self.bar_list.append(self.progTrack)

        # Make progress bar sprite
        wd = 2
        self.progBar = arcade.SpriteSolidColor(
            wd, ht, (100,100,100))
        self.progBar.center_x = self.progTrackLeft + wd/2
        self.progBar.center_y = self.progTrack.center_y
        self.bar_list.append(self.progBar)

        # Make progress knob sprite (radius: 10, color: Blue):
        wd, ht = 5, 16
        self.progKnob = arcade.SpriteSolidColor(
            wd, ht, (100,100,100))
        self.progKnob.center_x = self.progTrackLeft + wd/2
        self.progKnob.center_y = self.progTrack.center_y
        self.bar_list.append(self.progKnob)
        
        # Play the song
        if len(self.music_list) > 0:
            self.play_song()

    def on_draw(self):
        """ Render the screen. """
        arcade.start_render()

        arcade.set_background_color(BACK_COLOR)

        self.button_list.draw()

        if len(self.music_list) > 0 and self.music:
            self.bar_list.draw()
            
            # Display time elapsed and total
            txt_x = 0
            txt_y = self.buttonTop + 30
            fontName = "GARA"
            fontSize = 20
            txt = f"Time Elapsed (min:sec): " \
                + f"{int(self.position//60):02}:" \
                + f"{int(self.position%60):02}  of  " \
                + f"{int(self.length // 60):02}:" \
                + f"{int(self.length % 60):02}"
            arcade.draw_text(txt, txt_x, txt_y, arcade.color.BLACK,
                font_size=fontSize, font_name=fontName,
                width=SCREEN_WIDTH, align="center")

            # Display Volume Level
            txt_x = self.volTrack.right + 12  # Allow for vol knob radius
            txt_y  = self.volTrack.bottom - 5
            txt = f"{int(100 * self.volume):02} %"
            arcade.draw_text(txt, txt_x, txt_y, arcade.color.BLACK,
                font_size=fontSize, font_name=fontName,
                align="left")

            self.songSpriteList.draw()
            self.bottomMaskSprite.draw()
            self.bottomMaskTxtSprite.draw()

            if self.currentSongSprite:
                self.currentSongSprite.draw()

    def on_update(self, dt):
        if not len(self.music_list) > 0:
            return
        
        for sp in self.songSpriteList:
            sp.center_y = sp.center_y + self.txtDy
            if int(sp.guid) - 1 == self.current_song_index:
                sp.height = 1.8 * self.songSpriteHt
            else:
                sp.height = self.songSpriteHt
            
            if sp.center_y < self.songBottomY:
                sp.center_y = self.songBottomY + self.totSongs * 40

        if self.currentSongSprite.width > \
            SCREEN_WIDTH - 2 * self.sideMargin:
            self.currentSongSprite.center_x = \
                self.currentSongSprite.center_x + self.txtDx           
            if (self.currentSongSprite.left
                        > self.sideMargin) or (
                        self.currentSongSprite.right
                        < SCREEN_WIDTH - self.sideMargin):
                self.txtDx = - self.txtDx
        else:
            self.currentSongSprite.center_x = SCREEN_WIDTH / 2
        
        if self.music and self.current_player:
            self.position = self.music.get_stream_position(
                self.current_player)
            self.length = self.music.get_length()

            if self.position >= 0.99 * self.length:
                self.play_next_track()

            # Pre-positioning of expanding sprite via its center_x
            # (instead of post-positioning after expansion, via its left
            # property), is found to give more consistent display
            dx = (self.progTrackWd * self.position) / self.length
            self.progKnob.center_x = self.progTrackLeft + dx
            self.progBar.center_x = self.progTrackLeft + dx/2
            self.progBar.width = dx

    def on_key_press(self, symbol, modifiers):
        """ Called whenever a key is released. """
        if symbol == arcade.key.SPACE:
            self.toggle_play_pause()
        elif symbol == arcade.key.LEFT:
            self.play_prev_track()
        elif symbol == arcade.key.RIGHT:
            self.play_next_track()
        elif symbol == arcade.key.UP:
            self.volume_up()
        elif symbol == arcade.key.DOWN:
            self.volume_down()

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        :param float x: x position of the mouse
        :param float y: y position of the mouse
        :param int button: What button was hit. One of:
            arcade.MOUSE_BUTTON_LEFT,
            arcade.MOUSE_BUTTON_RIGHT,
            arcade.MOUSE_BUTTON_MIDDLE
        :param int modifiers:
            Bitwise 'and' of all modifiers (shift, ctrl, num lock)
            pressed during this event. See :ref:`keyboard_modifiers`.
        """
        if self.volKnob.collides_with_point((x,y)):
            self.volClick = True

        if self.progKnob.collides_with_point((x,y)):
            self.progClick = True

        if  x > (self.volTrackLeft + 2) and (
            self.volBar.collides_with_point((x,y))
            or self.volTrack.collides_with_point((x,y))):
            dx = x - self.volTrackLeft
            self.volBar.center_x = self.volTrackLeft + dx/2
            self.volBar.width = dx
            self.volKnob.center_x = x
            self.volume = self.volBar.width/self.volTrackWd
            self.current_player.volume =  self.volume

        """
        if  x > (self.progTrackLeft + 2) and (
            self.progBar.collides_with_point((x,y))
            or self.progTrack.collides_with_point((x,y))):
            dx = x - self.progTrackLeft
            self.progBar.center_x = self.progTrackLeft + dx/2
            self.progBar.width = dx
            self.progKnob.center_x = x
            self.position = dx / self.progTrackWd
            #self.current_player.position =  self.position  # No Effect
            #self.current_player.time =  self.position  # Not Allowed
            # set_stream_position() method not yet available in arcade
            #self.music.set_stream_position(self.position)
        """
        
        hit_sprites = arcade.get_sprites_at_point(
            (x, y), self.button_list)
        hit_list = [sp.guid for sp in hit_sprites]

        if "PP_Btn" in hit_list or "PP_Txt" in hit_list:
            self.toggle_play_pause()
        elif "Prev_Btn" in hit_list or "Prev_Txt" in hit_list:
            self.play_prev_track()
        elif "Next_Btn" in hit_list or "Next_Txt" in hit_list:
            self.play_next_track()
        elif "Files_Btn" in hit_list or "Files_Txt" in hit_list:
            af.loadSelectedFiles("Music", ".mp3")
            time.sleep(0.2)
            if self.current_player:
                self.current_player.pause()
            self.setup()
        elif "Exit_Btn" in hit_list or "Exit_Txt" in hit_list:
            if self.current_player:
                self.current_player.pause()
                self.stop_play()
            arcade.close_window()
        elif "Clear_Btn" in hit_list or "Clear_Txt" in hit_list:
            if self.current_player:
                self.current_player.pause()
            af.clearFolder("Music")
            self.setup()
        elif "Reset_Btn" in hit_list or "Reset_Txt" in hit_list:
            # Clear existing music files:
            if self.current_player:
                self.current_player.pause()
            af.clearFolder("Music")
            self.setup()

            # Load files from MusicLib folder
            af.loadFilesFromFolder("MusicLib", "Music")
            time.sleep(0.2)
            self.setup()
        
        hit_sprites = arcade.get_sprites_at_point(
            (x, y), self.songSpriteList)
        if len(hit_sprites) > 0:
            sp = hit_sprites[0]
            index = int(sp.guid) - 1
            
            if not index == self.current_song_index:
                self.current_song_index = index
                self.play_song()
                
                for s in self.songSpriteList:
                    s.height = self.songSpriteHt                    
                
                sp.height = 1.8 * self.songSpriteHt

    def on_mouse_release(self, x: float, y: float, button: int,
                         modifiers: int):
        """
        :param float x:
        :param float y:
        :param int button:
        :param int modifiers:
            Bitwise 'and' of all modifiers (shift, ctrl, num lock)
            pressed during this event. See :ref:`keyboard_modifiers`.
        """
        self.volClick = False
        self.progClick = False

    def on_mouse_drag(
                self, x: float, y: float, dx: float, dy: float,
                buttons: int, modifiers: int):
        """
        :param float x: x position of mouse
        :param float y: y position of mouse
        :param float dx: Change in x since the last time this method
        was called
        :param float dy: Change in y since the last time this method
        was called
        :param int buttons: Which button is pressed
        :param int modifiers:
            Bitwise 'and' of all modifiers (shift, ctrl, num lock)
            pressed during this event. See :ref:`keyboard_modifiers`.
        """
        if self.volClick and x > (self.volTrackLeft + 2):
            if x > self.volTrack.right:
                x = self.volTrack.right
            self.volKnob.center_x = x
            dx = x - self.volTrack.left
            self.volBar.center_x = self.volTrackLeft + dx/2
            self.volBar.width = dx
            self.volume = dx/self.volTrackWd
            self.current_player.volume =  self.volume

#===================
def main():
    """ Main method """
    gp = GamePlay()
    gp.setup()
    gp.maximize()
    arcade.run()

#===================
if __name__ == "__main__":
    main()
