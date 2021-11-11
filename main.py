from TennisScore import AdvantageType, Match, MatchType, PlayerNames, SetLength, TieBreakStart

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