import tkinter as tk
from PIL import Image, ImageTk  # Им

class AvatarProject:
    def __init__(self, root):
        self.root = root
        self.root.title("Аватар Легенда об Аанге")
        self.root.geometry("600x800")
        
        self.colors = {
            "bg": "#F0F4F8",
            "card": "#FFFFFF",
            "text": "#2C3E50",
            "fun": "#FFD93D",
            "eat": "#FF8066",
            "sleep": "#47B5FF",
            "fly": "#6BCB77"
        }
        self.root.configure(bg=self.colors["bg"])

        self.satiety = 50
        self.fatigue = 0
        self.strength = 50
        self.joy = 50

        self.indices = {"fun": 0, "fly": 0, "sleep": 0, "eat": 0}
        self.images = {"fun": [], "fly": [], "sleep": [], "eat": [], "normal": None}
        
        self.img_size = (380, 380)

        self.load_assets()
        self.setup_ui()

    def load_image_helper(self, filename):
        try:
            full_img = Image.open(filename)
            resized_img = full_img.resize(self.img_size, Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(resized_img)
        except Exception as e:
            print(f"Ошибка загрузки {filename}: {e}")
            return None

    def load_assets(self):

        exts = ['png', 'jpg', 'jpeg', 'webp']
        
        for action in ["fun", "fly", "sleep", "eat"]:
            for i in range(1, 4):
                found = False
                for ext in exts:
                    path = f"{action}{i}.{ext}"
                    img = self.load_image_helper(path)
                    if img:
                        self.images[action].append(img)
                        found = True
                        break
                if not found:
                    self.images[action].append(None)

        for ext in exts:
            img = self.load_image_helper(f"normal.{ext}")
            if img:
                self.images["normal"] = img
                break

    def setup_ui(self):
        self.stats_label = tk.Label(
            self.root, text=self.get_stats_text(),
            font=("Segoe UI", 12, "bold"), bg=self.colors["bg"], fg=self.colors["text"], pady=15
        )
        self.stats_label.pack()

        canvas_frame = tk.Frame(self.root, bg="#D5DBDB", padx=2, pady=2)
        canvas_frame.pack(pady=5)

        self.canvas = tk.Canvas(canvas_frame, width=400, height=400, bg=self.colors["card"], highlightthickness=0)
        self.canvas.pack()
        
        self.avatar_img_item = self.canvas.create_image(200, 200, image=self.images["normal"])
        self.fallback_text = self.canvas.create_text(200, 200, text="", font=("Segoe UI", 18), fill=self.colors["text"])
        
        if not self.images["normal"]:
            self.canvas.itemconfig(self.fallback_text, text="Картинка не найдена\n(Добавьте normal.png)")

        self.speech_label = tk.Label(
            self.root, text="Привет Я Аанг твой персонаж",
            font=("Segoe UI", 11, "italic"), bg="white", width=50, height=3, relief="flat", wraplength=400
        )
        self.speech_label.pack(pady=20)

        btn_frame = tk.Frame(self.root, bg=self.colors["bg"])
        btn_frame.pack(side="bottom", pady=20)

        self.create_btn(btn_frame, "Веселиться", self.colors["fun"], self.action_fun, 0, 0)
        self.create_btn(btn_frame, "Съесть", self.colors["eat"], self.action_eat, 0, 1)
        self.create_btn(btn_frame, "Спать", self.colors["sleep"], self.action_sleep, 1, 0)
        self.create_btn(btn_frame, "Полететь", self.colors["fly"], self.action_fly, 1, 1)

    def create_btn(self, frame, text, color, command, r, c):
        btn = tk.Button(
            frame, text=text, bg=color, command=command,
            font=("Segoe UI", 10, "bold"), width=15, height=2,
            relief="flat", cursor="hand2", fg="#2C3E50" if text == "Веселиться" else "white"
        )
        btn.grid(row=r, column=c, padx=10, pady=10)

    def get_stats_text(self):
        return (f"Сытость: {self.satiety}%   |   Усталость: {self.fatigue}%\n"
                f"Сила: {self.strength}%   |   Радость: {self.joy}%")

    def update_view(self, action_type, message):
        idx = self.indices[action_type]
        img_list = self.images[action_type]
        
        if img_list[idx]:
            self.canvas.itemconfig(self.avatar_img_item, image=img_list[idx])
            self.canvas.itemconfig(self.fallback_text, text="")
        else:
            self.canvas.itemconfig(self.avatar_img_item, image="")
            self.canvas.itemconfig(self.fallback_text, text=f"Фото {action_type}{idx+1} не найдено")

        self.indices[action_type] = (idx + 1) % 3
        self.speech_label.config(text=message)
        self.stats_label.config(text=self.get_stats_text())


    def action_eat(self):
        if self.satiety < 100:
            self.satiety = min(100, self.satiety + 20)
            self.update_view("eat", "Ммм очень вкусные пельмени")
        else:
            self.speech_label.config(text="Я ......")

    def action_fly(self):
        if self.fatigue >= 100:
            self.speech_label.config(text=" Не могу больше летать, я голоден")
        else:
            self.fatigue = min(100, self.fatigue + 15)
            self.update_view("fly", "До встречи, увидимся.")

    def action_sleep(self):
        if self.strength < 100:
            self.strength = min(100, self.strength + 20)
            self.fatigue = max(0, self.fatigue - 20)
            msg = "Спокойной ночи."
            if self.strength == 100:
                msg = " Я полон сил,  хочу полететь"
            self.update_view("sleep", msg)
        else:
            self.speech_label.config(text="Я полон сил, я хочу полететь!")

    def action_fun(self):
        if self.joy < 100:
            self.joy = min(100, self.joy + 20)
            self.update_view("fun", "Юху Это было весело")
        else:
            self.speech_label.config(text="Я не могу веселиться  больше 100 процентов.")

if __name__ == "__main__":
    root = tk.Tk()
    app = AvatarProject(root)
    root.mainloop()
