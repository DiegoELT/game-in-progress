# game-in-progress
Description-based game recommendation system for Engineering of AI Intensive Systems Class

## Before you Start
At the moment this project has been fully developed in `Python 3.11.5` and `SQLite 3.41.2`, so it is recommended to use this or a newer version to make it run properly.

In the [following Google Drive](https://drive.google.com/drive/folders/1kr_l00xgUe6k-qdhBndfLHi8Ue32yjJj?usp=sharing) you can find the files for the `.csv` with videogame descriptions parsed used for the database and the Google Model used for text distance comparison. 

You also need to install `NLTK Data`, preferably with the folder in the root of this repository but the default instalation should work as well. 

The initial folder structure, then, should be the following:

```
.
├── game-in-progress/
│   ├── modules
│   ├── static
│   └── templates
├── nltk_data
├── db_file.csv
├── google_model.bin
├── LICENSE
├── README.md
└── requirements.txt
```

## Initializing the Project

(Preferably) create a virtual environment and install the requirements

```
$ pip install -r requirements.txt
```

With Flask installed, and the `.csv` downloaded you can create the SQLite3 instance for the project.

```
$ flask --app game-in-progress init-db 
$ sqlite3 instance/game-in-progress.sqlite
sqlite> .mode csv
sqlite> .import <route_to_basic_db> game
```

## Running the Project

After that you should be able to run the project with:

```
$ flask --app game-in-progress run --debug
```

Find the games that you enjoy!