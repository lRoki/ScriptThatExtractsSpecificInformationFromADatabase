from mysql.connector import connect, Error
import os
import sys
import time
import logging
import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.withdraw()


logging.basicConfig(filename='filelog.log', filemode="w",level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


HOST = "216.172.173.7"

DATABASE_SISTEMA_INTERNO = "NAME OF THE DATABASE WHERE THE INFORMATION IS EXTRACTED "
USER_SISTEMA_INTERNO = "USER OF THE DATABASE WHERE THE INFORMATION IS EXTRACTED"
PASSWORD_SISTEMA_INTERNO = "PASSWORD OF THE DATABASE WHERE THE INFORMATION IS EXTRACTED"

DATABASE_ANALISTAS = "NAME OF THE DATABASE WHERE THE INFORMATION IS STORED"
USER_ANALISTA = "USER OF THE DATABASE WHERE THE INFORMATION IS STORED"
PASSWORD_ANALISTA = "PASSWORD OF THE DATABASE WHERE THE INFORMATION IS STORED"


try:
    connection_sistema_interno = connect(host=HOST, database=DATABASE_SISTEMA_INTERNO, user=USER_SISTEMA_INTERNO, password=PASSWORD_SISTEMA_INTERNO,autocommit=True,buffered=True)
except Error as e:
    print(e)
    logging.info("Error: %s",e)
    messagebox.showerror("Error",e)
    sys.exit()


try:
    connection_analistas = connect(host=HOST, database=DATABASE_ANALISTAS, user=USER_ANALISTA, password=PASSWORD_ANALISTA,autocommit=True,buffered=True)
except Error as e:
    print(e)
    logging.info("Error: %s",e)
    messagebox.showerror("Error",e)
    sys.exit()
    

cursor_sistema_insterno = connection_sistema_interno.cursor()

cursor_connection_analistas = connection_analistas.cursor()


def get_sum_valor_liqui_aprovado():
    sql = "SELECT Vendedor, SUM(REPLACE(REPLACE(ValorLiquido,'.',''),',','.')) FROM usuarios WHERE Situacao = 'Aprovado' Group By Vendedor"
    cursor_sistema_insterno.execute(sql)
    rows = cursor_sistema_insterno.fetchall()
    if rows:
        return rows
    else:
        return False


def check_vendedor_name_exist(vendedor_name):
    sql = f'SELECT Valor FROM valorliquido WHERE Nome = "{vendedor_name}"'
    cursor_connection_analistas.execute(sql)
    if cursor_connection_analistas.fetchone():
        return True
    else:
        return False
    
def insert_valor_liquido(name,valor_liquido):
    sql = f'INSERT INTO valorliquido (Nome,Valor) VALUES ("{name}",{valor_liquido})'
    cursor_connection_analistas.execute(sql)
    count_row = cursor_connection_analistas.rowcount
    if count_row > 0:
        return True
    else:
        return False
    

def update_valor_liquido(name,valor_liquido):
    sql = f'UPDATE valorliquido SET Valor = {valor_liquido} WHERE Nome = "{name}"'
    cursor_connection_analistas.execute(sql)
    count_row = cursor_connection_analistas.rowcount
    if count_row > 0:
        return True
    else:
        return False
       
    
def main():
    logging.info("Main Iniciado")
    rows = get_sum_valor_liqui_aprovado()
    if rows:
        for row in rows:
            vendedor_name = row[0]
            valor_liquido = row[1]
            valor_liquido_format =  "{:.2f}".format(valor_liquido)

            print(vendedor_name,valor_liquido_format)
            logging.info("Vendedor: %s - Valor Liquido: %s",vendedor_name,valor_liquido_format)

            if check_vendedor_name_exist(vendedor_name):
                if update_valor_liquido(vendedor_name,valor_liquido_format):
                    print("Actualizado:",vendedor_name,valor_liquido_format)
                    logging.info("Actualizado: %s - %s",vendedor_name,valor_liquido_format)
                else:
                    print("Existente:",vendedor_name,valor_liquido_format)
                    logging.info("Existente: %s - %s",vendedor_name,valor_liquido_format)

            else:
                if insert_valor_liquido(vendedor_name,valor_liquido_format):
                    print("Insertado:",vendedor_name,valor_liquido_format)
                    logging.info("Insertado: %s - %s",vendedor_name,valor_liquido_format)
                else:
                    print("No Insertado:",vendedor_name,valor_liquido_format)
                    logging.info("No Insertado: %s - %s",vendedor_name,valor_liquido_format)
    else:
        print("No rows en get_sum_valor_liqui_aprovado")
        logging.info("No rows en get_sum_valor_liqui_aprovado")


    logging.info("Main Finalizado")

     
if __name__ == "__main__":
    main()

