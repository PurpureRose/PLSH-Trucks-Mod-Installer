from lib.gui import *
from lib.utils import *
from tkinter import filedialog
import threading

class ModInstallerApp:
    def __init__(self):
        
        self.root = ttk.Window(themename="darkly")  # Инициализация стиля
        self.gui = ModInstallerGui(self.root)       # Инициализия интерфейса
        self.app = ModInstallerCore()               # Инициализация функций
        self.guifunction = GuiFunctions(self.gui)   # Инициализация функций интерфейса

        self.root.iconbitmap(self.app.app_dir + '\\resources\\icon.ico')
   
        self.selected_tab = 0                       # Вкладка по умолчанию

        self.gui.tab_manager.bind("<<NotebookTabChanged>>", self.on_tab_selection) # привязываем функцию к событию смены вкладки 
        self.gui.ets2_profiles_listbox.bind("<<ListboxSelect>>")                   # привязываем событие выбора элемента в списке

        self.profiles_data = {} # Информация про профили тута

        self.gui.ets2_find_profile_button.configure(command=self.profile_locator)
        self.gui.ats_find_profile_button.configure(command=self.profile_locator)

        self.gui.ets2_download_button.configure(command=self.download_mods)
        self.gui.ats_download_button.configure(command=self.download_mods)

        self.gui.ets2_install_button.configure(command=self.install_modlist)
        self.gui.ats_install_button.configure(command=self.install_modlist)

        self.gui.ets2_export_button.configure(command=self.export_modlist)
        self.gui.ats_export_button.configure(command=self.export_modlist)
        
        self.gui.ets_link_label.configure(text=f'Download id ETS2: {self.app.ets_mods_id}')
        self.gui.ats_link_label.configure(text=f'Download id ATS: {self.app.ats_mods_id}')

        self.gui.cleaning_button.configure(command=self.app.emergency_cleaning)

        self.root.mainloop()

    def on_tab_selection(self, event):
        
        self.selected_tab = self.gui.tab_manager.index(self.gui.tab_manager.select()) # Получаем 0 или 1 на основе выбранного меню
        self.app.game_type(self.selected_tab)                                         # В зависимости от результата обновляем директории
        
        if self.selected_tab == 0:
            self.profiles_listbox = self.gui.ets2_profiles_listbox
        elif self.selected_tab == 1:
            self.profiles_listbox = self.gui.ats_profiles_listbox  
        
        self.profiles_data.clear() # Чистка листа профилей на всякий случай

        self.app.download_mods_check() #Чекаем на предмет уже скачанных модов
        if self.app.mods_downloaded == True:
            self.gui.bottom_log.configure(text='Моды уже скачанны', foreground='')
        elif self.app.mods_downloaded == False:
            self.gui.bottom_log.configure(text='Моды не скачанны', foreground='')

    def profile_locator(self):

        self.app.profile_search()
        self.profiles_data.clear()
        self.profiles_data.update(self.app.profiles)
        self.profiles_listbox.delete(0, ttk.END)

        for profile_name in self.profiles_data:
            self.profiles_listbox.insert(ttk.END, f"Профиль: {profile_name}")

    def download_mods(self):

        def download_progressbar():

            self.gui.bottom_log.configure(text='Запрос метаданных...', foreground='')
            progress = 0
            while progress < 1:
                for filename in os.listdir(self.app.data_folder):
                    if filename.startswith('mods'):
                        self.gui.bottom_log.configure(text='Загрузка...', foreground='')
                        dw_file = os.path.join(self.app.data_folder, filename)
                        progress = (os.path.getsize(dw_file) / self.app.file_size_bytes)
                        self.gui.progress_bar['value'] = round(progress, 2)
                        if progress >= 1: break

                if progress >= 0.99:
                    self.gui.progress_bar['value'] = 1
                    self.gui.bottom_log.configure(text='Загрузка завершена', foreground='green')
                    break

        target = threading.Thread(target=self.app.download_mods)
        target.start()

        target1 = threading.Thread(target=download_progressbar)
        target1.start()

    def install_modlist(self):

        def install_thread():
            
            index = self.profiles_listbox.curselection()
            try:
                selected_item = self.profiles_listbox.get(index[0])
            except:
                self.gui.bottom_log.configure(text='Не выбран профиль', foreground='red')

            if index:

                self.gui.bottom_log.configure(text='Установка...', foreground='')

                profile_name = selected_item.split(": ")[1]
                profile_location = self.profiles_data[selected_item.split(": ")[1]]

                self.selected_item = self.profiles_listbox.get(index[0])
                self.app.install_mods(profile_name, profile_location)
                        
                self.gui.bottom_log.configure(text='Модлист установлен!', foreground='green')
            else:
                self.gui.bottom_log.configure(text='Не выделен профиль / Нет доступа', foreground='red')

        source_files = [entry for entry in os.scandir(os.path.join(self.app.dw_mods_dir, "mod"))]
        destination_files = [entry for entry in os.path.join(self.app.game_dir, "mod")]

        install = threading.Thread(target=install_thread)
        install.start()

        progressbar = threading.Thread(target=self.guifunction.progressbar_filetransfer(source_files, destination_files))
        progressbar.start()

    def export_modlist(self):
        export_location = filedialog.askdirectory()

        def export_thread():
            index = self.profiles_listbox.curselection()
            if index:
                self.selected_item = self.profiles_listbox.get(index[0])
                profile_name = self.selected_item.split(": ")[1]
                profile_location = self.profiles_data[self.selected_item.split(": ")[1]]

                self.app.export_mods(profile_name, profile_location, export_location)

                self.gui.bottom_log.configure(text=f'Модпак {profile_name} експортирован!', foreground='green')
            else:
                self.gui.bottom_log.configure(text='Не выделен профиль!', foreground='red')

        def progressbar_thread():
            source_files = [entry for entry in os.scandir(os.path.join(self.app.dw_mods_dir, "mod"))]
            destination_files = [entry for entry in os.path.join(export_location, self.app.output_name)]

            if source_files:
                progress = len(destination_files) / len(source_files)
            else:
                progress = 0

            self.gui.progress_bar["value"] = progress

        export = threading.Thread(target=export_thread)
        export.start()

        progressbar = threading.Thread(target=progressbar_thread)
        progressbar.start()

if __name__ == "__main__":
    app_instance = ModInstallerApp()
else:
    raise SystemExit("This is Main File")
