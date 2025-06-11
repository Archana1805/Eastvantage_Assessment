import pandas as pd
import sqlite3

connection = None
try:
    db = 'database.db'
    connection = sqlite3.connect(db)

    df_sales = pd.read_sql("Select * from Sales",connection)
    df_customer = pd.read_sql("Select * from Customer",connection)
    df_orders = pd.read_sql("Select * from Orders",connection)
    df_items = pd.read_sql("Select * from Items",connection)

    df_cust = df_customer[(df_customer['age']>=18)&(df_customer['age']<=35)]

    df = df_cust.merge(df_sales,on="customer_id")
    df = df.merge(df_orders,on='sales_id')
    df = df.merge(df_items,on='item_id')

    df = df.groupby(["customer_id","age","item_name"])['quantity'].sum()

    df = df[df['quantity']>0]

    df.columns = ['Customer','Age','Item_Name','Quantity']

    df['Quantity'] = df['Quantity'].astype(int)

    df.to_csv("Quantity_details.csv", sep=';', index=False)

except Exception as e:
    print(f"Error:{e}")

finally:
    connection.close()
