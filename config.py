class Server :
    server_add = ('', 2540)
    database_name = 'mydatabase.db'

class Purchase :
    headers_to_extract = ['OrderNumber','Ref', 'Date', 'Supplier', 'Amount']

class Sales :
    headers_to_extract = ['CUST_ORDER_NUMBER','ORDER_DATE','UNIT_PRICE', 'QTY_ORDER', 'STOCK_CODE','DESCRIPTION','CARR_NOM_CODE','CARR_GROSS','TAX_CODE']

class Styles :
    styles = [
    {
        'selector': 'table',
        'props': [
            ('border-collapse', 'collapse'),
            ('width', '100%'),
            ('border-radius', '8px'),
            ('overflow', 'hidden'),
            ('box-shadow', '0 4px 8px rgba(0, 0, 0, 0.1)'),
            ('margin', '20px 0'),
        ]
    },
    {
        'selector': 'th, td',
        'props': [
            ('padding', '12px'),
            ('text-align', 'left'),
            ('border-bottom', '1px solid #ddd'),
        ]
    },
    {
        'selector': 'th',
        'props': [
            ('background-color', '#3498db'),
            ('color', 'white'),
        ]
    },
    {
        'selector': 'tr:nth-child(even)',
        'props': [
            ('background-color', '#f2f2f2'),
        ]
    },
    {
        'selector': 'tr:hover',
        'props': [
            ('background-color', '#eaf7fd'),
        ]
    },
    {
        'selector': '.center-table',  # Class for centering
        'props': [
            ('display', 'flex'),
            ('justify-content', 'center'),
            ('align-items', 'center'),
            ('height', '100vh'),  # Set height for full page height
        ]
    }
]
