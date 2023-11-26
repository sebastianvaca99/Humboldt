#Archivo encargado de la conexión con la base de datos y de la ejecución de las consultas
import psycopg2
import psycopg2.extras

#Funcion que retorna las categorias de la base de datos para seleccionar en el dropdown
def get_categorias():
    conn = psycopg2.connect(
            host="35.239.3.252",
            database="humboldt",
            user="postgres",
            password="mine")

    # Abre un cursor para realizar operaciones en la base de datos
    cur = conn.cursor()

    # Hace la consulta
    cur.execute('SELECT DISTINCT capitulo_del_arancel FROM public.consolidado')

    # Obtiene todas las filas
    rows = cur.fetchall()

    conn.commit()

    cur.close()
    conn.close()

    # Retorna una lista con las categorias
    return [row[0] for row in rows]

#Funcion que verifica que el correo haga parte de la base de datos
def verificar_usuario(email):
    conn = psycopg2.connect(
            host="35.239.3.252",
            database="humboldt",
            user="postgres",
            password="mine")

    # Abre un cursor para realizar operaciones en la base de datos
    cur = conn.cursor()

    # Hace la consulta
    cur.execute('''SELECT id, password FROM public.users WHERE email = %s''', (email,))

    # Obtiene la fila
    row = cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()

    # Retorna una lista con las categorias
    return row if row else None

def get_proyectos():
    conn = psycopg2.connect(
            host="35.239.3.252",
            database="humboldt",
            user="postgres",
            password="mine")

    # Abre un cursor para realizar operaciones en la base de datos
    cur = conn.cursor()

    # Hace la consulta
    cur.execute('''SELECT project_name FROM public.projects''')

    # Obtiene la fila
    rows = cur.fetchall()

    conn.commit()
    cur.close()
    conn.close()

    # Retorna una lista con las categorias
    return [row[0] for row in rows]

#Funcion que verifica sin un usuario tiene permiso sobre un proyecto
def verificar_permiso_proyecto(user_id, project_id):
    conn = psycopg2.connect(
            host="35.239.3.252",
            database="humboldt",
            user="postgres",
            password="mine")

    # Abre un cursor para realizar operaciones en la base de datos
    cur = conn.cursor()

    # Hace la consulta
    cur.execute('''SELECT * 
                    FROM public.user_projects
                    WHERE user_id = %s AND project_id = %s
                ''', (user_id, project_id))

    # Obtiene la fila
    row = cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()

    # Retorna una lista con las categorias
    return row if row else None

def set_proyecto(project_id):
    conn = psycopg2.connect(
            host="35.239.3.252",
            database="humboldt",
            user="postgres",
            password="mine")
     
    cur = conn.cursor()

    # Hace la consulta
    cur.execute('''UPDATE public.project_temp 
                    SET project = %s
                    WHERE id = 1
                ''', (project_id,))

    conn.commit()
    cur.close()
    conn.close()

def get_project():
    conn = psycopg2.connect(
            host="35.239.3.252",
            database="humboldt",
            user="postgres",
            password="mine")

    # Abre un cursor para realizar operaciones en la base de datos
    cur = conn.cursor()

    # Hace la consulta
    cur.execute('''SELECT project FROM public.project_temp WHERE id = 1''')

    # Obtiene la fila
    row = cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()

    # Retorna una lista con las categorias
    return row if row else None
     
#Funcion que corre las diferentes consultas segun el capitulo de arancel seleccionado
def run_query(numero):
    conn = psycopg2.connect(
            host="35.239.3.252",
            database="humboldt",
            user="postgres",
            password="mine")
    
    print(numero)

    # Abre un cursor para realizar operaciones en la base de datos
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if numero == 1:
    # Query total export quantities for each country where capitulo_del_arancel is not null
        cur.execute('''
            SELECT "país_de_destino" as Pais_destino, COUNT(*) AS Numero_de_Exportaciones 
            FROM public.consolidado
            GROUP BY "país_de_destino" 
            ORDER BY Numero_de_Exportaciones  DESC 
            LIMIT 5; 
        ''')

    elif numero == 2:
        # Query total export quantities for each month
        cur.execute('''
            SELECT capitulo_del_arancel as Categorias_productos, COUNT(*) AS Numero_de_Exportaciones 
            FROM public.consolidado 
            GROUP BY capitulo_del_arancel 
            ORDER BY Numero_de_Exportaciones DESC 
            LIMIT 5;
        ''')
    
    rows = cur.fetchall()
    print(rows)
    conn.commit()

    cur.close()
    conn.close()
    return [dict(row) for row in rows]