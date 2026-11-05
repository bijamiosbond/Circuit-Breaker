import pygame

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1000, 650))
pygame.display.set_caption("CIRCUIT BREAKER")
font = pygame.font.Font(None, 64)
restart_button = pygame.Rect(400, 370, 200, 60)

running = True
game_over = False
game_won = False
trace_color = (0, 200, 120)

player_trail = []
traces = [
    [(250, 80), (250, 300)],
    [(420, 350), (420, 550)],
    [(550, 100), (750, 100)],
    [(700, 250), (700, 400)],
    [(850, 400), (850, 550)],
    [(100, 350), (300, 350)],
    [(350, 180), (350, 280)],
    [(500, 450), (650, 450)],
    [(550, 250), (550, 350)],
    [(780, 180), (920, 180)],
    [(150, 500), (300, 500)]

]
nodes = [
    point
    for trace in traces
    for point in trace
]
start_port = pygame.Rect(45, 120, 55, 60)
end_port = pygame.Rect(900, 450, 55, 60)

player_x = 100
player_y = 150
player_speed = 290
player_direction = None

while running:
    dt = clock.tick(200) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and not game_over:
            if event.key == pygame.K_RIGHT and player_direction != "left":
                player_direction = "right"
            elif event.key == pygame.K_LEFT and player_direction != "right":
                player_direction = "left"
            elif event.key == pygame.K_UP and player_direction != "down":
                player_direction = "up"
            elif event.key == pygame.K_DOWN and player_direction != "up":
                player_direction = "down"
        if event.type == pygame.MOUSEBUTTONDOWN and (game_over or game_won):
            if restart_button.collidepoint(event.pos):
                game_over = False
                player_x = 100
                player_y = 150
                player_direction = None  
                player_trail.clear()
                game_won = False

    keys = pygame.key.get_pressed()
    if not game_over and not game_won:
        if player_direction == "right":
            player_x += player_speed * dt
        elif player_direction == "left":
            player_x -= player_speed * dt
        elif player_direction == "up":
            player_y -= player_speed * dt
        elif player_direction == "down":
            player_y += player_speed * dt
        if not player_trail or abs(player_x - player_trail[-1][0]) >= 3 or abs(player_y - player_trail[-1][1]) >= 3:
            player_trail.append((player_x, player_y))
        if end_port.collidepoint(player_x, player_y):
            game_won = True
    
    screen.fill((8, 18, 15))
    pygame.draw.rect(screen, (50, 120, 75), (20, 20, 960, 610), 3)
    

    for trace in traces:
        pygame.draw.lines(screen, trace_color, False, trace, 8)
        for i in range(len(trace) - 1):
            start = trace[i]
            end = trace[i + 1]

            obstacle = pygame.Rect(
                
                min(start[0], end[0]) - 5,
                min(start[1], end[1]) - 5,
                abs(start[0] - end[0]) + 10,
                abs(start[1] - end[1]) + 10
            )
            pygame.draw.rect(screen, (0,90,65), obstacle, border_radius=3)
            pygame.draw.rect(screen, (0, 200, 140), obstacle, 2, border_radius=3)
            
            if obstacle.collidepoint(player_x, player_y):
                game_over = True
    # USB ports
    pygame.draw.rect(screen, (130, 130, 140), start_port, border_radius=5)
    pygame.draw.rect(screen, (130, 130, 140), end_port, border_radius=5)

    pygame.draw.rect(screen, (0, 255, 150), start_port, 2, border_radius=5)
    pygame.draw.rect(screen, (0, 255, 150), end_port, 2, border_radius=5)
    for node in nodes:
        pygame.draw.circle(screen, (100, 255, 190), node, 5)
        pygame.draw.circle(screen, (0, 120, 80), node, 8, 1)
    if len(player_trail) > 1:
        pygame.draw.lines(screen, (0, 255, 150), False, player_trail, 4)
    pygame.draw.circle(screen, (255, 255, 255), (player_x, player_y), 7)
    pygame.draw.circle(screen, (0, 255, 150), (player_x, player_y), 4)
    if player_x < 30 or player_x > 970 or player_y < 30 or player_y > 620:
        game_over = True
    if end_port.collidepoint(player_x, player_y):
        level_complete = True
    if game_over:
        text = font.render("GAME OVER", True, (255, 70, 70))
        text_rect = text.get_rect(center=(500, 300))
        screen.blit(text, text_rect)
        pygame.draw.rect(screen, (255, 70, 70), restart_button, 3)
        pygame.draw.rect(screen, (0, 120, 80), restart_button, border_radius=10)
        button_text = pygame.font.Font(None, 40).render("RESTART", True, (255, 255, 255))
        button_rect =  button_text.get_rect(center=restart_button.center)
        screen.blit(button_text, button_rect)
    if game_won:
        text = font.render("LEVEL COMPLETE", True, (0, 255, 150))
        text_rect = text.get_rect(center=(500, 300))
        screen.blit(text, text_rect)
        pygame.draw.rect(screen, (255, 70, 70), restart_button, 3)
        pygame.draw.rect(screen, (0, 120, 80), restart_button, border_radius=10)
        button_text = pygame.font.Font(None, 40).render("RESTART", True, (255, 255, 255))
        button_rect =  button_text.get_rect(center=restart_button.center)
        screen.blit(button_text, button_rect)
    pygame.display.flip()
    clock.tick(200)
pygame.quit()
