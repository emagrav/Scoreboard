from enum import Enum

class DefaultPlayerNames(Enum):
  Player1 = 1
  Player2 = 2

class MatchType(Enum):
  On3Sets = 1
  On3SetsLTB = 2
  On5Sets = 3

class SetLength(Enum):
  On4Games = 4
  On6Games = 6

class AdvantageType(Enum):
  ClassicAdv = 1 # classic advantages
  NoAdv = 2 # killer point
  NoAdvAfter1stDeuce = 3 # killer point after 1st deuce

class TieBreakStart(Enum):
  On6All = 6
  On4All = 4
  On3All = 3

class SetMode(Enum):
  NormalGamesSet = 1 
  LongTieBreakSet = 9

class GameMode(Enum):
  StandardGame = 40 # 15, 30, 40, game
  TieBreakGame = 6
  LongTieBreakGame = 9

class Game: 
  gameMode = None
  advantageType = None
  playerWonThePoint = 0 # può valere 1 o 2
  playerLoseThePoint = 0 # vale l'altro valore della variabile precedente
  playedPoints = 0 # totale corrente dei punti giocati nel game
  score = [] # es. [40, 15] ovvero [50, 40] 50 è da considerarsi vantaggio , oppure [9, 8] in un tie break
  
  def __init__(self, gameMode = GameMode.StandardGame, advantageType = AdvantageType.ClassicAdv) -> None:
    self.gameMode = gameMode
    self.advantageType = advantageType
    self.score = [0, 0]  # si parte da 0 a 0

  def getVisualScore(self):
    # punteggio nel game es. "40-15" oppure "0-4" nel tie break
    s = self.score
    primo = ""
    secondo = ""

    if s[0] > s[1] and s[0] > 40:
      primo = "Adv"
      secondo = "40"
    elif s[1] > s[0] and s[1] > 40:
      primo = "40"
      secondo = "Adv"
    elif s[0] == s[1] and s[0] > 40:
      primo = "40"
      secondo = "40"
    else:
      primo = str(s[0])
      secondo = str(s[1])
    return primo + "-" + secondo

  def hasWonTheGame(self):
    i = self.playerWonThePoint - 1
    j = self.playerLoseThePoint - 1

    # verifico se è un game normale e non un (long) tie break
    if self.gameMode == GameMode.StandardGame:
      # verifico quindi se il vincitore del punto ha superato il punteggio di 40
      if self.score[i] > 40:
        # se vige la regola del no-adv, allora il game l'ha vinto
        if self.advantageType == AdvantageType.NoAdv:
          return True
        # se vige la regola del no-adv dopo il primo deuce e supera quindi il punteggio di 50, allora il game l'ha vinto
        if self.advantageType == AdvantageType.NoAdvAfter1stDeuce and self.score[i] > 50:
            return True
        # se invece vige la regola classica dei vantaggi, il game lo vince se c'è una differenza di 20 col punteggio dell'avversario
        if self.score[i] - self.score[j] > 10:
          return True
    else:
      # caso tie break o long tie break
      # il game lo vince se c'è una differenza di 2 col punteggio dell'avversario
      if self.score[i] > self.gameMode.value and self.score[i] - self.score[j] > 1:
          return True

    return False

  def newPoint(self, player): 
    """
    player vale 1 o 2 a seconda del giocatore che ha fatto il punto
    """
    self.playerWonThePoint = player
    self.playerLoseThePoint = 2 if self.playerWonThePoint == 1 else 1

    i = self.playerWonThePoint - 1
    j = self.playerLoseThePoint - 1

    self.playedPoints += 1 # incremento il numero di punti giocati nel game

    # verifico se la modalità del game corrente è standard
    if self.gameMode == GameMode.StandardGame:
      # in tal caso aggiungo il 15 al giocatore che ha vinto il punto (che possono come sappiamo valere anche solo 10 punti)
      self.score[i] += 15 if self.score[i] <= 15 else self.score[i] + 10
    else: 
      # caso tie break o long tie break: aggiungo un semplice punticino
      self.score[i] += 1
    
    pass

class Set:
  """
  Gestisce tutto quanto di competenza del set
  """
  setMode = None
  setLength = None
  tieBreakStart = None
  advantageType = None
  score = [0, 0] # es. [4, 2] oppure [6, 6]
  visualScore = "" # punteggio nel set es. "4-2" oppure "6-6"
  totGames = 0 # totale corrente dei game giocati
  game = None # il riferimento al game corrente

  def __str__(self) -> str:
    s = "-".join(str(n) for n in self.score)
    return s

  def __init__(self, setMode = SetMode.NormalGamesSet, setLength = SetLength.On6Games, tieBreakStart = TieBreakStart.On6All, advantageType = AdvantageType.ClassicAdv): 
    
    self.setMode = setMode
    self.setLength = setLength
    self.tieBreakStart = tieBreakStart
    self.advantageType = advantageType

     # parte il primo gioco del set
    self.newGame()

  def newPoint(self, player):
    self.game.newPoint(player)

  def newGame(self):
    '''
    dopo aver capito che tipo di game far partire, lo istanzia
    '''
    if self.setMode == SetMode.LongTieBreakSet:
      self.game = Game(GameMode.LongTieBreakGame)
    else:
      # caso set normale (potrebbe essere a 6 o a 4 game quindi)
      # verifico quindi quanti game sono necessari per vincere
      if (self.setLength == SetLength.On6Games and self.tieBreakStart == TieBreakStart.On6All and self.score == [6, 6]) \
        or (self.setLength == SetLength.On4Games and ((self.tieBreakStart == TieBreakStart.On3All and self.score == [3, 3])  or (self.tieBreakStart == TieBreakStart.On4All and self.score == [4, 4]))):   
          # istanzio il nuovo game con punti da tie break
          self.game = Game(GameMode.TieBreakGame)
      else:
        # se non devo istanziare un tie break, istanzio il nuovo game con punti standard e passando il tipo di vantaggi definito per il match
        self.game = Game(GameMode.StandardGame, advantageType = self.advantageType)
    
    # incremento il numero di game giocati nel set
    self.totGames += 1

  def hasWonTheSet(self):
     # se nessuno ha ancora vinto un punto, restituisco ovviamente False
    if self.game.playerWonThePoint == 0:
      return False

    i = self.game.playerWonThePoint - 1
    j = self.game.playerLoseThePoint - 1

    # se è un game standard
    if self.game.gameMode == GameMode.StandardGame:
      # verifico se la differenza è di 2 game qualora raggiunto o superato il numero di game per vincere il set 
      if (self.game.score[i] >= self.setLength.value) and (self.game.score[i] - self.game.score[j] == 2):
        return True
    
    # se è un tie break vince il set così come se è un long tie break (in questo caso ha vinto il match)
    if self.game.gameMode == GameMode.TieBreakGame or self.game.gameMode == GameMode.LongTieBreakGame:
      return True
    
    return False

