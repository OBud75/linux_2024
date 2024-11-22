"""
Bash ou Python pour le script de scrapping
Postgres ou sqlite3 si abstraction de la difficulté lié à la DBB
https://readi.fi/sitemap.xml
-> Récupérer les urls qui commencent par https://readi.fi/asset
  Combien de liens différents ?
-> Aller sur ces urls
-> Mettre en base de données le contenu de:
  - La balise title
  - Le content de la balise meta name="description"

Quels sont les programmes necessaires ? curl? wget?
Commandes utiles ?
libpq-dev postgresql postgresql-contrib / 

Pseudocode
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
"""
from re import search
from requests import get
from sqlite3 import connect, Cursor


def sql(query, params=(), commit=False) -> Cursor:
    global db_cursor
    if commit and not params:
        return db_cursor
    db_cursor.execute(query, params)
    if commit:
        db_cursor.connection.commit()
    return db_cursor

def create_tables() -> None:
    sql(query="DROP TABLE IF EXISTS assets;")
    sql(query="CREATE TABLE assets (title VARCHAR(255), description VARCHAR(255));")

def insert(meta, description) -> None:
    query = "INSERT INTO assets(title, description) VALUES (?, ?);"
    sql(query=query, params=(meta, description), commit=True)

def get_sitemap() -> str:
    return get(url="https://readi.fi/sitemap.xml").text

def get_urls(sitemap: str, section: str) -> list[str]:
    return list(set(url.split(sep="</loc>")[0] for url in
            sitemap.split(sep="<loc>") if f"{section}/" in url))

def get_meta_and_description(page):
    title = search(pattern=r"<title>(.*?)</title>", string=page)
    description = search(pattern=r'<meta name="description" content="(.*?)"/>', string=page)
    return title.group(1) if title else None, description.group(1) if description else None


if __name__ == "__main__":
    db_cursor: Cursor = connect(database="db.sqlite3").cursor()
    create_tables()
    for url in get_urls(sitemap=get_sitemap(), section="asset"):
        insert(*get_meta_and_description(page=get(url=url).text))
    print(f"{sql(query="SELECT COUNT(*) FROM assets;").fetchone()[0]} assets added.")
    db_cursor.connection.close()
