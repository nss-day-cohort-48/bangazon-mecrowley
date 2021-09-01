"""Module for generating games by user report"""
import sqlite3
from django.shortcuts import render
from bangazonreports.views import Connection


def customer_favorite_sellers_list(request):
    """Function to build an HTML report showing all users that have favorited a seller,
        including the favorited sellers"""

    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()
            db_cursor.execute("""
                SELECT
                    f.customer_id customer_id,
                    u.first_name || ' ' || u.last_name AS customer_name,
                    favorite_sellers.seller_id,
                    favorite_sellers.seller_name
                FROM
                    bangazonapi_favorite f
                JOIN
                    bangazonapi_customer c ON c.id = f.customer_id
                JOIN
                    auth_user u ON c.user_id = u.id
                JOIN
                    (SELECT
                        f.seller_id seller_id,
                        u.first_name || ' ' || u.last_name AS seller_name
                    FROM
                        bangazonapi_favorite f
                    JOIN
                        bangazonapi_customer c ON c.id = f.seller_id
                    JOIN
                        auth_user u ON u.id = c.user_id) AS favorite_sellers
                    ON f.seller_id = favorite_sellers.seller_id
            """)

            dataset = db_cursor.fetchall()

            customer_favorite_sellers = {}

            for row in dataset:
                favorite_seller = {}
                favorite_seller["seller_id"] = row["seller_id"]
                favorite_seller["full_name"] = row["seller_name"]

                cid = row["customer_id"]

                if cid in customer_favorite_sellers:
                    customer_favorite_sellers[cid]['favorite_sellers'].append(favorite_seller)

                else:
                    customer_favorite_sellers[cid] = {}
                    customer_favorite_sellers[cid]["customer_id"] = cid
                    customer_favorite_sellers[cid]["full_name"] = row["customer_name"]
                    customer_favorite_sellers[cid]["favorite_sellers"] = [favorite_seller]

        list_of_customers_with_favorite_sellers = customer_favorite_sellers.values()

        template = 'users/customers_with_favorite_sellers.html'
        context = {
            'customer_favorite_sellers_list': list_of_customers_with_favorite_sellers
        }

        return render(request, template, context)
