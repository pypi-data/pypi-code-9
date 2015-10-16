from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.testing import z2
from plone.app.testing import IntegrationTesting, FunctionalTesting
from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE

from zope.interface import Interface
from zope.component import getSiteManager
from collective.zamqp.interfaces import (
    IBrokerConnection,
    IProducer,
    IConsumer,
    IMessageArrivedEvent
)
from collective.zamqp.connection import BrokerConnection
from collective.zamqp.server import ConsumingServer
from collective.zamqp.producer import Producer
from collective.zamqp.consumer import Consumer

from zope.configuration import xmlconfig

class EDepositPolicy(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)
    trace_on = False
    zserver = True
    user_id="admin"
    
    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import edeposit.policy
        import edeposit.user
        import edeposit.content
        import plone.app.versioningbehavior
        import collective.oaiintercom
        xmlconfig.file('configure.zcml', edeposit.content, context=configurationContext) 
        xmlconfig.file('configure.zcml', edeposit.user, context=configurationContext)
        xmlconfig.file('configure.zcml', edeposit.policy, context=configurationContext)
        xmlconfig.file('configure.zcml', plone.app.versioningbehavior, context=configurationContext)
        xmlconfig.file('configure.zcml', collective.oaiintercom, context=configurationContext)

        # import collective.pfg.dexterity
        # self.loadZCML(package=collective.pfg.dexterity)
        # z2.installProduct(app, "Products.PloneFormGen")
        # z2.installProduct(app, "Products.DataGridField")
        # z2.installProduct(app, "collective.pfg.dexterity")

        # Define dummy request handler to replace ZPublisher

        def handler(app, request, response):
            from zope.event import notify
            from zope.component import createObject
            message = request.environ.get('AMQP_MESSAGE')
            event = createObject('AMQPMessageArrivedEvent', message)
            notify(event)

        # Define ZPublisher-based request handler to be used with zserver

        def zserver_handler(app, request, response):
            from ZPublisher import publish_module
            publish_module(app, request=request, response=response)

        # Create connections and consuming servers for registered
        # producers and consumers
        sm = getSiteManager()

        connections = []
        consuming_servers = []

        for producer in sm.getAllUtilitiesRegisteredFor(IProducer):
            if not producer.connection_id in connections:
                connection = BrokerConnection(producer.connection_id,
                                              virtual_host=producer.connection_id,
                )
                sm.registerUtility(connection, provided=IBrokerConnection,
                                   name=connection.connection_id)
                connections.append(connection.connection_id)

        for consumer in sm.getAllUtilitiesRegisteredFor(IConsumer):
            if not consumer.connection_id in connections:
                connection = BrokerConnection(consumer.connection_id,
                                              virtual_host=consumer.consumer_id
                )
                sm.registerUtility(connection, provided=IBrokerConnection,
                                   name=connection.connection_id)
                connections.append(connection.connection_id)

            if not consumer.connection_id in consuming_servers:
                if self.zserver:
                    ConsumingServer(consumer.connection_id, 'plone',
                                    user_id=self.user_id,
                                    handler=zserver_handler,
                                    hostname='nohost',  # taken from z2.Startup
                                    port=80,
                                    use_vhm=False)
                else:
                    ConsumingServer(consumer.connection_id, 'plone',
                                    user_id=self.user_id,
                                    handler=handler,
                                    use_vhm=False)
                consuming_servers.append(consumer.connection_id)

        # Connect all connections

        from collective.zamqp import connection
        connection.connect_all()



    def tearDownZope(self, app):
        # Uninstall products installed above
        # z2.uninstallProduct(app, 'Products.PloneFormGen')
        # z2.uninstallProduct(app, 'Products.TemplateFields')
        # z2.uninstallProduct(app, 'Products.TALESField')
        # z2.uninstallProduct(app, 'Products.PythonField')
        pass

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'edeposit.content:default')
        applyProfile(portal, 'edeposit.user:default')
        applyProfile(portal, 'edeposit.policy:default')
        # self.applyProfile(portal, "Products.PloneFormGen:default")
        # self.applyProfile(portal, "Products.DataGridField:default")
        # self.applyProfile(portal, "collective.pfg.dexterity:default")

    def testSetUp(self):
        # XXX: How should we invalidate Dexterity fti.lookupSchema() cache?
        import plone.dexterity.schema
        for name in dir(plone.dexterity.schema.generated):
            if name.startswith("plone"):
                delattr(plone.dexterity.schema.generated, name)
        plone.dexterity.schema.SCHEMA_CACHE.clear()

class EDepositWithDiazoPolicy(EDepositPolicy):
    def setUpZone(self, app, configurationContext):
        super(EDepositWithDiazoPolicy,self).setUpZone(app, configurationContext)
        import edeposit.theme
        xmlconfig.file('configure.zcml', edeposit.theme, context=configurationContext) 
        pass
        

    # def setUpPloneSite(self, portal):
    #     super(EDepositWithDiazoPolicy,self).setUpPloneSite(portal)
    #     applyProfile(portal, 'edeposit.theme:default')

EDEPOSIT_POLICY_FIXTURE = EDepositPolicy()
EDEPOSIT_POLICY_ROBOT_TESTING = FunctionalTesting(
    bases=(EDEPOSIT_POLICY_FIXTURE,
           AUTOLOGIN_LIBRARY_FIXTURE,
           z2.ZSERVER_FIXTURE),
    name="E-Deposit Policy:Robot")

EDEPOSIT_WITH_DIAZO_POLICY_FIXTURE = EDepositWithDiazoPolicy()
EDEPOSIT_WITH_DIAZO_POLICY_ROBOT_TESTING = FunctionalTesting(
    bases=(EDEPOSIT_WITH_DIAZO_POLICY_FIXTURE,
           AUTOLOGIN_LIBRARY_FIXTURE,
           z2.ZSERVER_FIXTURE),
    name="E-Deposit With Diazo Policy:Robot")

EDEPOSIT_POLICY_INTEGRATION_TESTING = IntegrationTesting( bases=(EDEPOSIT_POLICY_FIXTURE,), 
                                                          name="EDeposit:Integration")

