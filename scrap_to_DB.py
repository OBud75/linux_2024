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
