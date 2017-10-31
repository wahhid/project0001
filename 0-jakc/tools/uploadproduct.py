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
    ids = sock_object.execute(dbname, uid, password, 'product.template', 'search', args)
    if ids:
        return sock_object.execute(dbname, uid, password, 'product.template', 'read', ids[0])
    else:
        return False


def create_product(vals):
    print vals.get('name')
    return sock_object.execute(dbname, uid, password, 'product.template', 'create', vals)


def update_product(product_id, vals):
    print vals.get('name')
    return sock_object.execute(dbname, uid, password, 'product.template', 'write', [product_id], vals)


def find_product_uom(name):
    args = [('name', '=', name)]
    ids = sock_object.execute(dbname, uid, password, 'product.uom', 'search', args)
    if ids:
        return sock_object.execute(dbname, uid, password, 'product.uom', 'read', ids[0])
    else:
        return False

def create_product_uom(vals):
    return sock_object.execute(dbname, uid, password, 'product.uom', 'create', vals)


def find_category(name):
    args = [('name', '=', name)]
    ids = sock_object.execute(dbname, uid, password, 'product.category', 'search', args)
    if ids:
        return sock_object.execute(dbname, uid, password, 'product.category', 'read', ids[0])
    else:
        return False


def create_category(vals):
    return sock_object.execute(dbname, uid, password, 'product.category', 'create', vals)


def find_merk(name):
    args = [('name', '=', name)]
    ids = sock_object.execute(dbname, uid, password, 'product.merk', 'search', args)
    if ids:
        return sock_object.execute(dbname, uid, password, 'product.merk', 'read', ids[0])
    else:
        return False


def create_merk(vals):
    return sock_object.execute(dbname, uid, password, 'product.merk', 'create', vals)


with open('Product.csv', 'rb') as csvfile:
    rowreader = csv.reader(csvfile)
    i = 0
    for row in rowreader:
        i = i + 1
        if i >= 1840:
            if row[0].strip():
                vals = {}
                vals.update({'default_code': row[0].strip()})
                vals.update({'name': row[2].strip()})
                if row[3].strip():
                    vals.update({'standart_price': int(row[3].strip())})
                else:
                    vals.update({'standart_price': 0})
                if row[4].strip():
                    vals.update({'list_price': int(row[4].strip())})
                else:
                    vals.update({'list_price': 0})

                product_merk = find_merk(row[5].strip())
                if not product_merk:
                    merk_vals = {}
                    merk_vals.update({'name': row[5].strip()})
                    merk_id = create_merk(merk_vals)
                    vals.update({'merk_id': merk_id})
                else:
                    vals.update({'merk_id': product_merk['id']})

                if row[6].strip():
                    vals.update({'warna': row[6].strip()})
                if row[7].strip():
                    vals.update({'motif': row[7].strip()})
                if row[8].strip():
                    vals.update({'page': row[8].strip()})

                product_category = find_category(row[9].strip())
                if not product_category:
                    category_vals = {}
                    category_vals.update({'name': row[9].strip()})
                    category_id = create_category(category_vals)
                    vals.update({'categ_id': category_id})
                else:
                    vals.update({'categ_id': product_category['id']})

                #if row[10].strip():
                #    product_uom = find_product_uom(row[10].strip())
                #    if not product_uom:
                #        uom_vals = {}
                #        uom_vals.update({'name': row[10].strip()})
                #        uom_vals.update({'category_id': 1})
                #        uom_id = create_product_uom(uom_vals)
                #        vals.update({'uom_id': uom_id})
                #    else:
                #        vals.update({'uom_id': product_uom['id']})

                #if row[11].strip():
                #    product_uom_po = find_product_uom(row[11].strip())
                #    if not product_uom_po:
                #        uom_vals = {}
                #        uom_vals.update({'name': row[10].strip()})
                #        uom_vals.update({'category_id': 1})
                #        uom_id = create_product_uom(uom_vals)
                #        vals.update({'uom_po_id': uom_id})
                #    else:
                #        vals.update({'uom_po_id': product_uom_po['id']})

                vals.update({'costing_method': 'average'})
                vals.update({'type': 'product'})

                product_template = find_product(row[0].strip())
                if not product_template:
                    product_id = create_product(vals)
                    if product_id:
                        print str(i) + " Product Created"
                else:
                    product_id = update_product(product_template['id'], vals)
                    print str(i) + " Product Updated"

        else:
            print row[0].strip() + ' ' + row[2].strip()
