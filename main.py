from graphics import Canvas
import random
import time

CANVAS_WIDTH = 400
CANVAS_HEIGHT = 400

def main():
    global canvas, tiles, flipped, start_time, game_over
    
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    
    colors = ["red", "blue", "green", "yellow", "purple", "orange"]
    color_pool = colors * 2
    random.shuffle(color_pool)
    color_dict = {i: color_pool[i] for i in range(12)}

    TILE_COLS = 4
    TILE_ROWS = 3
    TILE_WIDTH = CANVAS_WIDTH // TILE_COLS
    TILE_HEIGHT = CANVAS_HEIGHT // TILE_ROWS
    GAP = 10

    tiles = []
    flipped = []
    game_over = False

    for i in range(12):
        row = i // TILE_COLS
        col = i % TILE_COLS

        x1 = col * TILE_WIDTH + GAP // 2
        y1 = row * TILE_HEIGHT + GAP // 2
        x2 = (col + 1) * TILE_WIDTH - GAP // 2
        y2 = (row + 1) * TILE_HEIGHT - GAP // 2

        rect = canvas.create_rectangle(x1, y1, x2, y2, "gray", outline="white")
    
        tile = {
            'id': rect,
            'color': color_dict[i],
            'flipped': False,
            'matched': False,
            'coords': (x1, y1, x2, y2),
            'index': i
        }

        tiles.append(tile)

    start_time = time.time()
    timer_id = canvas.create_text(10, 10, text="", font_size=20)

    while not game_over:
        click = canvas.get_last_click()
        if click is not None:
            check_mouse_click(click)
        
        elapsed_time = time.time() - start_time
        canvas.change_text(timer_id, f"Time: {int(elapsed_time)} s")
        
        time.sleep(0.01)

def check_mouse_click(click):
    global flipped
    for tile in tiles:
        x1, y1, x2, y2 = tile['coords']
        if x1 <= click[0] <= x2 and y1 <= click[1] <= y2:
            if tile['matched'] or tile in flipped:
                return
            if len(flipped) < 2:
                flip_tile(tile)
                if len(flipped) == 2:
                    time.sleep(0.7)
                    check_match()

def flip_tile(tile):
    if tile['flipped'] or tile['matched']:
        return
    canvas.set_color(tile['id'], tile['color'])
    tile['flipped'] = True
    flipped.append(tile)

def check_match():
    global flipped, game_over
    t1, t2 = flipped
    if t1['color'] == t2['color']:
        t1['matched'] = True
        t2['matched'] = True
        if all(tile['matched'] for tile in tiles):
            game_over = True
            canvas.clear()  # Clear all shapes
            canvas.create_text(CANVAS_WIDTH //4, CANVAS_HEIGHT // 2, text="Congratulations!", font_size=30, color="green")
            return
    else:
        for t in flipped:
            canvas.set_color(t['id'], "gray")
            t['flipped'] = False
    flipped = []


if __name__ == '__main__':
    main()