import kivy
import copy
import random

from kivy.config import Config
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Ellipse, Line, Color
from kivy.properties import NumericProperty

Config.set('graphics', 'resizable', False)
window = Window.size

class GameCell(Widget):
    toggle = NumericProperty(0)
    status =  0

    def __init__(self, **kwargs):
        super(GameCell, self).__init__(**kwargs)

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            if self.status == 0:
                self.status = 1
                self.toggle += 1


class Board:
    cells = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    isPlayer = None
    root = None
    turn = None     # True면 플레이어턴, False면 인공지능 턴
    value = None    # 0이면 무승부, 1이면 플레이어 승리각, 2이면 인공지능 승리각
    child = []    # 이 다음턴에 가능한 경우의 수가 모두 온다.

    def __init__(self, isPlayer, root, cells, turn):
        self.root = root
        self.cells = copy.deepcopy(cells)
        self.turn = copy.deepcopy(turn)
        self.isPlayer = isPlayer

        # isEnd() 호출해서 결과에 따라 분기한다.
        # 게임이 끝나지 않으면 칸마다 해당 플레이어의 값을 넣으면서 child 생성한다.
        # 승부가 나면 value를 결정한다.
        # 무승부면 value 값을 0으로 결정한다.
        if not self.isPlayer:
            result = self.isEnd()
            if type(result) == int:
                if result == 0:         # 승부가 나지 않았을 때
                    self.child = []

                    for i in range(0, len(self.cells)):
                        for j in range(0, len(self.cells[i])):
                            if self.cells[i][j] == 0:
                                if self.turn == True:
                                    self.cells[i][j] = 2
                                else:
                                    self.cells[i][j] = 1
                                self.child.append(Board(False, self, self.cells, not self.turn))
                                self.cells[i][j] = 0

                    # 이제 자식 노드들의 값을 체크해서 유리한 다음 수를 결정한다.
                    for i in range(0, len(self.child)):
                        isWin = list(filter(lambda item: item.value == 2, self.child))
                        isDraw = list(filter(lambda item : item.value == 0, self.child))
                        isDefeat = list(filter(lambda item : item.value == 1, self.child))
                        if self.turn == True:   #현재 턴이 플레이어가 둔 상태
                            if len(isWin) > 0:
                                self.value = 2
                                break
                            elif len(isDraw) > 0:
                                self.value = 0
                                break
                            elif len(isDefeat) > 0:
                                self.value = 1
                                break
                        else:                   #현재 턴이 인공지능이 둔 상태
                            if len(isDefeat) > 0:
                                self.value = 1
                                break
                            elif len(isDraw) > 0:
                                self.value = 0
                                break
                            elif len(isWin) > 0:
                                self.value = 2
                                break
                elif result == 2:       # 승부가 무승부일 때
                    self.value = 0
            elif result[0] == 1:        # 승부가 났음.
                if result[1] == 3:      # 플레이어가 이기는 경우
                    self.value = 1
                else:                   # 인공지능이 이기는 경우
                    self.value = 2

    # 빈칸이 있는지 체크하는 함수
    def isEmpty(self):
        emptyCell = list(filter(lambda item : item[0] == 0 or item[1] == 0 or item[2] == 0, self.cells))

        if len(emptyCell) > 0:
            return True
        else:
            return False

    # 게임이 끝나지 않으면 (0) 반환, 승부가 나면 (1, Int) 형태로 반환, 무승부이면 (2) 형태로 반환
    def isEnd(self):
        if self.cells[0][0] == self.cells[0][1] == self.cells[0][2]:
            firstRowSum = sum(self.cells[0])
            if firstRowSum == 3 or firstRowSum == 6:
                return (1, firstRowSum)
        if self.cells[1][0] == self.cells[1][1] == self.cells[1][2]:
            secondRowSum = sum(self.cells[1])
            if secondRowSum == 3 or secondRowSum == 6:
                return (1, secondRowSum)
        if self.cells[2][0] == self.cells[2][1] == self.cells[2][2]:
            thirdRowSum = sum(self.cells[2])
            if thirdRowSum == 3 or thirdRowSum == 6:
                return (1, thirdRowSum)

        if self.cells[0][0] == self.cells[1][0] == self.cells[2][0]:
            firstColSum = self.cells[0][0] + self.cells[1][0] + self.cells[2][0]
            if firstColSum == 3 or firstColSum == 6:
                return (1, firstColSum)
        if self.cells[0][1] == self.cells[1][1] == self.cells[2][1]:
            secondColSum = self.cells[0][1] + self.cells[1][1] + self.cells[2][1]
            if secondColSum == 3 or secondColSum == 6:
                return (1, secondColSum)
        if self.cells[0][2] == self.cells[1][2] == self.cells[2][2]:
            thirdColSum = self.cells[0][2] + self.cells[1][2] + self.cells[2][2]
            if thirdColSum == 3 or thirdColSum == 6:
                return (1, thirdColSum)

        if self.cells[0][0] == self.cells[1][1] == self.cells[2][2]:
            leftSideSum = self.cells[0][0] + self.cells[1][1] + self.cells[2][2]
            if leftSideSum == 3 or leftSideSum == 6:
                return (1, leftSideSum)
        if self.cells[2][0] == self.cells[1][1] == self.cells[0][2]:
            rightSideSum = self.cells[2][0] + self.cells[1][1] + self.cells[0][2]
            if rightSideSum == 3 or rightSideSum == 6:
                return (1, rightSideSum)

        if not self.isEmpty():
            return (2)

        return (0)

