from flask import Flask,render_template,request,redirect,url_for,flash,session
import requests
import backend as re
app=Flask(__name__)
app.secret_key = "fhgztghgdh"
@app.route("/",methods=["POST","GET"])
def home():
    if request.method=="POST":
        pnamee=request.form['pokemon']
        return redirect(url_for("info",pname=pnamee))
    else:
     return render_template("home.html")

@app.route("/pokemon/<pname>")
def info(pname):
    url=f"https://pokeapi.co/api/v2/pokemon/{pname}"
    
    data=requests.get(url)
    if(data.status_code==200):
        response=data.json()

        hight=response.get('height')

        return render_template("info.html",pname=pname,height=hight)
    elif(data.status_code==404):
    
        flash(f"Pokemon not found in database perhapes you meant {re.ai_module(pname)}?","warning")
        return redirect(url_for("home"))
    else:
        flash("poki api down","warning")
        return redirect(url_for("home"))
    


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form['username']
        session['username'] = username  # <-- Saves the user to the session!
        return redirect(url_for("pro", profile=username))
    else:
        return render_template("login.html")
    
@app.route("/profile/<profile>")
def pro(profile):
    return render_template("user.html",usr=profile)

@app.route("/delete/<uname>",methods=["POST"])
def delete_username(uname):
    session.pop('username',None)
    flash(f"{uname} have been logged out ")
    return redirect(url_for("home"))





    

""" @app.route("/<usr>")
def profile(usr):
    return render_template("user.html",usr=usr) """



if __name__=="__main__":
    app.run(debug=True)