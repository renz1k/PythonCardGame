from PIL import Image
import os

def create_ico():
    # Открываем PNG изображение
    img = Image.open('images/icon.png')
    
    # Преобразуем в RGB если изображение в RGBA
    if img.mode == 'RGBA':
        img = img.convert('RGB')
    
    # Создаем ICO файл только с одним размером
    img.save('images/icon.ico', format='ICO', sizes=[(256, 256)])
    
    print("ICO файл успешно создан!")

if __name__ == "__main__":
    create_ico() 