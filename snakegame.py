import tkinter as tk
import random

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game")
        
        self.width = 600
        self.height = 400
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg='black')
        self.canvas.pack()
        
        self.snake_color = 'green'
        self.food_color = 'red'
        self.snake_size = 20
        self.food_size = 20
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.food = self.create_food()
        self.direction = 'Right'
        self.running = True
        self.paused = False
        self.score = 0
        
        self.root.bind("<KeyPress>", self.on_key_press)
        
        self.score_label = tk.Label(self.root, text=f"Score: {self.score}", font=("Arial", 14))
        self.score_label.pack()
        
        self.restart_button = tk.Button(self.root, text="Restart", command=self.restart)
        self.restart_button.pack(side=tk.LEFT, padx=20)
        
        self.pause_button = tk.Button(self.root, text="Pause", command=self.toggle_pause)
        self.pause_button.pack(side=tk.RIGHT, padx=20)
        
        self.update()
    
    def create_food(self):
        while True:
            x = random.randint(0, (self.width - self.food_size) // self.food_size) * self.food_size
            y = random.randint(0, (self.height - self.food_size) // self.food_size) * self.food_size
            food = (x, y)
            if food not in self.snake:
                return food
    
    def draw_snake(self):
        self.canvas.delete("snake")
        for segment in self.snake:
            self.canvas.create_rectangle(segment[0], segment[1], segment[0] + self.snake_size, segment[1] + self.snake_size, fill=self.snake_color, tag="snake")
    
    def draw_food(self):
        self.canvas.delete("food")
        self.canvas.create_oval(self.food[0], self.food[1], self.food[0] + self.food_size, self.food[1] + self.food_size, fill=self.food_color, tag="food")
    
    def move_snake(self):
        head_x, head_y = self.snake[0]
        if self.direction == 'Left':
            new_head = (head_x - self.snake_size, head_y)
        elif self.direction == 'Right':
            new_head = (head_x + self.snake_size, head_y)
        elif self.direction == 'Up':
            new_head = (head_x, head_y - self.snake_size)
        elif self.direction == 'Down':
            new_head = (head_x, head_y + self.snake_size)
        
        self.snake = [new_head] + self.snake
        
        if new_head == self.food:
            self.food = self.create_food()
            self.score += 1
            self.update_score()
        else:
            self.snake.pop()
    
    def check_collisions(self):
        head_x, head_y = self.snake[0]
        if (head_x < 0 or head_x >= self.width or head_y < 0 or head_y >= self.height):
            self.running = False
        if len(self.snake) != len(set(self.snake)):
            self.running = False
    
    def on_key_press(self, e):
        new_direction = e.keysym
        all_directions = {'Left', 'Right', 'Up', 'Down'}
        opposites = ({'Left', 'Right'}, {'Up', 'Down'})
        if (new_direction in all_directions and 
            {new_direction, self.direction} not in opposites):
            self.direction = new_direction
    
    def update(self):
        if self.running and not self.paused:
            self.move_snake()
            self.check_collisions()
            self.draw_snake()
            self.draw_food()
            self.root.after(100, self.update)
        elif not self.running:
            self.game_over()
    
    def update_score(self):
        self.score_label.config(text=f"Score: {self.score}")
    
    def game_over(self):
        self.canvas.create_text(self.width / 2, self.height / 2, text=f"Game Over\nScore: {self.score}", fill="white", font=('Arial', 24), tag="game_over")
    
    def restart(self):
        self.canvas.delete("game_over")
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.food = self.create_food()
        self.direction = 'Right'
        self.running = True
        self.paused = False
        self.score = 0
        self.update_score()
        self.pause_button.config(text="Pause")
        self.update()
    
    def toggle_pause(self):
        self.paused = not self.paused
        if self.paused:
            self.pause_button.config(text="Play")
        else:
            self.pause_button.config(text="Pause")
            self.update()

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
