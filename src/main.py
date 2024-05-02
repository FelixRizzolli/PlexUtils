from menu import Menu


def option_1():
    print("\nYou selected Option 1.")


def menu():
    menu_list = Menu([
        {"id": "1", "name": "Option 1", "action": option_1}
    ])

    while True:
        print("\nConsole Menu:")
        for option in menu_list.get_list():
            print(f"{option["id"]}. {option["name"]}")

        choice = input("\nEnter your choice: ")

        if menu_list.id_exists(choice):
            menu_list.get_option_by_id(choice)["action"]()
        else:
            print("\nInvalid choice. Please enter a valid option.")


if __name__ == '__main__':
    menu()
