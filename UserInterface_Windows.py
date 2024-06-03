from tkinter import *
import cv2
from PIL import Image, ImageTk
from datetime import datetime
import requests

LABEL_LARGE_FONT = ("Arial", 20)
LABEL_SMALL_FONT = ("Arial", 12)


class MainScreen:
    def __init__(self, root: Tk, screen_size: str = "1920x1080") -> None:
        self.root = root
        self.root.title("Timski projekt | SmartMirror")
        self.root.geometry(screen_size)

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # ----------------------
        # VIDEO FRAME
        # ----------------------
        self.video_label = Label(self.root)
        self.video_label.grid(row=0, column=0, sticky="nsew")

        self.cap = cv2.VideoCapture(0)

        # -----------------------------
        # FRAME - DATUM I VRIJEME LABELS
        # -----------------------------

        self.top_frame_label_2 = Label(
            self.root,
            text="Ucitavanje...",
            font=LABEL_SMALL_FONT,
            bd=1,
            fg="white",
            bg="black",
            padx=5,
            pady=5,
            justify=CENTER,
        )
        self.top_frame_label_2.place(relx=0.025, rely=0.025, anchor=NW)

        # -----------------------------
        # FRAME - TEMPERATURA LABELS
        # -----------------------------

        self.top_frame_label_4 = Label(
            self.root,
            text="Ucitavanje...",
            font=LABEL_SMALL_FONT,
            bd=1,
            fg="white",
            bg="black",
            padx=5,
            pady=5,
            justify=CENTER,
        )
        self.top_frame_label_4.place(relx=0.975, rely=0.025, anchor=NE)

        # -----------------------------
        # CITAT LABELS
        # -----------------------------

        self.top_frame_citat_label_2 = Label(
            self.root,
            text="Ucitavanje...",
            font=LABEL_SMALL_FONT,
            bd=1,
            fg="white",
            bg="black",
            padx=5,
            pady=5,
            justify=CENTER,
        )
        self.top_frame_citat_label_2.place(relx=0.975, rely=0.45, anchor=NE)

        # --------------------------
        # UPDATEAJ PODATKE
        # --------------------------
        self.update_frame()

        self.root.after(1000, self.update_time)
        self.root.after(1000, self.update_quote)
        self.root.after(1000, self.update_temperature)

    # -----------------------
    # FUNKCIJE
    # -----------------------
    # -----------------------
    # DATUM I VRIJEME
    # -----------------------
    def update_time(self):
        """Ažuriraj vrijeme u Tkinter prozoru"""
        trenutno_vrijeme = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.top_frame_label_2.configure(text=f"Datum i vrijeme: {trenutno_vrijeme}")
        self.root.after(1000, self.update_time)

    # -----------------------
    # TRENUTNA TEMPERATURA
    # -----------------------
    def update_temperature(self, grad="Zagreb"):
        Api_Key = "2606f769271b8d545fe3458b2b72ed9f"
        final_URL = f"http://api.openweathermap.org/data/2.5/weather?q={grad}&appid={Api_Key}&units=metric"
        try:
            response = requests.get(final_URL)
            response.raise_for_status()
            data = response.json()
            temperature = data["main"]["temp"]
            grad_display = grad
            self.top_frame_label_4.configure(
                text=f"Temperatura u mjestu {grad_display}: {temperature}°C"
            )
        except requests.exceptions.RequestException as e:
            self.top_frame_label_4.configure(text=f"Greska: {e}")
        self.root.after(5000, self.update_temperature)

    # -----------------------
    # CITAT DANA
    # -----------------------
    def return_quote(self, url="https://api.tronalddump.io/random/quote"):
        """Dohvati random Donald Tramp quote sa URL-a"""
        response = requests.get(url)
        result = response.json()["value"]
        return result

    def format_quote(self, quote, words_per_line=6):
        """formatiraj Donald Trump quote na duzinu od n rijeci po liniji"""
        words = quote.split()
        formatted_quote = ""
        for i in range(0, len(words), words_per_line):
            formatted_quote += " ".join(words[i : i + words_per_line]) + "\n"
        return formatted_quote.strip()

    def update_quote(self):
        self.top_frame_citat_label_2.configure(
            text=self.format_quote(self.return_quote())
        )
        self.root.after(15000, self.update_quote)

    # -----------------------
    # VIDEO CAPTURE
    # -----------------------
    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Get the current window dimensions
            window_width = self.root.winfo_width()
            window_height = self.root.winfo_height()

            # Resize the frame to fit the window
            frame = cv2.resize(frame, (window_width, window_height))

            img = Image.fromarray(frame)
            self.imgtk = ImageTk.PhotoImage(image=img)

            self.video_label.imgtk = self.imgtk
            self.video_label.configure(image=self.imgtk)

        self.video_label.after(10, self.update_frame)

    def __del__(self):
        self.cap.release()
        cv2.destroyAllWindows()
