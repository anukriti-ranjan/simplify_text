import numpy as np
import os
import json
#from transformers import AutoTokenizer, AutoModelForSequenceClassification
import streamlit as st
import cohere
import unicodedata
import string
import re
from st_btn_select import st_btn_select


API_KEY = st.secrets["cohere_API_key"]
co = cohere.Client(API_KEY)

def clean_text(s):
    # Turn a Unicode string to plain ASCII, thanks to
    # https://pytorch.org/tutorials/intermediate/seq2seq_translation_tutorial.html
    def unicodeToAscii(s1):
        return ''.join(
            c for c in unicodedata.normalize('NFD', s1)
            if unicodedata.category(c) != 'Mn')

   # Trim, and remove non-letter characters

    pattern = r'\[.*?\]'
    s= re.sub(pattern, '', s)
 
    s = unicodeToAscii(s.strip())
    s = re.sub(r"([.!?])", r" \1", s)
    s = re.sub(r"[^a-zA-Z.!?]+", r" ", s)
    if len(s.split())>250:
        s=" ".join(s.split()[0:250])
    return s

classify_dict={0:"Elementary",1:"Intermediate",2:"Advanced"}

st.header('SimpliFY')
st.subheader("Check the level of complexity of your text")
st.write("or")
st.subheader("Get a simplified version of your complicated text")

text = st.text_area('Text to analyze','''
        enter your text here
        ''')

selection = st_btn_select(('IdleState','Classify', 'Simplify'),index=0)

if f"{selection}"=='Classify':
    classification = co.classify(
                            model='64c82c5f-061d-46a7-9b32-44dee36ef3db-ft',
                            taskDescription='',
                            outputIndicator='',
                            inputs=[clean_text(text)]
                            ).classifications[0].prediction

    to_write=classify_dict[int(classification)]
    st.write(f"Result of Classification")
    st.write(f"{to_write}")

if f"{selection}"=='Simplify':
#Text: Androcentrism is the practice, conscious or otherwise, of placing a masculine point of view at the center of one\'s world view, culture, and history, thereby culturally marginalizing femininity. \nSimplify: Androcentrism is the belief that males are superior to females, or that male values are more important than female values. This can manifest in many ways, such as through sexist attitudes or institutional policies that favor men, rendering women as inferior.\n\n   
        response = co.generate(
                            model='xlarge',
                            prompt=f'Text: So corrosive are the sexual politics of refugees in Turkey that a false rumor attributed the killing to the Turk’s demand for sex with the Syrian’s wife in return for rent.\nSimplify: A Syrian killed a Turk. Lots of people, probably in the Syrian refugee community, think that the reason is that the Turk demanded to have sex with the Syrian\'s wife. The destructive sexual politics of refugees in Turkey is what allows this false rumor to be believed.\n\nText: This driver training school has and will maintain for the protection of the contractual rights of the student a performance bond in the principal sum of ten thousand dollars for the students to be written by a company authorized to do business in the state of Georgia.\nSimplify: The driver school has a performance bond (i.e., if you give them your money and they fail to provide the training that they promised you, you could seek to get a refund of your money from the company that issued the performance bond to the driver school).\n\nText: Basic changes in the way Congress functions as well as in the outlook of its newer members toward their institution and their constituencies have made Congress less amenable to persuasion. A decline of political party influence has contributed to a dispersion of power within Congress, making it more difficult for presidents to work through party leaders to develop and steer a legislative agenda through the Senate and House.\nSimplify: Congress is harder to convince and prevail on since basic changes have been made to the way it is run and it has new members with new ideas. Members of Congress are now less likely to vote the way their party tells them too. Thus, Presidents can no longer get their way easily.\n\nText: The auditor\'s responsibilities for the audit of the financial statements can be included by a specific reference within the auditor\'s report to the location of such description on a website of an appropriate authority.\nSimplify: The auditor\'s responsibilities can be included in their report by providing a specific reference to a URL for the relevant webpage on an authority\'s website, rather than having to describe those responsibilities in the report itself.\n\nText: Kept hidebound by cloying commercial radio and clueless record executives, the American popular music scene has frequently depended on cities at the edges of the cultural map to provide a much-needed shot of originality. The momentary consensus about what the next big thing is seems to come out of nowhere as if someone blows a whistle only those in the know can hear, and suddenly record executives and journalists are crawling all over what had previously been an obscure locale.\nSimplify: American popular music falls into ruts and is formulaic and unoriginal. This is because radio and record executives lack boldness and want to play it safe with what\'s already established as popular. New popular music comes from more niche / less well known cultural groups. Trends in pop culture seem to come from nowhere. Suddenly, something goes viral, and a new genre of music is formed, and record executives, journalists, etc. are all clamoring over what had originally been a very niche music type.\n\nText: {text}\nSimplify:',
                            max_tokens=100,
                            temperature=0.7,
                            k=0,
                            p=1,
                            frequency_penalty=0.35,
                            presence_penalty=0.3,
                            stop_sequences=["Text:"],
                            return_likelihoods='NONE')
        st.write(f"{response.generations[0].text}")
