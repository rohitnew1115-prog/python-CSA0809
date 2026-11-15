"""Isolated experiment: a broad except hides a controlled NameError."""


def main():
    try:
        line_number = 7
        print(line_numer)  # Deliberate spelling error for the assignment experiment.
    except Exception:
        pass
    print("Program continued; the NameError was hidden.")


if __name__ == "__main__":
    main()
