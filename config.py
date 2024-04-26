from rich import print as printc
from rich.console import Console
from dbconfig import *
import sys

console = Console()
def checkConfig():
	db = dbconfig()
	cursor = db.cursor()
	query = "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA  WHERE SCHEMA_NAME = 'IntelliDocs'"
	cursor.execute(query)
	results = cursor.fetchall()
	db.close()
	if len(results)!=0:
		return True
	return False

def config():
    db = dbconfig()
    cur = db.cursor()
    printc("[green][+][/green] Enter the Owner name")
    owner = input()
    printc("[green][+][/green] Enter the Github Access Token")
    github_access_token = input()
    printc("[green][+][/green] Enter the repo name ")
    repo = input()

    query = "INSERT INTO IntelliDocs.secrets(owner,github_access_token,repo) VALUES (%s,%s,%s)"
    val=(owner,github_access_token,repo)
    cur.execute(query,val)
    db.commit()

    printc("[green][+][/green] Added to the database")
    printc("[green][+]Configuration done[/green]")
    db.close()

def db__init__():
    try:
        if not checkConfig():
            db = dbconfig()  # Assuming dbconfig() establishes the database connection
            cur = db.cursor()
            try:
                cur.execute("CREATE DATABASE IntelliDocs")
            except Exception as e:
                printc("[red][!] An error occured while creating a database")
                console.print_exception(show_locals = True)
                sys.exit(0)
            printc("[green][+][/green] Database 'pm created")

            query = "CREATE TABLE IntelliDocs.secrets(owner TEXT NOT NULL, github_access_token TEXT NOT NULL, repo TEXT NOT NULL)"
            res = cur.execute(query)
            printc("[green][+][/green]Tables secret created")

            query = "CREATE TABLE IntelliDocs.entries(filepath TEXT NOT NULL, code TEXT NOT NULL,documenatation TEXT NOT NULL )" 
            res = cur.execute(query)
            printc('[green][+][/green] Tables entries created')
            db.commit()
            db.close()

            
            printc('[green]Database initialized successfully[/green]')
        else:
            printc('[yellow]Database already initialized[/yellow]')

    except Exception as e:
        printc(f'[red]Error initializing database: {e}[/red]')

def delete():
    printc("[green][-][/green] Deleting config")

    if not checkConfig():
        printc("[yellow][-][/yellow] No configuration exists to delete!")
        return

    success = True
    try:
        db = dbconfig()
        cursor = db.cursor()
        query = "DROP DATABASE intellidocs"
        cursor.execute(query)
        db.commit()
        db.close()
    except Exception as e:
        print(f"Error deleting config: {e}")
        success = False
    if success:
        printc("[green][+] Config deleted![/green]")
    sys.exit()

