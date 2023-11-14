import pymysql

user = "tommy"
password = "Borehole@1"
database = "snipeitdb"
host = "localhost"

csv_file = "spreadsheet.csv"
table_name = "assets"

connection = pymysql.connect(host=host,
                             user=user,
                             password=password,
                             database=database,
                             cursorclass=pymysql.cursors.DictCursor)

try:
    with connection.cursor() as cursor:
        check_query = f"SELECT COUNT(*) FROM {table_name}"
        cursor.execute(check_query)
        result = cursor.fetchone()
        empty_table = result["COUNT(*)"] == 0
        
        if empty_table: # normal import for empty database
            query = f"""
            LOAD DATA INFILE '{csv_file}'
            INTO TABLE {table_name}
            FIELDS TERMINATED BY ','
            ENCLOSED BY '"'
            LINES TERMINATED BY '\n'
            IGNORE 1 ROWS
            (id, asset_tag, category, name, _snipeit_ip_address_2, _snipeit_mac_address_3, status_id, manufacturer, model_name, model_id)
            """
            cursor.execute(query)
        else: # update existing entries
            with open(csv_file, 'r') as file:
                next(file)
                
                for line in file:
                    values = line.strip().split(',')
                    
                    query = f"""
                    INSERT INTO {table_name} (id, asset_tag, category, name, _snipeit_ip_address_2, _snipeit_mac_address_3, status_id, manufacturer, model_name, model_id)
                    VALUES ({','.join('%s' for _ in values)})
                    ON DUPLICATE KEY UPDATE
                        category = VALUES(category),
                        name = VALUES(name),
                        _snipeit_ip_address_2 = VALUES(_snipeit_ip_address_2),
                        status_id = VALUES(status_id),
                        manufacturer = VALUES(manufacturer),
                        model_name = VALUES(model_name),
                        model_id = VALUES(model_id)
                """
                    cursor.execute(query, values)
    connection.commit()
finally:
    connection.close()