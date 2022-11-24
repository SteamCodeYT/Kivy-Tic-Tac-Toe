from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window

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

#define the game Board
class Board(GridLayout):
    def __init__(self,**kwargs):
        super(Board, self).__init__(**kwargs)

        #an array to represent the board
        self.boardArray = [""] * 9
    
    def updateBoardArray(self):
        for index in range(9):
            #create an id to represent the current cell
            id = "cell" + str(index)
            self.boardArray[index] = self.ids.get(id).text
        
        return self.boardArray
    
    #checks whether the passed player has won
    def hasWon(self, player):
        #check rows
        for i in range(0, 9, 3): #go from 0 to 9 and step 3
            if(self.boardArray[i] == self.boardArray[i+1] and self.boardArray[i] == self.boardArray[i+2] and self.boardArray[i] == player):
                print(player + " has won")
                return True
        
        #check columns
        for i in range(3):
            if(self.boardArray[i] == self.boardArray[i+3] and self.boardArray[i] == self.boardArray[i+6] and self.boardArray[i] == player):
                print(player + " has won")
                return True
        
        #check diagonals
        if(self.boardArray[0] == self.boardArray[4] and self.boardArray[0] == self.boardArray[8] and self.boardArray[0] == player):
                print(player + " has won")
                return True
        if(self.boardArray[2] == self.boardArray[4] and self.boardArray[2] == self.boardArray[6] and self.boardArray[2] == player):
                print(player + " has won")
                return True

        #print("no winner")
        return False

#define the game Cell
class Cell(Button):
    def __init__(self, **kwargs):
        super(Cell, self).__init__(**kwargs)

        #initialize the object variables
        self.player = "-"
        self.empty = True
    
    def on_release(self):
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
                screen.ids.turnLabel.text = "Turn: " + screen.getCurrentTurn() #change the text of the Label to reflect the current player

class MainApp(App):
    def build(self):
        #get the window size
        window_sizes = Window.size
        print(str(window_sizes))

        #create screen manager
        sm = ScreenManager()
        sm.add_widget(MainScreen(name="mainScreen"))

        return sm


if __name__ == '__main__':
    app = MainApp()
    app.run()