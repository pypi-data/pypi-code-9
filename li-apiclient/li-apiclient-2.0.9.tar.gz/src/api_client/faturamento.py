from api_client.utils import ApiClientBase

class ApiFaturamento(ApiClientBase):
    NOME = "API_FATURAMENTO"
    AUTENTICA_APLICACAO = True

    def dados_cobranca_consultar(self, conta_id, **kwargs):
        path = '/conta/{}/dados_cobranca/'.format(conta_id)
        return self.to_dict(path,method="get",meta=True, **kwargs)

    def dados_cobranca_editar(self, conta_id, **kwargs):
        path = '/conta/{}/dados_cobranca/'.format(conta_id)
        return self.to_dict(path, method="put", meta=True, **kwargs)

    def dados_cobranca_cartao_consultar(self, conta_id):
        path = '/conta/{}/dados_cobranca/cartao/'.format(conta_id)
        return self.to_dict(path,method="get",meta=True)

    def dados_cobranca_cartao_editar(self, conta_id, **kwargs):
        path = '/conta/{}/dados_cobranca/cartao/'.format(conta_id)
        return self.to_dict(path, method="put", meta=True, **kwargs)

    def colecoes(self):
        path = '/colecoes/'
        return self.to_dict(path,"get",meta=True)

    def planos(self, colecao_id):
        path = '/colecao/{}/planos/'.format(colecao_id)
        return self.to_dict(path,"get",meta=True)

    def plano(self, colecao_id, plano_id):
        path = '/colecao/{}/plano/{}/'.format(colecao_id, plano_id)
        return self.to_dict(path,method="get",meta=True)

    def plano_assinaturas(self, conta_id):
        path = '/conta/{}/plano/assinaturas/'.format(conta_id)
        return self.to_dict(path,method="get",meta=True)

    def loja_faturas(self, conta_id, **kwargs):
        path = '/conta/{}/faturas/'.format(conta_id)
        return self.to_dict(path,method="get",meta=True, **kwargs)

    def loja_fatura(self, conta_id, fatura_id):
        path = '/conta/{}/fatura/{}/'.format(conta_id,fatura_id)
        return self.to_dict(path,method="get",meta=True)

    def loja_fatura_cancelar(self, conta_id, fatura_id):
        path = '/conta/{}/fatura/{}/cancelar/'.format(conta_id, fatura_id)
        return self.to_dict(path,method="put",meta=True)

    def loja_fatura_cancelar(self, conta_id, fatura_id):
        path = '/conta/{}/fatura/{}/cancelar/'.format(conta_id, fatura_id)
        return self.to_dict(path,method="put",meta=True)

    def faturas(self, **kwargs):
        path = '/faturas/'
        return self.to_dict(path,method="get",meta=True, **kwargs)

    def fatura(self, fatura_id, **kwargs):
        path = '/fatura/{}/'.format(fatura_id)
        return self.to_dict(path,method="get",meta=True, **kwargs)

    def plano_vigente(self, conta_id, **kwargs):
        path = '/conta/{}/plano/vigente/'.format(conta_id)
        return self.to_dict(path,method="get",meta=True, **kwargs)

    def plano_pago_vigente(self, conta_id):
        path = '/conta/{}/plano/pago_vigente/'.format(conta_id)
        return self.to_dict(path,method="get",meta=True)

    def simular_proximo_ciclo(self, conta_id, plano_id):
        path = '/conta/{}/plano/{}/simular_proximo_ciclo/'.format(conta_id,plano_id)
        return self.to_dict(path,method="get",meta=True)

    def assinar(self, conta_id, plano_id, method="post"):
        path = '/conta/{}/plano/{}/assinar/'.format(conta_id,plano_id)
        return self.to_dict(path,method=method,meta=True)

    def comprar_certificado(self, conta_id, certificado_id):
        path = '/conta/{}/certificado/{}/comprar/'.format(conta_id,certificado_id)
        return self.to_dict(path,method="post",meta=True)

    def certificado_faturas(self, conta_id, **kwargs):
        path = '/conta/{}/certificado/faturas/'.format(conta_id)
        return self.to_dict(path,method="get",meta=True, **kwargs)

    def fatura_enviar_lancamento(self, fatura_id, **kwargs):
        path = '/fatura/{}/enviar_lancamento/'.format(fatura_id)
        return self.to_dict(path,method="post",meta=True, **kwargs)

    def fatura_quitar_lancamento(self, fatura_id, **kwargs):
        path = '/fatura/{}/quitar_lancamento/'.format(fatura_id)
        return self.to_dict(path,method="post",meta=True, **kwargs)

    def conta_consumo_reduzir_visitas(self, conta_id, porcento, **kwargs):
        path = '/conta/{}/consumo/reduzir/{}/porcento/'.format(conta_id,porcento)
        return self.to_dict(path,method="put",meta=True, **kwargs)

    def comprar_tema(self, conta_id, tema_id):
        path = '/conta/{}/tema/{}/comprar/'.format(conta_id,tema_id)
        return self.to_dict(path,method="post",meta=True)

    def tema_faturas(self, conta_id, **kwargs):
        path = '/conta/{}/tema/faturas/'.format(conta_id)
        return self.to_dict(path,method="get",meta=True, **kwargs)

    def comprar_banner(self, conta_id, banner_id):
        path = '/conta/{}/banner/{}/comprar/'.format(conta_id,banner_id)
        return self.to_dict(path,method="post",meta=True)

    def banner_faturas(self, conta_id, **kwargs):
        path = '/conta/{}/banner/faturas/'.format(conta_id)
        return self.to_dict(path,method="get",meta=True, **kwargs)