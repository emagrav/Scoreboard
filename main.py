from TennisScore import AdvantageType, Match, MatchType, SetLength, TieBreakStart

incontro = Match(
                player1Name = "Emanuele"
                , player2Name = "Novak"
                , matchType = MatchType.On3SetsLTB
                , setLength = SetLength.On4Games
                , advantageType = AdvantageType.NoAdv
                , tieBreakStart = TieBreakStart.On3All
                , startToServe = 1
                )

incontro.newPoint(1)
print(incontro.getVisualScore())