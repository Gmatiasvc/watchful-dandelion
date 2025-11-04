import sqlite3
import qr_generator
import time

connection = sqlite3.connect("data.sqlite")

cursor = connection.cursor()

def register(name : str , lastName : str, docIC : str) -> bool:
    hashed = qr_generator.generate(name,lastName,docIC)    
    print("hashed: ",hashed, len(hashed))
    
    if hashed == "NULL":
        return False
    cursor.execute("INSERT INTO data (id_hash, time_entry, time_exit) VALUES (?, ?, ?)",
            (hashed, 0, 0))
    connection.commit()
    return True

def entryAction(hashed:str)->tuple:
    
    r = cursor.execute("SELECT * FROM data WHERE id_hash = ?", (hashed,))
    
    r = r.fetchall()
    
    if len(r) == 0:
        return (-1,0)
    
    else:
        if r[0][1] == 0:
            t = int(time.time())
            cursor.execute("UPDATE data SET time_entry = ? WHERE id_hash = ?",
            (t,hashed))
            connection.commit()
            return (1,t)
        
        elif r[0][2] == 0:
            t = int(time.time())
            cursor.execute("UPDATE data SET time_exit = ? WHERE id_hash = ?",
            (t,hashed))
            
            connection.commit()
            return (2,t)
        
        else:
            return (0,0)

if __name__ == "__main__":
    print(register("Valentina","Pajares","99999999"))
    print(register("Jean","Bernilla","99999999"))
    print(register("Andre","Rebaza","99999999"))
    print(register("Camila","Zevallos","99999999"))
    print(register("Angela","Roldan","99999999"))