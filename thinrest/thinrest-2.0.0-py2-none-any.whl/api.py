from tastypie.authorization import Authorization
from tastypie.resources import NamespacedModelResource

from .models import Employee
from .models import SystemSetting

class EmployeeResource(NamespacedModelResource):
    '''
    API for model Employee
    '''
    class Meta:
        queryset = Employee.objects.all()
        allowed_methods = ['get', 'post', 'delete']
        resource_name = 'employee'
        collection_name = 'employee_list'
        always_return_data = True
        include_resource_uri = False
        authorization = Authorization()

class SettingResource(NamespacedModelResource):
    '''
    API for model System Setting.

    "name" column is used as key for this API.
    As model is having key-value type schema
    '''
    class Meta:
        queryset = SystemSetting.objects.all()
        allowed_methods = ['get', 'post', 'delete']
        resource_name = 'setting'
        collection_name = 'setting_list'
        excludes = ['id']
        always_return_data = True
        include_resource_uri = False
        authorization = Authorization()

    def obj_get(self, bundle, **kwargs):
        #replacing the pk with name column in the request
        query_param = kwargs['pk']
        del kwargs['pk']
        kwargs['name'] = query_param

        return super(SettingResource, self).obj_get(bundle, **kwargs)

    def obj_create(self, bundle, **kwargs):
        kwargs["name"] = bundle.data["name"]

        #If record exists with passed name then update else create
        try:
            bundle.obj = self.obj_get(bundle=bundle, **kwargs)
            bundle = super(SettingResource,self).obj_update(bundle,**kwargs)
        except:
            bundle = super(SettingResource,self).obj_create(bundle,**kwargs)
        return bundle
