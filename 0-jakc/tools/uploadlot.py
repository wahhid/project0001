import csv
import xmlrpclib

username = 'admin'
password = 'password123'
dbname = 'erp_dev'
sock_common = xmlrpclib.ServerProxy('http://103.252.101.243:8069/xmlrpc/common')
sock_object = xmlrpclib.ServerProxy('http://103.252.101.243:8069/xmlrpc/object')
uid = sock_common.login(dbname, username, password)


def find_product(default_code):
    args = [('default_code', '=', default_code)]
    ids = sock_object.execute(dbname, uid, password, 'product.product', 'search', args)
    if ids:
        return sock_object.execute(dbname, uid, password, 'product.product', 'read', ids[0])
    else:
        return False


def find_lot(product_id, lot_name):
    args = [('product_id', '=', product_id)]
    ids = sock_object.execute(dbname, uid, password, 'stock.production.lot', 'search', args)
    if ids:
        return sock_object.execute(dbname, uid, password, 'stock.production.lot', 'read', ids[0])
    else:
        return False


def create_lot(vals):
    print vals.get('name')
    return sock_object.execute(dbname, uid, password,  'stock.production.lot', 'create', vals)

with open('Lot.csv', 'rb') as csvfile:
    rowreader = csv.reader(csvfile)
    i = 0
    for row in rowreader:
        i = i + 1
        if row[3].strip():
            product_id = find_product(row[0].strip())
            if product_id:
                if row[3].strip():
                    lot = find_lot(product_id.get('id'), row[3].strip())
                    if not lot:
                        values = {}
                        values.update({'product_id': product_id.get('id')})
                        values.update({'name': row[3].strip()})
                        result = create_lot(values)
                        print str(i) + ' ' +  row[0].strip() + 'Lot Created'
                    else:
                        print str(i) + ' ' +  row[0].strip() + 'Lot Found'

