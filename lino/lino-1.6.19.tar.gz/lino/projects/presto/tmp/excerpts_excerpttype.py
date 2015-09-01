# -*- coding: UTF-8 -*-
logger.info("Loading 3 objects to table excerpts_excerpttype...")
# fields: id, build_method, template, name, attach_to_email, email_template, certifying, remark, body_template, content_type, primary, backward_compat, print_recipient, print_directly, shortcut
loader.save(create_excerpts_excerpttype(1,None,u'',[u'Invoice', u'Rechnung', u'Invoice', u'Arve'],False,u'',True,u'',u'',sales_VatProductInvoice,True,False,True,True,None))
loader.save(create_excerpts_excerpttype(2,None,u'',[u'Service Report', u'Service Report', u'Service Report', u'Service Report'],False,u'',True,u'',u'default.body.html',clocking_ServiceReport,True,False,False,True,None))
loader.save(create_excerpts_excerpttype(3,None,u'',[u'Milestone', u'Milestone', u'Milestone', u'Milestone'],False,u'',True,u'',u'default.body.html',tickets_Milestone,True,False,False,True,None))

loader.flush_deferred_objects()
