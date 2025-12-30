import pygame
import random
import os

width, height = 600, 900
ring_x = 150
FPS = 60

BLACK = (50, 50, 50)
BLUE = (0, 0, 255)
GREEN = (0, 200, 0)
WHITE = (245, 245, 245)
RED = (255, 0, 0)
PINK = (231, 217, 217)


class Course:
    def __init__(self):
        self.points = [[i * 20, height // 2, "BLACK"]for i in range(width//20 +2)]
        self.speed = 3#流れる速さ
        self.current_zone_color = "BLACK"
        self.zone_remaining = 0 #あと何個この色を続けるか,一旦初期値0
    
    def get_zone_now(self, x):
        idx = int((x - self.points[0][0]) // 20)
        if 0 <= idx < len(self.points):
            return self.points[idx][2]
        return "BLACK"
    
    def update(self):
        zone = self.get_zone_now(ring_x)
        if zone == "BLUE":
            self.speed = 2
        elif zone == "GREEN":
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
        self.gravity = 0.25#落ちてくる
        self.jump_power = -3#跳ねあがり
        self.split_offset = 10
        
        #あたり判定用サイズ
        self.radius = 120#外円半径
        self.hole_radius = 70 #内円半径
        
        raw_img = pygame.image.load("doughnut.png").convert_alpha()
        orig_w, orig_h = raw_img.get_size()# アスペクト比を維持してスケーリング
        ratio = orig_w / orig_h
        self.display_w = 200
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
        check_x = self.x + self.split_offset 
        idx = int((check_x - points[0][0]) // 20)
        
        if 0 <= idx < len(points):
            target_p = points[idx]
            distance = abs(self.y - target_p[1])
            if distance > self.hole_radius:
                return True
        return False
        
    def draw_back(self, screen):
        #doughnutの右半分だけ(線の後ろに配置)
        split_x = self.display_w // 2 + self.split_offset
        base_x = self.x - self.display_w // 2
        base_y = int(self.y) - self.display_h // 2
        area_rect = (split_x, 0, self.display_w - split_x, self.display_h)
        screen.blit(self.image, (base_x + split_x, base_y), area_rect)
        
        # -----デバッグ用(あたり範囲)-----
        # pygame.draw.circle(screen, GREEN, (self.x, int(self.y)), self.hole_radius, 2)
        # pygame.draw.line(screen, BLUE, (self.x + self.split_offset, base_y), (self.x + self.split_offset, base_y + self.display_h), 2)
    
    def draw_front(self, screen):
        #doughnutの左半分(線の手前に表示)
        split_x = self.display_w // 2 + self.split_offset
        base_x = self.x - self.display_w // 2
        base_y = int(self.y) - self.display_h // 2
        area_rect = (0, 0, split_x, self.display_h)
        screen.blit(self.image, (base_x, base_y), area_rect)




class Score:
    def __init__(self):
        self.font = pygame.font.SysFont(None, 50)
        self.start_ticks = pygame.time.get_ticks()
        self.high_score = self.load_highscore()
        self.value = 0 #スコア保存用
        
    def load_highscore(self):
        if os.path.exists("highscore.txt"):
            with open("highscore.txt", "r") as f:
                try:
                    return int(f.read())
                except:
                    return 0
        return 0
    
    def save_highscre(self):
        with open("highscore.txt", "w") as f:
            f.write(str(self.high_score))
            
    def update(self, is_game_over):
        if is_game_over == False:
            now = pygame.time.get_ticks()
            self.value = (now - self.start_ticks)//1000
            
            if self.value > self.high_score:
                self.high_score = self.value
                
        else:
            self.save_highscre()
                
            
    def reset(self):
        self.start_ticks = pygame.time.get_ticks()
        self.value = 0    
        
            
    def draw(self, screen):
        score_msg = self.font.render(f"SCORE: {self.value}", True, BLACK)
        screen.blit(score_msg, (width -400, 30))
        high_msg = self.font.render(f"BEST: {self.high_score}", True, (100, 100, 100))
        screen.blit(high_msg, (30, 70))




class Background:
    def __init__(self):
        self.color = list(PINK)  # 現在の背景色
        self.target_color = list(PINK) # 目標の背景色

    def update(self,  zone_type):
        # ゾーンの線の色に合わせて背景色も変える
        if zone_type == "BLUE":
            self.target_color = [230, 230, 255] #薄い青
        elif zone_type == "GREEN":
            self.target_color = [230, 255, 230] #薄い緑
        else:
            self.target_color = [231, 217, 217] #薄いピンク

        for i in range(3):
            if self.color[i] < self.target_color[i]:
                self.color[i] += 1
            if self.color[i] > self.target_color[i]:
                self.color[i] -= 1
                
    def draw(self, screen):
        screen.fill(tuple(self.color))

        
class AppMain:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Don't touch the line!")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 80)
        self.course = Course()
        self.doughnut = Doughnut()
        self.score = Score() 
        self.background = Background()
        self.game_over = False
        
    
    def reset_game(self):
        self.course = Course()
        self.doughnut = Doughnut()
        self.score.reset()
        self.background = Background()
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
                current_zone = self.course.get_zone_now(self.doughnut.x + self.doughnut.split_offset)
                self.course.update()
                self.doughnut.update()
                self.score.update(self.game_over)
                self.background.update(current_zone)

                if self.doughnut.is_touching(self.course.points):
                    self.game_over = True
                    self.score.update(self.game_over) #スコア保存アップデート
                    
            self.background.draw(self.screen)
            self.doughnut.draw_back(self.screen)
            self.course.draw(self.screen)
            self.doughnut.draw_front(self.screen)
            self.score.draw(self.screen)

            if self.game_over:
                msg = self.font.render("GAME OVER", True, RED)
                text_rect = msg.get_rect(center = (width//2, height//2))
                self.screen.blit(msg, text_rect)       
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