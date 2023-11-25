import os
import webbrowser
import subprocess
import gdown
import zipfile
import requests
import re
import shutil
import json

class ModInstallerCore:
    def __init__(self):
        
        with open('settings.json', 'r') as file:
            self.json_data = file.read()

        self.settings_data = json.loads(self.json_data)
        for link in self.settings_data["links"]:
                if link['name'] == 'ETS2':
                    self.ets_mods_id = link['url']
                if link['name'] == 'ATS':
                    self.ats_mods_id = link['url']
        self.app_dir = os.getcwd()
        
    def game_type(self, game):
        self.game = game
        
        home_dir = os.path.join(os.path.expanduser("~")) #директория виндовских юзеверей

        documents_default = os.path.join(home_dir, 'Documents' or 'Документы')
        documents_onedrive = os.path.join((os.path.join(home_dir, 'OneDrive')), 'Documents' or 'Документы') 
        
        if os.path.exists(os.path.join(documents_default, 'Euro Truck Simulator 2')) or os.path.exists(os.path.join(documents_default, 'American Truck Simulator')):
            self.documents = documents_default
        elif os.path.exists(os.path.join(documents_onedrive, 'Euro Truck Simulator 2')) or os.path.exists(os.path.join(documents_onedrive, 'American Truck Simulator')):
            self.documents = documents_onedrive
        
        self.data_folder = os.path.join(self.app_dir, 'data')
        os.makedirs(self.data_folder, exist_ok=True)

        if self.game == 0:
            self.game_dir = os.path.join(self.documents, 'Euro Truck Simulator 2')
            self.users_dir = os.path.join(self.game_dir, 'profiles')
            self.dw_mods_dir = os.path.join(self.data_folder, 'ETS2')
            self.mods_id = self.ets_mods_id #данные из json
            self.steamlink = 'https://steamcommunity.com/sharedfiles/filedetails/?id=2581290581'
        elif self.game == 1:
            self.game_dir = os.path.join(self.documents, 'American Truck Simulator')
            self.users_dir = os.path.join(self.game_dir, 'profiles')
            self.dw_mods_dir = os.path.join(self.data_folder, 'ATS')
            self.mods_id = self.ats_mods_id #данные из json
            self.steamlink = 'https://steamcommunity.com/sharedfiles/filedetails/?id=2682389791'
        os.makedirs(self.dw_mods_dir, exist_ok=True)

    def open_workshop(self):
        webbrowser.open(self.steamlink)

    def profile_search(self):
        self.profiles = {}                                                                      #найденные профили запишем в этот словарь
        self.encryptor_path = os.path.join(self.app_dir, 'resources\\tools\\SII_Decrypt.exe')
        for dirpath, _, filenames in os.walk(self.users_dir):
            if 'profile.sii' in filenames:
                self.profile_path = os.path.join(dirpath, 'profile.sii')
                
                decrypt = subprocess.Popen([self.encryptor_path, self.profile_path], shell=True) #Дешефруем найденные файлики
                decrypt.wait() 
                
                with open(self.profile_path, 'r', encoding='utf-8', errors='ignore') as file:    #Поиск имени профиля в расшированном файле
                    names = file.readlines()
                    for line in names:
                        if "profile_name:" in line: 
                            self.profile_name = line.split("profile_name:")[1].strip()
                            self.profiles[self.profile_name] = self.profile_path                 #Запись в словарь имени профиля с прикреплённым к нему расположением онного                  

    def download_mods(self):
        
        try: #Чистка старых фалов             
            for filename in os.scandir(self.dw_mods_dir):
                os.remove(filename)
                for files in os.scandir(self.dw_mods_dir + '\\mod'):
                    os.remove(files.path)

            for file_name in os.listdir(self.data_folder):
                if file_name.startswith("mods"):
                    file_path = os.path.join(self.data_folder, file_name)
            os.remove(file_path)
        except: pass #Дабы не было ошибки в случае ненахода

        self.download_link = f'https://drive.google.com/uc?id={self.mods_id}'
        
        self.response = requests.get(self.download_link)            #Парсим страничу с файлом
        self.matches = re.findall(r'\((.*?)\)', self.response.text) #Ответ даётся в виде листа

        self.size_dict = {'G':1024 ** 3, 'M': 1024 ** 2, 'K': 1024} #Словарь для конвертации форматов
        
        for file_size_string in self.matches: #Поиск веса файла в парснутой страничке
            file_size_match = re.match(r'(\d+(\.\d+)?)\s*([GgMmKk])B?', file_size_string)

            if file_size_match:
                value = file_size_match.group(1)
                unit = file_size_match.group(3).upper()

                value_float = float(value)

                if unit in self.size_dict:
                    self.file_size_bytes = int(value_float * self.size_dict[unit])   
        
        self.downloaded_file = os.path.join(self.data_folder, 'mods.zip')
        
        try: gdown.download(self.download_link, self.downloaded_file) 
        except gdown.DownloadError as e: print(f'Download Error:{e}')
        
        with zipfile.ZipFile(self.downloaded_file, 'r') as zip_file: #Распаковка с последующим удалением архива
            zip_file.extractall(self.dw_mods_dir)
        os.remove(self.downloaded_file)  
    
    def install_mods(self, profile_name, profile_location):
        
        self.profile_name = profile_name
        self.profile_location = profile_location

        source_path = os.path.join(self.dw_mods_dir, 'mod')
        destination_path = os.path.join(self.game_dir, 'mod')
       
        pattern_a = r'active_mods:\s+(\S+)'             #active_mods: x
        pattern_b = r'active_mods(?:\[\d+\]?: "[^"]+")' #active_mods[x]: 'sample_text'
        
        with open(os.path.join(self.dw_mods_dir, 'loadorder.txt'),'r') as manifestfile, open (self.profile_location, 'r') as profilefile:
            manifest = manifestfile.read()
            profile = profilefile.read()
         
        for entry in os.scandir(destination_path): #Чистка старых модов
            if entry.is_file():
                os.remove(entry.path)
        
        for entry in os.scandir(source_path): #Копирование в акутал
            if entry.is_file():
                shutil.copy2(entry.path, os.path.join(destination_path, entry.name))
        
        cleaned_profile = re.sub(pattern_b, '', profile, count=0, flags=re.IGNORECASE)              #Чистка старого модлиста
        modded_profile = re.sub(pattern_a, manifest, cleaned_profile, count=1, flags=re.IGNORECASE) #Вставка нового модлиста
        export_profile = re.sub(r'\s*\n', '\n', modded_profile)                                     #Готовый к записи профиль   
        
        with open(profile_location, 'w') as profilefile: #Запись нового модлиста
            profilefile.write(export_profile)

    def export_mods(self, profile_name, profile_location, export_location):

        self.profile_name = profile_name
        self.profile_location = profile_location
        self.export_locaion = export_location
         
        manifest_file = os.path.join(self.game_dir, 'loadorder.txt')
        export_mods_path = os.path.join(self.game_dir, 'mod')
        
        self.output_name = ''
        if self.game == 0: self.output_name ='etsmods.zip' #Название архива зависит от типа игры 
        else: self.output_name = 'atsmods.zip'             #(дегенеративное решение)
        #Паттерны для поиска модов
        pattern = r'active_mods(?:\[\d+\]?: "[^"]+"|:\s*\d+)'                #active_mods[x]: 'sample_text' or ': x'
        pattern_a = r'active_mods(?:\[\d+\]?: "mod_workshop_package.[^"]+")' #active_mods[x]: '"mod_workshop_package.xxx|sample_text'
        pattern_b = r'active_mods(?:\[\d+\]?: "[^"]+")'                      #active_mods[x]: 'sample_text'
        pattern_c = r': "(.*?)\|'                                            #'"sample_text/'

        with open (self.profile_location, 'r') as profilefile:
            profile = profilefile.read()
        
        loadorder = re.findall(pattern, profile)                                                            #Найходим моды в файле
        loadorder_formated = '\n'.join([' ' + line if i > 0 else line for i, line in enumerate(loadorder)]) #Форматирование для нормальной записи

        loadorder_mods = '\n'.join(re.findall(pattern_b, re.sub(pattern_a, '', ('\n'.join(re.findall(pattern_b, profile)))))) #Поиск не воркшоповских модов
        export_mods = re.findall(pattern_c, loadorder_mods)

        mods_files =  {os.path.splitext(file)[0] for file in os.listdir(export_mods_path)} #Список модов без разшерения файла в папке с модами

        with open(manifest_file, 'w') as manifestfile:
            manifestfile.write(loadorder_formated)
        
        with zipfile.ZipFile(os.path.join(self.export_locaion, self.output_name), 'w') as archive:
            archive.write(manifest_file, arcname='loadorder.txt')    #Запись в архив манифеста
            all_mods = os.listdir(export_mods_path)
            matched_mods = set(mods_files).intersection(export_mods) #Поиск не вокшоповских модов для экспорта
            for filename in all_mods:
                file, extension = os.path.splitext(filename)         #Разделение на имя файла и его разширение
                if file in matched_mods:
                    mod_path = os.path.join(export_mods_path, file + extension)
                    archive.write(mod_path, os.path.join('mod', os.path.basename(mod_path)))

    def settings_url_edit(self, new_ets_id, new_ats_id):
        
        self.new_ets_id = new_ets_id
        self.new_ats_id = new_ats_id

        try:
            with open('settings.json', 'r') as file:
                self.json_data = file.read()

            settings_data = json.loads(self.json_data)
            
            for link in settings_data["links"]: #Получение новых id для каждоый игры
                if link['name'] == 'ETS2': 
                    link['url'] = self.new_ets_id
                if link['name'] == 'ATS':
                    link['url'] = self.new_ats_id
            
            with open('settings.json', 'w') as file: #Запись новых id
                json.dump(settings_data, file)

        except Exception as e:
            print('JSON Write Error:', e)
            
    def emergency_cleaning(self):
        folders = ['ATS', 'ETS2']
        
        try: #Пытаемся читстить файлы, если нет то скипаем без ошибок             
            for folder in folders:
                folder_path = os.path.join(self.data_folder, folder)
                files = os.listdir(folder_path)

                for entry in files:
                    entry_path = os.path.join(folder_path, entry)

                    if os.path.isfile(entry_path):
                        os.remove(entry_path)
                    elif os.path.isdir(entry_path):
                        shutil.rmtree(entry_path)     
        except: pass            
        try:
            for file_name in os.listdir(self.data_folder):
                if file_name.startswith("mods"):
                    file_path = os.path.join(self.data_folder, file_name)
            os.remove(file_path)
        except: pass    
        try:
            os.remove(self.downloaded_file)
        except: pass
            

if __name__ == "__main__":
  ModInstallerCore()
