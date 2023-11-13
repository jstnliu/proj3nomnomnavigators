# Generated by Django 4.2.7 on 2023-11-09 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_remove_recipe_dish_types_delete_dish_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Nutrient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=50)),
                ('quantity', models.FloatField()),
                ('unit', models.CharField(max_length=10)),
            ],
        ),
        migrations.RemoveField(
            model_name='nutrition_label',
            name='cholesterol',
        ),
        migrations.RemoveField(
            model_name='nutrition_label',
            name='protein',
        ),
        migrations.RemoveField(
            model_name='nutrition_label',
            name='sodium',
        ),
        migrations.RemoveField(
            model_name='nutrition_label',
            name='total_carbs',
        ),
        migrations.RemoveField(
            model_name='nutrition_label',
            name='total_fats',
        ),
        migrations.AddField(
            model_name='nutrition_label',
            name='recipe_uri',
            field=models.URLField(default='UNKNOWN_RECIPE_URI'),
        ),
        migrations.AddField(
            model_name='nutrition_label',
            name='yield_value',
            field=models.FloatField(default=1.0),
        ),
        migrations.AlterField(
            model_name='nutrition_label',
            name='calories',
            field=models.FloatField(),
        ),
        migrations.AddField(
            model_name='nutrition_label',
            name='nutrients',
            field=models.ManyToManyField(to='main_app.nutrient'),
        ),
    ]