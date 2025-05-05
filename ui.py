from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QLineEdit, QTextEdit, QInputDialog, QHBoxLayout, QVBoxLayout
import json
import os

# Проверка существования файла и загрузка данных
if os.path.exists("notes_data.json"):
    with open("notes_data.json", "r", encoding="utf-8") as file:
        notes = json.load(file)
else:
    notes = {
        "Ласкаво просимо!": {
            "текст": "Це найкращий додаток для заміток у світі!",
            "теги": ["добро", "інструкція"]
        }
    }
    with open("notes_data.json", "w", encoding="utf-8") as file:
        json.dump(notes, file, ensure_ascii=False, indent=4)

app = QApplication([])

notes_win = QWidget()
notes_win.setWindowTitle('Розумні замітки')
notes_win.resize(900, 600)

list_notes = QListWidget()
list_notes_label = QLabel('Список заміток')

button_note_create = QPushButton('Створити замітку')
button_note_del = QPushButton('Видалити замітку')
button_note_save = QPushButton('Зберегти замітку')

field_tag = QLineEdit('')
field_tag.setPlaceholderText('Введіть тег...')
field_text = QTextEdit()
button_tag_add = QPushButton('Додати до замітки')
button_tag_del = QPushButton('Відкріпити від замітки')
button_tag_search = QPushButton('Шукати замітки по тегу')
list_tags = QListWidget()
list_tags_label = QLabel('Список тегів')

layout_notes = QHBoxLayout()
col_1 = QVBoxLayout()
col_1.addWidget(field_text)

col_2 = QVBoxLayout()
col_2.addWidget(list_notes_label)
col_2.addWidget(list_notes)

row_1 = QHBoxLayout()
row_1.addWidget(button_note_create)
row_1.addWidget(button_note_del)
col_2.addLayout(row_1)

row_2 = QHBoxLayout()
row_2.addWidget(button_note_save)
col_2.addLayout(row_2)

col_2.addWidget(list_tags_label)
col_2.addWidget(list_tags)
col_2.addWidget(field_tag)

row_3 = QHBoxLayout()
row_3.addWidget(button_tag_add)
row_3.addWidget(button_tag_del)
col_2.addLayout(row_3)

row_4 = QHBoxLayout()
row_4.addWidget(button_tag_search)
col_2.addLayout(row_4)

layout_notes.addLayout(col_1, stretch=2)
layout_notes.addLayout(col_2, stretch=1)
notes_win.setLayout(layout_notes)

# Показать замітку
def show_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        field_text.setText(notes[key]["текст"])
        list_tags.clear()
        list_tags.addItems(notes[key]["теги"])

# Створення замітки
def add_note():
    note_name, ok = QInputDialog.getText(notes_win, "Додати замітку", "Назва замітки:")
    if ok and note_name:
        notes[note_name] = {"текст": "", "теги": []}
        list_notes.addItem(note_name)
        with open("notes_data.json", "w", encoding="utf-8") as file:
            json.dump(notes, file, ensure_ascii=False, indent=4)

# Видалення замітки
def del_note():
    if list_notes.selectedItems():
        note_name = list_notes.selectedItems()[0].text()
        notes.pop(note_name, None)
        with open("notes_data.json", "w", encoding="utf-8") as file:
            json.dump(notes, file, ensure_ascii=False, indent=4)
        list_notes.clear()
        list_notes.addItems(notes.keys())
        list_tags.clear()
        field_text.clear()

# Додавання тегу
def add_tag():
    if list_notes.selectedItems():
        note_name = list_notes.selectedItems()[0].text()
        tag = field_tag.text()
        if tag and tag not in notes[note_name]["теги"]:
            notes[note_name]["теги"].append(tag)
            list_tags.addItem(tag)
            field_tag.clear()
            with open("notes_data.json", "w", encoding="utf-8") as file:
                json.dump(notes, file, ensure_ascii=False, indent=4)

# Видалення тегу
def del_tag():
    if list_notes.selectedItems() and list_tags.selectedItems():
        note_name = list_notes.selectedItems()[0].text()
        tag = list_tags.selectedItems()[0].text()
        if tag in notes[note_name]["теги"]:
            notes[note_name]["теги"].remove(tag)
            list_tags.clear()
            list_tags.addItems(notes[note_name]["теги"])
            with open("notes_data.json", "w", encoding="utf-8") as file:
                json.dump(notes, file, ensure_ascii=False, indent=4)

# Зберегти замітку
def save_note():
    if list_notes.selectedItems():
        note_name = list_notes.selectedItems()[0].text()
        notes[note_name]["текст"] = field_text.toPlainText()
        with open("notes_data.json", "w", encoding="utf-8") as file:
            json.dump(notes, file, ensure_ascii=False, indent=4)

# Пошук за тегом
def search_tag():
    tag = field_tag.text()
    if tag:
        filtered_notes = {}
        for note_name, note_data in notes.items():
            if tag in note_data["теги"]:
                filtered_notes[note_name] = note_data
        list_notes.clear()
        list_tags.clear()
        field_text.clear()
        list_notes.addItems(filtered_notes.keys())

# Подключение сигналов
list_notes.itemClicked.connect(show_note)
button_note_create.clicked.connect(add_note)
button_note_del.clicked.connect(del_note)
button_note_save.clicked.connect(save_note)
button_tag_add.clicked.connect(add_tag)
button_tag_del.clicked.connect(del_tag)
button_tag_search.clicked.connect(search_tag)

# Показать стартовые заметки
list_notes.addItems(notes.keys())

notes_win.show()
app.exec_()
