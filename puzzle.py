from queue import PriorityQueue


class puzzle():
    def __init__(self, board, g, previous):
        self.board = board
        self.g = g
        self.previous = previous
        self.goal = [1, 2, 3, 4, 5, 6, 7, 8, 'b']

    def __eq__(self, other):
        if other is None:
            return False
        else:
            return self.board == other.board


    def find_b(self):
    #find blank index
        for i in range(9):
            if self.board[i] == 'b':
                return i


    def move_b(self, direction):
    # move blank in a direction
        blank = self.find_b()
        new_location = None

        if direction == 'left':
            if blank % 3 != 0:
                row, col = divmod(blank, 3)
                #col = (blank % 3) + 1
                #row = blank // 3
                new_location = row*3 + col-1
                self.board[blank], self.board[new_location] = self.board[new_location], self.board[blank]

        elif direction == 'right':
            if blank % 3 != 2:
                row, col = divmod(blank, 3)
                #col = (blank % 3) + 1
                #row = blank // 3
                new_location = row*3 + col+1
                self.board[blank], self.board[new_location] = self.board[new_location], self.board[blank]

        elif direction == 'up':
            if blank // 3 != 0:
                row, col = divmod(blank, 3)
                #col = blank % 3
                #row = blank // 3 - 1
                new_location = (row-1)*3 + col
                self.board[blank], self.board[new_location] = self.board[new_location], self.board[blank]

        elif direction == 'down':
            if blank // 3 != 2:
                row, col = divmod(blank, 3)
                #col = blank % 3
                #row = (blank // 3) + 1
                new_location = (row+1)*3 + col
                self.board[blank], self.board[new_location] = self.board[new_location], self.board[blank]

        
    def new_children(self):
        # find all possible moves from current position
        blank = self.find_b()
        children = []

        if blank % 3 != 0:
            new_node = puzzle(self.board.copy(), self.g+1, self)
            new_node.move_b('left')
            children.append(new_node)

        if blank % 3 != 2:
            new_node = puzzle(self.board.copy(), self.g+1, self)
            new_node.move_b('right')
            children.append(new_node)

        if int(blank // 3) != 2:
            new_node = puzzle(self.board.copy(), self.g+1, self)
            new_node.move_b('down')
            children.append(new_node)

        if int(blank // 3) != 0:
            new_node = puzzle(self.board.copy(), self.g+1, self)
            new_node.move_b('up')
            children.append(new_node)
        return children

        
    def manhattan(self):
        # manhattan heuristic
        manhattan = 0
        pos = 0
        for i in range(9):
            if self.board[i] != i + 1 and self.board[i] != 'b':
                pos = self.board[i] - 1
                curr_row, curr_col = divmod(i, 3)
                pos_row, pos_col = divmod(pos, 3)
                manhattan += abs(pos_row - curr_row) + abs(pos_col - curr_col)
            if self.board[i] == 'b':
                pos = 8
                curr_row, curr_col = divmod(i, 3)
                pos_row, pos_col = divmod(pos, 3)
                manhattan += abs(pos_row - curr_row) + abs(pos_col - curr_col)
        return manhattan

    def miss_tile(self):
        # misplaced tile heuristic
        miss = 0
        for i in range(9):
            if i == 8 and self.board[i] != 'b':
                miss += 1
            elif self.board[i] != i+1:
                miss += 1
        
        return miss


    
    def solution_steps(self):
        # show all moves to get to goal board
        steps = [self.board]
        before = self.previous
        while before is not None:
            steps.append(before.board)
            before = before.previous
        
        steps.reverse()
        
        return steps


def solver(initial_board, search_alg, heuristic):
    prioQueue = PriorityQueue()
    explored = []

    if search_alg == 'a-star':
        if heuristic == 'miss_tile':
            prioQueue.put((initial_board.g + initial_board.miss_tile(), 0, initial_board))
        elif heuristic == 'manhattan':
            prioQueue.put((initial_board.g + initial_board.manhattan(), 0, initial_board))
        elif heuristic == 'both':
            prioQueue.put((initial_board.g + initial_board.miss_tile() + initial_board.manhattan(), 0, initial_board))
    
    elif search_alg == 'best-first':
        if heuristic == 'miss_tile':
            prioQueue.put((initial_board.miss_tile(), 0, initial_board))
        elif heuristic == 'manhattan':
            prioQueue.put((initial_board.manhattan(), 0, initial_board))
        elif heuristic == 'both':
            prioQueue.put((initial_board.manhattan() + initial_board.miss_tile(), 0, initial_board))
        
    i = 1
    count = 0
    while prioQueue.empty() is False:
        curr_board = prioQueue.get()[2]
        explored.append(curr_board.board)
        if curr_board.board != curr_board.goal:
            for node in curr_board.new_children():
                if node != curr_board.previous and node.board not in explored:
                    if search_alg == 'a-star':
                        if heuristic == 'miss_tile':
                            prioQueue.put((node.g + node.miss_tile(), i, node))
                        elif heuristic == 'manhattan':
                            prioQueue.put((node.g + node.manhattan(), i, node))
                        elif heuristic == 'both':
                            prioQueue.put((node.g + node.miss_tile() + node.manhattan(), i, node))
                    elif search_alg == 'best-first':
                        if heuristic == 'miss_tile':
                            prioQueue.put((node.miss_tile(), i, node))
                        elif heuristic == 'manhattan':
                            prioQueue.put((node.manhattan(), i, node))
                        elif heuristic == 'both':
                            prioQueue.put((node.manhattan() + node.miss_tile(), i, node))
                    i+=1
        else:
            return curr_board.solution_steps()
        count += 1
        if count == 20000:
            break
    return None


def main():
    
    initial = []
    initial.append(puzzle([2,3,6,'b',1,8,4,5,7], 0, None))
    initial.append(puzzle([4,1,2,5,8,3,7,'b',6], 0, None))
    initial.append(puzzle([5,2,8,4,1,7,'b',3,6], 0, None))
    initial.append(puzzle([1,2,3,7,'b',5,8,4,6], 0, None))
    initial.append(puzzle([1,8,'b',4,3,2,5,7,6], 0, None))

    # best-first, misplaced tile
    bf_mt = []
    # best-first, manhattan
    bf_man = []
    # best-first, with made up heuristic (misplaced + manhattan)
    bf_both = []
    # a*, misplaced tile
    a_mt = []
    # a*, manhattan
    a_man = []
    # a*, with made up heuristic (misplaced + manhattan)
    a_both = []


    for search in initial:
        bf_mt.append(solver(search, 'best-first', 'miss_tile'))
        bf_man.append(solver(search, 'best-first', 'manhattan'))
        bf_both.append(solver(search, 'best-first', 'both'))
        a_mt.append(solver(search, 'a-star', 'miss_tile'))
        a_man.append(solver(search, 'a-star', 'manhattan'))
        a_both.append(solver(search, 'a-star', 'both'))
        

    print('\nBest-First Search with misplaced tiles heuristic\n')
    for each in bf_mt:
        if each is not None:
            for steps in each:
                print(steps)
            print('\nTook: %2d steps\n' %(len(each)))
        else:
            print('Not solvable')
    
    print('\nFinished all Best-First Search with misplaced tiles heuristics\n')
    

    print('\nBest-First Search with manhattan heuristic\n')
    for each in bf_man:
        if each is not None:
            for steps in each:
                print(steps)
            print('\nTook: %2d steps\n' %(len(each)))
        else:
            print('Not solvable')
    print('\nFinished all Best-First Search with manhattan heuristics\n')

    print('\nBest-First Search with misplaced tiles and manhattan heuristic\n')
    for each in bf_both:
        if each is not None:
            for steps in each:
                print(steps)
            print('\nTook: %2d steps\n' %(len(each)))
        else:
            print('Not solvable')
    print('\nFinished all Best-First Search with manhattan heuristics\n')

    print('\nA* search with misplaced tiles heuristic\n')
    for each in a_mt:
        if each is not None:
            for steps in each:
                print(steps)
            print('\nTook: %2d steps\n' %(len(each)))
        else:
            print('Not solvable')
    print('\nFinished all A* search with misplaced tiles heuristics\n')

    print('\nA* search with manhattan heuristic\n')
    for each in a_man:
        if each is not None:
            for steps in each:
                print(steps)
            print('\nTook: %2d steps\n' %(len(each)))
        else:
            print('Not solvable')
    print('\nFinished all A* search with manhattan heuristics\n')

    print('\nA* search with misplaced tiles and manhattan heuristic\n')
    for each in a_both:
        if each is not None:
            for steps in each:
                print(steps)
            print('\nTook: %2d steps\n' %(len(each)))
        else:
            print('Not solvable')
    print('\nFinished all A* search with misplaced tiles and manhattan heuristics\n')


if __name__ == '__main__':
    main()