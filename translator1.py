import tkinter as tk
from tkinter import ttk, messagebox
import requests
import webbrowser
import urllib.parse

class TranslatorApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🌐 Language Translator")
        self.root.geometry("780x580")
        self.root.resizable(False, False)
        self.root.configure(bg="#f5f6fa")  # soft background

        self.languages = {
            "Auto Detect": "auto",
            "English": "en",
            "Urdu": "ur",
            "French": "fr",
            "Spanish": "es",
            "German": "de",
            "Arabic": "ar",
            "Chinese": "zh"
        }

        self.ui()
        self.root.mainloop()

    def ui(self):
        # ------------- INPUT LABEL -------------
        tk.Label(self.root, text="Enter Text", font=("Helvetica", 13, "bold"), bg="#f5f6fa").pack(pady=(20, 5))

        # ------------- INPUT BOX -------------
        self.input_text = tk.Text(self.root, height=7, width=85, font=("Helvetica", 11),
                                  bg="#ffffff", bd=0, relief="flat", wrap="word", padx=10, pady=10)
        self.input_text.pack(pady=(0, 15))
        self.input_text.configure(highlightbackground="#dcdde1", highlightthickness=1)

        # ------------- LANGUAGE SELECTION FRAME -------------
        frame = tk.Frame(self.root, bg="#f5f6fa")
        frame.pack(pady=10)

        self.src = ttk.Combobox(frame, values=list(self.languages.keys()), width=18, state="readonly", font=("Helvetica", 11))
        self.src.set("Auto Detect")
        self.src.grid(row=0, column=0, padx=8)

        self.dest = ttk.Combobox(frame, values=list(self.languages.keys()), width=18, state="readonly", font=("Helvetica", 11))
        self.dest.set("Urdu")
        self.dest.grid(row=0, column=1, padx=8)

        # ------------- BUTTON STYLING -------------
        style_btn = {"width": 12, "font": ("Helvetica", 11, "bold"), "bg": "#4cd137", "fg": "white",
                     "bd": 0, "activebackground": "#44bd32", "activeforeground": "white", "cursor": "hand2"}

        self.translate_btn = tk.Button(frame, text="Translate 🔁", command=self.translate, **style_btn)
        self.translate_btn.grid(row=0, column=2, padx=6)
        self.translate_btn.bind("<Enter>", lambda e: self.translate_btn.config(bg="#44bd32"))
        self.translate_btn.bind("<Leave>", lambda e: self.translate_btn.config(bg="#4cd137"))

        self.speak_btn = tk.Button(frame, text="Speak 🔊", command=self.speak, **style_btn)
        self.speak_btn.grid(row=0, column=3, padx=6)
        self.speak_btn.bind("<Enter>", lambda e: self.speak_btn.config(bg="#44bd32"))
        self.speak_btn.bind("<Leave>", lambda e: self.speak_btn.config(bg="#4cd137"))

        self.copy_btn = tk.Button(frame, text="Copy 📋", command=self.copy, **style_btn)
        self.copy_btn.grid(row=0, column=4, padx=6)
        self.copy_btn.bind("<Enter>", lambda e: self.copy_btn.config(bg="#44bd32"))
        self.copy_btn.bind("<Leave>", lambda e: self.copy_btn.config(bg="#4cd137"))

        # ------------- OUTPUT LABEL -------------
        tk.Label(self.root, text="Translated Text", font=("Helvetica", 13, "bold"), bg="#f5f6fa").pack(pady=(20, 5))

        # ------------- OUTPUT BOX -------------
        self.output_text = tk.Text(self.root, height=7, width=85, font=("Helvetica", 11),
                                   bg="#f1f2f6", bd=0, relief="flat", wrap="word", padx=10, pady=10)
        self.output_text.pack(pady=(0, 20))
        self.output_text.configure(highlightbackground="#dcdde1", highlightthickness=1)

    # ---------------- TRANSLATE ----------------
    def translate(self):
        text = self.input_text.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Warning", "Enter text first")
            return

        src = self.languages[self.src.get()]
        dest = self.languages[self.dest.get()]

        if src == "auto":
            src = "en"  # safe fallback

        try:
            url = "https://api.mymemory.translated.net/get"
            params = {"q": text, "langpair": f"{src}|{dest}"}
            r = requests.get(url, params=params, timeout=10)
            result = r.json()["responseData"]["translatedText"]

            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, result)

        except:
            messagebox.showerror("Error", "Internet or API issue")

    # ---------------- SPEAK ----------------
    def speak(self):
        text = self.output_text.get("1.0", tk.END).strip()
        if not text:
            return

        encoded = urllib.parse.quote(text)
        webbrowser.open(f"https://translate.google.com/?sl=auto&tl=en&text={encoded}&op=translate")

    # ---------------- COPY ----------------
    def copy(self):
        text = self.output_text.get("1.0", tk.END).strip()
        if text:
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
            messagebox.showinfo("Copied", "Copied successfully")


if __name__ == "__main__":
    TranslatorApp()
