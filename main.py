from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.config import Config
from kivy.uix.anchorlayout import AnchorLayout

# --- this changes the app's default background --- #
#Window.clearcolor = (1, 1, 1, 1.0)
Window.size = (300, 600)

#define the MainScreen
class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

        #define the game variables
        self.currentTurn = "X"
    
    def getCurrentTurn(self):
        return self.currentTurn
    
    def changeTurn(self):
        if(self.currentTurn == "X"):
            self.currentTurn = "O"
        else:
            self.currentTurn = "X"

        print(self.currentTurn)
        return self.currentTurn
    
    def changeTurnToX(self):
        self.currentTurn = "X"
    
    def changeTurnToO(self):
        self.currnetTurn = "O"
    
    def updateTurnLabel(self, updatedText):
        self.ids.turnLabel.update(updatedText)    

class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)

#define the turn Label
class TurnLabel(Label):
    def __init__(self,**kwargs):
            super(TurnLabel, self).__init__(**kwargs)
    
    def update(self, updatedText):
        self.text = updatedText
        return self.text

#define the restart button
class RestartButton(Button):
    def __init__(self,**kwargs):
            super(RestartButton, self).__init__(**kwargs)

    def on_release(self):
        screen = self.parent.parent.parent
        screen.ids.board.clearCells()
        screen.changeTurnToX()
        screen.updateTurnLabel("Turn: " + screen.getCurrentTurn())

#define the settings button
class SettingsButton(Button):
    def __init__(self,**kwargs):
            super(SettingsButton, self).__init__(**kwargs)    
    
    def on_release(self):
        screen = self.parent.parent.parent
        screen.manager.current = "settingsScreen"

#define the game Board
class Board(GridLayout):
    def __init__(self,**kwargs):
        super(Board, self).__init__(**kwargs)

        #an array to represent the board
        self.boardArray = [""] * 9
        self.winIndices = [None] * 3
    
    #updates the board array to accurately reflect the board
    def updateBoardArray(self):
        for index in range(9):
            #create an id to represent the current cell
            id = "cell" + str(index)
            self.boardArray[index] = self.ids.get(id).text
        
        return self.boardArray
    
    #clears each of the cells of their content and resets the color
    def clearCells(self):
        for index in range(9):
            #create an id to represent the current cell
            id = "cell" + str(index)
            self.ids.get(id).clear()
            self.ids.get(id).changeBackgroundColor(218, 218, 218, 0.3)

        return(self.updateBoardArray())
    
    #checks whether the passed player has won
    def hasWon(self, player):
        #check rows
        for i in range(0, 9, 3): #go from 0 to 9 and step 3
            if(self.boardArray[i] == self.boardArray[i+1] and self.boardArray[i] == self.boardArray[i+2] and self.boardArray[i] == player):
                print(player + " has won")
                self.winIndices = [i, i+1, i+2]
                return True
        
        #check columns
        for i in range(3):
            if(self.boardArray[i] == self.boardArray[i+3] and self.boardArray[i] == self.boardArray[i+6] and self.boardArray[i] == player):
                print(player + " has won")
                self.winIndices = [i, i+3, i+6]
                return True
        
        #check diagonals
        if(self.boardArray[0] == self.boardArray[4] and self.boardArray[0] == self.boardArray[8] and self.boardArray[0] == player):
                print(player + " has won")
                self.winIndices = [0, 4, 8]
                return True
        if(self.boardArray[2] == self.boardArray[4] and self.boardArray[2] == self.boardArray[6] and self.boardArray[2] == player):
                print(player + " has won")
                self.winIndices = [2, 4, 6]
                return True

        #nobody has won
        return False
    
    def updateWinningCells(self, player):
        for index in self.winIndices:
            id = "cell" + str(index)
            self.ids.get(id).changeBackgroundColor(255, 0, 0, 0.3)

#define the game Cell
class Cell(Button):
    def __init__(self, **kwargs):
        super(Cell, self).__init__(**kwargs)

        #initialize the object variables
        self.player = ""
        self.empty = True
    
    #changes the background color of the cell to the specified rgba value
    def changeBackgroundColor(self, r, g, b, a):
        self.background_color = (r/255, g/255, b/255, a)
    
    #will make the cell empty
    def clear(self):
        self.player = ""
        self.empty = True
        self.text = self.player
    
    def on_release(self):
        print(Window.size[0])
        print(Window.size[1])
        screen = self.parent.parent.parent #the screen that the cell is in
        gridLayout = self.parent.parent #the gridLayout that the cell is in

        #if the current cell is empty and nobody has already won the game
        if(self.empty and not self.parent.hasWon(screen.getCurrentTurn())):
            self.text = screen.getCurrentTurn() #change the text of the cell to the current turn
            
            #the cell is no longer empty
            self.empty = False
            self.parent.updateBoardArray() #update the array that represents the board

            #if nobody has won the game, change the current player
            if not self.parent.hasWon(screen.getCurrentTurn()): #check whether anyone has won
                #change to the next player
                screen.changeTurn() #change the turn
                screen.updateTurnLabel("Turn: " + screen.getCurrentTurn()) #change the text of the Label to reflect the current player

            #if somebody has won, change the color of the winning cells
            if self.parent.hasWon(screen.getCurrentTurn()):
                self.parent.updateWinningCells(screen.getCurrentTurn())
                screen.ids.turnLabel.update(screen.getCurrentTurn() + " has won!")

class MainApp(App):
    def build(self):
        #get the window size
        window_sizes = Window.size
        print(str(window_sizes))

        #create screen manager
        sm = ScreenManager()
        sm.add_widget(MainScreen(name="mainScreen"))
        sm.add_widget(SettingsScreen(name="settingsScreen"))

        return sm


if __name__ == '__main__':
    app = MainApp()
    app.run()