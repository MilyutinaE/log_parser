работы с логами и форматом JSON установить:
pip install python-json-logger

Скрипт принимает один обязательный аргумент - путь к файлу или директории с логами. 
Опционально можно указать путь к файлу, в который будет сохранена статистика (по умолчанию stats.json).
При запуске скрипт анализирует лог файл(ы) и выводит статистику в терминале. Также статистика сохраняется в 
JSON файле, указанном в параметрах командной строки.

Для запуска скрипта достаточно выполнить следующую команду:

python log_analyzer.py <log_path> [-o output_file]

Где <log_path> - путь к файлу или директории с логами, output_file - путь к файлу, в который будет 
сохранена статистика (опционально).