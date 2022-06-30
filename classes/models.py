import config
from peewee import *
from datetime import datetime


class BaseModel(Model):
    class Meta:
        database = SqliteDatabase(config.DB_FILE_NAME)


class TableCommand(BaseModel):
    id = PrimaryKeyField(null=False)
    id_user = CharField(max_length=50)
    command = CharField(max_length=20)
    city = CharField()
    count = IntegerField()
    day = DateField()
    day_count = IntegerField()
    foto = BooleanField()
    foto_count = IntegerField()
    price_start = IntegerField()
    price_stop = IntegerField()
    distance_start = IntegerField()
    distance_stop = IntegerField()

    created_at = DateTimeField(default=datetime.now().replace(microsecond=0))

    class Meta:
        order_by = 'id'


class TableHotel(BaseModel):
    id = PrimaryKeyField(null=False)
    command = ForeignKeyField(TableCommand, related_name='fk_cat_prod', to_field='id', on_delete='cascade',
                              on_update='cascade')
    name = CharField()
    star_rating = CharField()
    address = CharField()
    price = IntegerField()
    centr_distance = CharField()
    label_distance = CharField()

    class Meta:
        order_by = ('update_at', id)


class TableState(BaseModel):
    id = IntegerField(null=False)
    state = CharField()

    @classmethod
    def get_state(cls, id_user: int) -> str:
        buf = cls.select().where(TableState.id == id_user)
        if len(buf) != 0:
            return buf[0].state

