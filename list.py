import pygame
import sys
import csv

# Initialize Pygame
pygame.init()

# Screen Dimensions and Colors
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CYAN = (0, 255, 255)
HOVER_COLOR = (0, 200, 200)
GREY = (105, 105, 105)

# Fonts
TITLE_FONT = pygame.font.Font(None, 64)
TEXT_FONT = pygame.font.Font(None, 36)
SEARCH_FONT = pygame.font.Font(None, 28)

# Screen Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Contact List")

# File Paths
CONTACT_FILE = "contact.txt"
CURRENT_FILE = "current.txt"

# UI Constants
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 40
SEARCH_BAR_HEIGHT = 40
BUTTON_MARGIN = 10
SEARCH_BAR_WIDTH = WIDTH - 200

def load_contacts():
    """Load contacts from the contact.txt file."""
    contacts = []
    try:
        with open(CONTACT_FILE, "r") as f:
            reader = csv.reader(f)
            contacts = [row for row in reader]
    except FileNotFoundError:
        pass  # If the file doesn't exist, return an empty list
    return contacts

def save_current_contact(sino):
    """Save the selected contact's SINO to the current.txt file."""
    with open(CURRENT_FILE, "w") as f:
        f.write(str(sino))

def draw_search_bar(search_text):
    """Draw the search bar and + button."""
    search_rect = pygame.Rect(100, 10, SEARCH_BAR_WIDTH, SEARCH_BAR_HEIGHT)
    add_button_rect = pygame.Rect(SEARCH_BAR_WIDTH + 120, 10, 50, SEARCH_BAR_HEIGHT)

    # Draw search bar
    pygame.draw.rect(screen, GREY, search_rect, border_radius=5)
    search_surface = SEARCH_FONT.render(search_text, True, WHITE)
    search_rect_inner = search_surface.get_rect(center=search_rect.center)
    screen.blit(search_surface, search_rect_inner)

    # Draw + button
    mouse_pos = pygame.mouse.get_pos()
    if add_button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, HOVER_COLOR, add_button_rect, border_radius=5)
    else:
        pygame.draw.rect(screen, CYAN, add_button_rect, border_radius=5)
    plus_surface = SEARCH_FONT.render("+", True, BLACK)
    plus_rect = plus_surface.get_rect(center=add_button_rect.center)
    screen.blit(plus_surface, plus_rect)

    return add_button_rect

def draw_contacts(contacts, search_text):
    """Draw the list of contacts."""
    filtered_contacts = [c for c in contacts if search_text.lower() in c[1].lower()]  # Filter by name
    if not filtered_contacts:
        no_contact_surface = TEXT_FONT.render("No contacts found", True, WHITE)
        no_contact_rect = no_contact_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(no_contact_surface, no_contact_rect)
        return []

    start_y = 80
    buttons = []
    for i, contact in enumerate(filtered_contacts):
        contact_name = contact[1]
        contact_rect = pygame.Rect(100, start_y + i * (BUTTON_HEIGHT + BUTTON_MARGIN), BUTTON_WIDTH, BUTTON_HEIGHT)

        # Draw button
        mouse_pos = pygame.mouse.get_pos()
        if contact_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, HOVER_COLOR, contact_rect, border_radius=5)
        else:
            pygame.draw.rect(screen, CYAN, contact_rect, border_radius=5)

        # Draw contact name
        contact_surface = TEXT_FONT.render(contact_name, True, BLACK)
        contact_text_rect = contact_surface.get_rect(center=contact_rect.center)
        screen.blit(contact_surface, contact_text_rect)

        buttons.append((contact_rect, contact[0]))  # Store button rect and SINO

    return buttons

def main():
    """Main loop for the contact list."""
    clock = pygame.time.Clock()
    search_text = ""
    contacts = load_contacts()
    contacts.sort(key=lambda x: x[1].lower())  # Sort contacts alphabetically by name
    
    # Clear the current.txt file
    with open(CURRENT_FILE, "w") as f:
        f.write("")
        
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Handle text input for search bar
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    search_text = search_text[:-1]
                elif event.unicode.isprintable():
                    search_text += event.unicode

            # Handle mouse clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                add_button_rect = draw_search_bar(search_text)
                if add_button_rect.collidepoint(mouse_pos):
                    return "add"  # Navigate to Add Contact

                buttons = draw_contacts(contacts, search_text)
                for button_rect, sino in buttons:
                    if button_rect.collidepoint(mouse_pos):
                        save_current_contact(sino)  # Save SINO of clicked contact
                        return "view"  # Navigate to View Contact

        # Draw the screen
        screen.fill(BLACK)
        draw_search_bar(search_text)
        draw_contacts(contacts, search_text)

        # Update display
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    next_screen = main()
    print(f"Transitioning to: {next_screen}")

