import sqlite3 as sql

class Preset:
    def __init__(self, target, replace, operator):
        self.target = target
        self.replace = replace
        self.operator = operator

        self.id: int = 0

        self.select_button = None
        self.remove_button = None

    def __str__(self):
        return f'{self.target} | {self.replace} | {self.operator}'

sql_connection = sql.connect('presets.db')
cursor = sql_connection.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS presets 
               (target, replace, operator)""")
sql_connection.commit()

def add_preset_to_database(preset: Preset) -> None:
    cursor.execute("""INSERT INTO presets VALUES (?, ?, ?)""",
                   (
                    f'{preset.target}'.replace(" ", '')[1:-1],
                    f'{preset.replace}'.replace(" ", '')[1:-1],
                    f'{preset.operator}'))
    sql_connection.commit()

def show_table() -> None:
    datas = cursor.execute("""SELECT * FROM presets""")
    sql_connection.commit()
    for data in datas:
        print(data)

def load_presets() -> list:
    presets = []
    datas = cursor.execute("""SELECT *, rowid FROM presets""")
    sql_connection.commit()
    for data in datas:
        presets.append(Preset(
            tuple(map(int, data[0].split(','))),
            tuple(map(int, data[1].split(','))),
            data[2])
        )
        print("rowid?", data[3])
    return presets

def get_row_id_from_record(preset: Preset):
    datas = cursor.execute(f"""SELECT rowid FROM presets WHERE 
                               target='{str(preset.target).replace(" ", '')[1:-1]}' AND replace='{str(preset.replace).replace(" ", '')[1:-1]}' AND operator='{preset.operator}'""")
    rowid = 0
    for data in datas:
        print(type(data))
        rowid = data
    return rowid

# user_packs = cursor.execute(f"""SELECT rowid, * FROM userdatas WHERE username='{username}'""")
#     sql_connection.commit()
#
# def get_records(username):
#     user_packs = cursor.execute(f"""SELECT rowid, * FROM userdatas WHERE username='{username}'""")
#     sql_connection.commit()
#     return user_packs
#
# def add_record(pack_info, pack_label, save_button, pack_entry, description_entry, x_button):
#     pack_label.pack(side=tk.RIGHT, padx=90)
#     save_button.configure(state='disabled')
#     pack_entry.configure(state='disabled')
#     description_entry.configure(state='disabled')
#     x_button.configure(state='disabled')
#     final_info = (pack_info[0], pack_info[1], pack_info[2], pack_info[3])
#     cursor.execute(f"""INSERT INTO userdatas VALUES (?, ?, ?, ?)""", final_info)
#     sql_connection.commit()
#
# def update_record(row_id, pack_name, description, cards_list):
#     cards = card_compressor(card_class_to_list(cards_list))
#     cursor.execute(f"""UPDATE userdatas SET pack_name="{pack_name}",
#                                             description="{description}",
#                                             cards="{cards}"
#                         WHERE rowid={row_id}""")
#     sql_connection.commit()
#
# def remove_record(pack_id: int):
#     cursor.execute(f"""DELETE from userdatas WHERE rowid={pack_id}""")
#     sql_connection.commit()