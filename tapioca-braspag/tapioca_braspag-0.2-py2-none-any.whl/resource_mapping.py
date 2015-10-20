# coding: utf-8

RESOURCE_MAPPING = {
    'sales_create': {
        'resource': 'v2/sales/',
        'docs': 'http://apidocs.braspag.com.br/'
        #post
    },
    'sales_capture': {
        'resource': 'v2/sales/{id}/capture',
        'docs': 'http://apidocs.braspag.com.br/'
        #put
    },
    'sales_cancel': {
        'resource': 'v2/sales/{id}/void',
        'docs': 'http://apidocs.braspag.com.br/'
        #put
    },
    'sales_consult': {
        'resource': 'v2/sales/{id}',
        'docs': 'http://apidocs.braspag.com.br/'
        #get
    },
    'recurrency_consult': {
        'resource': 'RecurrentPayment/{id}',
        'docs': 'http://apidocs.braspag.com.br/'
        #get
    },
    'recurrency_change_customer_data': {
        'resource': 'v2/RecurrentPayment/{id}/Customer',
        'docs': 'http://apidocs.braspag.com.br/'
        #put
    },
    'recurrency_change_end_date': {
        'resource': 'v2/RecurrentPayment/{id}/EndDate',
        'docs': 'http://apidocs.braspag.com.br/'
        #put
    },
    'recurrency_change_installments': {
        'resource': 'v2/RecurrentPayment/{id}/Installments',
        'docs': 'http://apidocs.braspag.com.br/'
        #put
    },
    'recurrency_change_interval': {
        'resource': 'v2/RecurrentPayment/{id}/Interval',
        'docs': 'http://apidocs.braspag.com.br/'
        #put
    },
    'recurrency_change_day': {
        'resource': 'v2/RecurrentPayment/{id}/RecurrencyDay',
        'docs': 'http://apidocs.braspag.com.br/'
        #put
    },
    'recurrency_change_next_date': {
        'resource': 'v2/RecurrentPayment/{id}/NextPaymentDate',
        'docs': 'http://apidocs.braspag.com.br/'
        #put
    },
    'recurrency_change_amount': {
        'resource': 'v2/RecurrentPayment/{id}/Amount',
        'docs': 'http://apidocs.braspag.com.br/'
        #put
    },
    'recurrency_change_payment_data': {
        'resource': 'v2/RecurrentPayment/{id}/Payment',
        'docs': 'http://apidocs.braspag.com.br/'
        #put
    },
    'recurrency_deactivate': {
        'resource': 'v2/RecurrentPayment/{id}/Deactivate',
        'docs': 'http://apidocs.braspag.com.br/'
        #put
    },
    'recurrency_reactivate': {
        'resource': 'v2/RecurrentPayment/{id}/Reactivate',
        'docs': 'http://apidocs.braspag.com.br/'
        #put
    },
    'merchant_consult_sales': {
        'resource': 'v2/sales?merchantOrderId={id}',
        'docs': 'http://apidocs.braspag.com.br/'
        #get
    },
}
