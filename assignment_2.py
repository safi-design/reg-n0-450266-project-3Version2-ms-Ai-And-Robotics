import tkinter as tk
import random

class eSnakeGame:
    def __init__(self, master):
        if isinstance(master, tk.Tk):
            self.master = master
            self.master.title("Snake Game")
            self.master.geometry("400x400")
            self.master.resizable(False, False)
        elif isinstance(master, tk.Frame):
            self.master = master

        self.canvas = tk.Canvas(self.master, bg="black", width=400, height=400)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.snake = [(100, 300), (90, 300), (80, 300)]
        self.direction = "Right"

        self.food = self.create_food()
        self.collider = None
        self.collider_positions = []  # Initialize collider_positions

        self.master.bind("<KeyPress>", self.change_direction)
        self.collider = self.create_colliders()  
        self.collider_positions = self.canvas.coords(self.collider)
        self.score = 0
        self.exclude_set = set()
        self.update()
        self.after_id = None

        self.update_exclude_set()

    def create_food(self):
        x = random.randint(0, 18) * 20
        y = random.randint(0, 18) * 20
        food = self.canvas.create_rectangle(x, y, x + 20, y + 20, fill="red", tags="food")
        return food

    def move_towards(self, target):
        head = self.snake[0]

        if target is None or not isinstance(target, tuple) or len(target) != 2:
            return

        target_x, target_y = target
        head_x, head_y = head

        dx = target_x - head_x
        dy = target_y - head_y

        if dx > 0:
            self.direction = "Right"
        elif dx < 0:
            self.direction = "Left"
        elif dy > 0:
            self.direction = "Down"
        elif dy < 0:
            self.direction = "Up"

    def manhattan_distance(self, point1, point2):
        x1, y1 = point1
        x2, y2 = point2
        return abs(x1 - x2) + abs(y1 - y2)

    def get_neighbors(self, current, goal, exclude_set=None):
        x, y = current
        neighbors = []

        if self.direction == "Right":
            neighbors.append((x, y - 20))
            neighbors.append((x, y + 20))
            neighbors.append((x + 20, y))
        elif self.direction == "Left":
            neighbors.append((x, y - 20))
            neighbors.append((x, y + 20))
            neighbors.append((x - 20, y))
        elif self.direction == "Up":
            neighbors.append((x - 20, y))
            neighbors.append((x + 20, y))
            neighbors.append((x, y - 20))
        elif self.direction == "Down":
            neighbors.append((x - 20, y))
            neighbors.append((x + 20, y))
            neighbors.append((x, y + 20))
        if exclude_set is not None:
            neighbors = list(set(neighbors) - set(exclude_set))

        return neighbors
    def find_nearest_neighbor(self, current, goal):
        min_distance = float('inf')
        nearest_neighbor = None

        for neighbor in self.get_neighbors(current, goal, self.exclude_set):
            distance = self.manhattan_distance(neighbor, goal)    
            if distance < min_distance:
                min_distance = distance
                nearest_neighbor = neighbor

        self.canvas.create_text(140, 20, text="nearest neighbor point", fill="white", font=("Arial", 12)) 
        self.canvas.create_text(300, 20, text="nearest distance", fill="white", font=("Arial", 12))
        self.canvas.delete("label")
        self.canvas.create_text(
            100, 50, text=f"{nearest_neighbor}", fill="white", font=("Arial", 12), tag="label"
        )
        self.canvas.create_text(
            300, 50, text=f"{min_distance}", fill="white", font=("Arial", 12), tag="label"
        )
        
        return nearest_neighbor 

    def create_colliders(self):
        colliders = []
        for _ in range(2):
            x = random.randint(0, 19) * 20
            y = random.randint(0, 19) * 20
            collider = self.canvas.create_rectangle(x, y, x + 20, y + 20, fill="purple", tags="collider")
            colliders.append(collider)
        return colliders

    def move_snake(self):
        head = self.snake[0]

        if self.direction == "Right":
            new_head = (head[0] + 20, head[1])
        elif self.direction == "Left":
            new_head = (head[0] - 20, head[1])
        elif self.direction == "Up":
            new_head = (head[0], head[1] - 20)
        elif self.direction == "Down":
            new_head = (head[0], head[1] + 20)

        self.snake.insert(0, new_head)
        self.update_exclude_set()

    def update_exclude_set(self):
        # Update exclude set with snake's tail, boundaries, and colliders
        self.exclude_set.clear()  # Clear the exclude set to start fresh
    
        for snake_segment in self.canvas.find_withtag("snake"):
            snake_coords = self.canvas.coords(snake_segment)
            self.exclude_set.add(tuple(snake_coords[:2]))  # Add the coordinates of the snake segment
    
        for collider in self.canvas.find_withtag("collider"):
            collider_coords = self.canvas.coords(collider)
            self.exclude_set.add(tuple(collider_coords[:2]))  # Add the coordinates of the collider
    
        for x in range(0, 400, 20):
            self.exclude_set.add((x, 0))
            self.exclude_set.add((x, 400))
    
        for y in range(0, 400, 20):
            self.exclude_set.add((0, y))
            self.exclude_set.add((400, y))


    def get_collider_positions(self):
        positions = []
        for collider in self.canvas.find_withtag("collider"):
            positions.append(tuple(self.canvas.coords(collider)[:2]))  # Convert to tuple
        return positions

    def update(self):
        
        self.update_exclude_set()

        self.move_snake()
        self.boundary_collision()
        self.snake.pop()
        self.self_collision()
        self.collider_collision()
        
        head = self.snake[0]
        self.canvas.delete("snake")
        for segment in self.snake:
            self.canvas.create_rectangle(
                segment[0], segment[1], segment[0] + 20, segment[1] + 20, fill="green", tags="snake"
            )
        
        food_coords = self.canvas.coords(self.food)
        if head[0] == food_coords[0] and head[1] == food_coords[1]:
            self.snake.append((0, 0))  # Just to increase the length
            self.canvas.delete("food")
            self.food = self.create_food()

            self.score += 1
            self.canvas.delete("score")
            self.canvas.create_text(
                30, 20, text=f"Score: {self.score}", fill="white", font=("Arial", 10), tags="score"
            )

        target = self.find_nearest_neighbor(head, (food_coords[0], food_coords[1]))
        self.move_towards(target)
        
        # Adjust the timing as needed
        self.after_id = self.master.after(1,self.update_exclude_set)
        self.after_id = self.master.after(200, self.update)

    def reset_game(self):
        self.canvas.delete("all")
        self.collider = self.create_colliders()
        self.collider_positions = self.canvas.coords(self.collider)
        self.master.after_cancel(self.after_id)
        self.snake = [(100, 300), (90, 300), (80, 300)]
        self.direction = "Right"
        self.food = self.create_food()
        self.collider = None
        self.score = 0
        self.update()
        
    def change_direction(self, event):
        if event.keysym == "space":
            self.reset_game()
    def boundary_collision(self):
        head = self.snake[0]
        if head[0] < 0 or head[0] >= 400 or head[1] < 0 or head[1] >= 400:
            self.canvas.delete("all")
            self.canvas.create_text(
                200, 200, text="Game Over: Boundary Collision", fill="white", font=("Arial", 16)
            )
            self.canvas.create_text(
                200, 300, text=f"Score: {self.score}", fill="white", font=("Arial", 16)
            )

    def self_collision(self):
        head = self.snake[0]
        if head in self.snake[1:]:
            self.game_over("Self Collision")
    
    def collider_collision(self):
        head = self.snake[0]
        for collider in self.canvas.find_withtag("collider"):
            collider_coords = self.canvas.coords(collider)
            if head[0] == collider_coords[0] and head[1] == collider_coords[1]:
                self.game_over("Collider Collision")
                return  # Stop checking for collisions after the first one
    
    def game_over(self, reason):
        self.canvas.delete("all")
        self.canvas.create_text(
            200, 200, text=f"Game Over: {reason}", fill="white", font=("Arial", 16)
        )
        self.canvas.create_text(
            200, 300, text=f"Score: {self.score}", fill="white", font=("Arial", 16)
        )
# # Create the main Tkinter window
# root = tk.Tk()
# root.title("Snake Game Window")

# # Create an instance of the SnakeGame class within the Tkinter window
# snake_game_instance = eSnakeGame(root)

# # Start the Tkinter main loop
# root.mainloop()
