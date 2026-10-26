import threading
import tkinter as tk
from tkinter import messagebox, ttk

from desktop.weather import Weather, get_weather


class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather App")
        self.root.geometry("400x400")
        self.root.resizable(False, False)

        # --- Стили ---
        style = ttk.Style()
        style.configure("TLabel", font=("Segoe UI", 10))
        style.configure("Header.TLabel", font=("Segoe UI", 14, "bold"))
        style.configure("Temp.TLabel", font=("Segoe UI", 28, "bold"))

        self.create_widgets()
        # По умолчанию загружаем Москву при старте
        self.search_weather("Moscow")

    def create_widgets(self):
        # --- Блок поиска ---
        search_frame = ttk.Frame(self.root, padding="10 15 10 5")
        search_frame.pack(fill=tk.X)

        self.city_entry = ttk.Entry(search_frame, font=("Segoe UI", 11))
        self.city_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.city_entry.bind(
            "<Return>", lambda event: self.search_weather(self.city_entry.get().strip())
        )

        self.search_btn = ttk.Button(
            search_frame, text="Найти", command=self.on_search_click
        )
        self.search_btn.pack(side=tk.RIGHT)

        # --- Блок с результатами ---
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        self.city_label = ttk.Label(
            main_frame, text="Введите город", style="Header.TLabel"
        )
        self.city_label.pack(pady=(0, 10))

        self.temp_label = ttk.Label(main_frame, text="--°C", style="Temp.TLabel")
        self.temp_label.pack(pady=(0, 5))

        self.desc_label = ttk.Label(main_frame, text="--")
        self.desc_label.pack(pady=(0, 20))

        info_frame = ttk.Frame(main_frame)
        info_frame.pack(fill=tk.X)

        self.feels_like_label = ttk.Label(info_frame, text="Ощущается как: --°C")
        self.feels_like_label.pack(anchor=tk.W, pady=3)

        self.wind_label = ttk.Label(info_frame, text="Скорость ветра: -- м/с")
        self.wind_label.pack(anchor=tk.W, pady=3)

        self.refresh_btn = ttk.Button(
            main_frame,
            text="Обновить",
            command=lambda: self.search_weather(self.city_entry.get().strip()),
        )
        self.refresh_btn.pack(pady=(25, 0))

    def on_search_click(self):
        city = self.city_entry.get().strip()
        if city:
            self.search_weather(city)
        else:
            messagebox.showwarning("Внимание", "Пожалуйста, введите название города.")

    def search_weather(self, city_name: str):
        if not city_name:
            return

        # Блокируем кнопки и показываем загрузку
        self.search_btn.config(state=tk.DISABLED)
        self.refresh_btn.config(state=tk.DISABLED)
        self.city_label.config(text="Загрузка...")
        self.temp_label.config(text="--°C")
        self.desc_label.config(text="--")
        self.feels_like_label.config(text="Ощущается как: --°C")
        self.wind_label.config(text="Скорость ветра: -- м/с")

        # Запускаем запрос в отдельном потоке, чтобы окно не зависало
        threading.Thread(
            target=self._fetch_data, args=(city_name,), daemon=True
        ).start()

    def _fetch_data(self, city_name: str):
        try:
            weather = get_weather(city_name)
            if weather:
                self.root.after(0, self._update_ui, weather)
            else:
                self.root.after(
                    0,
                    self._show_error,
                    f"Не удалось найти город '{city_name}'.\nПроверьте название или ваш API-токен.",
                )
        except Exception as e:
            self.root.after(0, self._show_error, str(e))

    def _update_ui(self, weather: Weather):
        self.city_label.config(text=weather.name)
        self.temp_label.config(text=f"{weather.temp}°C")
        self.desc_label.config(text=weather.description.capitalize())
        self.feels_like_label.config(text=f"Ощущается как: {weather.feels_like}°C")
        self.wind_label.config(text=f"Скорость ветра: {weather.wind_speed} м/с")

        # Разблокируем кнопки
        self.search_btn.config(state=tk.NORMAL)
        self.refresh_btn.config(state=tk.NORMAL)

    def _show_error(self, message):
        messagebox.showerror("Ошибка", message)
        self.city_label.config(text="Ошибка")
        self.search_btn.config(state=tk.NORMAL)
        self.refresh_btn.config(state=tk.NORMAL)


def main() -> None:
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()
