from zope.formlib import form
from zope import schema
from zope.interface import implements
from zope.component import getMultiAdapter
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from raptus.mailchimp import MessageFactory as _
from raptus.mailchimp import interfaces


def available_list(context):
    lists = interfaces.IConnector(context).getLists()
    return SimpleVocabulary([SimpleTerm(value=SimpleTerm(value=li['id'], title=li['name']), token=li['id'], title=li['name']) for li in lists])

class IMailChimpPortlet(IPortletDataProvider):
    """A Mailchimp portlet"""

    name = schema.TextLine(
    title=_(u'Title'),
    description=_(u'The title of the portlet'))
    
    available_list = schema.List(
    title=_(u'Available Lists'),
    description=_(u'Select available lists as subscribe in'),
    required=True,
    min_length=1,
    value_type=schema.Choice(source='raptus.mailchimp.available_list'))

class Assignment(base.Assignment):
    """Portlet assignment"""
    
    implements(IMailChimpPortlet, interfaces.IProperties)
    
    def __init__(self, name=u'', available_list=[]):
        self.name = name
        self.available_list = available_list

    @property
    def title(self):
        return _(u"MailChimp")
    
    def getAvailableList(self):
        return SimpleVocabulary(self.available_list)

class Renderer(base.Renderer):
    """Portlet renderer"""
    
    render = ViewPageTemplateFile('portlet.pt')

    def form(self):
        return getMultiAdapter((self.data, self.request), name='raptus.mailchimp.subscriberForm')()

    @property
    def name(self):
        return self.data.name or _(u"Subscribe for newsletter")

    @property
    def available(self):
        return True

class AddForm(base.AddForm):
    """Portlet add form"""
    form_fields = form.Fields(IMailChimpPortlet)
    def create(self, data):
        return Assignment(**data)

class EditForm(base.EditForm):
    """Portlet edit form"""
    form_fields = form.Fields(IMailChimpPortlet)