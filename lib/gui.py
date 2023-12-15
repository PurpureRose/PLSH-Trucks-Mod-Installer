import tkinter as tk
import ttkbootstrap as ttk

class ModInstallerGui:
    def __init__(self, root):
       
        self.root = root

        self.root.title("PLSH Mod Installer")
        self.root.geometry("470x411")
        self.root.grid_columnconfigure(0, weight=1)
        root.resizable(width=False, height=False)
        self.custom_font = ttk.font.nametofont("TkDefaultFont")
        self.custom_font.configure(family="Default", size=12, weight="bold")

        self.style = ttk.Style(theme='darkly')
        self.style.configure("TNotebook.Tab", font=self.custom_font)
        
        self.selected_tab = 0
        self.game = self.selected_tab

        self.create_ui()
    
    def create_ui(self):
        self.tab_manager = ttk.Notebook(self.root)
        self.tab_manager.grid(sticky="nsew")
        
        self.bottom_frame = ttk.Frame(self.root)
        self.bottom_frame.grid()

        self.bottom_log = ttk.Label(self.bottom_frame, padding=1, text='')
        self.bottom_log.grid(padx=0, pady=0, sticky="n")

        self.progress_bar = ttk.Progressbar(self.bottom_frame, length=470)
        self.progress_bar.grid(sticky="nsew")
        self.progress_bar["maximum"] = 1

        self.create_ets2_tab()
        self.create_ats_tab()
        self.create_tab_settings() 

    def create_game_tab(self, game_name):
        tab = ttk.Frame(self.tab_manager)
        self.tab_manager.add(tab, text=game_name, sticky="n")

        upper_buttons_grid = ttk.Frame(tab)
        upper_buttons_grid.grid(padx=5, pady=5, column=0, row=1)

        profiles_listbox = tk.Listbox(tab, borderwidth=1, highlightthickness=1, width=47)
        profiles_listbox.grid(padx=5, pady=5, column=0, row=2)

        down_buttons_grid = ttk.Frame(tab)
        down_buttons_grid.grid(padx=5, pady=5, column=0, row=3)

        find_profile_button = ttk.Button(upper_buttons_grid, text="Найти профили", padding=10, width=20, bootstyle="primary")
        find_profile_button.grid(padx=8, pady=5, column=0, row=0)

        download_button = ttk.Button(upper_buttons_grid, text="Скачать модпак", padding=10, width=20, bootstyle="primary")
        download_button.grid(padx=8, pady=5, column=1, row=0)

        install_button = ttk.Button(down_buttons_grid, text="Установить модпак", padding=10, width=20, bootstyle="primary")
        install_button.grid(padx=8, pady=5, column=0, row=0)

        export_button = ttk.Button(down_buttons_grid, text="Экспорт модпака", padding=10, width=20, bootstyle="primary")
        export_button.grid(padx=8, pady=5, column=1, row=0)

        return tab, profiles_listbox, find_profile_button, download_button, install_button, export_button
    
    def create_ets2_tab(self):
        self.ets2_tab, self.ets2_profiles_listbox, self.ets2_find_profile_button, self.ets2_download_button, self.ets2_install_button, self.ets2_export_button = self.create_game_tab("ETS2")

    def create_ats_tab(self):
        self.ats_tab, self.ats_profiles_listbox, self.ats_find_profile_button, self.ats_download_button, self.ats_install_button, self.ats_export_button = self.create_game_tab("ATS")

    def create_tab_settings(self):
        tab_settings = ttk.Frame(self.tab_manager)
        self.tab_manager.add(tab_settings, text="Настройки", sticky="n")

        id_frame = ttk.LabelFrame(tab_settings)
        id_frame.grid()

        self.ets_link_label = ttk.Label(id_frame, font=('TkDefaultFont', 10))
        self.ets_link_label.grid(padx=10, pady=10)

        self.ats_link_label = ttk.Label(id_frame, font=('TkDefaultFont', 10))
        self.ats_link_label.grid(padx=10, pady=10)

        self.change_button = ttk.Button(tab_settings, text="Изменить Download id", padding=10, width=20, command=self.url_entry_popup)
        self.change_button.grid(padx=10, pady=10)

        self.cleaning_button = ttk.Button(tab_settings, text="Очистить данные", padding=10, width=20, bootstyle="danger")
        self.cleaning_button.grid(padx=10, pady=10)

        self.faq_dw_id = ttk.Label(tab_settings, text="Download id можно найти в #poligon_haulage_ltd")
        self.faq_dw_id.grid(padx=10, pady=10, sticky='s')

    def url_entry_popup(self):
        
        popup = ttk.Toplevel(self.root)
        popup.columnconfigure(0, weight=1)
        popup.columnconfigure(1, weight=1)

        popup.title('')

        self.imput_ets_id = ttk.StringVar(value='')
        self.imput_ats_id = ttk.StringVar(value='')

        warning_label = ttk.Label(popup, text='Необходим перезапуск программы!')
        warning_label.grid(row=0, padx=10, pady=10, sticky="n")

        frame_ets = ttk.Frame(popup)
        frame_ets.grid(row=1, padx=10, pady=10, sticky="n")

        frame_ats = ttk.Frame(popup)
        frame_ats.grid(row=2, padx=10, pady=10, sticky="n")
        
        label_ets = ttk.Label(frame_ets, text='ETS2 id: ')
        label_ets.grid(column=0, row=0, sticky="e")
        entry_ets = ttk.Entry(frame_ets, textvariable=self.imput_ets_id, width=45)
        entry_ets.grid(column=1, row=0, sticky="w")
        
        label_ats = ttk.Label(frame_ats, text='ATS id:   ')
        label_ats.grid(column=0, row=0, sticky="e")
        entry_ats = ttk.Entry(frame_ats, textvariable=self.imput_ats_id, width=45)
        entry_ats.grid(column=1, row=0, sticky="w")

        save_button = ttk.Button(popup,text='Сохранить', command=lambda: self.app.settings_url_edit(self.app, self.imput_ets_id.get(), self.imput_ats_id.get()))
        save_button.grid(row=3, padx=10, pady=10, sticky="nsew")

class GuiFunctions:
    def __init__(self, maingui):
        self.maingui = maingui

    def progressbar_filetransfer(self, source_files, destination_files):
        source_files = source_files
        destination_files = destination_files
        if source_files:
            progress = len(destination_files) / len(source_files)
        else:
            progress = 0

        self.maingui.progress_bar["value"] = progress


if __name__ == "__main__":
  ModInstallerGui()
  GuiFunctions()