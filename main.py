from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager, WipeTransition
from TennisScore import AdvantageType, Match, MatchType, PlayerNames, SetLength, TieBreakStart

class MainWindow(BoxLayout):
    pass

kv = Builder.load_file("style.kv")

class MainApp(App):
    def build(self):
        return MainWindow()

incontro = Match(
                player1Name = "Emanuele Gravina"
                , player2Name = "Novak Djokovic"
                , matchType = MatchType.On3SetsLTB
                , setLength = SetLength.On4Games
                , advantageType = AdvantageType.NoAdv
                , tieBreakStart = TieBreakStart.On3All
                , startToServe = PlayerNames.Player1.value
                ) 

print(f"Incontro di tennis tra {incontro.playerNames[PlayerNames.Player1.value]} e {incontro.playerNames[PlayerNames.Player2.value]}")
print("Inizio partita..")
print("Alla battuta:", incontro.playerNames[incontro.startToServe])
incontro.newPoint(PlayerNames.Player1.value)
print(incontro.getVisualScore())