class Puzzle:
    def __init__(self, state):
        self.state = [row[:] for row in state]  # deep copy

    def find_zero(self):
        for y in range(3):
            for x in range(3):
                if self.state[y][x] == 0:
                    return x, y
        return None

    def move(self, tx, ty):
        zero_x, zero_y = self.find_zero()
        if abs(zero_x - tx) + abs(zero_y - ty) == 1:
            self.state[zero_y][zero_x], self.state[ty][tx] = self.state[ty][tx], self.state[zero_y][zero_x]
            return True
        return False

    def copy(self):
        return Puzzle(self.state)

    def __eq__(self, other):
        return self.state == other.state

    def __repr__(self):
        return '\n'.join([' '.join(map(str, row)) for row in self.state])