@echo off
echo APPLYING MIGRATIONS
venv\Scripts\python.exe manage.py migrate
echo SEEDING DATA
venv\Scripts\python.exe seed_hotel_data.py
echo DONE
