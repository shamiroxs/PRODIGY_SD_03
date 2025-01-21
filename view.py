import pygame
import sys
import csv
import os

pygame.init()

WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
HOVER_COLOR = (0, 200, 200)

TITLE_FONT = pygame.font.Font(None, 64)
TEXT_FONT = pygame.font.Font(None, 36)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("View Contact")

CONTACT_FILE = "contact.txt"
CURRENT_FILE = "current.txt"

BUTTON_WIDTH = 150
BUTTON_HEIGHT = 50

def load_current_contact():
    """Load the SINO of the contact being viewed."""
    try:
        with open(CURRENT_FILE, "r") as f:
            sino = f.read().strip()
            if sino.isdigit():
                return int(sino)
    except FileNotFoundError:
        pass
    return None

def load_contact_by_sino(sino):
    """Load a contact by its SINO from contact.txt."""
    try:
        with open(CONTACT_FILE, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] == str(sino):
                    return row
    except FileNotFoundError:
        pass
    return None

def delete_contact(sino):
    """Delete a contact by its SINO from contact.txt."""
    contacts = []
    try:
        with open(CONTACT_FILE, "r") as f:
            reader = csv.reader(f)
            contacts = [row for row in reader if row[0] != str(sino)]
    except FileNotFoundError:
        pass

    with open(CONTACT_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(contacts)

def main():
    """Main loop for viewing a contact."""
    clock = pygame.time.Clock()
    running = True

    sino = load_current_contact()
    if not sino:
        return "list"  

    contact = load_contact_by_sino(sino)
    if not contact:
        return "list"  

    name, phone, email = contact[1], contact[2], contact[3]

    with open(CURRENT_FILE, "w") as f:
        f.write("")

    deleting = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if not deleting:
                    if back_button.collidepoint(mouse_pos):
                        return "list"  
                    if edit_button.collidepoint(mouse_pos):
                        with open(CURRENT_FILE, "w") as f:
                            f.write(str(sino))
                        return "add"
                    if delete_button.collidepoint(mouse_pos):
                        deleting = True  
                else:
                    if confirm_button.collidepoint(mouse_pos):
                        delete_contact(sino)
                        return "list"
                    if cancel_button.collidepoint(mouse_pos):
                        deleting = False  # Cancel delete

        screen.fill(BLACK)

        title_surface = TITLE_FONT.render(name, True, WHITE)
        title_rect = title_surface.get_rect(center=(WIDTH // 2, 50))
        screen.blit(title_surface, title_rect)

        detail_y = 150
        for label, value in [("Phone:", phone), ("Email:", email)]:
            detail_surface = TEXT_FONT.render(f"{label} {value}", True, WHITE)
            detail_rect = detail_surface.get_rect(topleft=(100, detail_y))
            screen.blit(detail_surface, detail_rect)
            detail_y += 50

        if not deleting:
            back_button = pygame.Rect(100, HEIGHT - 100, BUTTON_WIDTH, BUTTON_HEIGHT)
            edit_button = pygame.Rect(WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT - 100, BUTTON_WIDTH, BUTTON_HEIGHT)
            delete_button = pygame.Rect(WIDTH - 100 - BUTTON_WIDTH, HEIGHT - 100, BUTTON_WIDTH, BUTTON_HEIGHT)

            for button, label, color in [
                (back_button, "×", CYAN),
                (edit_button, "Edit", GREEN),
                (delete_button, "Delete", RED),
            ]:
                mouse_pos = pygame.mouse.get_pos()
                if button.collidepoint(mouse_pos):
                    pygame.draw.rect(screen, HOVER_COLOR, button, border_radius=5)
                else:
                    pygame.draw.rect(screen, color, button, border_radius=5)
                button_surface = TEXT_FONT.render(label, True, BLACK)
                button_rect = button_surface.get_rect(center=button.center)
                screen.blit(button_surface, button_rect)
        else:
            confirm_surface = TEXT_FONT.render("Are you sure you want to delete?", True, WHITE)
            confirm_rect = confirm_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
            screen.blit(confirm_surface, confirm_rect)

            confirm_button = pygame.Rect(WIDTH // 4 - BUTTON_WIDTH // 2, HEIGHT // 2 + 20, BUTTON_WIDTH, BUTTON_HEIGHT)
            cancel_button = pygame.Rect(3 * WIDTH // 4 - BUTTON_WIDTH // 2, HEIGHT // 2 + 20, BUTTON_WIDTH, BUTTON_HEIGHT)

            for button, label, color in [
                (confirm_button, "Yes", RED),
                (cancel_button, "No", GREEN),
            ]:
                mouse_pos = pygame.mouse.get_pos()
                if button.collidepoint(mouse_pos):
                    pygame.draw.rect(screen, HOVER_COLOR, button, border_radius=5)
                else:
                    pygame.draw.rect(screen, color, button, border_radius=5)
                button_surface = TEXT_FONT.render(label, True, BLACK)
                button_rect = button_surface.get_rect(center=button.center)
                screen.blit(button_surface, button_rect)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    next_screen = main()
    print(f"Transitioning to: {next_screen}")

