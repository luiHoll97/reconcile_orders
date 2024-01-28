from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from constants import HttpStatus, ContentType
from config import Server as serv
from config import Purchase as purch
from config import Sales as sales
from config import Styles as styles
import logging
from dotenv import load_dotenv
import os
import pandas as pd
import numpy as np
import re

# load .env file variables
load_dotenv()

# Sales Order File
sales_file_path = './Sales Order Example.csv'
unfiltered_sales_orders = pd.read_csv(sales_file_path)
unstyled_sales_orders = unfiltered_sales_orders[sales.headers_to_extract]
sales_orders = unstyled_sales_orders.style.set_table_styles(styles.styles)


purchase_file_path = './Purchase Orders Example.csv'
unfiltered_pos = pd.read_csv(purchase_file_path, encoding='utf-8')

# Extract order number from the 'Organizer' column
unfiltered_pos['OrderNumber'] = unfiltered_pos['Organizer'].apply(lambda x: re.search(r'#(\d+)', x).group(1) if re.search(r'#(\d+)', x) else np.nan)
unstyled_purchase_orders = unfiltered_pos[purch.headers_to_extract]
purchase_orders = unstyled_purchase_orders.style.set_table_styles(styles.styles)
#unfiltered_pos = purchase_orders.drop('Organizer', axis=1)


# merge the tables
merged_tables = pd.merge(unstyled_sales_orders, unstyled_purchase_orders, left_on='CUST_ORDER_NUMBER', right_on='OrderNumber', how='inner')
styled_table = merged_tables.style.set_table_styles(styles.styles)


# Logging config
logging.basicConfig(level=logging.INFO)

class SimpleHandler(BaseHTTPRequestHandler):

    def _send_response(self, status_code, content_type, message):

        self.send_response(status_code)
        self.send_header('Content-type', content_type)
        self.end_headers()

         # Ensure that message is in bytes format
        if not isinstance(message, bytes):
            message = message.encode('utf-8')
        self.wfile.write(message)

    def handle_get(self, path, queryparams) :
        if path == '/':
            self.send_response(HttpStatus.OK)
            self.send_header('Content-type', ContentType.HTML)
            self.end_headers()

             # Convert DataFrame to HTML table with minimal white space
            html_table = styled_table.to_html(index=False, escape=False, na_rep='', justify='left')
            print(purchase_orders)

            # Send the HTML table back to the user
            self._send_response(HttpStatus.OK, ContentType.HTML, html_table)
        elif path == '/sales' :
            self.send_response(HttpStatus.OK)
            self.send_header('Content-type', ContentType.HTML)
            self.end_headers()

             # Convert DataFrame to HTML table with minimal white space
            html_table = sales_orders.to_html(index=False, escape=False, na_rep='', justify='left')

            # Send the HTML table back to the user
            self._send_response(HttpStatus.OK, ContentType.HTML, html_table)
        elif path == '/purchase' :
            self.send_response(HttpStatus.OK)
            self.send_header('Content-type', ContentType.HTML)
            self.end_headers()

             # Convert DataFrame to HTML table with minimal white space
            html_table = purchase_orders.to_html(index=False, escape=False, na_rep='', justify='left')

            # Send the HTML table back to the user
            self._send_response(HttpStatus.OK, ContentType.HTML, html_table)
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'404 Not Found')

    def do_GET(self):
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        query_params = parse_qs(parsed_url.query)
        self.handle_get(path, query_params)


if __name__ == '__main__':
    try :
        print('Starting server...')
        httpd = HTTPServer(serv.server_add, SimpleHandler)
        logging.info(' Server started successfully. You now owe your son an additional £1 💰')
        httpd.serve_forever()
    except KeyboardInterrupt :
        print('')
        print('Stopping Server...')
        httpd.server_close()
        logging.info(' Server stopped. Seeya later 👊')
    