from flask import Flask,render_template,request,redirect,url_for,flash
import requests
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
    
        flash("Pokemon not found in database","warning")
        return redirect(url_for("home"))
    else:
        flash("poki api down","warning")
        return redirect(url_for("home"))

if __name__=="__main__":
    app.run(debug=True)