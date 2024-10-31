# linux_2024

## Bash ou Python pour le script de scrapping
## Postgres ou sqlite3 si abstraction de la difficulté lié à la DBB
## https://readi.fi/sitemap.xml
-> Récupérer les urls qui commencent par https://readi.fi/asset
  Combien de liens différents ?
-> Aller sur ces urls
-> Mettre en base de données le contenu de:
  - La balise title
  - Le content de la balise meta name="description"

Quels sont les programmes necessaires ? curl? wget?
Commandes utiles ?
libpq-dev postgresql postgresql-contrib / 


## Pseudocode
fichier .sql qui insert ligne par ligne (permet de tester séparément le SQL)
Dans un fichier .py ou .sh:

	- Requete http GET sur readi.fi/sitemap.xml
 
	- Filtrer les urls qui commencent par /asset
 
	- Mettre le tout dans un fichier temporaire ou dans une variable du script

 	- Faire dans une loop une autre requete GET sur le fichier / variable
		- Isoler les balises title et meta: description
		- Enlever les balises (on veut le contenu sans les balises)
		- Appeler le fichier .sql avec en arguments les valeurs récupérées


> https://www.scrapingbee.com/blog/web-scraping-with-linux-and-bash/

> https://www.postgresql.org/docs/current/libpq-envars.html

> https://stackoverflow.com/questions/9736085/run-a-postgresql-sql-file-using-command-line-arguments
