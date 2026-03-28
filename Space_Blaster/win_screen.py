import pygame

def win_screen(screen, WIDTH, HEIGHT, score, level, player_name):
    clock = pygame.time.Clock()

    # Background
    bg = pygame.image.load("assets/win.png")
    bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

    # Music
    pygame.mixer.music.load("sounds/win.mp3")  # or victory music
    pygame.mixer.music.play(-1)

    # Fonts
    title_font = pygame.font.SysFont("arial", 80, bold=True)
    font = pygame.font.SysFont("arial", 40)

    # Button
    restart_btn = pygame.Rect(WIDTH//2 - 100, HEIGHT - 200, 200, 60)

    running = True
    while running:
        clock.tick(60)
        screen.blit(bg, (0, 0))

        # ---------------- TITLE ----------------
        title = title_font.render("", True, (255, 215, 0))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))

        # ---------------- PLAYER INFO ----------------
        margin_left =50
        start_y = HEIGHT - 220


        name_text = font.render(f"Player: {player_name}", True, (255,255,255))
        score_text = font.render(f"Score: {score}", True, (0,255,0))
        level_text = font.render(f"Completed Level: {level}", True, (255,255,0))

        screen.blit(name_text, (margin_left, start_y))
        screen.blit(score_text, (margin_left, start_y + 50))
        screen.blit(level_text, (margin_left, start_y + 100))

        # ---------------- BUTTON ----------------
        pygame.draw.rect(screen, (0,200,0), restart_btn, border_radius=10)

        btn_text = font.render("PLAY AGAIN", True, (0,0,0))
        screen.blit(btn_text, (
            restart_btn.x + restart_btn.width//2 - btn_text.get_width()//2,
            restart_btn.y + restart_btn.height//2 - btn_text.get_height()//2
        ))

        # ---------------- EVENTS ----------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_btn.collidepoint(event.pos):
                    pygame.mixer.music.stop()
                    return True

        pygame.display.update()