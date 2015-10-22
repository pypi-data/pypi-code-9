# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import sorl.thumbnail.fields
import model_utils.fields
import froala_editor.fields
import luhublog.models.entry
import django.utils.timezone
from django.conf import settings
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('name', models.CharField(default=b'', max_length=200, verbose_name=b'Nombre / seud\xc3\xb3nimo del autor', blank=True)),
                ('headline', models.CharField(default=b'', max_length=255, verbose_name=b'Corta descripci\xc3\xb3n', blank=True)),
                ('twitter', models.CharField(default=b'', help_text=b'@EsLuhu', max_length=50, verbose_name=b'Twitter', blank=True)),
                ('facebook_page_url', models.URLField(verbose_name=b'URL Perfil Facebook', blank=True)),
                ('google_plus_url', models.URLField(verbose_name=b'URL Perfil Google Plus', blank=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='is active')),
                ('user', models.OneToOneField(related_name='weblog_author', verbose_name=b'Perfil de usuario', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created'],
                'verbose_name': 'Autor',
                'verbose_name_plural': 'Autores',
            },
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('title', models.CharField(max_length=60, verbose_name=b'Nombre del blog')),
                ('tag_line', models.CharField(max_length=140, verbose_name=b'Descripci\xc3\xb3n del blog')),
                ('entries_per_page', models.IntegerField(default=10, verbose_name=b'Entradas por pagina')),
                ('recents', models.IntegerField(default=5, verbose_name=b'Numero de entradas recientes a mostrar')),
                ('site', models.OneToOneField(verbose_name=b'Site', to='sites.Site')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BlogSocialMedia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('facebook', models.URLField(verbose_name=b'Facebook URL', blank=True)),
                ('twitter', models.URLField(verbose_name=b'Twitter URL', blank=True)),
                ('google_plus', models.URLField(verbose_name=b'Google plus URL', blank=True)),
                ('instagram', models.URLField(verbose_name=b'Instagram URL', blank=True)),
                ('linkedin', models.URLField(verbose_name=b'Linkedin URL', blank=True)),
                ('youtube', models.URLField(verbose_name=b'YouTube URL', blank=True)),
                ('pinterest', models.URLField(verbose_name=b'Pinterest URL', blank=True)),
                ('blog', models.OneToOneField(related_name='social_media', verbose_name=b'Blog', to='luhublog.Blog')),
            ],
            options={
                'verbose_name': 'Redes sociales de los blogs',
            },
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('title', models.CharField(max_length=100, verbose_name=b'title')),
                ('slug', models.SlugField(help_text=b"Used to build the entry's URL.", unique=True, verbose_name=b'slug')),
                ('lead_entry', models.CharField(max_length=255, verbose_name=b'Encabezado', blank=True)),
                ('image_header', sorl.thumbnail.fields.ImageField(upload_to=luhublog.models.entry.rename_filename, null=True, verbose_name=b'Imagen de encabezado', blank=True)),
                ('image_caption', sorl.thumbnail.fields.ImageField(upload_to=luhublog.models.entry.rename_filename, null=True, verbose_name=b'Imagen de la entrada', blank=True)),
                ('content', froala_editor.fields.FroalaField(verbose_name=b'Cuerpo de la entrada')),
                ('status', model_utils.fields.StatusField(default=b'DRAFT', max_length=100, no_check_for_status=True, choices=[(b'DRAFT', b'DRAFT'), (b'HIDDEN', b'HIDDEN'), (b'PUBLISHED', b'PUBLISHED')])),
                ('start_publication', models.DateTimeField(db_index=True, null=True, verbose_name=b'Fecha de publicaci\xc3\xb3n', blank=True)),
                ('seo_title', models.CharField(default=b'', help_text=b'Google typically displays the first 50-60 characters of a title tag', max_length=60, verbose_name=b'Meta Title', blank=True)),
                ('seo_description', models.CharField(default=b'', help_text=b'The description should optimally be between 10-155 characters', max_length=155, verbose_name=b'Meta Description', blank=True)),
                ('seo_keywords', models.CharField(default=b'', help_text=b'Opcional', max_length=400, verbose_name=b'Meta Keywords', blank=True)),
                ('author', models.ForeignKey(related_name='entries', verbose_name=b'Autor de la entrada', to='luhublog.Author')),
                ('blog', models.ForeignKey(blank=True, editable=False, to='luhublog.Blog', verbose_name=b'Site')),
            ],
            options={
                'ordering': ['-created'],
                'get_latest_by': '-start_publication',
                'verbose_name': 'Entrada',
                'verbose_name_plural': 'Entradas',
            },
        ),
        migrations.CreateModel(
            name='EntryCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('name', models.CharField(max_length=60, verbose_name=b'Nombre')),
                ('slug', models.SlugField(verbose_name=b'ULR Slug')),
                ('description', models.CharField(max_length=255, verbose_name=b'Descripci\xc3\xb3n', blank=True)),
                ('image_cover', sorl.thumbnail.fields.ImageField(upload_to=luhublog.models.entry.rename_filename, null=True, verbose_name=b'Imagen de portada', blank=True)),
                ('blog', models.ForeignKey(blank=True, editable=False, to='luhublog.Blog', verbose_name=b'Site')),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags')),
            ],
            options={
                'verbose_name': 'Categor\xeda',
                'verbose_name_plural': 'Categor\xedas',
            },
        ),
        migrations.CreateModel(
            name='OpenGraph',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('og_type', models.CharField(default=b'blog', max_length=255, verbose_name='Resource type', choices=[(b'article', 'Article'), (b'website', 'Website'), (b'blog', 'Blog'), (b'book', 'Book'), (b'game', 'Game'), (b'movie', 'Movie'), (b'food', 'Food'), (b'city', 'City'), (b'country', 'Country'), (b'actor', 'Actor'), (b'author', 'Author'), (b'politician', 'Politician'), (b'company', 'Company'), (b'hotel', 'Hotel'), (b'restaurant', 'Restaurant')])),
                ('og_title', models.CharField(default=b'', help_text=b'titulo', max_length=255, verbose_name='Open Graph Title', blank=True)),
                ('og_description', models.CharField(default=b'', help_text=b'Facebook can display up to 300 characters, but I suggest treating anything above 200 as something extra.', max_length=300, verbose_name='Open Graph Description', blank=True)),
                ('og_app_id', models.CharField(default=b'', max_length=255, verbose_name='Facebook App ID', blank=True)),
                ('og_image', sorl.thumbnail.fields.ImageField(help_text=b'Imagen de 1200px por 630px', upload_to=b'seo/opengraph/', verbose_name=b'twitter:site')),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': 'Social Metadata',
            },
        ),
        migrations.CreateModel(
            name='TwitterCard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('site', models.CharField(help_text=b'@empresa', max_length=30, verbose_name=b'twitter:site')),
                ('creator', models.CharField(help_text=b'@autor', max_length=30, verbose_name=b'twitter:creator')),
                ('title', models.CharField(help_text=b'M\xc3\xa1ximo 70 caracteres', max_length=70, verbose_name=b'twitter:title')),
                ('description', models.CharField(help_text=b'M\xc3\xa1ximo 200 caracteres', max_length=200, verbose_name=b'twitter:description')),
                ('image', sorl.thumbnail.fields.ImageField(help_text=b'Imagen de 280px por 150px', upload_to=b'seo/twitter_cards/', verbose_name=b'twitter:site')),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': 'Twitter Card',
            },
        ),
        migrations.AddField(
            model_name='entry',
            name='category',
            field=models.ForeignKey(verbose_name=b'Categor\xc3\xada', blank=True, to='luhublog.EntryCategory', null=True),
        ),
        migrations.AddField(
            model_name='entry',
            name='related',
            field=models.ManyToManyField(related_name='_related_+', verbose_name='related entries', to='luhublog.Entry', blank=True),
        ),
        migrations.AddField(
            model_name='entry',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags'),
        ),
        migrations.AlterIndexTogether(
            name='entry',
            index_together=set([('slug', 'created'), ('status', 'created', 'start_publication')]),
        ),
    ]
