import pygame
import random

width, height = 600, 900
ring_x = 150
hole_radius = 30
FPS = 60

BLACK = (50, 50, 50)
BLUE = (0, 0, 255)
GREEN = (0, 200, 0)
WHITE = (245, 245, 245)


class Course:
    def __init__(self):
        #25の点で画面の線を表す
        self.points = [[i * 20, height // 2, "BLACK"]for i in range(40)]
        self.speed = 3
        
        self.current_zone_color = "BLACK"
        self.zone_remaining = 0 #あと何個この色を続けるか
        
    def update(self):
        #輪の位置を左から5個めの点の位置
        idx = ring_x //20 
        current_segment = self.points[idx]
        if current_segment[2] == "BLUE":
            self.speed = 2
        elif current_segment[2] == "GREEN":
            self.speed = 4
        else:
            self.speed = 3
        
        #全部の点を←に動かす
        for p in self.points:
            p[0] -= self.speed
        
        #画面左端で消す、
        if self.points[0][0] < -20:
            self.points.pop(0)
            last_x, last_y, last_type = self.points[-1]
            
            #色の管理
            if self.zone_remaining <= 0:
                self.current_zone_color = random.choices(
                    ["BLACK", "BLUE", "GREEN"], 
                    weights=[70, 10, 10]
                )[0]
                
            # ゾーンの長さを設定
                if self.current_zone_color == "BLACK":
                    self.zone_remaining = random.randint(20, 40)
                else:
                    self.zone_remaining = random.randint(45, 65) # 色付きは長め
            else:
                self.zone_remaining -= 1
                
            #右端で新しい点を追加   
            new_y = last_y + random.randint(-30, 30)#ジグザグ
            new_y = max(200, min(height - 100, new_y))
        
            self.points.append([last_x + 20, new_y, self.current_zone_color])
        
    def draw(self, screen):
        for i in range(len(self.points) - 1):
            p1 = self.points[i]
            p2 = self.points[i+1]
            color_map = {"BLACK": BLACK, "BLUE": BLUE, "GREEN": GREEN}
            color = color_map[p1[2]]

            #点を待つく塗りつぶす
            pygame.draw.circle(screen, color, (int(p1[0]), int(p1[1])), 4)

            # 2. 線を描画
            pygame.draw.line(screen, color, (p1[0], p1[1]), (p2[0], p2[1]), 8)
            
            # 最後の点にも円を描画
            if i == len(self.points) - 2:
                pygame.draw.circle(screen, color, (int(p2[0]), int(p2[1])), 4)


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
        
        