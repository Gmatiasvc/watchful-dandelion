import qrcode
import time
import hashlib

def generate(str1 :str, str2: str , str3:str ) -> str:
    try:
        toHash = str1+str2+str3
        hashed = hashlib.sha256(toHash.encode()).hexdigest() 
        qrcode.make(hashed).save(f"./out/{time.time_ns()}.jpg") # pyright: ignore[reportArgumentType]
        qrcode.make(hashed).save("latest.jpg") # pyright: ignore[reportArgumentType]
        return hashed
    except Exception:
        return "NULL"

if __name__ == "__main__":
    print(generate("Gerardo","Venegas","60529950"))