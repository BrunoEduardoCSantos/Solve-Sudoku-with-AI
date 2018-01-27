
from utils import *

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units


units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)


def naked_twins(values):
    """Eliminate values using the naked twins strategy.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the naked twins eliminated from peers

    """


    unitlists = row_units + square_units + column_units + findDiag()
    for unit in unitlists:
        # Find pairs
        s = [values[s] for s in unit if (len(values[s])==2)]
        candidate = [s for s in unit if (len(values[s]) == 2)]

        # find naked twin pairs
        paired_candidates = [(a, b) for a in candidate for b in candidate if a != b and values[a] == values[b]]

        #Replace naked twin
        for pairs in paired_candidates:
            for peer in unit:
                if (peer not in pairs) and (len(values[peer])>1):
                    for digit in values[pairs[0]]:
                            values[peer] = values[peer].replace(digit,'')

    return values


#Dictionary to convert grid into int row/number
def convertGridColRowToNumber(elements):
    nb = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    col_element = dict()
    for col in zip(elements,nb):
        for c in col[0]:
            col_element[c]= col[1]
    return col_element


def invConvertGridColRowToNumber(row,col):
    row_dic = convertGridColRowToNumber(row_units)
    col_dic = convertGridColRowToNumber(column_units)
    for key, val in row_dic.items():
        for keys,vals in col_dic.items():
            if (val==row) & (vals==col) & (key==keys):
                return key

def findDiag():
    row_total = convertGridColRowToNumber(row_units)
    column_total= convertGridColRowToNumber(column_units)
    diag_left = []
    diag_right = []
    for row in row_units:
        for column in column_units:
            set_1, set_2 = set(row), set(column)
            intes= list(set_1 & set_2)
            if (row_total[intes[0]]== column_total[intes[0]]) :
                diag_left.append(intes[0])
                row_op = len(column)- row_total[intes[0]] + 1
                diag_right.append(str(invConvertGridColRowToNumber(row_op,column_total[intes[0]])))
    return [diag_right[::-1]]+[diag_left]


def eliminate(values):
    """Eliminate values from peers of each box with a single value.

       Go through all the boxes, and whenever there is a box with a single value,
       eliminate this value from the set of values of all its peers.

       Args:
           values: Sudoku in dictionary form.
       Returns:
           Resulting Sudoku in dictionary form after eliminating values.
       """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for i in solved_values:
        va = values[i]
        for p in peers[i]:
            values[p] = values[p].replace(va, '')

    return values


def only_choice(values):
    """Apply the only choice strategy to a Sudoku puzzle

    The only choice strategy says that if only one box in a unit allows a certain
    digit, then that box must be assigned that digit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with all single-valued boxes assigned


    """
    for i in unitlist:
        for digit in '123456789':
            space = [box for box in i if digit in values[box]]
            if len(space) == 1:
                values[space[0]] = digit

    return values



def reduce_puzzle(values):
    """Reduce a Sudoku puzzle by repeatedly applying all constraint strategies

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary after continued application of the constraint strategies
        no longer produces any changes, or False if the puzzle is unsolvable 
    """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Use the Eliminate Strategy
        values = eliminate(values)
        values = only_choice(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    """Apply depth first search to solve Sudoku puzzles in order to solve puzzles
    that cannot be solved by repeated reduction alone.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary with all boxes assigned or False
    -----
    """
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False  ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes):
        return values  ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n, s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt


def solve(grid):
    """Find the solution to a Sudoku puzzle using search and constraint propagation

    Parameters
    ----------
    grid(string)
        a string representing a sudoku grid.
        
        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    Returns
    -------
    dict or False
        The dictionary representation of the final sudoku grid or False if no solution exists.
    """
    values = grid2values(grid)
    values = search(values)
    return values


if __name__ == "__main__":
    before_naked_twins_1 = {'I6': '4', 'H9': '3', 'I2': '6', 'E8': '1', 'H3': '5', 'H7': '8', 'I7': '1', 'I4': '8',
                            'H5': '6', 'F9': '7', 'G7': '6', 'G6': '3', 'G5': '2', 'E1': '8', 'G3': '1', 'G2': '8',
                            'G1': '7', 'I1': '23', 'C8': '5', 'I3': '23', 'E5': '347', 'I5': '5', 'C9': '1', 'G9': '5',
                            'G8': '4', 'A1': '1', 'A3': '4', 'A2': '237', 'A5': '9', 'A4': '2357', 'A7': '27',
                            'A6': '257', 'C3': '8', 'C2': '237', 'C1': '23', 'E6': '579', 'C7': '9', 'C6': '6',
                            'C5': '37', 'C4': '4', 'I9': '9', 'D8': '8', 'I8': '7', 'E4': '6', 'D9': '6', 'H8': '2',
                            'F6': '125', 'A9': '8', 'G4': '9', 'A8': '6', 'E7': '345', 'E3': '379', 'F1': '6',
                            'F2': '4', 'F3': '23', 'F4': '1235', 'F5': '8', 'E2': '37', 'F7': '35', 'F8': '9',
                            'D2': '1', 'H1': '4', 'H6': '17', 'H2': '9', 'H4': '17', 'D3': '2379', 'B4': '27',
                            'B5': '1', 'B6': '8', 'B7': '27', 'E9': '2', 'B1': '9', 'B2': '5', 'B3': '6', 'D6': '279',
                            'D7': '34', 'D4': '237', 'D5': '347', 'B8': '3', 'B9': '4', 'D1': '5'}
    #diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    #display(grid2values(diag_sudoku_grid))
    result = naked_twins(before_naked_twins_1)
    #display(result)

    #try:
     #   import PySudoku
      #  PySudoku.play(grid2values(diag_sudoku_grid), result, history)

#    except SystemExit:
 #       pass
  #  except:
   #     print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
