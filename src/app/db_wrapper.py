from database import get_db_cursor

def execute_sql(sql, params=None, fetch_one=False, fetch_all=False):
    """
    Универсальная функция для выполнения SQL запросов
    Автоматически конвертирует ? в %s для PostgreSQL
    """
    if '?' in sql and '%s' not in sql:
        sql = sql.replace('?', '%s')
    
    with get_db_cursor() as cursor:
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        
        if fetch_one:
            return cursor.fetchone()
        elif fetch_all:
            return cursor.fetchall()

def execute(sql, params=None):
    """INSERT, UPDATE, DELETE"""
    return execute_sql(sql, params)

def query_one(sql, params=None):
    """SELECT одна запись"""
    return execute_sql(sql, params, fetch_one=True)

def query_all(sql, params=None):
    """SELECT все записи"""
    return execute_sql(sql, params, fetch_all=True)