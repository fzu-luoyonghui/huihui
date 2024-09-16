import unittest
import pygame
import sys
import random
from game.py import CustomTile, difficulty_select, init_tile_group, on_mouse_down, draw, main  # 确保导入你的游戏模块

class TestGame(unittest.TestCase):
    def setUp(self):
        # 初始化pygame和测试环境
        pygame.init()
        self.screen = pygame.display.set_mode((600, 720))
        pygame.display.set_caption('测试游戏')
        self.clock = pygame.time.Clock()
        self.FONT = pygame.font.SysFont(None, 36)
        self.DIFFICULTY = difficulty_select(self.screen)  # 模拟选择难度
        init_tile_group(self.screen)  # 初始化牌组

    def test_difficulty_selection(self):
        # 测试难度选择
        self.assertIn(self.DIFFICULTY, ['easy', 'normal', 'hard'], "Difficulty should be 'easy', 'normal', or 'hard'")

    def test_tile_group_initialization(self):
        # 测试牌组初始化
        self.assertGreater(len(CustomTile.tiles), 0, "There should be tiles initialized")

    def test_mouse_click(self):
        # 模拟鼠标点击事件
        for tile in CustomTile.tiles:
            tile.status = 1  # 假设所有牌都是可点击状态
        for tile in CustomTile.tiles:
            if tile.status == 1:
                on_mouse_down(tile.rect.center)  # 点击每张牌的中心
                self.assertEqual(tile.status, 2, "Tile should be selected when clicked")

    def test_draw_function(self):
        # 测试绘制函数
        draw(self.screen, CustomTile.tiles, self.FONT)  # 确保绘制函数可以正常运行
        pygame.display.update()

    def tearDown(self):
        # 清理测试环境
        pygame.quit()

if __name__ == '__main__':
    unittest.main()