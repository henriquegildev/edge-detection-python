import sqlite3

con = sqlite3.connect("photos.db")
cur = con.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS imperfect_photos
                    (ID_PHOTO INT PRIMARY KEY NOT NULL,
                    PHOTO_NAME VARCHAR NOT NULL,
                    FOLDER_ID SMALLINT NOT NULL))''')

cur.execute('''CREATE TABLE IF NOT EXISTS original_photos
                    (ID_PHOTO INT PRIMARY KEY NOT NULL,
                    PHOTO_NAME VARCHAR NOT NULL,
                    FOLDER_ID SMALLINT NOT NULL))''')

cur.execute('''CREATE TABLE IF NOT EXISTS perfect_photos
                    (ID_PHOTO INT PRIMARY KEY NOT NULL,
                    PHOTO_NAME VARCHAR NOT NULL,
                    FOLDER_ID SMALLINT NOT NULL))''')

con.commit()


#for row in cur.execute('''SELECT * FROM galery'''):


#def add_selected_photos(selected_photos):
#    for photos in selected_photos:
 #       cur.execute('''INSERT OR IGNORE INTO photos VALUES
  #                          ("", "", "")''')




   # print(row)
