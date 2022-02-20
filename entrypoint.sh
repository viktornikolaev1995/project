#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py flush --no-input
python manage.py migrate
python manage.py loaddata auth_user book_of_recipes_category book_of_recipes_ingredient book_of_recipes_recipe \
book_of_recipes_recipecomments book_of_recipes_stepcookingatrecipe

exec "$@"