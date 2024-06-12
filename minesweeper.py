import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):

        if len(self.cells) == self.count:
            return self.cells
    
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        ##raise NotImplementedError

    def known_safes(self):
        if self.count == 0:
            return self.cells
      
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        ##raise NotImplementedError

    def mark_mine(self, cell):
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -=1
            
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        ##raise NotImplementedError

    def mark_safe(self, cell):
        if cell in self.cells:
            self.cells.remove(cell)
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        ##raise NotImplementedError


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            Sentence.mark_mine(sentence,cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            Sentence.mark_safe(sentence,cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        cells = set()
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Add to the cell collection if the cell is not yet explored
                # and is not the mine already none
                if 0 <= i < self.height and 0 <= j < self.width:
                    if (i, j) not in self.moves_made and (i, j) not in self.mines:
                        cells.add((i, j))
                    # when excluding a known mine cell, decrease the count by 1
                    elif (i, j) in self.mines:
                        count -= 1
        self.moves_made.add(cell)
        self.knowledge.append(Sentence(cells,count))
        self.mark_safe(cell) 
        for i in range(len(self.knowledge)):
            sentence1 = self.knowledge[i] 
            Sentence.mark_mine(sentence1,Sentence.known_mines(sentence1))
            Sentence.mark_safe(sentence1,Sentence.known_safes(sentence1))
            if Sentence.known_mines(sentence1) is not None:
                self.mines = self.mines.union(Sentence.known_mines(sentence1))
            if Sentence.known_safes(sentence1) is not None:
                self.safes = self.safes.union(Sentence.known_safes(sentence1))
            for j in range(i+1,len(self.knowledge)):
                sentence2 = self.knowledge[j]
                if(sentence1.cells.issubset(sentence2.cells)):
                    sentnc = Sentence(sentence2.cells-sentence1.cells,sentence2.count - sentence1.count)
                    self.knowledge.append(sentnc)
                    if Sentence.known_mines(sentnc) is not None:
                        self.mines = self.mines.union(Sentence.known_mines(sentnc))
                    if Sentence.known_safes(sentnc) is not None:
                        self.safes = self.safes.union(Sentence.known_safes(sentnc))
                    
                    
        
        #raise NotImplementedError
        

    def make_safe_move(self):
        if len(self.safes-self.moves_made)!=0:
            available = self.safes - self.moves_made
            return random.choice(tuple(available))
            '''
            for cell in self.safes:
                if cell not in self.moves_made:
                    return cell
            '''
        return None
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        raise NotImplementedError

    def make_random_move(self):
        if len((self.moves_made.union(self.mines))) == self.height*self.width:
            return None
        i = random.randint(0,self.height-1)
        j = random.randint(0,self.width-1)
        cell = (i,j)
        if cell not in self.moves_made and cell not in self.mines:
            return cell
        else:
            MinesweeperAI.make_random_move(self)

        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        ##raise NotImplementedError
