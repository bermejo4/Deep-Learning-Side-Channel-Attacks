import sqlite3
import json
import os
from dotenv import load_dotenv

## ----------------- OBTENCIÓN DE DATOS DE LA BASE DE DATOS -------------------------------
def get_ids_best_models(database, analysis_id_range, table):
    min_id, max_id = analysis_id_range
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    
    query = f"""
    SELECT id 
    FROM {table} 
    WHERE label = 'Validation Set Best Model'
    AND analysis_id BETWEEN ? AND ?
    """
    
    cursor.execute(query, (min_id, max_id))
    results = cursor.fetchall()

    print("Results:"+str(results))
    
    # Extract IDs from the query results
    ids = [row[0] for row in results]
    
    conn.close()
    
    return ids

def get_hyperparameter_id(database, id, table):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    
    query = f"""
    SELECT hyperparameters_id 
    FROM hyperparameter_{table} 
    WHERE {table}_id = ?
    """
    
    cursor.execute(query, (id, ))
    result = cursor.fetchone()
    
    conn.close()
    
    if result:
        return result[0]
    else:
        return None

def get_analysis_id(database, id, table):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    
    query = f"""
    SELECT analysis_id 
    FROM hyperparameter_{table} 
    WHERE {table}_id = ?
    """
    
    cursor.execute(query, (id, ))
    result = cursor.fetchone()
    
    conn.close()
    
    if result:
        return result[0]
    else:
        return None
    
def get_hyperparameters(database, hyperparameter_id):
    
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    
    query = """
    SELECT hyperparameters 
    FROM hyperparameter 
    WHERE id = ?
    """
    
    cursor.execute(query, (hyperparameter_id,))
    result = cursor.fetchone()
    
    conn.close()
    
    if result:
        return result[0]
    else:
        return None
    
    
def get_data_from_analysis(database, id):
    
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    
    query = """
    SELECT settings
    FROM analysis
    WHERE id = ?
    """

    cursor.execute(query, (id,))
    result = cursor.fetchall()
    
    # Extract IDs from the query results
    data =[row[0] for row in result]
    
    conn.close()
    
    return data

    

## ----------------- CREACIÓN DE LA NUEVA TABLA -------------------------------
def create_table(database):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    # Borrar la tabla si existe
    cursor.execute('''
    DROP TABLE IF EXISTS best_models_hyp
    ''')
    
    # Crear la tabla con todas las columnas necesarias
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS best_models_hyp (
        conv_layers INTEGER,
        kernel_1 INTEGER,
        stride_1 INTEGER,
        filters_1 INTEGER,
        pooling_size_1 INTEGER,
        pooling_stride_1 INTEGER,
        pooling_type_1 TEXT,
        neurons INTEGER,
        layers INTEGER,
        activation TEXT,
        learning_rate REAL,
        optimizer TEXT,
        seed INTEGER,
        epochs INTEGER,
        batch_size INTEGER,
        val_ge REAL,
        val_sr REAL,
        leakage_model TEXT,
        byte INTEGER,
        key TEXT,
        model TEXT,
        analysis_id TEXT,
        file_name TEXT,
        more_info TEXT
    )
    """)

    # Confirmar la creación de la tabla
    conn.commit()
    conn.close()


## ----------------- INSERCIÓN DE DATOS EN LA NUEVA TABLA -------------------------------
def insert_into_table(database, json_data):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    
    # Preparar los datos para la inserción
    columns = ', '.join(json_data.keys())
    placeholders = ', '.join('?' * len(json_data))
    values = tuple(json_data.values())
    
    # Crear la consulta de inserción
    query = f"INSERT INTO best_models_hyp ({columns}) VALUES ({placeholders})"
    
    # Ejecutar la consulta
    cursor.execute(query, values)
    
    conn.commit()
    conn.close()


# Use example:

#Type of search: 
# search = 'random_search'
search = 'grid_search'

load_dotenv('../.env')
data_type = os.getenv("data_type")
database_name = f"database_{data_type}_hyper_selec_{search}_cnn.sqlite"
database_path = os.getenv("HYPERPARAMETERS_SELECTION_DATABASE_FOLDER_PATH")
database_file = database_path + '/' +database_name

analysis_id_range = (0, 16)  # ANALYSIS IDS RANGE
filter_by = 'guessing_entropy'
# filter_by = 'success_rate'


create_table(database_file)

print("WORKING WITH: "+ str(database_name)+ ", Filtered by: " + str(filter_by))
ids = get_ids_best_models(database_file, analysis_id_range, filter_by)
print("IDs encontrados:", ids)

dictionary = {}
for id in ids:
    hyp_id = get_hyperparameter_id(database_file, int(id), filter_by)
    analysis_id = get_analysis_id(database_file, int(id), filter_by)
    dictionary[int(id)] = (hyp_id, analysis_id)
    hyperparameters = get_hyperparameters(database_file, hyp_id)
    data_settings = get_data_from_analysis(database_file, analysis_id)[0]
    print(f"Hyperparameters from {analysis_id} : {hyperparameters}")
    data = json.loads(str(data_settings))
    print(f"Data from {analysis_id} : {data}")
    hyperparameters = json.loads(hyperparameters)
    json_data_renamed = {
    "conv_layers": hyperparameters["conv_layers"],
    "kernel_1": hyperparameters["kernel_1"],
    "stride_1": hyperparameters["stride_1"],
    "filters_1": hyperparameters["filters_1"],
    "pooling_size_1": hyperparameters["pooling_size_1"],
    "pooling_stride_1": hyperparameters["pooling_stride_1"],
    "pooling_type_1": hyperparameters["pooling_type_1"],
    "neurons": hyperparameters["neurons"],
    "layers": hyperparameters["layers"],
    "activation": hyperparameters["activation"],
    "learning_rate": hyperparameters["learning_rate"],
    "optimizer": hyperparameters["optimizer"],
    "seed": hyperparameters["seed"],
    "epochs": hyperparameters["epochs"],
    "batch_size": hyperparameters["batch_size"],
    "val_ge": hyperparameters["Val GE"],
    "val_sr": hyperparameters["Val SR"],
    "leakage_model": data['leakage_model']['leakage_model'],
    "byte": data['leakage_model']['byte'],
    "key":data['key'],
    "batch_size": data['batch_size'],
    "epochs": data['epochs'],
    "model": data[search]['neural_network'],
    "analysis_id": data['analysis_id'],
    "file_name": data['filename'],
    "more_info": str(data_settings),
}
    insert_into_table(database_file, json_data_renamed)

print(f"Dictionary: {dictionary}")

