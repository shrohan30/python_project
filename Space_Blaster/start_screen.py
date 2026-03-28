import pygame

def start_screen(screen, WIDTH, HEIGHT):
    clock = pygame.time.Clock()

    # -------------------- BACKGROUND --------------------
    bg = pygame.image.load("assets/start_bg.png")
    bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

    # -------------------- MUSIC --------------------
    pygame.mixer.music.load("sounds/menu_music.mp3")
    pygame.mixer.music.play(-1)

    # -------------------- FONTS --------------------
    title_font = pygame.font.SysFont(None, 70)
    font = pygame.font.SysFont(None, 40)

    # -------------------- INPUT BOX --------------------
    input_box = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 + 120, 300, 50)
    player_name = ""
    active = False

    # -------------------- START BUTTON --------------------
    start_button = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 200, 200, 50)

    running = True
    while running:
        clock.tick(60)
        screen.blit(bg, (0, 0))

        # -------------------- TITLE --------------------
        title = title_font.render("", True, (255, 255, 0))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))

        # -------------------- INPUT BOX --------------------
        # Draw white background for input
        pygame.draw.rect(screen, (255, 255, 255), input_box)
        # Draw black border
        pygame.draw.rect(screen, (0, 0, 0), input_box, 2)

        # Render typed text
        name_surface = font.render(player_name, True, (0, 0, 0))
        screen.blit(name_surface, (input_box.x + 10, input_box.y + 10))

        # Placeholder text
        if player_name == "":
            placeholder = font.render("Enter your name...", True, (150, 150, 150))
            screen.blit(placeholder, (input_box.x + 10, input_box.y + 10))

        # -------------------- START BUTTON --------------------
        pygame.draw.rect(screen, (0, 200, 0), start_button)
        btn_text = font.render("START", True, (0, 0, 0))
        screen.blit(btn_text, (
            start_button.x + start_button.width//2 - btn_text.get_width()//2,
            start_button.y + start_button.height//2 - btn_text.get_height()//2
        ))

        # -------------------- EVENTS --------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # Mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = True
                else:
                    active = False

                if start_button.collidepoint(event.pos):
                    if player_name.strip() == "":
                        player_name = "Player"
                    pygame.mixer.music.stop()
                    return player_name

            # Keyboard typing
            if event.type == pygame.KEYDOWN and active:
                if event.key == pygame.K_RETURN:
                    if player_name.strip() == "":
                        player_name = "Player"
                    pygame.mixer.music.stop()
                    return player_name
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                else:
                    if len(player_name) < 12:  # max length
                        player_name += event.unicode

        pygame.display.update()