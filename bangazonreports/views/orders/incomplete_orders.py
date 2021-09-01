"""Module for generating games by user report"""
import sqlite3
from django.shortcuts import render
from bangazonreports.views import Connection


def incomplete_orders_list(request):
    """Function to build an HTML report showing all users that have favorited a seller,
        including the favorited sellers"""

    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()
            db_cursor.execute("""
                SELECT
                    u.first_name || ' ' || u.last_name customer_name,
                    o.id order_id,
                    SUM(p.price) order_total_cost
                FROM
                    auth_user u
                JOIN
                    bangazonapi_customer c ON c.user_id = u.id
                JOIN
                    bangazonapi_order o ON o.customer_id = c.id
                JOIN
                    bangazonapi_orderproduct op ON op.order_id = o.id
                JOIN
                    bangazonapi_product p ON p.id = op.product_id
                WHERE
                    o.payment_type_id IS NULL
                GROUP BY
                    order_id;
            """)

            dataset = db_cursor.fetchall()

            incomplete_orders = []

            for row in dataset:
                incomplete_order = {}
                incomplete_order["order_id"] = row["order_id"]
                incomplete_order["customer_name"] = row["customer_name"]
                incomplete_order["order_total_cost"] = row["order_total_cost"]
                incomplete_orders.append(incomplete_order)


        template = 'orders/incomplete_orders.html'
        context = {
            'incomplete_orders_list': incomplete_orders
        }

        return render(request, template, context)
