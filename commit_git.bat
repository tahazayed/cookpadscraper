git add *
git commit -m "%DATE:~-4%-%DATE:~4,2%-%DATE:~7,2%"
git push origin master
git push heroku master

@echo delpoy heroku
rem git push heroku master

rem pause