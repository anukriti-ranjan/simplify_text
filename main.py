from flask import Flask, render_template
from flask import request
import random
import unicodedata
import re
from pathlib import Path
import os
import openai

os.environ["OPENAI_API_KEY"]='<enter your API key here>'
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_response(text_to_simplify):
        response = openai.Completion.create(
                                        model="text-curie-001",
                                        prompt=f"For some complex text after 'Text:', write a simplified version after 'Simplify:'\n\nText: This driver training school has and will maintain for the protection of the contractual rights of the student a performance bond in the principal sum of ten thousand dollars for the students to be written by a company authorized to do business in the state of Georgia.\nSimplify: The driver school has a performance bond (i.e., if you give them your money and they fail to provide the training that they promised you, you could seek to get a refund of your money from the company that issued the performance bond to the driver school).\n--\nText: Without granting any right or license, the Disclosing Party agrees that the foregoing shall not apply with respect to any information after five (5) years following the disclosure thereof or any information that the Receiving Party can document (i) is or becomes (through no improper action or inaction by the Receiving Party or any affiliate, agent, consultant or employee) generally available to the public, or (ii) was in its possession or known by it prior to receipt from the Disclosing Party as evidenced in writing, except to the extent that such information was unlawfully appropriated.\nSimplify: Any information we consider confidential will be kept confidential by OP for the 5 years after acceptor learns it. This doesn't mean that after 5 years acceptor owns the information and can do with it as he pleases. Exceptions to the above include information that becomes available to the public (and acceptor didn't have anything to do with it becoming public) or the acceptor already had that information before learning it from NDA offerer. The acceptor must prove this was the case via a writing of some sort unless the acceptor acquired this knowledge illicitly.\n--\nText: {text_to_simplify}\nSimplify:",
                                        temperature=0.7,
                                        max_tokens=256,
                                        top_p=1,
                                        frequency_penalty=0.35,
                                        presence_penalty=0.35,
                                        stop=["--"]
                                        )
        return response.choices[0].text

app = Flask(__name__)


def clean_text(s):
    # Turn a Unicode string to plain ASCII
    def unicodeToAscii(s1):
        return ''.join(
            c for c in unicodedata.normalize('NFD', s1)
            if unicodedata.category(c) != 'Mn')
    s=" ".join(unicodeToAscii(s.strip()).split())
    if len(s.strip())>250:
        return " ".join(s.strip()[0:250])
    return s

#@app.route('/')
#def index():
#    return render_template('index.html')


@app.route('/', methods=['GET', 'POST'])
def sumbit_text():
    if request.method == 'POST':
        text_to_simplify = request.form.get("text_")
        result= get_response(clean_text(text_to_simplify))
        return render_template('index.html',value=result)
    return render_template('index.html')

if __name__=="__main__":
    port = os.environ.get("PORT",5000)
    app.run(debug=True,host='0.0.0.0',port=port)
