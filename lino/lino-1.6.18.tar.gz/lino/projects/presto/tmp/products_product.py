# -*- coding: UTF-8 -*-
logger.info("Loading 4 objects to table products_product...")
# fields: id, ref, name, description, cat, vat_class, sales_account, sales_price, purchases_account
loader.save(create_products_product(1,u'lino',[u'Lino Core', u'', u'', u''],[None, u'', u'', u''],None,None,None,None,None))
loader.save(create_products_product(2,u'welfare',[u'Lino Welfare', u'', u'', u''],[None, u'', u'', u''],None,None,None,None,None))
loader.save(create_products_product(3,u'cosi',[u'Lino Cosi', u'', u'', u''],[None, u'', u'', u''],None,None,None,None,None))
loader.save(create_products_product(4,u'faggio',[u'Lino Faggio', u'', u'', u''],[None, u'', u'', u''],None,None,None,None,None))

loader.flush_deferred_objects()
