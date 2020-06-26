import sqlite3

class storeData:

    #write an algorithm that checks the inputs for validity and add them to the list
    data = []
    def __init__(self, name, amount, DOL, DOR):
        self.name = name
        self.amount = amount
        self.DOL = DOL
        self.DOR = DOR

    def getUserData(self):
        conn = sqlite3.connect("iplannerdb.db")
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS users(
        name text,
        amount int,
        DOL datetime,
        DOR datetime
        )
        """)

        cur.execute("INSERT INTO users VALUES(:name,:amount,:DOL,:DOR)",
        {
        "name":self.name,
        "amount":self.amount,
        "DOL":self.DOL,
        "DOR":self.DOR
        })

        conn.commit()
        conn.close()

class deleteUser:
    def __init__(self, id):
        self.id = id

    def deleteSelected(self):
        connection = sqlite3.connect("iplannerdb.db")
        connCur = connection.cursor()
        connCur.execute("DELETE FROM users WHERE oid = "+ str(self.id))
        connection.commit()
        connection.close()

            #from UI
        selected_item = treeView.selection()[0]
        treeView.delete(selected_item)
