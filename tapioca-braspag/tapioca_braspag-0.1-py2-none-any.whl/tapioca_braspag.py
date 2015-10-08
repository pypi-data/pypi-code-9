# coding: utf-8
import uuid

from tapioca import (
    TapiocaAdapter, JSONAdapterMixin, generate_wrapper_from_adapter)

from tapioca.adapters import TapiocaInstantiator

from tapioca.exceptions import ResponseProcessException, ClientError,\
     ServerError

from resource_mapping import RESOURCE_MAPPING


class BraspagBaseClientAdapter(JSONAdapterMixin, TapiocaAdapter):
    resource_mapping = RESOURCE_MAPPING

    def get_request_kwargs(self, api_params, *args, **kwargs):
        params = super(BraspagBaseClientAdapter, self).get_request_kwargs(
            api_params, *args, **kwargs)

        if 'headers' in api_params:
            params['headers'] = api_params['headers']
            params['headers']['ResponseId'] = self.generate_response_id()

        return params

    def get_iterator_list(self, response_data):
        return response_data

    def process_response(self, response):
        if str(response.status_code).startswith('5'):
            raise ResponseProcessException(ServerError, None)

        if response.content:
            data = self.response_to_native(response)
        else:
            data = None

        if str(response.status_code).startswith('4'):
            raise ResponseProcessException(ClientError, data)

        return data

    def generate_response_id(self):
        hash = uuid.uuid4()
        return str(hash)


class BraspagClientAdapter(BraspagBaseClientAdapter):
    api_root = 'https://apihomolog.braspag.com.br/'


class BraspagConsultClientAdapter(BraspagBaseClientAdapter):
    api_root = 'https://apiqueryhomolog.braspag.com.br/'


BraspagConsult = generate_wrapper_from_adapter(BraspagConsultClientAdapter)
Braspag = generate_wrapper_from_adapter(BraspagClientAdapter)

class TapiocaBraspagInstantiator(TapiocaInstantiator):

    def __call__(self, merchant_id=None, merchant_key=None, *args, **kwargs):
        if not 'headers' in kwargs:
            kwargs['headers'] = {
                "Content-Type": "application/json",
                "MerchantId": merchant_id,
                "MerchantKey": merchant_key,
                "ResponseId": None,
            }

        return super(TapiocaBraspagInstantiator, self).__call__(*args, **kwargs)

BraspagConsult = TapiocaBraspagInstantiator(BraspagConsultClientAdapter)
Braspag = TapiocaBraspagInstantiator(BraspagClientAdapter)

