import json
import os
import sqlite3
from android.storage import app_storage_path
from kivy import platform


def open_db():

    if platform == 'android':
        dir = app_storage_path()
        con = sqlite3.connect(os.path.join(dir, 'sqldbtesting.db'))
    elif platform == 'win':
        con = sqlite3.connect('sqldbtesting.db')
    c = con.cursor()
    return con, c


def solo_check_saves():
    print('antidata.solo_check_saves')
    con, c = open_db()
    SoloGameSaves = c.execute(
        """SELECT Name FROM sqlite_master WHERE type='table'
        AND Name='SoloGameSaves'; """).fetchall()
    con.commit()
    con.close()
    if SoloGameSaves:
        return True
    else:
        return False


def solo_create_table():
    print('antidata.solo_create_table')
    con, c = open_db()
    c.execute("""CREATE TABLE SoloGameSaves (
        hand_cards text,
        table_cards text,
        deck text,
        sorcerer int,
        codex text,
        counter int,
        counter_max int,
        crystals int,
        crystals_target int,
        stage text,
        reliquary,
        reliquary_cards text
        )""")
    con.commit()
    con.close()


def solo_add_save(hand_cards, table_cards, deck, sorcerer, codex, counter, counter_max, crystals, crystals_target, stage, reliquary, reliquary_cards):
    print('antidata.solo_add_save')
    hand = transform_list_to_string(hand_cards)
    table = transform_list_to_string(table_cards)
    deck = transform_list_to_string(deck)
    reliq_cards = transform_list_to_string(reliquary_cards)

    last_save = solo_get_last_save()

    if not last_save or last_save[9] != stage:
        con, c = open_db()
        c.execute("INSERT INTO SoloGameSaves VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                  (hand, table, deck, sorcerer, codex, counter, counter_max, crystals, crystals_target, stage, reliquary, reliq_cards))
        con.commit()
        con.close()


def solo_get_undo_save():
    print('antidata.solo_get_undo_save')
    # Getting the last
    con, c = open_db()
    # c.execute('SELECT max(rowid) FROM SoloGameSaves')
    # c.execute('SELECT * FROM SoloGameSaves WHERE ID = (SELECT MAX(ID) FROM SoloGameSaves')
    last_two_saves = c.execute('SELECT * FROM SoloGameSaves ORDER BY rowid DESC').fetchmany(2)
    con.commit()
    con.close()

    if len(last_two_saves) < 2:
        return False

    undo_save = last_two_saves[1]

    # Making Tuple as list and Removing the quotation marks on the lists
    load_game = []
    for i in range(len(undo_save)):
        if i < 3 or i == (len(undo_save) - 1):
            load_game.append(undo_save[i][1:-1].split(','))
        else:
            load_game.append(undo_save[i])

    return load_game


def solo_get_last_save():
    print('antidata.solo_get_last_save')

    # Getting the last
    con, c = open_db()
    last_save = c.execute('SELECT * FROM SoloGameSaves ORDER BY rowid DESC').fetchone()
    con.commit()
    con.close()

    if not last_save:
        return False

    # Making Tuple as list and Removing the quotation marks on the lists
    load_game = []
    for i in range(len(last_save)):
        if i < 3 or i == (len(last_save) - 1):
            load_game.append(last_save[i][1:-1].split(','))
        else:
            load_game.append(last_save[i])

    return load_game


def solo_delete_last_save():
    print('antidata.solo_delete_last_save')

    # print(f'id: {id_row}')

    con, c = open_db()
    c.execute("DELETE FROM SoloGameSaves WHERE rowid = (SELECT MAX(rowid) from SoloGameSaves)")
    con.commit()
    con.close()


def solo_delete_all():
    print('antidata.solo_delete_all')
    con, c = open_db()
    c.execute("""DROP TABLE IF EXISTS SoloGameSaves""")
    con.commit()
    con.close()






#####################




# def check_list():
#     con, c = open_db()
#     l = c.execute("SELECT * FROM SoloGameSaves").fetchall()
#     print(f'Saved SoloGames {l}')


# def create_ai_saves(c):
#     c.execute("""CREATE TABLE AIGamesSaves (
#         hand_cards text,
#         table_cards text,
#         deck text,
#         counter text,
#         counter_max text,
#         crystals text,
#         crystals_target text
#         )""")





#####################################

def transform_list_to_string(this_list):
    s = ""
    for i in this_list:
        s = s + str(i) + ","
        # if len(s) == 0:
        #     s = str(i)
        # else:
        #     n = str(i)
        #     s = s + "," + n
    s = "'" + s[:-1] + "'"
    return s



