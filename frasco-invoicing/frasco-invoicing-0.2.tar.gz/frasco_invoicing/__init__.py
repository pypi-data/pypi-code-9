from frasco import Feature, action, signal, current_app
from frasco_models import as_transaction, save_model, ref
import datetime
from contextlib import contextmanager


class InvoicingFeature(Feature):
    name = "invoicing"
    requires = ["models"]
    defaults = {"model": "Invoice",
                "item_model": "InvoiceItem",
                "send_email": None}

    invoice_issueing_signal = signal('invoice_issueing')
    invoice_issued_signal = signal('invoice_issued')

    def init_app(self, app):
        self.ref_creator_callback = self.create_ref

        self.model = app.features.models.ensure_model(self.options['model'],
            ref=dict(type=str, index=True),
            currency=str,
            subtotal=float,
            total=float,
            tax_rate=float,
            tax_amount=float,
            description=str,
            name=str,
            email=str,
            address_line1=str,
            address_line2=str,
            address_city=str,
            address_state=str,
            address_zip=str,
            address_country=str,
            country=str,
            customer_special_mention=str,
            issued_at=datetime.datetime,
            charge_id=str,
            external_id=str,
            customer=ref(),
            items=list)

        self.item_model = app.features.models.ensure_model(self.options['item_model'],
            amount=float,
            description=str,
            quantity=int,
            subtotal=float,
            currency=str,
            external_id=str)

        if app.features.exists("emails"):
            app.features.emails.add_templates_from_package(__name__)
            if self.options['send_email'] is None:
                self.options['send_email'] = True


    def ref_creator(self, func):
        self.ref_creator_callback = func
        return func

    def create_ref(self, category=None, counter=None, separator='-', merge_date=True):
        today = datetime.date.today()
        parts = [today.year, today.month, today.day]
        if merge_date:
            parts = ["".join(map(str, parts))]
        if category:
            parts.append(category)
        if counter is None:
            counter = current_app.features.models.query(self.model).count() + 1
        parts.append(counter)
        return separator.join(map(str, parts))

    @contextmanager
    def create(self, **ref_kwargs):
        invoice = self.model()
        invoice.ref = self.ref_creator_callback(**ref_kwargs)
        yield invoice
        self.save(invoice)

    @as_transaction
    def save(self, invoice):
        self.invoice_issueing_signal.send(invoice)
        save_model(invoice)
        self.invoice_issued_signal.send(invoice)
        if invoice.email and self.options['send_email']:
            self.send_email(invoice.email, invoice)

    def send_email(self, email, invoice, **kwargs):
        items = []
        for item in invoice.items:
            items.append((item.description, item.amount))
        current_app.features.emails.send(email, 'invoice.html',
            invoice_date=invoice.issued_at,
            invoice_items=items,
            invoice_currency=invoice.currency.upper(),
            invoice_total=invoice.total,
            **kwargs)