# 遊び方
重力のように画面y軸下方向に落ちてくるので、スペースキーを押してドーナッツをジャンプさせる
ドーナッツの輪が線を通り、ドーナッツに当たらないように動かすこと
最高得点が表示されているので超えれるように頑張ってください

# 構成
### 初期項目

### class Course:
#### def __init__():
#### get_zone_now():
#### update():
#### draw():

### class Doughnut:
#### def __init__():
#### def update():
#### def jump():
#### def is_touching():
#### def draw_back():
#### def draw_front():

### class Score:
#### def __init__():
#### def load_highscore():
#### def save_highscore():
#### def update():
#### def reset():
#### def draw():

### class Background:
#### def __init__():
#### def move_objects():
#### def update_color():
#### def update():
#### def draw():

### class AppMain:
#### def __init__():
#### def reset_game():
#### def run():

if __name__ == "__main__":
    app = AppMain()
    app.run()

# 工夫したところ
