"""Assistente grafico (tkinter) do instalador da traducao PT-BR de P5R.

Fluxo: detecta/escolhe a pasta do jogo -> (opcional) pasta do Reloaded-II ->
instala o mod e tenta ativa-lo -> mostra os proximos passos. Toda a logica
pesada vem de steam.py e reloaded.py.
"""

from __future__ import annotations

import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, scrolledtext

from . import reloaded, steam

TITLE = "Tradução PT-BR — Persona 5 Royal (instalador)"

DISCLAIMER = (
    "Projeto de fã, não-oficial (sem vínculo com Atlus/Sega). Você precisa ter o "
    "jogo legalmente. Este instalador aplica a tradução; não distribui o jogo."
)


class InstallerApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        root.title(TITLE)
        root.geometry("640x520")

        tk.Label(root, text=TITLE, font=("Segoe UI", 13, "bold")).pack(pady=(12, 2))
        tk.Label(root, text=DISCLAIMER, wraplength=600, justify="left", fg="#555").pack(
            padx=16, pady=(0, 10)
        )

        # Pasta do jogo
        self.game_var = tk.StringVar()
        self._path_row("Pasta do Persona 5 Royal (contém P5R.exe):", self.game_var, self._browse_game)

        # Pasta do Reloaded-II (opcional)
        self.reloaded_var = tk.StringVar()
        self._path_row(
            "Pasta do Reloaded-II (opcional — deixe vazio para baixar):",
            self.reloaded_var,
            self._browse_reloaded,
        )

        btns = tk.Frame(root)
        btns.pack(pady=8)
        tk.Button(btns, text="Detectar jogo automaticamente", command=self._autodetect).pack(
            side="left", padx=4
        )
        self.install_btn = tk.Button(
            btns, text="Instalar tradução", command=self._install_async, default="active"
        )
        self.install_btn.pack(side="left", padx=4)

        self.log_widget = scrolledtext.ScrolledText(root, height=14, state="disabled")
        self.log_widget.pack(fill="both", expand=True, padx=16, pady=10)

        self._autodetect(silent=True)

    # ----- UI helpers -----
    def _path_row(self, label: str, var: tk.StringVar, browse) -> None:
        frame = tk.Frame(self.root)
        frame.pack(fill="x", padx=16, pady=2)
        tk.Label(frame, text=label, anchor="w").pack(fill="x")
        row = tk.Frame(frame)
        row.pack(fill="x")
        tk.Entry(row, textvariable=var).pack(side="left", fill="x", expand=True)
        tk.Button(row, text="Procurar...", command=browse).pack(side="left", padx=(6, 0))

    def log(self, msg: str) -> None:
        self.log_widget.configure(state="normal")
        self.log_widget.insert("end", msg + "\n")
        self.log_widget.see("end")
        self.log_widget.configure(state="disabled")
        self.root.update_idletasks()

    def _browse_game(self) -> None:
        path = filedialog.askdirectory(title="Selecione a pasta do Persona 5 Royal")
        if path:
            self.game_var.set(path)

    def _browse_reloaded(self) -> None:
        path = filedialog.askdirectory(title="Selecione a pasta do Reloaded-II")
        if path:
            self.reloaded_var.set(path)

    def _autodetect(self, silent: bool = False) -> None:
        found = steam.find_game_via_steam()
        if found:
            self.game_var.set(str(found))
            self.log(f"Jogo detectado: {found}")
        elif not silent:
            messagebox.showinfo(
                TITLE, "Não encontrei o jogo automaticamente. Selecione a pasta manualmente."
            )

    # ----- instalacao -----
    def _install_async(self) -> None:
        self.install_btn.configure(state="disabled")
        threading.Thread(target=self._install, daemon=True).start()

    def _install(self) -> None:
        try:
            self._do_install()
        except Exception as exc:  # noqa: BLE001 - reportar qualquer erro na UI
            self.log(f"ERRO: {exc}")
            messagebox.showerror(TITLE, f"Falha na instalação:\n{exc}")
        finally:
            self.install_btn.configure(state="normal")

    def _do_install(self) -> None:
        game = Path(self.game_var.get().strip())
        if not game or not steam.looks_like_game_dir(game):
            messagebox.showwarning(
                TITLE, "Pasta do jogo inválida (não encontrei P5R.exe). Verifique o caminho."
            )
            return

        mod_src = reloaded.bundled_mod_dir()
        self.log(f"Mod da tradução: {mod_src}")

        reloaded_root = self.reloaded_var.get().strip()
        if not reloaded_root:
            self.log("Reloaded-II não informado. Tentando baixar o instalador oficial...")
            url = reloaded.latest_reloaded_setup_url()
            if url:
                dest = Path.home() / "Downloads" / "Reloaded-II-Setup.exe"
                try:
                    reloaded.download_file(url, dest)
                    self.log(f"Baixado: {dest}")
                    self.log(
                        "Rode esse Setup.exe para instalar o Reloaded-II, depois rode este "
                        "instalador de novo apontando a pasta do Reloaded-II."
                    )
                except Exception as exc:  # noqa: BLE001
                    self.log(f"Não consegui baixar automaticamente ({exc}).")
                    self.log("Baixe o Reloaded-II em: https://reloaded-project.github.io/Reloaded-II/")
            else:
                self.log("Baixe o Reloaded-II em: https://reloaded-project.github.io/Reloaded-II/")
            messagebox.showinfo(
                TITLE,
                "Instale o Reloaded-II e rode este instalador de novo indicando a pasta dele "
                "para concluir a instalação automática do mod.",
            )
            return

        reloaded_root_path = Path(reloaded_root)
        mods_dir = reloaded_root_path / "Mods"
        mods_dir.mkdir(parents=True, exist_ok=True)
        dest = reloaded.install_mod_files(mods_dir, mod_src)
        self.log(f"Mod instalado em: {dest}")

        mod_ids = [reloaded.MOD_ID, *reloaded.mod_dependencies(mod_src)]
        changed = reloaded.enable_mod_in_app_configs(reloaded_root_path, mod_ids)
        if changed:
            self.log(f"Mod ativado para o jogo em {len(changed)} configuração(ões).")
        else:
            self.log(
                "Não localizei a configuração do jogo no Reloaded-II. Abra o Reloaded-II, "
                "adicione o Persona 5 Royal e ative o mod 'Tradução PT-BR' (ele baixa as "
                "dependências sozinho)."
            )

        self.log("\nConcluído! Abra o jogo pelo Reloaded-II.")
        messagebox.showinfo(TITLE, "Tradução instalada! Abra o jogo pelo Reloaded-II.")


def main() -> None:
    root = tk.Tk()
    InstallerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
