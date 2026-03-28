import pygame

def game_over_screen(screen, WIDTH, HEIGHT, score, highscore, level, player_name):
    clock = pygame.time.Clock()

    # -------------------- Load Background --------------------
    bg = pygame.image.load("assets/gameover_bg.png")
    bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

    # -------------------- Music --------------------
    pygame.mixer.music.load("sounds/menu_music.mp3")
    pygame.mixer.music.play(-1)

    # -------------------- Fonts --------------------
    font_big = pygame.font.SysFont("arial", 80, bold=True)
    font_small = pygame.font.SysFont("arial", 40)

    # -------------------- Buttons (Horizontal at Bottom) --------------------
    btn_width, btn_height = 200, 60
    spacing = 50  # space between buttons
    restart_btn = pygame.Rect(WIDTH//2 - btn_width - spacing//2, HEIGHT - 120, btn_width, btn_height)
    exit_btn = pygame.Rect(WIDTH//2 + spacing//2, HEIGHT - 120, btn_width, btn_height)

    # -------------------- Fade Effect --------------------
    fade_alpha = 255
    fade_surface = pygame.Surface((WIDTH, HEIGHT))
    fade_surface.fill((0, 0, 0))

    running = True
    while running:
        clock.tick(60)

        # -------------------- Draw Background --------------------
        screen.blit(bg, (0, 0))

        # -------------------- Fade-in --------------------
        if fade_alpha > 0:
            fade_alpha -= 5
            fade_surface.set_alpha(fade_alpha)
            screen.blit(fade_surface, (0, 0))

        # -------------------- Title --------------------
        game_over_text = font_big.render("", True, (255, 50, 50))
        screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, 120))

        # -------------------- Score (LEFT SIDE) --------------------
        score_label = font_small.render("YOUR SCORE", True, (255,255,255))
        score_text = font_small.render(f"{score}", True, (0,255,0))
        high_text = font_small.render(f"HIGH: {highscore}", True, (0,255,255))
        level_text = font_small.render(f"LEVEL: {level} ", True, (255, 255, 0))
        name_text = font_small.render(f"Player: {player_name}", True, (255, 255, 0))
        

        screen.blit(name_text, (WIDTH//2 - name_text.get_width()//2, 60))
        screen.blit(level_text, (WIDTH//2 - level_text.get_width()//2, 120))
        screen.blit(score_label, (50, HEIGHT//2 - 40))
        screen.blit(score_text, (50, HEIGHT//2))
        screen.blit(high_text, (50, HEIGHT//2 + 50))


        # -------------------- Button Hover --------------------
        mouse_pos = pygame.mouse.get_pos()

        # Restart button
        if restart_btn.collidepoint(mouse_pos):
            pygame.draw.rect(screen, (0,255,100), restart_btn, border_radius=12)
        else:
            pygame.draw.rect(screen, (0,200,0), restart_btn, border_radius=12)

        # Exit button
        if exit_btn.collidepoint(mouse_pos):
            pygame.draw.rect(screen, (255,80,80), exit_btn, border_radius=12)
        else:
            pygame.draw.rect(screen, (200,0,0), exit_btn, border_radius=12)

        # -------------------- Button Text (LEFT ALIGN INSIDE BUTTON) --------------------
        padding = 20
        restart_text = font_small.render("▶ RESTART", True, (0,0,0))
        exit_text = font_small.render("✖ EXIT", True, (0,0,0))

        screen.blit(restart_text, (
            restart_btn.x + padding,
            restart_btn.y + restart_btn.height//2 - restart_text.get_height()//2
        ))

        screen.blit(exit_text, (
            exit_btn.x + padding,
            exit_btn.y + exit_btn.height//2 - exit_text.get_height()//2
        ))

        # -------------------- Events --------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_btn.collidepoint(event.pos):
                    pygame.mixer.music.stop()
                    return True  # restart game

                if exit_btn.collidepoint(event.pos):
                    pygame.quit()
                    exit()

        pygame.display.update()