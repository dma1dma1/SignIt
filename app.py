import os

import openai
from flask import Flask, redirect, render_template, request, url_for, session
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm, CSRFProtect
from wtforms.fields import TextAreaField, SubmitField
from werkzeug.datastructures import MultiDict

app = Flask(__name__)
bootstrap = Bootstrap5(app)
csrf = CSRFProtect(app)

app.secret_key = 'CS177'
openai.api_key = os.getenv("OPENAI_API_KEY")

class BigForm(FlaskForm):
    Text = TextAreaField(render_kw={"rows": 10})
    Simplified = TextAreaField(render_kw={"rows": 10})
    Simplify = SubmitField(render_kw={"class": "dark_button"})

@app.route("/", methods=("GET", "POST"))
def home():
    form = BigForm()
    if request.method == "GET":
        print("HERE")
        formdata = session.get("formdata", None)
        if formdata:
            form = BigForm(MultiDict(formdata))
            form.validate()
            session.pop('formdata')
        return render_template("base.html", form=form)

    if request.method == "POST" and form.validate_on_submit():
        text = request.form["Text"]
        if text:

            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=simplify(text=text),
                temperature=0.7,
                max_tokens=128
            )
            session['formdata'] = MultiDict({
                'csrf_token': request.form['csrf_token'],
                'Text': text,
                'Simplify': 'Simplify',
                'Simplified': response.choices[0].text[1:] #1: to get rid of /n
            })
            print(response)
        return redirect(url_for("home"))

def simplify(text):
    return """
    Simplify the following text: {}
    """.format(text)
