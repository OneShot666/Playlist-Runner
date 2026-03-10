import pygame
import sys

# . Fonction de rotation de texte prête à être insérée dans le menu manager (pour le 'v' button pour ouvrir/fermer le menu)
pygame.init()
ecran = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Rotation !")
horloge = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 50, bold=True)
texte_original = font.render("v", True, (255, 255, 0))
rect_original = texte_original.get_rect(center=(300, 200))                      # Text center

is_counterclockwise_rotate = False
current_angle = 0
final_angle = -90
rotate_speed = 3

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                is_counterclockwise_rotate = True
                final_angle += 90
            if event.key == pygame.K_RIGHT:
                is_counterclockwise_rotate = False
                final_angle -= 90

    if is_counterclockwise_rotate:
        if current_angle < final_angle:
            current_angle += rotate_speed                                       # Rotate counterclockwise
            if current_angle > final_angle: current_angle = final_angle
    else:
        if current_angle > final_angle:
            current_angle -= rotate_speed                                       # Rotate clockwise
            if current_angle < final_angle: current_angle = final_angle

    texte_tourne = pygame.transform.rotate(texte_original, current_angle)       # Apply angle to text object
    rect_tourne = texte_tourne.get_rect(center=rect_original.center)            # Recenter new object (change size)

    ecran.fill((50, 50, 50))                                                    # Background color

    ecran.blit(texte_tourne, rect_tourne)                                       # Display text

    pygame.display.flip()
    horloge.tick(60)