class GameBoard(GridLayout):
    board = Board(True, 111, [[0, 0, 0], [0, 0, 0], [0, 0, 0]], True)

    def __init__(self, **kwargs):
        super(GameBoard, self).__init__(**kwargs)
        self.cols = 3
        self.rows = 3

        self.drawBoard()

        for i in range(1, 10):
            cell = GameCell()
            cell.bind(toggle=self.changeTurn)
            self.add_widget(cell)

    def drawBoard(self):
        with self.canvas:
            Color(1, 1, 1)
            Line(points=[0, window[1] / 3, window[0], window[1] / 3], width=3)
            Line(points=[0, window[1] / 3 * 2, window[0], window[1] / 3 * 2], width=3)
            Line(points=[window[0] / 3, 0, window[0] / 3, window[1]], width=3)
            Line(points=[window[0] / 3 * 2, 0, window[0] / 3 * 2, window[1]], width=3)

    def showWinner(self, message):
        content = Button(text=message)
        popup = Popup(title='Game Over', content=content, size_hint=(None, None), size=(400, 400), auto_dismiss=False)
        content.bind(on_press=popup.dismiss)
        content.bind(on_release=self.resetGame)
        
        popup.open()

    def changeTurn(self, instance, pos):
        # 인공지능이 둔 수 중에서 인공지능이 이기는 수를 뽑아 board를 갱신한다.
        # 그리고 최종 업데이트 된 board 값으로 판을 다시 그린다.
        for i in range(0, 3):
            for j in range(0, 3):
                self.board.cells[i][j] = self.children[3 * i + j].status

        playerResult = self.board.isEnd()
        if type(playerResult) == int:
            if playerResult == 2:
                self.showWinner("It's draw game.")
                return
        else:
            if playerResult[1] == 3:
                self.showWinner("It's player's win.")
                return
            elif playerResult[1] == 6:
                self.showWinner("It's Artificial Intelligence win")
                return

        aiBoard = Board(False, None, self.board.cells, True)

        if len(aiBoard.child) > 0:
            count = list(filter(lambda item : item.value == 2 or item.value == 0, aiBoard.child))

            if len(count) > 0:
                idx = 0
                sortedLink = list(sorted(aiBoard.child, key=lambda item: item.value, reverse=True))
                for i in range(0, len(sortedLink)):
                    if sortedLink[i].value == 2 or sortedLink[i].value == 0:
                        self.board.cells = copy.deepcopy(sortedLink[i].cells)
                        break
                else:
                    self.board.cells = copy.deepcopy(sortedLink[0].cells)
            else:
                idx = random.randint(0, len(aiBoard.child) - 1)
                self.board.cells = copy.deepcopy(aiBoard.child[idx].cells)

        self.canvas.clear()
        self.drawBoard()

        with self.canvas:
            for i in range(0, len(self.board.cells)):
                for j in range(0, len(self.board.cells[i])):
                    if self.board.cells[i][j] == 1:
                        self.drawCircle(i, j)
                    elif self.board.cells[i][j] == 2:
                        self.drawX(i, j)

        #실제 클릭 영역의 상태 값도 바꿔준다.
        for i in range(0, 3):
            for j in range(0, 3):
                if self.board.cells[i][j] == 2:
                    self.children[3 * i + j].status = 2

        aiResult = self.board.isEnd()
        if type(aiResult) == int:
            if aiResult == 2:
                self.showWinner("It's draw game.")
                return
        else:
            if aiResult[1] == 3:
                self.showWinner("It's player's win.")
                return
            elif aiResult[1] == 6:
                self.showWinner("It's Artificial Intelligence win.")
                return

    def drawCircle(self, i, j):
        width = window[0] / 3
        height = window[1] / 3

        with self.canvas:
            Color(0, 0, 1)
            Line(circle=(width * (2 - j) + width / 2, height * i + height / 2, width / 3), width=3)

    def drawX(self, i, j):
        width = window[0] / 3
        height = window[1] / 3

        centerX = width * (2 - j) + width / 2
        centerY = height * i + height / 2 

        with self.canvas:
            Color(1, 0, 0)
            Line(points=(centerX - width / 3, centerY - width / 3, centerX + width / 3, centerY + width / 3), width=3)
            Line(points=(centerX - width / 3, centerY + width / 3, centerX + width / 3, centerY - width / 3), width=3)

    def resetGame(self, *kwargs):
        self.board = Board(True, None, [[0, 0, 0], [0, 0, 0], [0, 0, 0]], True)
        for item in self.children:
            item.status = 0
        self.canvas.clear()
        self.drawBoard()

class TicTacToeApp(App):
    def build(self):
        return GameBoard()

if __name__ == '__main__':
    TicTacToeApp().run()