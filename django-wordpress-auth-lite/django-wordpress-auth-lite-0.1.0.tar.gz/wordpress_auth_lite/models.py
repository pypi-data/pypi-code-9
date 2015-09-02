import phpserialize

from django.db import models
from django.utils.encoding import force_bytes

from wordpress_auth_lite import WORDPRESS_TABLE_PREFIX


class WpOptions(models.Model):
    option_id = models.BigIntegerField(primary_key=True)
    option_name = models.CharField(max_length=192, unique=True)
    option_value = models.TextField()
    autoload = models.CharField(max_length=60)

    class Meta:
        db_table = WORDPRESS_TABLE_PREFIX + 'options'
        managed = False


class WpUsermeta(models.Model):
    id = models.BigIntegerField(db_column='umeta_id', primary_key=True)
    user = models.ForeignKey('wordpress_auth_lite.WpUsers', db_column='user_id',
        related_name='meta')
    meta_key = models.CharField(max_length=765, blank=True)
    meta_value = models.TextField(blank=True)

    class Meta:
        db_table = WORDPRESS_TABLE_PREFIX + 'usermeta'
        managed = False


class WpUsers(models.Model):
    # Field name made lowercase.
    id = models.BigIntegerField(primary_key=True, db_column='ID')

    login = models.CharField(max_length=180, db_column='user_login')
    password = models.CharField(max_length=192, db_column='user_pass')
    nicename = models.CharField(max_length=150, db_column='user_nicename')
    email = models.CharField(max_length=300, db_column='user_email')
    url = models.CharField(max_length=300, db_column='user_url')
    user_registered = models.DateTimeField(db_column='user_registered')
    user_activation_key = models.CharField(max_length=180,
                                           db_column='user_activation_key')
    user_status = models.IntegerField(db_column='user_status')
    display_name = models.CharField(max_length=750, db_column='display_name')

    class Meta:
        db_table = WORDPRESS_TABLE_PREFIX + 'users'
        managed = False

    def __str__(self):
        return self.login

    def get_session_tokens(self):
        """Retrieve all sessions of the user."""
        opt = self.meta.get(meta_key='session_tokens').meta_value

        return phpserialize.loads(force_bytes(opt), decode_strings=True)
