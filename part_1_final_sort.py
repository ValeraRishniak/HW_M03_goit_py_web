import sys
import shutil
from pathlib import Path
import re
import os
import time
from threading import Thread
from datetime import datetime



FILES_EXTENTIONS = {
    "Audio": [".mp3", ".aac", ".ac3", ".wav", ".amr", ".ogg"],
    "Video": [".mp4", ".mov", ".avi", ".mkv"],
    "Images": [".jpg", ".jpeg", ".png", ".svg", ".gif", ".bmp"],
    "Documents": [".doc", ".docx", ".txt", ".pdf", ".xls", ".xlsx", ".pptx", ".rtf"],
    "Books": [".fb2", ".epub", ".mobi"],
    "Archives": [".zip", ".rar", ".tar", ".gz"]
}

# Create rule of chanding cyrillic letters to latin letters
CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ?<>,!@#[]#$%^&*()-=; "
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g", "_", "_", "_", "_",
               "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_")
TRANS = {}

class Translate():
    for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()


    def normalize(name: str) -> str:
        t_name = name.translate(TRANS)
        t_name = re.sub(r'\W', '_', t_name)
        return t_name


#Функція що повертає повний шлях до теки, яку необхідно опрацювати(сортувати)
def get_main_path() -> str:
    main_path = ""
    args = sys.argv
    if len(args) == 1:
        main_path = input("Enter path to your folder: ")
    else:
        main_path = args[1]
    while True:
        if not os.path.exists(main_path):
            if main_path:
                print(f"{main_path} not exist")
            main_path = input("Enter path to your folder: ")
        else:
            if os.path.isdir(main_path):
                break
            else:
                print(f"{main_path} this is not a folder")
                main_path = ""
    return main_path

#функція що рекурсивно повертає список усіх повних шляхів файлів у папці, що сортується.
def files_list(path: str) -> list:
    list_of_files = list()    
    for root, dirs, files in os.walk(path, topdown=False):  
        for filename in files:
            file_path_ = os.path.join(root, filename)
            list_of_files.append(file_path_)
    return list_of_files


#функція що змінює назву файла і додає timestamp
def normalize_name(file_name: str) -> str:
    ts = datetime.now().timestamp()
    new_file_name = Translate.normalize(file_name)+'_'+str(ts) #+ full_file_name.suffix #сворюємо нове нормалізоване ім'я
    return new_file_name


#функція що видаляє пусті теки
def delete_emtpy_dir():
    for root, dirs, files in os.walk(main_path, topdown=False):
        for name in dirs:
            if len(os.listdir(os.path.join(root, name))) == 0:
                    os.rmdir(os.path.join(root, name))


# функція що перейменовує файли в системі
def rename_file(path: str) -> None:
    for file in files_list(path):
        full_file_name = Path(file)
        suffix = full_file_name.suffix.lower()
        new_name = normalize_name(full_file_name.stem) + suffix
        path_for_renamed_file = path +'/'+ new_name
        os.rename(full_file_name, path_for_renamed_file)



#Сортування файлів -> створення теки та переміщення в неї файла
def sort(path: str) -> None:
    #1 перебрати файли у каталозі
    for file in files_list(path):
        full_file_name = Path(file)
        print(full_file_name)
        suffix = full_file_name.suffix.lower()
        #2 порівняти суфікс із словником
        for file_type, extension in FILES_EXTENTIONS.items():
            if suffix in extension:
                #3 створити теку по суфіксу
                destination_folder = Path(path) / file_type
                destination_folder.mkdir(exist_ok=True)   
                #4 якщо архів, розпаковуємо                
                if file_type == 'Archives':
                    try:
                        shutil.unpack_archive(
                            full_file_name, destination_folder.joinpath(full_file_name.stem))
                    except shutil.ReadError:
                        pass
                #5 перемістити у створену теку по суфіксу
                shutil.move(full_file_name, destination_folder) #/ full_file_name)
                break
        # Умова що оминає помилку "файл не знайдено", бо його вже переміщено, а дає можливість перемістити в іншу теку файл із невідомим розширенням 
        try:
            destination_folder_2 = Path(path) / 'Other'
            destination_folder_2.mkdir(exist_ok=True)
            shutil.move(full_file_name, destination_folder_2)
        except FileNotFoundError:
            continue




if __name__ == "__main__":
    start_time = datetime.now()
    main_path = get_main_path()
        
    t_1 = Thread(target=get_main_path)
    t_2 = Thread(target=get_main_path)
    t_3 = Thread(target=get_main_path)
        
    t_1.start()
    t_2.start()
    t_3.start()
    
    t_1.join()
    t_2.join()
    t_3.join() 
    rename_file(main_path) 
    sort(main_path)

    delete_emtpy_dir()
    end_time = datetime.now() - start_time
    print(f'Scripst done by {end_time} seconds') 
    
    