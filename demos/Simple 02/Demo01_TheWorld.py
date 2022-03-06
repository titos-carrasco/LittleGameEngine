from lge.Engine import Engine
from lge.Sprite import Sprite
from lge.Canvas import Canvas


class MiJuego():
    def __init__( self ):
        # creamos el juego
        Engine.Init( (800, 440), "The World" )
        Engine.SetOnUpdate( self.MainUpdate )

        # activamos la musica de fondo
        Engine.LoadSound( "fondo", "../sounds/happy-and-sad.wav" )
        Engine.SetSoundVolume( "fondo", 0.5 )
        Engine.PlaySound( "fondo", loop=-1 )

        # cargamos los recursos que usaremos
        Engine.LoadImage( "fondo", "../images/Backgrounds/FreeTileset/Fondo.png", (800,440) )
        Engine.LoadImage( "heroe", "../images/Swordsman/Idle/Idle_00*.png", 0.08 )
        Engine.LoadImage( "mute", "../images/icons/sound-*.png" )
        Engine.LoadTTFFont( "backlash", 40, "../fonts/backlash.ttf" )
        Engine.LoadTTFFont( "monospace", 16, "../fonts/FreeMono.ttf" )

        # agregamos el fondo
        fondo = Sprite( "fondo", (0,0), "fondo" )
        Engine.AddGObject( fondo, 0 )

        # agregamos un Sprite
        heroe = Sprite( "heroe", (226,142), "Heroe" )
        Engine.AddGObject( heroe, 1 )

        # agregamos un texto con transparencia
        canvas = Canvas( (200,110), (400,200) )
        canvas.Fill( (0,0,0,40) )
        canvas.DrawText( "Little Game Engine", (40,70), "backlash", (30,30,30) )
        Engine.AddGObjectGUI( canvas )

        # agregamos la barra de info
        infobar = Canvas( (0,420), (800,20), "infobar" )
        Engine.AddGObjectGUI( infobar )

        mute = Sprite( "mute", (8,423), "mute" )
        mute.SetShape( "mute", 1 )
        Engine.AddGObjectGUI( mute )

        # un poco mas avanzado
        heroe.OnUpdate = lambda dt: heroe.NextShape(dt,0.060)

    def MainUpdate( self, dt ):
        # abortamos con la tecla Escape
        if( Engine.KeyUp( Engine.CONSTANTS.K_ESCAPE ) ):
            Engine.Quit()

        # mostramos info
        fps = Engine.GetFPS()
        fps = "FPS: %07.2f" % fps

        ngobjs = len( Engine.GetGObject( "*") )
        ngobjs = "gObjs: %03d" % ngobjs

        mx, my = Engine.GetMousePosition()
        mb1, mb2, mb3 = Engine.GetMouseButtons()
        minfo = "Mouse: (%3d,%3d) (%d,%d,%d)" % ( mx, my, mb1, mb2, mb3 )

        infobar = Engine.GetGObject( "infobar" )
        infobar.Fill( (0,0,0,20) )
        infobar.DrawText( fps + " - " + ngobjs + " - " + minfo, (150,0), "monospace", (0,0,0) )

        mp = Engine.GetMousePressed( 1 )
        if( mp ):
            mx, my = mp

            mute = Engine.GetGObject( "mute")
            iname, idx = mute.GetCurrentShape()
            if( idx ):
                Engine.SetSoundVolume( "fondo", 0 )
                mute.SetShape( iname, 0 )
            else:
                Engine.SetSoundVolume( "fondo", 0.5 )
                mute.SetShape( iname, 1 )

    # main loop
    def Run( self ):
        Engine.Run( 60 )


# -- show time
game = MiJuego()
game.Run()
