from django.conf import settings
from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist


SYNCHRONIZED_MODEL_FIELDS = ("uuid", "is_deleted")


class I18NModelField(serializers.CharField):
    def get_attribute(self, instance):
        request = self.context["request"]
        relation = getattr(instance, self.source.split(".")[0])
        try:
            i18n_instance = relation.get(language=request.LANGUAGE_CODE, base_model=instance)
        except ObjectDoesNotExist:
            try:
                i18n_instance = relation.get(language=settings.LANGUAGES[0][0], base_model=instance)
            except ObjectDoesNotExist:
                i18n_instance = None
        return i18n_instance

    def to_representation(self, value):
        return getattr(value, self.field_name) if value is not None else None

    def to_internal_value(self, data):
        return data


class I18NModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        if hasattr(self, "Meta") and hasattr(self.Meta, "i18n_fields"):
            for i18n_field in self.Meta.i18n_fields:
                self.fields[i18n_field.split(".")[1]] = I18NModelField(source=i18n_field)
        super().__init__(*args, **kwargs)

    @property
    def i18n_fields(self):
        i18n_fields = {}
        for field_name, field in self.fields.items():
            if issubclass(type(field), I18NModelField):
                i18n_fields[field_name] = field
        return i18n_fields

    def extract_i18n_content(self, validated_data):
        content = dict()
        for i18n_field in self.i18n_fields.values():
            source = i18n_field.source.split(".")[0]
            if source not in content and source in validated_data:
                content[source] = validated_data.pop(source)
        return content

    def update_i18n_content(self, instance, i18n_data):
        request = self.context["request"]
        for attribute_name, data in i18n_data.items():
            related_field = instance._meta.get_field_by_name(attribute_name)[0]
            try:
                i18n_instance = related_field.related_model.objects.get(**{"language": request.LANGUAGE_CODE,
                                                                           related_field.field.name: instance})
            except ObjectDoesNotExist:
                i18n_instance = related_field.related_model(**{"language": request.LANGUAGE_CODE,
                                                               related_field.field.name: instance})
            for attr, value in data.items():
                setattr(i18n_instance, attr, value)
            i18n_instance.save()

    def create(self, validated_data):
        i18n_attributes = self.extract_i18n_content(validated_data)
        instance = super(I18NModelSerializer, self).create(validated_data)
        self.update_i18n_content(instance, i18n_attributes)
        return instance

    def update(self, instance, validated_data):
        i18n_attributes = self.extract_i18n_content(validated_data)
        super(I18NModelSerializer, self).update(instance, validated_data)
        self.update_i18n_content(instance, i18n_attributes)
        return instance


def synchronized(cls):
    meta = getattr(cls, 'Meta', None)
    if meta is None: 
        meta = type('Meta', (), {})
    fields = getattr(meta, 'fields', None)
    if fields is None:
        fields = list()
    else:
        fields = list(fields)
    fields += SYNCHRONIZED_MODEL_FIELDS
    setattr(meta, 'fields', fields)
    setattr(cls, 'Meta', meta)
    return cls
