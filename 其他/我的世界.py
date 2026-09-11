import pygame
import sys
import os

# 初始化Pygame
pygame.init()

# 游戏配置
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("简易我的世界（究极完整版·带排行榜）")

# ===== 排行榜配置 =====
RANK_FILE = "mc_rank.txt"  # 保存排行榜的文件
MAX_RANK_ENTRIES = 5  # 排行榜最多保存5条记录

# ===== 多种方块属性配置 =====
BLOCK_SIZE = 50
# 方块类型：(颜色, 名称, 放置得分)
BLOCK_TYPES = {
    1: ((34, 139, 34), "草方块", 1),
    2: ((128, 128, 128), "石头", 2),
    3: ((139, 69, 19), "木头", 3),
    4: ((255, 215, 0), "金方块(回血)", 5)
}
current_block_type = 1  # 默认选中草方块

# ===== 玩家属性 =====
player_color = (255, 0, 0)
player_speed = 5
gravity = 0.8
fall_speed = 0
max_fall_speed = 10
jump_force = -15
is_on_ground = False
max_hp = 100  # 最大血量
current_hp = max_hp  # 当前血量
hp_bar_width = 200  # 血条宽度
hp_bar_height = 20  # 血条高度
heal_amount = 2  # 每帧回血值
heal_range = 80  # 回血范围（像素）
game_over = False  # 游戏结束标记
score = 0  # 玩家分数
score_per_destroy = -2  # 破坏方块扣分

# ===== 方块放置冷却配置 =====
place_cooldown = 300  # 冷却时间（毫秒）
last_place_time = 0  # 上一次放置方块的时间

# 玩家初始位置
player_x, player_y = WIDTH // 2, HEIGHT // 2
player_rect = pygame.Rect(player_x, player_y, BLOCK_SIZE, BLOCK_SIZE)

# 存储方块：(Rect对象, 方块类型, 闪烁次数, 是否在销毁中)
blocks = []

# 字体配置
pygame.font.init()
font = pygame.font.SysFont("SimHei", 20)
hp_font = pygame.font.SysFont("SimHei", 16)
game_over_font = pygame.font.SysFont("SimHei", 60)  # 游戏结束字体
tip_font = pygame.font.SysFont("SimHei", 30)  # 提示字体
score_font = pygame.font.SysFont("SimHei", 20)  # 分数字体
rank_font = pygame.font.SysFont("SimHei", 18)  # 排行榜字体


# ===== 排行榜核心函数 =====
def load_ranks():
    """加载本地排行榜数据"""
    ranks = []
    if os.path.exists(RANK_FILE):
        with open(RANK_FILE, "r", encoding="utf-8") as f:
            for line in f.readlines():
                line = line.strip()
                if line:
                    ranks.append(int(line))
    # 排序并保留前MAX_RANK_ENTRIES条
    ranks = sorted(ranks, reverse=True)[:MAX_RANK_ENTRIES]
    return ranks


def save_rank(new_score):
    """保存新分数到排行榜"""
    ranks = load_ranks()
    ranks.append(new_score)
    ranks = sorted(ranks, reverse=True)[:MAX_RANK_ENTRIES]
    with open(RANK_FILE, "w", encoding="utf-8") as f:
        for r in ranks:
            f.write(f"{r}\n")


def draw_ranks():
    """绘制排行榜到屏幕"""
    ranks = load_ranks()
    # 绘制排行榜标题
    rank_title = rank_font.render("历史最高分数", True, (255, 215, 0))
    screen.blit(rank_title, (WIDTH - 160, 40))
    # 绘制每条记录
    for i, r in enumerate(ranks):
        rank_text = rank_font.render(f"第{i + 1}名: {r}", True, (0, 0, 0))
        screen.blit(rank_text, (WIDTH - 160, 70 + i * 25))


