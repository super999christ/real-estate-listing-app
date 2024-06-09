import os


def count_startup() -> None:
    """Function for incrementing a number inside a file."""
    file_path = 'count.txt'

    # Check if the file exists or is empty
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        # Read the last line's number and add one to it
        with open(file_path, 'r') as file:
            first_line = file.readline(5_000_000).strip()
            last_number = int(first_line)
            new_number = last_number + 1

        # Append the new number to the next line
        with open(file_path, 'w') as file:
            file.write(str(new_number) + '\n')
    else:
        # Write the number 1 to the file
        with open(file_path, 'w') as file:
            file.write('1\n')
