import cgi
import mysql.connector
from mysql.connector import errorcode

print("Content-type: text/html; charset=utf-8\n")

header = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="ali.b.css">
</head>
<body>

  <div style="width:100%;min-height: 800px;text-align: center;background-color:rgb(191, 216, 81);margin:0 auto;">
        <header style="font-weight: bold;font-size:xx-large;text-align: center;padding: 20px;margin-bottom: 40px;"> 
                    Un Minichat
        </header>

        <form action="/index.py" method="post" style="width: 40%;margin: 0 auto;text-align: justify;">
            <label for="pseudo">pseudo :</label>
            <input type="text" name="pseudo" id="pseudo"><br><br>

            <label for="mesaage">Message :</label>
            <textarea id="view" name="msg" rows="4" cols="50"> </textarea>
            <br><br>
            <input id="button" type="submit" value="Envoyer" style="width:100px;height: 3Opx;display: block;margin: 0 auto;">
            <br><br>
        </form>

"""
footer = "</div></body></html>"


# Connection a la base de donnee
try:
    conn = mysql.connector.connect(
        host="localhost", user="root", password="admin", database="MYDATABASE", port=3306)
    cursor = conn.cursor()
except mysql.connector.errors.ProgrammingError as e1:
    print("Error de Connection a La Base de Donnes")


def DisplayGenerateContextHTML(header, body, footer):
    html = header + body + footer
    return html


def AfficheMessages(connx):
    connx.execute(
        """ SELECT * FROM Message order by id desc LIMIT 10
        """)
    rows = connx.fetchall()  # Execute Select
    styledev = """height:max-content;width:60%;background-color: aliceblue;color: black;text-align: left;margin: 0 auto;margin-top: 30px;padding: 10px;"""
    items = f"<div style=\"{styledev}\">"
    for row in rows:         # Parcour Les Resaulta
        items = items + f"<strong> {row[1]} <strong> :{row[2]}" + "<br><br>"
    items = items + "</div>"

    return items


try:
    # Creating a database
    cursor.execute("CREATE database IF NOT EXISTS MYDATABASE")
    # Creation de Table
    cursor.execute(
        "CREATE TABLE  IF NOT EXISTS Message(id INT AUTO_INCREMENT PRIMARY KEY,pseudo varchar(50) NOT NULL,msg varchar(200) NOT NULL)")
except mysql.connector.IntegrityError as e:
    print("Errror de Creation de DataBase")
except mysql.connector.errors as e2:
    print("Error de Creaton de la Base de Donnes")


html = DisplayGenerateContextHTML(header, AfficheMessages(cursor), footer)
# Pour Reciper les Donnes
form = cgi.FieldStorage()
# Reciper les donnes est verife esq c pas null
if form.getvalue("pseudo") != None and form.getvalue("msg") != None:
    getfromform = (form.getvalue("pseudo"), form.getvalue("msg"))
    # L insertion  dans la table de la base de donnee
    cursor.execute(
        """INSERT INTO MYDATABASE.Message (pseudo, msg) VALUES(%s, %s)""", getfromform)
    conn.commit()  # Enrigistre les changement
    # Appel au Fonctoion pour l'affichage des Nouvelle Message
    html = DisplayGenerateContextHTML(header, AfficheMessages(cursor), footer)
print(html)

conn.close()  # shutdown
