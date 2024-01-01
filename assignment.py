import tkinter as tk
import random
from assignment_2 import eSnakeGame

class SnakeGame:
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

        self.snake = [(100, 100), (90, 100), (80, 100)]
        self.direction = "Right"
        
        self.food = self.create_food()
        self.collider = None

        self.master.bind("<KeyPress>", self.change_direction)

        self.score = 0

        self.update()
        self.after_id = None

    def create_food(self):
        x = random.randint(0, 19) * 20
        y = random.randint(0, 19) * 20
        food = self.canvas.create_rectangle(x, y, x + 20, y + 20, fill="red", tags="food")
        return food

    def create_colliders(self):
        collider = []
        for _ in range(2):
            x = random.randint(0, 19) * 20
            y = random.randint(0, 19) * 20
            collider = self.canvas.create_rectangle(x, y, x + 20, y + 20, fill="purple", tags="collider")
        return collider

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

    def update(self):
        
        self.move_snake()
        
        if not self.collider:
            self.collider = self.create_colliders()
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

        self.after_id = self.master.after(200, self.update)
        self.after_id = self.master.after(200000000, self.create_colliders)

 
    def change_direction(self, event):
        if event.keysym == "Right" and not self.direction == "Left":
            self.direction = "Right"
        elif event.keysym == "Left" and not self.direction == "Right":
            self.direction = "Left"
        elif event.keysym == "Up" and not self.direction == "Down":
            self.direction = "Up"
        elif event.keysym == "Down" and not self.direction == "Up":
            self.direction = "Down"
        elif event.keysym == "space":
            self.enemy_game.reset_game()
            self.canvas.delete("all")
            self.master.after_cancel(self.after_id)
            self.snake = [(100, 100), (90, 100), (80, 100)]
            self.direction = "Right"
            self.food = self.create_food()
            self.collider = None
            self.score = 0
            self.update()
            

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
            self.canvas.delete("all")
            self.canvas.create_text(
                200, 200, text="Game Over: Self Collision", fill="white", font=("Arial", 16)
            )
            self.canvas.create_text(
                200, 300, text=f"Score: {self.score}", fill="white", font=("Arial", 16)
            )

    def collider_collision(self):
        head = self.snake[0]
        for collider in self.canvas.find_withtag("collider"):
            self.collider_coords = self.canvas.coords(collider)
            if head[0] == self.collider_coords[0] and head[1] == self.collider_coords[1]:
                self.canvas.delete("collider")
                self.canvas.delete("all")
                self.canvas.create_text(
                    200, 200, text="Game Over: Collider Collision", fill="white", font=("Arial", 16), tags="collider"
                )
                self.canvas.create_text(
                    200, 300, text=f"Score: {self.score}", fill="white", font=("Arial", 16)
                )
        return  # Stop checking for collisions after the first one
            
class SnakeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Snake Game")
        self.geometry("800x400")
        self.resizable(False, False)

        self.user_frame = tk.Frame(self)
        self.user_frame.pack(side=tk.LEFT, padx=.1, fill=tk.BOTH, expand=True)

        self.enemy_frame = tk.Frame(self)
        self.enemy_frame.pack(side=tk.RIGHT, padx=.1, fill=tk.BOTH, expand=True)

        self.user_game = SnakeGame(self.user_frame)
        self.enemy_game = eSnakeGame(self.enemy_frame)  
        self.bind("<KeyPress-space>", self.on_space_press)
        self.bind("<KeyPress-Up>", self.on_up_key_press)
        self.bind("<KeyPress-Down>", self.on_down_key_press)
        self.bind("<KeyPress-Left>", self.on_left_key_press)
        self.bind("<KeyPress-Right>", self.on_right_key_press)

    def on_space_press(self, event):
        self.        enemy_game.reset_game()
        self.user_game.canvas.delete("all")
        self.user_game.master.after_cancel(self.user_game.after_id)
        self.user_game.snake = [(100, 100), (90, 100), (80, 100)]
        self.user_game.direction = "Right"
        self.user_game.food = self.user_game.create_food()
        self.user_game.collider = None
        self.user_game.score = 0
        self.user_game.update()

    def on_up_key_press(self, event):
        self.user_game.change_direction(event)

    def on_down_key_press(self, event):
        self.user_game.change_direction(event)

    def on_left_key_press(self, event):
        self.user_game.change_direction(event)

    def on_right_key_press(self, event):
        self.user_game.change_direction(event)

if __name__ == "__main__":
    app = SnakeApp()
    app.mainloop()