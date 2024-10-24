from flask import Flask, render_template, request, redirect
import psycopg2
import os

app = Flask(__name__)

# Connexion à la base de données PostgreSQL sur Heroku
DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL)

@app.route('/')
def index():
    cur = conn.cursor()
    cur.execute("SELECT * FROM clients;")
    rows = cur.fetchall()
    cur.close()
    return render_template('index.html', clients=rows)

@app.route('/add_client', methods=['GET', 'POST'])
def add_client():
    if request.method == 'POST':
        nb_enfants = request.form['nb_enfants']
        categorie_socio = request.form['categorie_socio']
        prix_panier_total = request.form['prix_panier_total']
        identifiant_collecte = request.form['identifiant_collecte']
        
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO clients (nb_enfants, categorie_socioprofessionnelle, prix_panier_total, identifiant_collecte)
            VALUES (%s, %s, %s, %s)
        """, (nb_enfants, categorie_socio, prix_panier_total, identifiant_collecte))
        conn.commit()
        cur.close()
        return redirect('/')
    return render_template('add_client.html')

if __name__ == '__main__':
    app.run(debug=True)

