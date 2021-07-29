from concurrent.futures import ProcessPoolExecutor

import chess
import pygame
import pygame as p

from search import find_best_move

WIDTH = HEIGHT = 720
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
path = "images"
IMAGES = {
    'P': p.transform.smoothscale(p.image.load("images/white_pawn.png"), (SQ_SIZE, SQ_SIZE)),
    'N': p.transform.smoothscale(p.image.load("images/white_knight.png"), (SQ_SIZE, SQ_SIZE)),
    'B': p.transform.smoothscale(p.image.load("images/white_bishop.png"), (SQ_SIZE, SQ_SIZE)),
    'R': p.transform.smoothscale(p.image.load("images/white_rook.png"), (SQ_SIZE, SQ_SIZE)),
    'Q': p.transform.smoothscale(p.image.load("images/white_queen.png"), (SQ_SIZE, SQ_SIZE)),
    'K': p.transform.smoothscale(p.image.load("images/white_king.png"), (SQ_SIZE, SQ_SIZE)),
    'p': p.transform.smoothscale(p.image.load("images/black_pawn.png"), (SQ_SIZE, SQ_SIZE)),
    'n': p.transform.smoothscale(p.image.load("images/black_knight.png"), (SQ_SIZE, SQ_SIZE)),
    'b': p.transform.smoothscale(p.image.load("images/black_bishop.png"), (SQ_SIZE, SQ_SIZE)),
    'r': p.transform.smoothscale(p.image.load("images/black_rook.png"), (SQ_SIZE, SQ_SIZE)),
    'q': p.transform.smoothscale(p.image.load("images/black_queen.png"), (SQ_SIZE, SQ_SIZE)),
    'k': p.transform.smoothscale(p.image.load("images/black_king.png"), (SQ_SIZE, SQ_SIZE))

}


def main():
    pool = ProcessPoolExecutor()
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    board = chess.Board()
    board.set_board_fen("8/8/5Q2/2k5/4K3/8/8/8")
    # board.set_board_fen("3q4/8/8/2k5/4K3/8/8/8")
    # board.set_board_fen("3k4/8/8/8/8/R7/6K1/8")
    running = True
    selected_square = ()
    player_clicks = []
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                file = location[0] // SQ_SIZE
                rank = location[1] // SQ_SIZE
                if selected_square == (file, rank):
                    selected_square = ()
                    player_clicks = []
                    print("make a new move")
                else:
                    selected_square = chess.square(file, rank)
                    print(chess.square_name(selected_square))
                    player_clicks.append(selected_square)
                if len(player_clicks) == 2:
                    from_square = chess.square_name(player_clicks[0])
                    to_square = chess.square_name(player_clicks[1])
                    if not board.turn:
                        try:
                            board.push_san(from_square + to_square)
                            player_clicks = []
                            selected_square = ()
                        except:
                            player_clicks = []
                            selected_square = ()
                            print("make a new move")
            elif e.type == p.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    if len(board.move_stack) > 1:
                        board.pop()
                        board.pop()

        clock.tick(MAX_FPS)
        draw_game(screen, board)
        p.display.flip()
        if not board.is_game_over():
            move_result = find_best_move(board, pool)
            board.push(move_result.move)
            print(f"move: {move_result.move}    score: {move_result.score * 10}")
        elif board.is_game_over():
            print("Game Over: " + board.result())


def draw_game(screen, board: chess.Board):
    draw_board(screen)
    draw_pieces(screen, board)


def draw_board(screen):
    colors = [p.Color(175, 182, 224), p.Color(125, 143, 245)]
    for file in range(DIMENSION):
        for rank in range(DIMENSION):
            color = colors[((rank + file) % 2)]
            p.draw.rect(screen, color, p.Rect(file * SQ_SIZE, rank * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def draw_pieces(screen, board: chess.Board):
    for file in range(DIMENSION):
        for rank in range(DIMENSION):
            piece = board.piece_at(chess.square(rank, file))
            if piece is not None:
                screen.blit(IMAGES[str(piece)], p.Rect(rank * SQ_SIZE, file * SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == '__main__':
    main()
