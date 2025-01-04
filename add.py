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
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Fonts
TITLE_FONT = pygame.font.Font(None, 64)
TEXT_FONT = pygame.font.Font(None, 36)
INPUT_FONT = pygame.font.Font(None, 32)

# Screen Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Add/Edit Contact")

# File Paths
CONTACT_FILE = "contact.txt"
CURRENT_FILE = "current.txt"

# UI Constants
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 40
TEXT_FIELD_WIDTH = 400
TEXT_FIELD_HEIGHT = 40
MARGIN = 20

def load_current_contact():
    """Load the SINO of the contact being edited."""
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

def save_contact(sino, name, phone, email):
    """Save or update a contact in contact.txt."""
    contacts = []
    contact_exists = False

    try:
        with open(CONTACT_FILE, "r") as f:
            reader = csv.reader(f)
            contacts = [row for row in reader]
    except FileNotFoundError:
        pass

    if sino is not None:
        # Update existing contact
        for i, row in enumerate(contacts):
            if row[0] == str(sino):
                contacts[i] = [str(sino), name, phone, email]
                contact_exists = True
                break

    if not contact_exists:
        # Add new contact
        new_sino = max((int(row[0]) for row in contacts), default=0) + 1
        contacts.append([str(new_sino), name, phone, email])

    with open(CONTACT_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(contacts)

def draw_text_field(label, value, y_pos):
    """Draw a text field with a label and return the input area rect."""
    label_surface = TEXT_FONT.render(label, True, WHITE)
    label_rect = label_surface.get_rect(topleft=(100, y_pos))
    screen.blit(label_surface, label_rect)

    input_rect = pygame.Rect(300, y_pos, TEXT_FIELD_WIDTH, TEXT_FIELD_HEIGHT)
    pygame.draw.rect(screen, GREY, input_rect, border_radius=5)

    value_surface = INPUT_FONT.render(value, True, WHITE)
    value_rect = value_surface.get_rect(topleft=(310, y_pos + 5))
    screen.blit(value_surface, value_rect)

    return input_rect

def main():
    """Main loop for adding/editing a contact."""
    clock = pygame.time.Clock()
    running = True

    # Load current contact (if editing)
    editing_sino = load_current_contact()
    if editing_sino:
        contact = load_contact_by_sino(editing_sino)
        name, phone, email = contact[1], contact[2], contact[3]
    else:
        name, phone, email = "", "", ""

    active_field = None  # Tracks which text field is active

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                # Check if the buttons are clicked
                if cancel_button.collidepoint(mouse_pos):
                    return "list"  # Return to list

                if save_button.collidepoint(mouse_pos):
                    if name.strip():  # Ensure the name is not empty
                        save_contact(editing_sino, name.strip(), phone.strip(), email.strip())
                        if editing_sino:
                            with open(CURRENT_FILE, "w") as f:
                                f.write("")  # Clear the current contact file
                        return "list"

                # Check if text fields are clicked
                for i, rect in enumerate([name_field, phone_field, email_field]):
                    if rect.collidepoint(mouse_pos):
                        active_field = i
                        break
                else:
                    active_field = None

            if event.type == pygame.KEYDOWN and active_field is not None:
                if event.key == pygame.K_BACKSPACE:
                    if active_field == 0:
                        name = name[:-1]
                    elif active_field == 1:
                        phone = phone[:-1]
                    elif active_field == 2:
                        email = email[:-1]
                elif event.unicode.isprintable():
                    if active_field == 0:
                        name += event.unicode
                    elif active_field == 1:
                        phone += event.unicode
                    elif active_field == 2:
                        email += event.unicode

        # Draw UI
        screen.fill(BLACK)

        # Title
        title = "Edit Contact" if editing_sino else "Add Contact"
        title_surface = TITLE_FONT.render(title, True, WHITE)
        title_rect = title_surface.get_rect(center=(WIDTH // 2, 50))
        screen.blit(title_surface, title_rect)

        # Text Fields
        name_field = draw_text_field("Name:", name, 150)
        phone_field = draw_text_field("Phone:", phone, 250)
        email_field = draw_text_field("Email:", email, 350)

        # Buttons
        cancel_button = pygame.Rect(WIDTH // 4 - BUTTON_WIDTH // 2, 500, BUTTON_WIDTH, BUTTON_HEIGHT)
        save_button = pygame.Rect(3 * WIDTH // 4 - BUTTON_WIDTH // 2, 500, BUTTON_WIDTH, BUTTON_HEIGHT)

        for button, label, color in [(cancel_button, "×", RED), (save_button, "√", GREEN)]:
            mouse_pos = pygame.mouse.get_pos()
            if button.collidepoint(mouse_pos):
                pygame.draw.rect(screen, HOVER_COLOR, button, border_radius=5)
            else:
                pygame.draw.rect(screen, color, button, border_radius=5)
            button_surface = TEXT_FONT.render(label, True, BLACK)
            button_rect = button_surface.get_rect(center=button.center)
            screen.blit(button_surface, button_rect)

        # Update display
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    next_screen = main()
    print(f"Transitioning to: {next_screen}")

