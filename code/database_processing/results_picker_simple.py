import sqlite3
import json
import os
from dotenv import load_dotenv


## ----------------- DATA EXTRACTION FROM DATABASE -------------------------------
def get_success_rate_ids(database, analysis_id_range, initial_table):
    min_id, max_id = analysis_id_range
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    
    query = f"""
    SELECT "values"
    FROM {initial_table} 
    WHERE analysis_id BETWEEN ? AND ?
    """
    
    cursor.execute(query, (min_id, max_id))
    results = cursor.fetchall()
    
    # Extract IDs from the query results
    ids = [row[0] for row in results]
    
    conn.close()
    
    return ids

# --------------------------------------------
def get_success_rate_from_id(database, id):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    
    query = """
    SELECT "values"
    FROM success_rate 
    WHERE analysis_id = ?
    """
    
    cursor.execute(query, (id, ))
    results = cursor.fetchall()
    
    # Extract data from the query results
    data_sr = [row[0] for row in results]
    info = json.loads(data_sr[0])
    info = json.loads(info)
    sr_value = info['99']
    
    conn.close()
    
    return sr_value

def get_guessing_entropy_from_id(database, id):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    
    query = """
    SELECT "values"
    FROM guessing_entropy 
    WHERE analysis_id = ?
    """
    
    cursor.execute(query, (id, ))
    results = cursor.fetchall()
    
    # Extract data from the query results
    data = [row[0] for row in results]
    info = json.loads(data[0])
    info = json.loads(info)
    ge_value = info['99']
    
    conn.close()
    
    return ge_value

# --------------------------------------------

def get_analysis_id_from_id(database, id, initial_table):
    
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    
    query = f"""
    SELECT analysis_id
    FROM {initial_table}
    WHERE id = ?
    """
    
    cursor.execute(query, (id, ))
    result = cursor.fetchall()
    
    # Extract IDs from the query results
    id =[row[0] for row in result]
    
    conn.close()
    
    return id


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


# ## ----------------- NEW TABLE CREATION -------------------------------
def create_table(database):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    # Delete the table if exists
    cursor.execute('''
    DROP TABLE IF EXISTS good_results_from_simple
    ''')
    
    # creating a table with all the columns
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS good_results_from_simple (
        byte INTEGER,
        key TEXT,
        leakage_model TEXT,
        batch_size INTEGER,
        epochs INTEGER,
        model TEXT,
        analysis_id INTEGER,
        file_name TEXT,
        guess_entropy FLOAT,
        success_rate FLOAT
    )
''')
    
    conn.commit()
    conn.close()

### ----------------- DATA INSERTION IN THE NEW TABLE -------------------------------
def insert_into_table(database, byte, key, leakage_model, batch_size, epochs, model, analysis_id, file_name, guess_entropy, success_rate):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO good_results_from_simple (byte, key, leakage_model, batch_size, epochs, model, analysis_id, file_name, guess_entropy, success_rate)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (byte, key, leakage_model, batch_size, epochs, model, analysis_id, file_name, guess_entropy, success_rate))
    
    conn.commit()
    conn.close()

# ------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------


### ----------------- MAIN -------------------------------

## IMPORTANT VARIABLES:
# Database name
database_name = 'database_ascad.sqlite'
load_dotenv('../.env')
database_path = os.getenv("SIMPLE_DATABASE_PATH")
database_file = database_path + '/' +database_name
# Ids Range
# analysis_id_range = (0, 4508)
analysis_id_range = (1, 45)

# Filter by Guessing Entropy or by Sucess Rate:
# filter_by = 'success_rate'
filter_by = 'guessing_entropy'

create_table(database_file)

for analysis_id in range(analysis_id_range[0], analysis_id_range[1]):

    print("ANALYSIS ID: "+ str(analysis_id))

    ge_value = get_guessing_entropy_from_id(database_file, analysis_id)
    sr_value = get_success_rate_from_id(database_file, analysis_id)

    if float(ge_value) <= 3 and filter_by == 'guessing_entropy':
        print("GE_VALUE: "+str(ge_value))
        print("SR_VALUE: "+str(sr_value))
        settings = str(get_data_from_analysis(database_file, int(analysis_id))[0])
        datos = json.loads(settings)
        byte = datos['leakage_model']['byte']
        key = datos['key']
        leakage_model = datos['leakage_model']['leakage_model']
        batch_size = datos['batch_size']
        epochs = datos['epochs']
        model = datos['models']['0']['model_name']
        analysis_id = datos['analysis_id']
        file_name = datos['filename']
        insert_into_table(database_file, byte, key, leakage_model, batch_size, epochs, model, analysis_id, file_name, ge_value, sr_value)

    if float(sr_value) >= 0.33 and filter_by == 'success_rate':
        print("GE_VALUE: "+str(ge_value))
        print("SR_VALUE: "+str(sr_value))
        settings = str(get_data_from_analysis(database_file, int(analysis_id))[0])
        datos = json.loads(settings)
        byte = datos['leakage_model']['byte']
        key = datos['key']
        leakage_model = datos['leakage_model']['leakage_model']
        batch_size = datos['batch_size']
        epochs = datos['epochs']
        model = datos['models']['0']['model_name']
        analysis_id = datos['analysis_id']
        file_name = datos['filename']
        insert_into_table(database_file, byte, key, leakage_model, batch_size, epochs, model, analysis_id, file_name, ge_value, sr_value)

