from flask import Flask, render_template, request, redirect, url_for, flash, session
import backend as re
from datetime import timedelta
from thefuzz import process
from pokidata import pok

app = Flask(__name__)
app.secret_key = "fhgztghgdh" 
app.permanent_session_lifetime = timedelta(days=30)

@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        pnamee = request.form['pokemon'].strip().lower()
        return redirect(url_for("info", pname=pnamee))
    return render_template("home.html")

@app.route("/pokemon/<pname>", methods=['POST', 'GET'])
def info(pname):
    
    signal, pokemon_data = re.get_pokemon_data(pname)
    
    if signal == "green":
        return render_template("info.html", pokemon=pokemon_data)
    
    elif signal == "red":
        idkname, score = process.extractOne(pname, pok)
        flash(f"Pokémon not found. Did you mean <strong>{idkname}</strong>?", "warning")
        return redirect(url_for("home"))
    
    else:
        flash("PokéAPI is currently down or unreachable.", "danger")
        return redirect(url_for("home"))



@app.route("/fav/<pname>", methods=["POST"])
def fav_pokemon(pname):
    session.permanent = True
    if 'fav_pokemon' not in session:
        session['fav_pokemon'] = []
    
    if pname not in session['fav_pokemon']:
        session['fav_pokemon'].append(pname)
        session.modified = True
        flash(f"{pname.capitalize()} added to favorites!", "success")
    else:
        flash(f"{pname.capitalize()} is already in your favorites.")
        
    return redirect(url_for("info", pname=pname))

@app.route("/deletep/<pname>", methods=["POST"])
def delete_fav(pname):
    if 'fav_pokemon' in session:
        session['fav_pokemon'] = [p for p in session['fav_pokemon'] if p != pname]
        session.modified = True
        flash(f"{pname.capitalize()} removed from favorites!", "info")
    return redirect(url_for("info", pname=pname))

if __name__ == "__main__":
    app.run(debug=True)