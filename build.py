import PyInstaller.__main__
import os

# Получаем путь к текущей директории
current_dir = os.path.dirname(os.path.abspath(__file__))

# Список файлов и папок, которые нужно включить в сборку
data_files = [
    ('images', 'images'),
    ('music', 'music'),
    ('theme.json', '.'),
    ('fonts', 'fonts')
]

# Формируем список аргументов для PyInstaller
args = [
    'main.py',  # Основной файл
    '--name=CyberDefense',  # Имя исполняемого файла
    '--onefile',  # Создать один исполняемый файл
    '--windowed',  # Не показывать консоль
    '--add-data=theme.json;.',  # Добавить файл темы
]

# Добавляем папки с ресурсами
for src, dst in data_files:
    args.append(f'--add-data={src};{dst}')

# Запускаем сборку
PyInstaller.__main__.run(args)