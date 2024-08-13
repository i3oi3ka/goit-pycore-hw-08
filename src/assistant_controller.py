"""
assistant controller
"""

from difflib import get_close_matches
from prompt_toolkit.completion import Completer, Completion
from src.models.address_book import AddressBook
from src.book_controller import (
    add_contact,
    change_contact,
    show_phone,
    show_all,
    add_birthday,
    show_birthday,
    birthdays,
)

COMMANDS = {
    "add": add_contact,
    "all": show_all,
    "add-birthday": add_birthday,
    "birthdays": birthdays,
    "change": change_contact,
    "phone": show_phone,
    "show-birthday": show_birthday,
    "exit": "",
    "close": "",
    "hello": "",
}


def suggest_command(command, available_commands):
    """
    Suggest the closest matching command based on user input.

    Args:
        command (str): The command to match.
        available_commands (list): List of available command strings.

    Returns:
        str: The closest matching command.
    """
    matches = get_close_matches(command, available_commands, n=1, cutoff=0.6)
    return matches[0] if matches else None


class CommandCompleter(Completer):
    """
    Command completer
    """

    def get_completions(self, document, complete_event):
        # Split input to get the command part only
        text_before_cursor = document.text_before_cursor
        words = text_before_cursor.strip().split()

        # Only suggest completions for the first word (command)
        if len(words) == 1 and " " not in text_before_cursor:
            matches = get_close_matches(
                words[0].lower(), COMMANDS.keys(), n=5, cutoff=0.1
            )
            for match in matches:
                yield Completion(match, start_position=-len(words[0]))


def execute_command(command: str, args: list, book: AddressBook) -> str:
    """
    Execute the given command with the provided arguments and address book.

    Args:
        command (str): The command to execute.
        args (list): The arguments for the command.
        book (AddressBook): The address book data.

    Returns:
        str: The result of the command execution.
    """

    match command:
        case "hello":
            return "How can I help you?"

        case command if command in COMMANDS:
            return COMMANDS[command](args, book)

        case _:
            suggested_command = suggest_command(command, list(COMMANDS.keys()))
            if suggested_command:
                return f"Invalid command. Did you mean '{suggested_command}'?"
            return "Invalid command."