# 游戏主循环
clock = pygame.time.Clock()
running = True
while running:
    current_time = pygame.time.get_ticks()  # 获取当前时间戳
    screen.fill((135, 206, 235))  # 天空蓝背景

    # ===== 游戏结束判定 =====
    if current_hp <= 0:
        if not game_over:
            # 游戏结束时保存分数
            save_rank(score)
            game_over = True
        # 绘制游戏结束提示
        game_over_text = game_over_font.render("游戏结束!", True, (255, 0, 0))
        tip_text = tip_font.render("按下R键重新开始", True, (0, 0, 0))
        final_score_text = score_font.render(f"最终分数: {score}", True, (0, 0, 0))
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 120))
        screen.blit(final_score_text, (WIDTH // 2 - final_score_text.get_width() // 2, HEIGHT // 2 - 50))
        screen.blit(tip_text, (WIDTH // 2 - tip_text.get_width() // 2, HEIGHT // 2 + 20))
        # 绘制排行榜
        draw_ranks()
        # 检测R键重启
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            # 重置所有游戏状态
            current_hp = max_hp
            game_over = False
            player_x, player_y = WIDTH // 2, HEIGHT // 2
            blocks.clear()
            score = 0  # 分数重置
        pygame.display.flip()
        continue  # 跳过后续游戏逻辑

    # ===== 事件处理 =====
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # 鼠标左键放置方块（带冷却+加分）
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if current_time - last_place_time >= place_cooldown:
                x = (pygame.mouse.get_pos()[0] // BLOCK_SIZE) * BLOCK_SIZE
                y = (pygame.mouse.get_pos()[1] // BLOCK_SIZE) * BLOCK_SIZE
                new_block = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
                blocks.append((new_block, current_block_type, 0, False))
                # 放置方块加分
                score += BLOCK_TYPES[current_block_type][2]
                last_place_time = current_time  # 更新上一次放置时间

        # 鼠标右键标记方块销毁（精准坐标匹配+扣分）
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            x = (pygame.mouse.get_pos()[0] // BLOCK_SIZE) * BLOCK_SIZE
            y = (pygame.mouse.get_pos()[1] // BLOCK_SIZE) * BLOCK_SIZE
            for i in range(len(blocks)):
                b_rect, b_type, flash_count, is_destroying = blocks[i]
                if b_rect.x == x and b_rect.y == y and not is_destroying:
                    blocks[i] = (b_rect, b_type, 0, True)
                    # 破坏方块扣分
                    score += score_per_destroy
                    score = max(score, 0)  # 分数不低于0
                    break

        # 切换方块类型 + 跳跃
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                current_block_type = 1
            elif event.key == pygame.K_2:
                current_block_type = 2
            elif event.key == pygame.K_3:
                current_block_type = 3
            elif event.key == pygame.K_4:  # 切换金方块
                current_block_type = 4
            elif event.key == pygame.K_SPACE and is_on_ground:
                fall_speed = jump_force
                is_on_ground = False

    # ===== 1. 玩家水平移动 + 碰撞检测 =====
    new_x = player_x
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        new_x -= player_speed
    if keys[pygame.K_d]:
        new_x += player_speed

    # 水平碰撞检测
    temp_rect_x = pygame.Rect(new_x, player_y, BLOCK_SIZE, BLOCK_SIZE)
    x_collision = False
    for b_rect, _, _, is_destroying in blocks:
        if not is_destroying and temp_rect_x.colliderect(b_rect):
            x_collision = True
            break
    if not x_collision:
        player_x = new_x
    else:
        # 碰撞到方块时掉血
        current_hp -= 0.5
        current_hp = max(0, current_hp)  # 血量不低于0

    # ===== 2. 重力掉落 + 垂直碰撞检测 + 跳跃 =====
    fall_speed += gravity
    if fall_speed > max_fall_speed:
        fall_speed = max_fall_speed
    new_y = player_y + fall_speed

    # 垂直碰撞检测
    temp_rect_y = pygame.Rect(player_x, new_y, BLOCK_SIZE, BLOCK_SIZE)
    y_collision = False
    for b_rect, _, _, is_destroying in blocks:
        if not is_destroying and temp_rect_y.colliderect(b_rect):
            y_collision = True
            fall_speed = 0
            is_on_ground = True
            player_y = b_rect.top - BLOCK_SIZE
            break
    if not y_collision:
        player_y = new_y
        is_on_ground = False
        # 掉出屏幕重置位置并掉血
        if player_y > HEIGHT:
            player_y = 0
            is_on_ground = True
            current_hp -= 10
            current_hp = max(0, current_hp)

    # ===== 3. 金方块回血逻辑 =====
    player_center = (player_x + BLOCK_SIZE // 2, player_y + BLOCK_SIZE // 2)
    for b_rect, b_type, _, is_destroying in blocks:
        if b_type == 4 and not is_destroying:
            block_center = (b_rect.x + BLOCK_SIZE // 2, b_rect.y + BLOCK_SIZE // 2)
            # 计算玩家与金方块的距离
            distance = ((player_center[0] - block_center[0]) ** 2 + (player_center[1] - block_center[1]) ** 2) ** 0.5
            if distance <= heal_range:
                current_hp += heal_amount
                current_hp = min(current_hp, max_hp)  # 血量不超过上限

    # 更新玩家矩形位置
    player_rect.topleft = (player_x, player_y)

    # ===== 4. 方块破坏动画逻辑 =====
    to_remove = []
    for i in range(len(blocks)):
        b_rect, b_type, flash_count, is_destroying = blocks[i]
        if is_destroying:
            flash_count += 1
            blocks[i] = (b_rect, b_type, flash_count, is_destroying)
            if flash_count >= 6:
                to_remove.append(i)
    # 倒序删除避免索引错乱
    for i in sorted(to_remove, reverse=True):
        del blocks[i]

    # ===== 5. 绘制所有元素 =====
    # 绘制方块
    for b_rect, b_type, flash_count, is_destroying in blocks:
        color, _, _ = BLOCK_TYPES[b_type]
        if is_destroying:
            # 闪烁效果：奇偶帧切换颜色
            pygame.draw.rect(screen, color if flash_count % 2 == 0 else (255, 255, 255), b_rect)
        else:
            pygame.draw.rect(screen, color, b_rect)

    # 绘制玩家
    pygame.draw.rect(screen, player_color, player_rect)

    # 绘制血条
    hp_ratio = current_hp / max_hp
    # 血条背景（灰色）
    pygame.draw.rect(screen, (100, 100, 100), (10, 40, hp_bar_width, hp_bar_height))
    # 血条前景（红色，随血量变化）
    pygame.draw.rect(screen, (255, 0, 0), (10, 40, hp_bar_width * hp_ratio, hp_bar_height))
    # 血条文字
    hp_text = hp_font.render(f"血量: {int(current_hp)}/{max_hp}", True, (255, 255, 255))
    screen.blit(hp_text, (10 + hp_bar_width + 10, 40))

    # 绘制当前方块类型提示
    current_color, current_name, _ = BLOCK_TYPES[current_block_type]
    type_text = font.render(f"当前方块：{current_name} (1-4切换)", True, (0, 0, 0))
    screen.blit(type_text, (10, 10))

    # 绘制回血范围提示
    heal_text = font.render(f"金方块回血范围: {heal_range}px", True, (0, 0, 0))
    screen.blit(heal_text, (10, 70))

    # 绘制当前分数
    score_text = score_font.render(f"当前分数: {score}", True, (0, 0, 0))
    screen.blit(score_text, (WIDTH - 150, 10))

    # 绘制排行榜（游戏中也显示）
    draw_ranks()

    # 更新屏幕
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()