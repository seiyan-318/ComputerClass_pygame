import pygame
import random

width, height = 400, 00
ring_x = 100
hole_radius = 30
FPS = 60

BLACK = (50, 50, 50)
BLUE = (0, 0, 255)
GREEN = (0, 200, 0)
WHITE = (245, 245, 245)


class Course:
    def __init__(self):
        #25の点で画面の線を表す
        self.points = [[i * 20, height // 2, "BLACK"]for i in range(25)]
        self.speed = 5
        
    def update(self):
        #輪の位置を左から5個めの点の位置
        current_segment = self.points[5]
        if current_segment[2] == "BLUE":
            self.speed = 2
        elif current_segment[2] == "GREEN":
            self.speed = 10
        else:
            self.speed = 5
        
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
            self.points.append([last_x + 20, new_y, new_type])
        
    def draw(self, screen):
        for i in range(len(self.points) - 1):
            p1 = self.points[i]
            p2 = self.points[i+1]
            color = {"BLACK": BLACK, "BLUE": BLUE, "GREEN": GREEN}[p1[2]]
            pygame.draw.line(screen, color, (p1[0], p1[1]), (p2[0], p2[1]), 5 )


class AppMain:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Don't touch the line!")
        self.clock = pygame.time.Clock()
        self.course = Course()
        
        
    def run(self):
        game_is_running = True
        
        while game_is_running:
            for event in pygame.event.get():
                #ゲーム強制終了
                if event.type == pygame.QUIT:
                    game_is_running = False #画面右上の×ボタン
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:#EscKey
                        game_is_running = False
                
            self.course.update()
            
            self.screen.fill(WHITE)
            self.course.draw(self.screen)
            
            pygame.display.flip()
            self.clock.tick(FPS)
                
        pygame.quit()
    

if __name__ == "__main__":
    app = AppMain()
    app.run()
        
        