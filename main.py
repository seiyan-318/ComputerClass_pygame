import pygame
import random

width, height = 600, 900
ring_x = 150
FPS = 60

BLACK = (50, 50, 50)
BLUE = (0, 0, 255)
GREEN = (0, 200, 0)
WHITE = (245, 245, 245)
RED = (255, 0, 0)
PINK = (100, 0, 0)


class Course:
    def __init__(self):
        self.points = [[i * 20, height // 2, "BLACK"]for i in range(width//20 +2)]
        self.speed = 3#流れる速さ
        self.current_zone_color = "BLACK"
        self.zone_remaining = 0 #あと何個この色を続けるか,一旦初期値0
        
    def update(self):
        #輪の位置にある線の色を確認してスピード変更
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
        
        #画面左端で消す
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
            pygame.draw.line(screen, color, (p1[0], p1[1]), (p2[0], p2[1]), 8)  
            pygame.draw.circle(screen, color, (int(p2[0]), int(p2[1])), 4)

class Doughnut:
    def __init__(self):
        self.x = ring_x
        self.y = height//2
        self.velocity = 0
        self.gravity = 0.2#落ちてくる
        self.jump_power = -3#跳ねあがり
        
        #あたり判定用サイズ
        self.radius = 60 #外円半径
        self.hole_radius = 25 #内円半径
                
        raw_img = pygame.image.load("doughnut.png").convert_alpha()
        
        # アスペクト比を維持してスケーリング
        orig_w, orig_h = raw_img.get_size()
        ratio = orig_w / orig_h
        self.display_w = self.radius * 3.5
        self.display_h = int(self.display_w / ratio)
        self.image = pygame.transform.scale(raw_img, (self.display_w, self.display_h))
    
    def update(self):
        
        self.velocity += self.gravity
        self.y += self.velocity
        
        #跳ね返りの制限
        if self.y <0:
            self.y = 0
            self.velocity =0
        if self.y > height:
            self.y = height
            self.velocity = 0
            
    def jump(self):
        self.velocity = self.jump_power
        
    def is_touching(self, points):
        idx = ring_x // 20
        if 0 <= idx < len (points):
            target_p = points[idx]
            distance = abs(self.y - target_p[1])
            #穴の半径より離れていたら接触判定
            if distance > self.hole_radius:
                return True
        return False

    
    def draw(self,screen):
        draw_pos = (self.x - self.display_w // 2, int(self.y) - self.display_h // 2)
        screen.blit(self.image, draw_pos)
        
        
        
        
class AppMain:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Don't touch the line!")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 80)
        self.course = Course()
        self.doughnut = Doughnut()
        self.game_over = False
    
    def reset_game(self):
        self.course = Course()
        self.doughnut = Doughnut()
        self.game_over = False
        
        
    def run(self):
        game_is_running = True
        
        while game_is_running:
            for event in pygame.event.get():
                #イベント管理
                if event.type == pygame.QUIT:
                    game_is_running = False #画面右上の×ボタン
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:#EscKey
                        game_is_running = False
                    if event.key ==pygame.K_SPACE:#スペースでジャンプ
                        self.doughnut.jump()
                    if event.key == pygame.K_r:
                        self.reset_game()
                elif event.type == pygame.MOUSEBUTTONDOWN:#マウスでもジャンプ
                    self.doughnut.jump()
                    
            if self.game_over == False:
                self.course.update()
                self.doughnut.update()
                
                if self.doughnut.is_touching(self.course.points):
                    self.game_over = True
                    
            self.screen.fill(WHITE)
            self.course.draw(self.screen)
            self.doughnut.draw(self.screen)
            
            if self.game_over:
                msg = self.font.render("GAME OVER", True, RED)
                text_rect = msg.get_rect(center = (width//2, height//2))
                self.screen.blit(msg, text_rect)
            
            # もう一回
                retry_font = pygame.font.SysFont(None, 40)
                retry_msg = retry_font.render("Press 'R' to Restart", True, BLACK)
                retry_rect = retry_msg.get_rect(center = (width // 2, height // 2 + 80))
                self.screen.blit(retry_msg, retry_rect)
            pygame.display.flip()
            self.clock.tick(FPS)
                
        pygame.quit()
    

if __name__ == "__main__":
    app = AppMain()
    app.run()
        
        
        