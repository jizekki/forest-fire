import numpy as np
import pygame

__screenSize__ = (600, 600)
__cellSize__ = 5
__gridDim__ = tuple(map(lambda x: int(x / __cellSize__), __screenSize__))


class Cell:
    FIRE = -5
    TREE = 1
    EMPTY = 0

    @staticmethod
    def get_color_cell(n):
        if n == -5:
            return 215, 126, 4
        elif n == 0:
            return 70, 41, 2
        elif n == 1:
            return 9, 133, 5


class Grid:

    def __init__(
            self,
            density=0.5,
            neighbors="neumann"
    ):
        if neighbors == "neumann":
            self._neighbors_index = [(-1, 0), (0, -1), (0, 1), (1, 0)]
        elif neighbors == "moore":
            self._neighbors_index = [(-1, 0), (0, -1), (0, 1), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        self.grid = np.zeros(__gridDim__, dtype='int8')
        nx, ny = __gridDim__
        self.initial_nb_trees = 0
        for i in range(nx):
            for j in range(ny):
                rand = np.random.randint(0, 100)
                if rand <= density * 100:
                    self.grid[i, j] = Cell.TREE
                    self.initial_nb_trees += 1
                else:
                    self.grid[i, j] = Cell.EMPTY

        self.grid[nx // 2, ny // 2] = Cell.FIRE
        self.grid[nx // 2 + 1, ny // 2] = Cell.FIRE
        self.grid[nx // 2, ny // 2 + 1] = Cell.FIRE
        self.grid[nx // 2 + 1, ny // 2 + 1] = Cell.FIRE
        return

    def neighbors_index(self, x, y):
        return [(dx + x, dy + y) for (dx, dy) in self._neighbors_index if
                0 <= dx + x < __gridDim__[0] and 0 <= dy + y < __gridDim__[1]]

    def neighbors(self, x, y):
        return [self.grid[vx, vy] for (vx, vy) in self.neighbors_index(x, y)]

    def sum_neighbors(self, x, y):
        return sum(self.neighbors(x, y))

    def sum_enumerate(self):
        return [(c, self.sum_neighbors(c[0], c[1])) for c, _ in np.ndenumerate(self.grid)]

    def draw_me(self):
        pass


class Scene:
    def __init__(
            self,
            density=0.5,
            neighbors="neumann",
            display=True
    ):
        self.grid = Grid(density, neighbors)
        self._display = display
        if self._display:
            pygame.init()
            self._screen = pygame.display.set_mode(__screenSize__)
            self._font = pygame.font.SysFont('Arial', 25)

    def draw_me(self):
        if self.grid.grid is None or not self._display:
            return
        self._screen.fill((255, 255, 255))
        for x in range(__gridDim__[0]):
            for y in range(__gridDim__[1]):
                pygame.draw.rect(self._screen,
                                 Cell.get_color_cell(self.grid.grid.item((x, y))),
                                 (x * __cellSize__, y * __cellSize__, __cellSize__, __cellSize__))

    def draw_text(self, text, position, color=(255, 64, 64)):
        if self._display:
            self._screen.blit(self._font.render(text, True, color), position)
        return

    def update_forest(self):
        state_changed = False
        for (x, y), s in self.grid.sum_enumerate():
            if self.grid.grid[x, y] == Cell.TREE and s < 0:
                self.grid.grid[x, y] = Cell.FIRE
                state_changed = True
            elif self.grid.grid[x, y] == Cell.FIRE:
                self.grid.grid[x, y] = 0
        return state_changed

    def nb_tree(self):
        return (self.grid.grid == Cell.TREE).sum()


def main():
    density = 0.6
    scene = Scene(density=density)
    done = False
    clock = pygame.time.Clock()
    while not done:
        scene.draw_me()
        pygame.display.flip()
        if not scene.update_forest():
            return scene.nb_tree()
        clock.tick(20)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True


if __name__ == "__main__":
    print("Finished with p = ", main())
