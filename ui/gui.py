# Example file showing a basic pygame "game loop"
import pygame
from game.gamestate import GameState
# Note l'import : on va chercher la classe dans le fichier board_renderer
from ui.board_renderer import BoardView
# pygame setup
def setup(gamestate: GameState):
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Chess")
    view = BoardView(screen) 

    running = True
    selected_piece = None
    click = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if(not click):
                    mouse_x, mouse_y = event.pos
                    col = (mouse_x - view.offset_x) // view.tile_size
                    row = (mouse_y - view.offset_y) // view.tile_size
                    print(f"Clicked on row {row}, col {col}")
                    selected_piece = gamestate.board[row][col]
                    if(selected_piece == None):
                        print("You did not select a piece.")
                    elif((gamestate.current_turn != selected_piece.color)):
                        selected_piece = None
                        print("It's not your turn!")
                    elif(selected_piece != None): 
                        print(f"Selected piece: {selected_piece}")
                        click = True
                else:
                    mouse_x, mouse_y = event.pos
                    col2 = (mouse_x - view.offset_x) // view.tile_size
                    row2 = (mouse_y - view.offset_y) // view.tile_size
                    selected_piece.move(row2, col2)

                    print(f"Clicked on row {row}, col {col}")
                    if (selected_piece.col==col and selected_piece.row==row):
                        print("Invalid move, try again")
                        click = False
                        selected_piece = None
                    else :
                        print(f"Selected piece: {selected_piece} moved to {row}, {col}")
                        gamestate.board=gamestate.update_board(selected_piece, row, col)
                        gamestate.switch_turn()
                        click = False
                        selected_piece = None


        screen.fill("white")
        view.draw_grid()
        view.draw_board(gamestate)  # On crée un GameState temporaire pour le dessi
        pygame.display.flip()

    pygame.quit()