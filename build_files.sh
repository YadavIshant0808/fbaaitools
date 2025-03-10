echo " BUILD START"
python3.11 -m pip install -r requirements.txt
python3.11 manage.py makemigrations --noinput --clear
python3.11 manage.py migrate --noinput --clear
python3.11 manage.py collectstatic --noinput --clear
echo " BUILD END" You, now committed changes
