import os
import subprocess
import shutil

def build_installer():
    # 1. Создаем exe файл
    print("Создаем exe файл...")
    subprocess.run(["pyinstaller", "--onefile", "--noconsole", "main.py"], check=True)
    
    # 2. Создаем директорию для установщика
    if not os.path.exists("installer"):
        os.makedirs("installer")
    
    # 3. Запускаем Inno Setup Compiler
    print("Создаем установщик...")
    inno_compiler = r"D:\Programs\Inno Setup 6\ISCC.exe"
    if os.path.exists(inno_compiler):
        subprocess.run([inno_compiler, "setup.iss"], check=True)
        print("Установщик успешно создан в папке 'installer'")
    else:
        print("Ошибка: Inno Setup не найден. Пожалуйста, установите Inno Setup 6")
        return False
    
    return True

if __name__ == "__main__":
    build_installer() 