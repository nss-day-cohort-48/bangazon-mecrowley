"""Module for generating games by user report"""
import sqlite3
from django.shortcuts import render
from bangazonreports.views import Connection


def completed_orders_list(request):
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
                    SUM(p.price) order_total_cost,
                    payment.merchant_name payment_merchant_name,
                    payment.account_number payment_account_number
                FROM
                    auth_user u
                JOIN
                    bangazonapi_customer c ON c.user_id = u.id
                JOIN
                    bangazonapi_order o ON o.customer_id = c.id
                LEFT JOIN
                    bangazonapi_orderproduct op ON op.order_id = o.id
                LEFT JOIN
                    bangazonapi_product p ON p.id = op.product_id
                JOIN
                    bangazonapi_payment payment ON payment.id = o.payment_type_id
                WHERE
                    o.payment_type_id IS NOT NULL
                GROUP BY
                    o.id;
            """)

            dataset = db_cursor.fetchall()

            completed_orders = []

            for row in dataset:
                complete_order = {}
                complete_order["order_id"] = row["order_id"]
                complete_order["customer_name"] = row["customer_name"]
                if row["order_total_cost"] is not None:
                    complete_order["order_total_cost"] = row["order_total_cost"]
                else:
                    complete_order["order_total_cost"] = 0
                complete_order["payment_merchant_name"] = row["payment_merchant_name"]
                complete_order["payment_account_number"] = row["payment_account_number"]
                completed_orders.append(complete_order)


        template = 'orders/completed_orders.html'
        context = {
            'completed_orders_list': completed_orders
        }

        return render(request, template, context)
