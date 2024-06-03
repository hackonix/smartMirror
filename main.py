from UserInterface import MainScreen
import tkinter as tk


def main():
    root = tk.Tk()
    root.wm_attributes("-modified", True, "-fullscreen", True)
    app = MainScreen(root)
    root.mainloop()


if __name__ == "__main__":
    main()
