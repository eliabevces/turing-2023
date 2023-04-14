class Tape:
    entrada = []
    head = 0

    def getEntrada(self) -> list:
        return self.entrada

    def setEntrada(self, entrada: list) -> None:
        self.entrada = entrada

    def setCharAt(self, pos: int, char: str) -> None:
        if pos >= len(self.entrada):
            self.entrada.append(char)
        else:
            self.entrada[pos] = char

    def getHead(self) -> int:
        return self.head

    def getCharAt(self, pos: int) -> str:
        if pos >= len(self.getEntrada()):
            return "B"
        return self.entrada[pos]

    def moveRight(self) -> None:
        self.head += 1

    def moveLeft(self, player_pos):
        self.head -= 1

    def resetTape(self) -> None:
        self.head = 0

    def checkFirstLast(self, player_pos) -> None:
        if self.entrada == []:
            self.entrada.append("B")
        if self.head >= len(self.entrada) - 1:
            self.entrada.append("B")
        if self.head == 0:
            self.entrada.insert(0, "B")
            self.head += 1
            player_pos -= 40
        return player_pos
