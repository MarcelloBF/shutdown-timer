import math
import subprocess
import sys
import time
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import messagebox

import customtkinter as ctk


class ShutdownTimerApp(ctk.CTk):
    """Interface e controle do temporizador de desligamento do Windows."""

    def __init__(self) -> None:
        super().__init__()

        self.running = False
        self.remaining_seconds = 0
        self.deadline: float | None = None
        self.shutdown_at: datetime | None = None
        self.timer_job: str | None = None

        self.title("PC Shutdown Timer")
        self.geometry("600x760")
        self.minsize(520, 680)
        self.configure(fg_color=("#f4f7fb", "#0f172a"))
        self.protocol("WM_DELETE_WINDOW", self.close_app)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self._create_variables()
        self._build_interface()
        self._set_initial_state()

    def _create_variables(self) -> None:
        self.hours_var = tk.StringVar(value="00")
        self.minutes_var = tk.StringVar(value="30")
        self.seconds_var = tk.StringVar(value="00")
        self.countdown_var = tk.StringVar(value="00:30:00")
        self.status_var = tk.StringVar(value="Aguardando...")
        self.schedule_var = tk.StringVar(value="")

    def _build_interface(self) -> None:
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=34, pady=(28, 8))
        header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            header,
            text="PC SHUTDOWN TIMER",
            font=ctk.CTkFont(family="Segoe UI", size=26, weight="bold"),
            text_color="#f8fafc",
        ).grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(
            header,
            text="Desligamento automático do Windows",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color="#94a3b8",
        ).grid(row=1, column=0, sticky="w", pady=(3, 0))
        ctk.CTkLabel(
            header,
            text="WINDOWS 10 / 11",
            font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"),
            text_color="#93c5fd",
            fg_color="#172554",
            corner_radius=8,
            padx=10,
            pady=5,
        ).grid(row=0, column=1, rowspan=2, sticky="e")

        self.content = ctk.CTkFrame(
            self,
            corner_radius=24,
            fg_color=("#ffffff", "#172033"),
            border_width=1,
            border_color=("#e2e8f0", "#26344d"),
        )
        self.content.grid(row=1, column=0, sticky="nsew", padx=26, pady=(12, 26))
        self.content.grid_columnconfigure((0, 1, 2), weight=1)

        ctk.CTkLabel(
            self.content,
            text="TEMPO RESTANTE",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            text_color="#60a5fa",
        ).grid(row=0, column=0, columnspan=3, pady=(35, 7))

        ctk.CTkLabel(
            self.content,
            textvariable=self.countdown_var,
            font=ctk.CTkFont(family="Consolas", size=52, weight="bold"),
            text_color="#f8fafc",
        ).grid(row=1, column=0, columnspan=3, pady=(0, 3))

        ctk.CTkLabel(
            self.content,
            textvariable=self.schedule_var,
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color="#94a3b8",
        ).grid(row=2, column=0, columnspan=3, pady=(0, 28))

        ctk.CTkLabel(
            self.content,
            text="Defina a duração do temporizador",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color="#e2e8f0",
        ).grid(row=3, column=0, columnspan=3, pady=(0, 12))

        self._create_time_input("Horas", self.hours_var, 0)
        self._create_time_input("Minutos", self.minutes_var, 1)
        self._create_time_input("Segundos", self.seconds_var, 2)

        self.start_button = ctk.CTkButton(
            self.content,
            text="▶  INICIAR DESLIGAMENTO",
            command=self.start_timer,
            height=52,
            corner_radius=14,
            font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
            fg_color="#2563eb",
            hover_color="#1d4ed8",
        )
        self.start_button.grid(row=6, column=0, columnspan=3, sticky="ew", padx=46, pady=(32, 12))

        self.cancel_button = ctk.CTkButton(
            self.content,
            text="■  CANCELAR",
            command=self.cancel_timer,
            height=44,
            corner_radius=12,
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            fg_color="#334155",
            hover_color="#475569",
        )
        self.cancel_button.grid(row=7, column=0, columnspan=3, sticky="ew", padx=46, pady=(0, 27))

        status_panel = ctk.CTkFrame(
            self.content,
            corner_radius=12,
            fg_color=("#f1f5f9", "#101827"),
        )
        status_panel.grid(row=8, column=0, columnspan=3, sticky="ew", padx=30, pady=(0, 30))
        status_panel.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            status_panel,
            text="STATUS",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color="#60a5fa",
        ).grid(row=0, column=0, padx=(16, 10), pady=14)
        ctk.CTkLabel(
            status_panel,
            textvariable=self.status_var,
            anchor="w",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color="#cbd5e1",
        ).grid(row=0, column=1, sticky="ew", padx=(0, 16), pady=14)

        footer = ctk.CTkFrame(self, fg_color="transparent")
        footer.grid(row=2, column=0, sticky="ew", padx=34, pady=(0, 18))
        footer.grid_columnconfigure(0, weight=1)
        ctk.CTkButton(
            footer,
            text="Minimizar",
            command=self.iconify,
            width=100,
            height=30,
            corner_radius=8,
            fg_color="transparent",
            border_width=1,
            border_color="#334155",
            hover_color="#1e293b",
            text_color="#cbd5e1",
        ).grid(row=0, column=1, padx=(8, 0))
        ctk.CTkButton(
            footer,
            text="Fechar",
            command=self.close_app,
            width=80,
            height=30,
            corner_radius=8,
            fg_color="transparent",
            border_width=1,
            border_color="#7f1d1d",
            hover_color="#450a0a",
            text_color="#fca5a5",
        ).grid(row=0, column=2, padx=(8, 0))

    def _create_time_input(self, label: str, variable: tk.StringVar, column: int) -> None:
        field = ctk.CTkFrame(self.content, fg_color="transparent")
        field.grid(row=4, column=column, sticky="ew", padx=8)
        field.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkLabel(
            field,
            text=label,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            text_color="#94a3b8",
        ).grid(row=0, column=0, columnspan=2, pady=(0, 7))
        entry = ctk.CTkEntry(
            field,
            textvariable=variable,
            width=100,
            height=42,
            justify="center",
            font=ctk.CTkFont(family="Consolas", size=18, weight="bold"),
            corner_radius=10,
            border_color="#334155",
        )
        entry.grid(row=1, column=0, columnspan=2, sticky="ew")
        entry.bind("<FocusIn>", lambda event: entry.select_range(0, tk.END))
        entry.bind("<FocusOut>", lambda event: self._normalize_time_field(variable))
        entry.bind("<Return>", lambda event: self._confirm_time_field(variable))

        limit = 59 if label in {"Minutos", "Segundos"} else None
        ctk.CTkButton(
            field,
            text="−",
            command=lambda: self._adjust_time_field(variable, -1, limit),
            width=42,
            height=30,
            corner_radius=8,
            font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold"),
            fg_color="#334155",
            hover_color="#475569",
        ).grid(row=2, column=0, sticky="e", padx=(0, 3), pady=(8, 0))
        ctk.CTkButton(
            field,
            text="+",
            command=lambda: self._adjust_time_field(variable, 1, limit),
            width=42,
            height=30,
            corner_radius=8,
            font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold"),
            fg_color="#334155",
            hover_color="#475569",
        ).grid(row=2, column=1, sticky="w", padx=(3, 0), pady=(8, 0))

    def _set_initial_state(self) -> None:
        self.cancel_button.configure(state="disabled")

    @staticmethod
    def _normalize_time_field(variable: tk.StringVar) -> None:
        value = variable.get().strip()
        if not value:
            variable.set("00")

    @staticmethod
    def _adjust_time_field(variable: tk.StringVar, amount: int, limit: int | None) -> None:
        value = variable.get().strip()
        current = int(value) if value.isdigit() else 0
        adjusted = max(0, current + amount)
        if limit is not None:
            adjusted = min(limit, adjusted)
        variable.set(f"{adjusted:02d}")

    def _confirm_time_field(self, variable: tk.StringVar) -> str:
        self._normalize_time_field(variable)
        return "break"

    @staticmethod
    def _read_duration(hours: str, minutes: str, seconds: str) -> tuple[int, str | None]:
        values = tuple(value.strip() or "0" for value in (hours, minutes, seconds))
        if any(not value.isdigit() for value in values):
            return 0, "Use apenas números inteiros nos campos de tempo."

        hour_value, minute_value, second_value = (int(value) for value in values)
        if minute_value > 59 or second_value > 59:
            return 0, "Minutos e segundos devem estar entre 0 e 59."

        total = hour_value * 3600 + minute_value * 60 + second_value
        if total <= 0:
            return 0, "Defina um tempo maior que zero."
        return total, None

    @staticmethod
    def _format_seconds(total_seconds: int) -> str:
        hours, remainder = divmod(max(0, total_seconds), 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def start_timer(self) -> None:
        if self.running:
            return

        total_seconds, error = self._read_duration(
            self.hours_var.get(), self.minutes_var.get(), self.seconds_var.get()
        )
        if error:
            messagebox.showwarning("Tempo inválido", error, parent=self)
            return

        if not messagebox.askyesno(
            "Confirmar desligamento",
            "Seu computador será desligado automaticamente após o término do timer.\n\nDeseja continuar?",
            parent=self,
        ):
            return

        try:
            self._schedule_windows_shutdown(total_seconds)
        except (OSError, subprocess.CalledProcessError) as error:
            messagebox.showerror(
                "Não foi possível programar",
                f"O Windows não aceitou o comando de desligamento.\n\n{error}",
                parent=self,
            )
            return

        self.running = True
        self.remaining_seconds = total_seconds
        self.deadline = time.monotonic() + total_seconds
        self.shutdown_at = datetime.now() + timedelta(seconds=total_seconds)
        self.countdown_var.set(self._format_seconds(total_seconds))
        self.schedule_var.set(f"Desligamento previsto para {self.shutdown_at:%H:%M:%S}")
        self.status_var.set("Contagem regressiva em andamento...")
        self.start_button.configure(state="disabled")
        self.cancel_button.configure(state="normal")
        self._tick()

    @staticmethod
    def _schedule_windows_shutdown(total_seconds: int) -> None:
        if sys.platform != "win32":
            raise OSError("Este aplicativo foi projetado para Windows 10 e Windows 11.")
        subprocess.run(
            ["shutdown", "/s", "/t", str(total_seconds)],
            check=True,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )

    @staticmethod
    def _abort_windows_shutdown() -> None:
        if sys.platform != "win32":
            return
        subprocess.run(
            ["shutdown", "/a"],
            check=True,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )

    def _tick(self) -> None:
        if not self.running or self.deadline is None:
            return

        remaining = max(0, math.ceil(self.deadline - time.monotonic()))
        self.remaining_seconds = remaining
        self.countdown_var.set(self._format_seconds(remaining))

        if remaining <= 0:
            self.running = False
            self.timer_job = None
            self.start_button.configure(state="normal")
            self.cancel_button.configure(state="disabled")
            self.status_var.set("Computador será desligado agora")
            self.schedule_var.set("")
            return

        self.timer_job = self.after(250, self._tick)

    def cancel_timer(self) -> None:
        if not self.running:
            return

        try:
            self._abort_windows_shutdown()
        except (OSError, subprocess.CalledProcessError) as error:
            messagebox.showerror(
                "Não foi possível cancelar",
                f"O Windows não aceitou o comando shutdown /a.\n\n{error}",
                parent=self,
            )
            return

        self._reset_timer("Desligamento cancelado")

    def _reset_timer(self, status: str) -> None:
        if self.timer_job is not None:
            self.after_cancel(self.timer_job)
            self.timer_job = None
        self.running = False
        self.remaining_seconds = 0
        self.deadline = None
        self.shutdown_at = None
        self.countdown_var.set("00:00:00")
        self.schedule_var.set("")
        self.status_var.set(status)
        self.start_button.configure(state="normal")
        self.cancel_button.configure(state="disabled")

    def close_app(self) -> None:
        if self.running:
            should_close = messagebox.askyesno(
                "Timer em andamento",
                "Existe um desligamento programado. Deseja cancelar e fechar o aplicativo?",
                parent=self,
            )
            if not should_close:
                return
            try:
                self._abort_windows_shutdown()
            except (OSError, subprocess.CalledProcessError):
                messagebox.showerror(
                    "Não foi possível fechar",
                    "Cancele o desligamento pelo Windows antes de fechar o aplicativo.",
                    parent=self,
                )
                return
        self.destroy()


if __name__ == "__main__":
    app = ShutdownTimerApp()
    app.mainloop()
