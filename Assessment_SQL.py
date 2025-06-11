import sqlite3
import csv

connection = None
try:
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    query = """
    select cust.customer_id,cust.age, item.item_name, cast(sum(ord.quantity),integer) as quantities
    from customer cust
    join sales s on cust.cust_id = s.customer_id
    join orders ord on ord.sales_id = s.sales_id
    join items item on item.item_id = ord.item_id
    where cust.age between 18 and 35
    group by cust.customer_id, item.item_name
    having quantities > 0
    order by cust.customer_id, item.item_name
    """

    cursor.execute(query)
    results = cursor.fetchall()

    with open("Quantity_details.csv",mode='w',newline='') as file:
        writer = csv.writer(file,delimiter=';')
        writer.writerow(['Customer','Age','Item','Quantity'])
        for row in results:
            writer.writerow(row)

except Exception as e:
    print(f"Error:{e}")

finally:
    connection.close()