class Match:
  '''
  Il match di tennis
  '''
  player1Name = ""
  player2Name = ""
  matchType = None
  setLength = None
  advantageType = None
  tieBreakStart = None
  startToServe = 0

  set = None # il set corrente
  sets = [] # Lista dei set del match

  def __init__(self, player1Name = DefaultPlayerNames.Player1.name, player2Name = DefaultPlayerNames.Player2.name, matchType = MatchType.On3Sets, setLength = SetLength.On6Games, advantageType = AdvantageType.ClassicAdv, tieBreakStart = TieBreakStart.On6All, startToServe = 1):
    '''
    gli input servono per definire le regole del punteggio
    '''
    # cerco contraddizioni nei parametri passati
    if tieBreakStart == TieBreakStart.On6All and setLength != SetLength.On6Games:
      raise Exception("Il tie break non può iniziare sul 6 pari se il numero di game in un set è inferiore") 
    if tieBreakStart == TieBreakStart.On4All and setLength == SetLength.On6Games:
      raise Exception("Il tie break non può iniziare sul 4 pari se il numero di game in un set è impostato a 6") 
    if tieBreakStart == TieBreakStart.On3All and setLength == SetLength.On6Games:
      raise Exception("Il tie break non può iniziare sul 3 pari se il numero di game in un set è impostato a 6") 
    
    self.player1Name = player1Name
    self.player2Name = player2Name
    self.matchType = matchType
    self.setLength = setLength
    self.advantageType = advantageType
    self.tieBreakStart = tieBreakStart
    self.startToServe = startToServe
    
    self.newSet() # parte il primo set e il primo game ovviamente
  
  def getVisualScore(self):
    s = ""
    for set in self.sets:
      s += str(set)
    s += " [" + self.set.game.getVisualScore() + "]"

    return s
  
  def newSet(self):
    # se i set finora giocati sono 2 e se il match prevede il long tie break al posto del terzo set
    if len(self.sets) == 2 and self.matchType == MatchType.On3SetsLTB:
        self.set = Set(setMode=SetMode.LongTieBreakSet)
    else:
      # nuovo set = set normale
      self.set = Set(setMode=SetMode.NormalGamesSet, setLength = self.setLength, tieBreakStart = self.tieBreakStart, advantageType = self.advantageType)
    
    self.sets.append(self.set)

  def hasWonTheMatch(self):
    '''
    dando per scontato che abbia vinto il set, verifico che il player non abbia vinto anche il match
    '''
    i = self.set.game.playerWonThePoint - 1
    j = self.set.game.playerLoseThePoint - 1

    # vinto il match?
    # se il numero di set vinti coincide con quello del numero di set max definito inizialmente
    if len(self.sets) == self.matchType.value:
      # fine partita, vinta
      return True
    # se invece non è stato raggiunto ancora il limite ma ci sono due set di differenza per match a 3 set ovvero tre set per match a 5 set
    if (self.set.score[i] - self.set.score[j] == 2) and (self.matchType.value == 3): 
        return True
    if (self.set.score[i] - self.set.score[j] == 3) and (self.matchType.value == 5): 
        return True
    
    return False  

  def newPoint(self, player) -> bool:    
    '''
    Aggiunge un punto al giocatore in input

      player -> Il giocatore che ha fatto il punto. Può valere 1 o 2
      return -> bool: True se ultimo punto del match
    '''
    # aggiungo un punto nel game al vincitore del punto
    self.set.newPoint(player)

    i = self.set.game.playerWonThePoint - 1
    j = self.set.game.playerLoseThePoint - 1
    
    # vinto il game?
    if self.set.game.hasWonTheGame():
      self.set.score[i] += 1
      if self.set.hasWonTheSet():
        if self.hasWonTheMatch():
          return True 
        # se il match non si è chiuso ma ha vinto solo un set
        self.newSet()
      # se il set non si è chiuso ma ha vinto solo un game
      self.set.newGame()

    return False
 
#########   
## inizio
#########
incontro = Match(player1Name = "Andrea", player2Name = "Emanuele", matchType = MatchType.On3SetsLTB, setLength = SetLength.On4Games, advantageType = AdvantageType.NoAdv, tieBreakStart = TieBreakStart.On3All, startToServe = 1)
incontro.newPoint(1)
print(incontro.getVisualScore())