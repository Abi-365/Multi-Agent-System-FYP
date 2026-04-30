import random
from agent import Agent


class GridEnvironment:
    def __init__(self, width, height, num_agents):
        self.width = width
        self.height = height
        self.num_agents = num_agents

        self.grid = [[0 for _ in range(width)] for _ in range(height)]
        self.agents = []
        self.create_agents()

    def create_agents(self):
        for _ in range(self.num_agents):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            agent = Agent(x, y)
            self.agents.append(agent)
            self.grid[y][x] = 1

    def get_valid_neighbours(self, x, y):
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        neighbours = []

        for dx, dy in directions:
            new_x = x + dx
            new_y = y + dy

            if 0 <= new_x < self.width and 0 <= new_y < self.height:
                neighbours.append((new_x, new_y))

        return neighbours

    def move_agents_random(self):
        for agent in self.agents:
            neighbours = self.get_valid_neighbours(agent.x, agent.y)
            new_x, new_y = random.choice(neighbours)

            agent.x = new_x
            agent.y = new_y
            self.grid[new_y][new_x] = 1

    def move_agents_decentralised(self):
        for agent in self.agents:
            neighbours = self.get_valid_neighbours(agent.x, agent.y)

            unvisited_neighbours = [
                (x, y) for x, y in neighbours if self.grid[y][x] == 0
            ]

            if unvisited_neighbours:
                new_x, new_y = random.choice(unvisited_neighbours)
            else:
                new_x, new_y = random.choice(neighbours)

            agent.x = new_x
            agent.y = new_y
            self.grid[new_y][new_x] = 1

    def get_unvisited_cells(self):
        unvisited = []
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == 0:
                    unvisited.append((x, y))
        return unvisited

    def move_agents_centralised(self):
        unvisited_cells = self.get_unvisited_cells()

        if not unvisited_cells:
            return

        for agent in self.agents:
            if not unvisited_cells:
                break

            target = min(
                unvisited_cells,
                key=lambda cell: abs(cell[0] - agent.x) + abs(cell[1] - agent.y)
            )

            target_x, target_y = target

            if agent.x < target_x:
                agent.x += 1
            elif agent.x > target_x:
                agent.x -= 1
            elif agent.y < target_y:
                agent.y += 1
            elif agent.y > target_y:
                agent.y -= 1

            self.grid[agent.y][agent.x] = 1

    def move_agents_hybrid(self):
        unvisited_cells = self.get_unvisited_cells()

        if not unvisited_cells:
            return

        for agent in self.agents:
            neighbours = self.get_valid_neighbours(agent.x, agent.y)

            unvisited_neighbours = [
                (x, y) for x, y in neighbours if self.grid[y][x] == 0
            ]

            if unvisited_neighbours:
                new_x, new_y = random.choice(unvisited_neighbours)
            else:
                target = min(
                    unvisited_cells,
                    key=lambda cell: abs(cell[0] - agent.x) + abs(cell[1] - agent.y)
                )

                target_x, target_y = target
                new_x, new_y = agent.x, agent.y

                if agent.x < target_x:
                    new_x += 1
                elif agent.x > target_x:
                    new_x -= 1
                elif agent.y < target_y:
                    new_y += 1
                elif agent.y > target_y:
                    new_y -= 1

            agent.x = new_x
            agent.y = new_y
            self.grid[new_y][new_x] = 1

    def agent_dropout(self, dropout_percentage):
        number_to_remove = int(len(self.agents) * dropout_percentage)

        if number_to_remove > 0:
            self.agents = self.agents[:-number_to_remove]

    def get_coverage(self):
        covered = sum(sum(row) for row in self.grid)
        total = self.width * self.height
        return (covered / total) * 100

    def get_agent_positions(self):
        return [(agent.x, agent.y) for agent in self.agents]
    