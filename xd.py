import sqlite3
import os

def fix_schema():
    db_path = 'data.sqlite'
    
    if not os.path.exists(db_path):
        print(f"❌ No se encontró el archivo {db_path}")
        return

    print(f"Conectando a {db_path}...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 1. Verificar columnas existentes
    try:
        cursor.execute("PRAGMA table_info(data)")
    except sqlite3.OperationalError:
        print("❌ La tabla 'data' no existe. Puedes ejecutar 'python manage.py migrate' normalmente.")
        return

    columns_info = cursor.fetchall()
    existing_columns = [col[1] for col in columns_info]
    
    print(f"Columnas actuales encontradas: {existing_columns}")
    
    # Definición de columnas nuevas según tu models.py
    # Usamos NULL para compatibilidad con datos existentes
    new_columns = {
        "nombre": "VARCHAR(100) NULL",
        "apellido": "VARCHAR(100) NULL",
        "documento": "VARCHAR(20) NULL"
    }
    
    # 2. Agregar columnas faltantes
    changes_made = False
    for col_name, col_type in new_columns.items():
        if col_name not in existing_columns:
            print(f"🛠️  Agregando columna faltante: {col_name}...")
            try:
                cursor.execute(f"ALTER TABLE data ADD COLUMN {col_name} {col_type}")
                changes_made = True
            except Exception as e:
                print(f"⚠️  Error agregando {col_name}: {e}")
        else:
            print(f"✅ La columna '{col_name}' ya existe.")
            
    if changes_made:
        conn.commit()
        print("\n✨ Estructura de la base de datos actualizada correctamente.")
    else:
        print("\n👌 No se requirieron cambios en la estructura.")

    conn.close()
    
    print("\n---------------------------------------------------------")
    print("PASO FINAL: Ejecuta el siguiente comando en tu terminal:")
    print("python manage.py migrate --fake-initial")
    print("---------------------------------------------------------")

if __name__ == "__main__":
    fix_schema()