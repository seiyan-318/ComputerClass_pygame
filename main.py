import pygame
import random

width, height = 400, 600
ring_x = 100
hole_radius = 30

class Course:
    def __init__(self):
        self.pints = [[i * 20, height // 2, BLACK]for i in range(25)]
        self.speed = 5
        
    def update(self):
        current_segment = self.points[5]
        if current_segment[2] = "BLUE":
            self.speed = 2
        elif current_segmanet[2] = "GREEN":
            self.speed = 10
        else self.speed = 5
        
        #全部の点を←に動かす
        for p in self.points:
            p[0] -= self.speed
        
        #画面左端で消す、右端で新しい点を追加
        if self.points[0][0] < -20:
            self.points.pop(0)
            last_x, last_y, last_type = self.points[-1]
            new_y = last_y + random.randint(-50, 50)#ジグザグ
            new_y = max(100, min(height - 100, new_y))
        
        #ランダムで色を変更
        new_type = random.choices(["BLACK", "BLUE", "GREEN"],
                        weights = [80,     10,     10,     ])[0]
        self.points.append([last_x + 20. new_y, new_type])
        
    def draw(self, screen):
        for i in range(len(self.points) - 1):
            p1 = self.points[i]
            p2 = self.points[i+1]
            color = {"BLACK":(50,50,50), "BLUE": (0, 0, 255), "GREEN" : (0, 255, 0)}[p1[2]]
            pygame.draw.line(screen, color, (p1[0], p1[1]), (p2[0], p2[1]), 5 )
