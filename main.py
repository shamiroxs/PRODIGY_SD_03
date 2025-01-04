import list
import add
import view

def main():
    """Main loop to manage transitions between modules."""
    current_screen = "list"  # Initial screen
    
    while True:
        if current_screen == "list":
            current_screen = list.main()
        elif current_screen == "add":
            current_screen = add.main()
        elif current_screen == "view":
            current_screen = view.main()
        else:
            print(f"Unknown screen: {current_screen}")
            break

if __name__ == "__main__":
    main()

