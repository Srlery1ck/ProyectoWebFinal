# Generado automáticamente por Django 5.2.7 el 2025-10-13 04:48
#
# Estas migraciones fueron creadas por Django. No edites este archivo
# manualmente salvo que sepas lo que haces. Para modificar modelos,
# cambia `shop/models.py` y ejecuta `python manage.py makemigrations`.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(max_length=60, verbose_name='Marca')),
                ('model', models.CharField(blank=True, max_length=80, verbose_name='Modelo')),
                ('year', models.PositiveIntegerField(verbose_name='Año')),
                ('transmission', models.CharField(choices=[('AT', 'Automática'), ('MT', 'Manual')], max_length=2, verbose_name='Transmisión')),
                ('body_type', models.CharField(choices=[('SD', 'Sedán'), ('CN', 'Camineta')], default='SD', max_length=2, verbose_name='Tipo')),
                ('color', models.CharField(max_length=40, verbose_name='Color')),
                ('mileage_km', models.PositiveIntegerField(default=0, verbose_name='Kilometraje (km)')),
                ('price_cop', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Precio (COP)')),
                ('image', models.ImageField(blank=True, null=True, upload_to='cars/', verbose_name='Imagen del carro')),
                ('is_active', models.BooleanField(default=True, verbose_name='Publicado')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Carro',
                'verbose_name_plural': 'Carros',
                'ordering': ['-created_at'],
            },
        ),
        migrations.RemoveField(
            model_name='post',
            name='category',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='author',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='post',
        ),
        migrations.RemoveField(
            model_name='post',
            name='author',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
        migrations.DeleteModel(
            name='Post',
        ),
    ]
