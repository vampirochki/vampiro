from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QListWidget,
    QLineEdit, QTextEdit, QInputDialog, QHBoxLayout, QVBoxLayout, QMessageBox
)
import json
import os

#Загрузка и создание файла с замітками
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

#Стиль интерфейса
style = """
QWidget {
    background-color: #f3f0ff;
}

QPushButton {
    background-color: #6c5ce7;
    color: white;
    border-radius: 8px;
    padding: 6px 12px;
    font-size: 14px;
    border: none;
}
QPushButton:hover {
    background-color: #a29bfe;
}
QPushButton:pressed {
    background-color: #4b4bff;
}
QLineEdit, QTextEdit {
    background-color: #f0f0f0;
    border: 1px solid #ccc;
    border-radius: 6px;
    padding: 4px;
    font-size: 14px;
}
QListWidget {
    background-color: #ffffff;
    border: 1px solid #ccc;
    border-radius: 6px;
    font-size: 14px;
}
QLabel {
    font-weight: bold;
    font-size: 14px;
}
"""
app.setStyleSheet(style)

#Интерфейс
notes_win = QWidget()
notes_win.setWindowTitle('Розумні замітки')
notes_win.resize(900, 600)

list_notes = QListWidget()
list_notes_label = QLabel('Список заміток')

button_note_create = QPushButton('Створити замітку')
button_note_del = QPushButton('Видалити замітку')
button_note_save = QPushButton('Зберегти замітку')

field_tag = QLineEdit()
field_tag.setPlaceholderText('Введіть тег...')
field_text = QTextEdit()
button_tag_add = QPushButton('Додати до замітки')
button_tag_del = QPushButton('Відкріпити від замітки')
button_tag_search = QPushButton('Шукати замітки по тегу')
list_tags = QListWidget()
list_tags_label = QLabel('Список тегів')

#Макет
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

#Функции
def show_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        field_text.setText(notes[key]["текст"])
        list_tags.clear()
        list_tags.addItems(notes[key]["теги"])

def add_note():
    note_name, ok = QInputDialog.getText(notes_win, "Додати замітку", "Назва замітки:")
    if ok and note_name:
        notes[note_name] = {"текст": "", "теги": []}
        list_notes.addItem(note_name)
        save_data()

def del_note():
    if list_notes.selectedItems():
        note_name = list_notes.selectedItems()[0].text()
        notes.pop(note_name, None)
        save_data()
        list_notes.clear()
        list_notes.addItems(notes.keys())
        list_tags.clear()
        field_text.clear()

def add_tag():
    if list_notes.selectedItems():
        note_name = list_notes.selectedItems()[0].text()
        tag = field_tag.text()
        if tag and tag not in notes[note_name]["теги"]:
            notes[note_name]["теги"].append(tag)
            list_tags.addItem(tag)
            field_tag.clear()
            save_data()

def del_tag():
    if list_notes.selectedItems() and list_tags.selectedItems():
        note_name = list_notes.selectedItems()[0].text()
        tag = list_tags.selectedItems()[0].text()
        if tag in notes[note_name]["теги"]:
            notes[note_name]["теги"].remove(tag)
            list_tags.clear()
            list_tags.addItems(notes[note_name]["теги"])
            save_data()

def save_note():
    if list_notes.selectedItems():
        note_name = list_notes.selectedItems()[0].text()
        notes[note_name]["текст"] = field_text.toPlainText()
        save_data()
        QMessageBox.information(notes_win, "Збережено", f"Замітку «{note_name}» збережено!")

def search_tag():
    tag = field_tag.text()
    if tag:
        filtered_notes = {k: v for k, v in notes.items() if tag in v["теги"]}
        list_notes.clear()
        list_tags.clear()
        field_text.clear()
        list_notes.addItems(filtered_notes.keys())

def save_data():
    with open("notes_data.json", "w", encoding="utf-8") as file:
        json.dump(notes, file, ensure_ascii=False, indent=4)

#Подключение
list_notes.itemClicked.connect(show_note)
button_note_create.clicked.connect(add_note)
button_note_del.clicked.connect(del_note)
button_note_save.clicked.connect(save_note)
button_tag_add.clicked.connect(add_tag)
button_tag_del.clicked.connect(del_tag)
button_tag_search.clicked.connect(search_tag)

#Заполнение начальных данных
list_notes.addItems(notes.keys())
notes_win.show()
app.exec_()


