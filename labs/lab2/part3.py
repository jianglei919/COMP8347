def main():
    try:
        height = int(input("Enter height: "))
    except ValueError:
        print("Height must be an integer.")
        return
    if height <= 0:
        print("Height must be positive.")
        return
    for i in range(1, height + 1):
        for _ in range(height - i):
            print(" ", end="")
        for _ in range(2 * i - 1):
            print("*", end="")
        print()


if __name__ == "__main__":
    main()
