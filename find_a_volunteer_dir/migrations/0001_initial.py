# Generated by Django 4.0 on 2021-12-28 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='accepted_organisations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accepted', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'accepted_organisations',
            },
        ),
        migrations.CreateModel(
            name='accepted_volunteers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accepted', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'accepted_volunteers',
            },
        ),
        migrations.CreateModel(
            name='matched_organisations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matched', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'matched_organisations',
            },
        ),
        migrations.CreateModel(
            name='matched_volunteers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matched', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'matched_volunteers',
            },
        ),
        migrations.CreateModel(
            name='organisation_profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('available_activity_1', models.CharField(choices=[('Admin', 'Admin'), ('Animal care', 'Animal care'), ('Babysitting', 'Babysitting'), ('Cooking', 'Cooking'), ('Cleaning', 'Cleaning'), ('Education', 'Education'), ('Elder care help', 'Elder care help'), ('Fundraising', 'Fundraising'), ('Music', 'Music')], max_length=40)),
                ('available_activity_2', models.CharField(blank=True, choices=[('Admin', 'Admin'), ('Animal care', 'Animal care'), ('Babysitting', 'Babysitting'), ('Cooking', 'Cooking'), ('Cleaning', 'Cleaning'), ('Education', 'Education'), ('Elder care help', 'Elder care help'), ('Fundraising', 'Fundraising'), ('Music', 'Music')], max_length=40)),
                ('available_activity_3', models.CharField(blank=True, choices=[('Admin', 'Admin'), ('Animal care', 'Animal care'), ('Babysitting', 'Babysitting'), ('Cooking', 'Cooking'), ('Cleaning', 'Cleaning'), ('Education', 'Education'), ('Elder care help', 'Elder care help'), ('Fundraising', 'Fundraising'), ('Music', 'Music')], max_length=40)),
                ('desired_age_lower_bound', models.IntegerField()),
                ('desired_age_upper_bound', models.IntegerField()),
                ('contact_details', models.CharField(max_length=70)),
                ('postcode', models.CharField(max_length=10)),
                ('self_description', models.CharField(max_length=300)),
                ('name', models.CharField(max_length=40)),
                ('monday_availability', models.CharField(choices=[('Morning', 'Morning'), ('Afternoon', 'Afternoon'), ('Evening', 'Evening'), ('All day', 'All day'), ('None', 'None')], max_length=20)),
                ('tuesday_availability', models.CharField(choices=[('Morning', 'Morning'), ('Afternoon', 'Afternoon'), ('Evening', 'Evening'), ('All day', 'All day'), ('None', 'None')], max_length=20)),
                ('wednesday_availability', models.CharField(choices=[('Morning', 'Morning'), ('Afternoon', 'Afternoon'), ('Evening', 'Evening'), ('All day', 'All day'), ('None', 'None')], max_length=20)),
                ('thursday_availability', models.CharField(choices=[('Morning', 'Morning'), ('Afternoon', 'Afternoon'), ('Evening', 'Evening'), ('All day', 'All day'), ('None', 'None')], max_length=20)),
                ('friday_availability', models.CharField(choices=[('Morning', 'Morning'), ('Afternoon', 'Afternoon'), ('Evening', 'Evening'), ('All day', 'All day'), ('None', 'None')], max_length=20)),
                ('saturday_availability', models.CharField(choices=[('Morning', 'Morning'), ('Afternoon', 'Afternoon'), ('Evening', 'Evening'), ('All day', 'All day'), ('None', 'None')], max_length=20)),
                ('sunday_availability', models.CharField(choices=[('Morning', 'Morning'), ('Afternoon', 'Afternoon'), ('Evening', 'Evening'), ('All day', 'All day'), ('None', 'None')], max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='volunteer_profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_preferred_activity', models.CharField(choices=[('Admin', 'Admin'), ('Animal care', 'Animal care'), ('Babysitting', 'Babysitting'), ('Cooking', 'Cooking'), ('Cleaning', 'Cleaning'), ('Education', 'Education'), ('Elder care help', 'Elder care help'), ('Fundraising', 'Fundraising'), ('Music', 'Music')], max_length=40)),
                ('second_preferred_activity', models.CharField(blank=True, choices=[('Admin', 'Admin'), ('Animal care', 'Animal care'), ('Babysitting', 'Babysitting'), ('Cooking', 'Cooking'), ('Cleaning', 'Cleaning'), ('Education', 'Education'), ('Elder care help', 'Elder care help'), ('Fundraising', 'Fundraising'), ('Music', 'Music')], max_length=40)),
                ('third_preferred_activity', models.CharField(blank=True, choices=[('Admin', 'Admin'), ('Animal care', 'Animal care'), ('Babysitting', 'Babysitting'), ('Cooking', 'Cooking'), ('Cleaning', 'Cleaning'), ('Education', 'Education'), ('Elder care help', 'Elder care help'), ('Fundraising', 'Fundraising'), ('Music', 'Music')], max_length=40)),
                ('contact_details', models.CharField(max_length=70)),
                ('self_description', models.CharField(max_length=300)),
                ('age', models.IntegerField()),
                ('monday_availability', models.CharField(choices=[('Morning', 'Morning'), ('Afternoon', 'Afternoon'), ('Evening', 'Evening'), ('All day', 'All day'), ('None', 'None')], max_length=20)),
                ('tuesday_availability', models.CharField(choices=[('Morning', 'Morning'), ('Afternoon', 'Afternoon'), ('Evening', 'Evening'), ('All day', 'All day'), ('None', 'None')], max_length=20)),
                ('wednesday_availability', models.CharField(choices=[('Morning', 'Morning'), ('Afternoon', 'Afternoon'), ('Evening', 'Evening'), ('All day', 'All day'), ('None', 'None')], max_length=20)),
                ('thursday_availability', models.CharField(choices=[('Morning', 'Morning'), ('Afternoon', 'Afternoon'), ('Evening', 'Evening'), ('All day', 'All day'), ('None', 'None')], max_length=20)),
                ('friday_availability', models.CharField(choices=[('Morning', 'Morning'), ('Afternoon', 'Afternoon'), ('Evening', 'Evening'), ('All day', 'All day'), ('None', 'None')], max_length=20)),
                ('saturday_availability', models.CharField(choices=[('Morning', 'Morning'), ('Afternoon', 'Afternoon'), ('Evening', 'Evening'), ('All day', 'All day'), ('None', 'None')], max_length=20)),
                ('sunday_availability', models.CharField(choices=[('Morning', 'Morning'), ('Afternoon', 'Afternoon'), ('Evening', 'Evening'), ('All day', 'All day'), ('None', 'None')], max_length=20)),
                ('name', models.CharField(max_length=30)),
                ('postcode', models.CharField(blank=True, max_length=10)),
            ],
        ),
    ]
