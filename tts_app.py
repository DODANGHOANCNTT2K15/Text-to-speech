import tkinter as tk
from tts_gui import TTSGui

def main():
    root = tk.Tk()
    app = TTSGui(root)
    root.mainloop()

if __name__ == "__main__":
    main()