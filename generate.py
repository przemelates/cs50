import sys, copy

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        for var in self.domains.keys():
            to_remove = set()
            for word in self.domains[var]:
                if(var.length != len(word)):
                    to_remove.add(word)
                else:
                    continue
            for word in to_remove:
                self.domains[var].remove(word)

        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        ##raise NotImplementedError

    def revise(self, x, y):
        if self.crossword.overlaps[x,y] == None:
            return False

        else:
            revision = False
            to_remove = set()
            for word1 in self.domains[x]:
                possible_value = False
                for word2 in self.domains[y]:
                    if word1 == word2:
                        continue
                    elif word1[self.crossword.overlaps[x,y][0]] == word2[self.crossword.overlaps[x,y][1]]:
                        possible_value = True
                        break
                    else:
                        continue
                if possible_value == False:
                    to_remove.add(word1)
                    revision = True
                else:
                    continue

            for word in to_remove:
                self.domains[x].remove(word)
            return revision
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        raise NotImplementedError

    def ac3(self, arcs=None):
        if arcs==None:
            for var in self.domains.keys():
                neighbours = self.crossword.neighbors(var)
                for var2 in neighbours:
                    self.revise(var,var2)
        else:
            for _var in arcs:
                self.revise(_var[0],_var[1])

        if None in self.domains.values():
            return False
        else:
            return True

        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        raise NotImplementedError

    def assignment_complete(self, assignment):
        if assignment.keys() == self.domains.keys():
            if len(assignment.values()) == len(self.domains.keys()) and None not in assignment.values():
                return True
            else:
                return False
        else:
            return False
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        raise NotImplementedError

    def consistent(self, assignment):
        if len(set(assignment.values())) == len(list(assignment.values())):
            pass
        else:
            return False

        for var in assignment.keys():
            word = assignment[var]
            if var.length != len(word):
                return False
            else:
                for neighbour in self.crossword.neighbors(var):
                    if neighbour in assignment.keys(): 
                        word2 = assignment[neighbour] 
                        if word[self.crossword.overlaps[var,neighbour][0]] != word2[self.crossword.overlaps[var,neighbour][1]]:
                            return False
                        else:
                            continue
                    else:
                        continue
        return True

        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        raise NotImplementedError

    def order_domain_values(self, var, assignment):
        variables = list(self.crossword.neighbors(var))
        for var in variables:
            if var in assignment.keys():
                variables.remove(var)
        values = self.domains(var)
        rule_out = list()
        for val in values:
            substract = 0
            for _var in variables:
                for value in self.domains[_var]:
                    if val[self.crossword.overlaps[var,_var][0]] != value[self.crossword.overlaps[var,_var][1]]:
                        substract+=1
            rule_out.append(substract)
                
        values = list(values)
        values.sort(key=rule_out)
        return values

        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        raise NotImplementedError

    def select_unassigned_variable(self, assignment : dict):
        unassigned = list(self.domains.keys() - assignment.keys())
        choice = unassigned[0]
        remaining_values = 9999
        degree = 0
        for variable in unassigned:
            if len(self.domains[variable]) < remaining_values:
                choice = variable
            elif len(self.domains[variable]) == remaining_values and len(self.crossword.neighbors(variable)) > degree:
                choice = variable
            else:
                continue
        return choice


        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        raise NotImplementedError

    def backtrack(self, assignment):
        if self.assignment_complete(assignment) == True:
            return assignment
        else:
            variable = self.select_unassigned_variable(assignment)
            for value in self.domains[variable]:
                assignment2 = copy.copy(assignment)
                assignment2[variable] = value
                if self.consistent(assignment2) and self.backtrack(assignment2) != None:
                    return assignment2
                else:
                    continue
            return None
                    


        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        raise NotImplementedError


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
