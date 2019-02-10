def start_screen(): 
    pygame.event.clear()
    gameDisplay.blit(start_menu, (0, 0))
    pygame.display.update()
    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            game_loop()
        else:
            continue
