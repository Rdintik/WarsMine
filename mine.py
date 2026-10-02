import os
print("=== ВСЕ ПЕРЕМЕННЫЕ ОКРУЖЕНИЯ НА СЕРВЕРЕ ===")
for key, value in os.environ.items():
    # Скроем сам токен от чужих глаз в логах, но покажем, что он есть
    if 'TOKEN' in key:
        print(f"{key}: {'*' * 20}")
    else:
        print(f"{key}: {value}")
print("==========================================")
