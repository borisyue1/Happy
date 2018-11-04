Quickstart
=========

Make sure `pipenv` is installed, then run `pipenv install` to prepare the dependencies.
```
pipenv install
```

Requirements:
- Flask
- Microsoft Cognitive_Faces API
- FFMPEG (brew install ffmpeg)


Local Dev
========
```
python dev.py
```

Production
=========
```
python run.py
```

About Pipenv
===========

Sync between pipenv with requirements for old school.
```
pipenv lock --requirements > requirements.txt
```
