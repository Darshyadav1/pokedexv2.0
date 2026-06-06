from flask import Flask,render_template,request,redirect,url_for,flash,session
import requests
import backend as re
from datetime import timedelta
app=Flask(__name__)
app.secret_key = "fhgztghgdh"

    

app.permanent_session_lifetime=timedelta(days=30)
@app.route("/",methods=["POST","GET"])
def home():
    if request.method=="POST":
        pnamee=request.form['pokemon']
        return redirect(url_for("info",pname=pnamee))
    else:
     return render_template("home.html")

@app.route("/pokemon/<pname>",methods=['POST','GET'])
def info(pname):
    if request.method=="POST":
        return redirect(url_for("delete_fav",pname=pname))

    else:
        signal, idd, weight, height , img = re.main(pname)
        if(signal=="green"):
            return render_template("info.html",pname=pname,height=height,weight=weight,id=idd,img=img)
        elif(signal=="red"):
            flash(f"Pokemon not found in database perhapes you meant {re.ai_module(pname)}?","warning")
            return redirect(url_for("home"))
        else:
            flash("poki api down","warning")
            return redirect(url_for("home"))
    

    



    


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent=True
        username = request.form['username']
        session['username'] = username  
        return redirect(url_for("home"))
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


@app.route("/fav/<pname>",methods=["POST"])
def fav_pokemon(pname):
    session.permanent=True
    if 'fav_pokemon' not in session:
     session['fav_pokemon']=[]
    if(request.method=="POST"):
        if pname not in session['fav_pokemon']:

            session['fav_pokemon'].append(pname)
            session.modified=True
            flash(f"{pname} is added to your fav")
            return redirect(url_for("info",pname=pname))
        else:
            flash(f"{pname} is already in your fav")
            return redirect(url_for("info",pname=pname))
        

@app.route("/deletep/<pname>", methods=["POST"])
def delete_fav(pname):
    
    if 'fav_pokemon' in session and isinstance(session['fav_pokemon'], list):
        
        
        session['fav_pokemon'] = [p for p in session['fav_pokemon'] if p != pname]
        
        
        session.modified = True
        flash(f"{pname} removed from favorites!","info")
    else:
        flash("No favorites list found.")

    return redirect(url_for("info", pname=pname))


    





    





if __name__=="__main__":
    app.run(debug=True)