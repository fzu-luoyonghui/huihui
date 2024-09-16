import pygame
import random
import sys
import pygame.font

# 定义游戏相关属性
TITLE = '洛了个洛'
WIDTH = 600
HEIGHT = 720
FPS = 60

# 初始化 Pygame
pygame.init()

try:
    # 设置窗口尺寸
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)

    # 设置帧率
    clock = pygame.time.Clock()

    # 在游戏属性定义部分添加字体初始化
    FONT = pygame.font.SysFont(None, 36)

    # 自定义游戏常量
    T_WIDTH = 60
    T_HEIGHT = 70

    # 下方牌堆的位置
    DOCK = pygame.Rect((90, 564), (T_WIDTH * 7, T_HEIGHT))

    # 上方的所有牌
    tiles = []
    # 牌堆里的牌
    docks = []

    # 难度设置
    DIFFICULTY = ''

    # 清空道具的属性
    CLEAR_ITEM_IMAGE = pygame.image.load('images/clear_item.png')
    CLEAR_ITEM_RECT = pygame.Rect((WIDTH - 100, HEIGHT - 100 + 30), (100, 100))
    has_clear_item = True

    # 记录游戏开始时间
    start_time = pygame.time.get_ticks()

    # 加载背景和遮罩图像
    background = pygame.image.load('images/back.png')
    mask = pygame.image.load('images/mask.png')
    end = pygame.image.load('images/end.png')
    win = pygame.image.load('images/win.png')

    # 加载按钮图片
    easy_button = pygame.image.load('images/easy_button.png')
    normal_button = pygame.image.load('images/normal_button.png')
    hard_button = pygame.image.load('images/hard_button.png')

    # 自定义牌类
    class CustomTile:
        def __init__(self, image, rect, tag, layer, status):
            self.image = image
            self.rect = rect
            self.tag = tag
            self.layer = layer
            self.status = status

    # 难度选择界面
    def difficulty_select():
        global DIFFICULTY
        easy_rect = easy_button.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
        normal_rect = normal_button.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        hard_rect = hard_button.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))

        DIFFICULTY = ''
        while DIFFICULTY not in ['easy', 'normal', 'hard']:
            screen.fill((0, 0, 0))
            screen.blit(background, (0, 0))
            screen.blit(easy_button, easy_rect)
            screen.blit(normal_button, normal_rect)
            screen.blit(hard_button, hard_rect)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if easy_rect.collidepoint(event.pos):
                        DIFFICULTY = 'easy'
                    elif normal_rect.collidepoint(event.pos):
                        DIFFICULTY = 'normal'
                    elif hard_rect.collidepoint(event.pos):
                        DIFFICULTY = 'hard'

        return DIFFICULTY

    # 初始化牌组，12*12张牌随机打乱
    def init_tile_group():
        ts = list(range(1, 7)) * 6
        random.shuffle(ts)
        n = 0
        for k in range(4):
            for i in range(4-k):
                for j in range(4-k):
                    t = ts[n]
                    n += 1
                    tile_image = pygame.image.load(f'images/tile{t}.png')
                    tile_image = pygame.transform.scale(tile_image, (T_WIDTH, T_HEIGHT))
                    tile_rect = tile_image.get_rect()
                    tile_rect.topleft = (120 + (k * 0.5 + j) * T_WIDTH, 100 + (k * 0.5 + i) * T_HEIGHT * 0.9)
                    tile = CustomTile(tile_image, tile_rect, t, k, 1 if k == 3 else 0)
                    tiles.append(tile)
        for i in range(6):
            t = ts[n]
            n += 1
            tile_image = pygame.image.load(f'images/tile{t}.png')
            tile_image = pygame.transform.scale(tile_image, (T_WIDTH, T_HEIGHT))
            tile_rect = tile_image.get_rect()
            tile_rect.topleft = (210 + i * T_WIDTH, 516-20)
            tile = CustomTile(tile_image, tile_rect, t, 0, 1)
            tiles.append(tile)

    # 游戏帧绘制函数
    def draw():
        screen.blit(background, (0, 0))
        for tile in tiles:
            screen.blit(tile.image, tile.rect)
            if tile.status == 0:
                screen.blit(mask, tile.rect)
        for i, tile in enumerate(docks):
            tile.rect.left = DOCK.x + i * T_WIDTH
            tile.rect.top = DOCK.y
            screen.blit(tile.image, tile.rect)
        if len(docks) >= 7:
            screen.blit(end, end.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
        if not tiles:
            screen.blit(win, win.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
        if has_clear_item:
            screen.blit(CLEAR_ITEM_IMAGE, CLEAR_ITEM_RECT)

        current_time = pygame.time.get_ticks()
        seconds = (current_time - start_time) // 1000
        mins, secs = divmod(seconds, 60)
        time_surface = FONT.render(f'Time: {mins}:{secs:02d}', True, (255, 255, 255))
        screen.blit(time_surface, (10, 10))
        pygame.display.flip()

    # 鼠标点击响应
    def on_mouse_down(pos):
        global docks, has_clear_item
        if len(docks) >= 7 or not tiles:
            return
        if has_clear_item and CLEAR_ITEM_RECT.collidepoint(pos):
            has_clear_item = False
            bottom_deck_start_y = 516 - 20 - T_HEIGHT
            for i, tile in enumerate(docks):
                tile.status = 1
                new_x = 210 + i * T_WIDTH
                new_y = bottom_deck_start_y + (i // 7) * T_HEIGHT
                tile.rect.topleft = (new_x, new_y)
                tiles.append(tile)
            docks.clear()
            return
        for tile in reversed(tiles):
            if tile.status == 1 and tile.rect.collidepoint(pos):
                tile.status = 2
                tiles.remove(tile)
                docks.append(tile)
                if DIFFICULTY == 'easy':
                    if len([t for t in docks if t.tag == tile.tag]) >= 1:
                        docks = [t for t in docks if t.tag != tile.tag]
                elif DIFFICULTY == 'normal':
                    if len([t for t in docks if t.tag == tile.tag]) >= 2:
                        docks = [t for t in docks if t.tag != tile.tag]
                elif DIFFICULTY == 'hard':
                    if len([t for t in docks if t.tag == tile.tag]) >= 3:
                        docks = [t for t in docks if t.tag != tile.tag]
                for down in tiles:
                    if down.layer == tile.layer - 1 and down.rect.colliderect(tile.rect):
                        for up in tiles:
                            if up.layer == down.layer + 1 and up.rect.colliderect(down.rect):
                                break
                        else:
                            down.status = 1
                return

    # 游戏主循环
    def main():
        difficulty_select()
        init_tile_group()
        has_clear_item = True
        running = True
        while running:
            current_time = pygame.time.get_ticks()
            seconds = (current_time - start_time) // 1000
            if seconds > 30:
                screen.blit(end, end.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
                pygame.display.flip()
                pygame.time.wait(3000)
                running = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    on_mouse_down(event.pos)
            draw()
            clock.tick(FPS)
        pygame.quit()

    main()
except SystemExit:
    pygame.quit()
    sys.exit()
except Exception as e:
    print(f"An error occurred: {e}")
    pygame.quit()
    sys.exit()