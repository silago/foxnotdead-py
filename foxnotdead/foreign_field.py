from peewee import *

class ForeignKeyField(ForeignKeyField):


    def __init__(self, model, field=None, backref=None, on_delete=None,
                 on_update=None, _deferred=None, rel_model=None, to_field=None,
                 object_id_name=None, related_name=None, *args, **kwargs):
        super().__init__(model, field=field, backref=backref, on_delete=on_delete, on_update=on_update,
                         _deferred=_deferred, rel_model=rel_model, to_field=to_field,
                         object_id_name=object_id_name,related_name=related_name,*args,**kwargs)

        if related_name is not None:
            self.related_name = related_name
        self.__class__ = ForeignKeyField

        #def __init__(self, *args, **kwargs):
        #super(ForeignKeyField, self).__init__(*args, **kwargs)
