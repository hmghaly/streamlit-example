import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
from annotated_text import annotated_text

import requests
import json
import re

diac=u'\u064e\u064f\u0650\u0651\u0652\u064c\u064b\u064d\ufc62'
def tok_ar_diac(text): #tokenize Arabic words with diacritics
  diac_list=[]
  for i0,dia0 in enumerate(diac):
    if not dia0 in text: continue
    place_holder0=f'_diac{i0}_'
    text=text.replace(dia0,place_holder0)
    diac_list.append((place_holder0,dia0))

  text=re.sub("(\W)",r" \1 ",text)
  for a,b in diac_list:
    text=text.replace(a,b)
  tokens=[v for v in re.split("\s+",text) if v]
  return tokens
    
def search_arabic_word(word):
    api_key = "470deac4-36a4-482c-a2e7-7dd97a88135a"
    base_url = "https://siwar.ksaa.gov.sa/api/alriyadh/search"
    headers = {"accept": "application/json", "apikey": api_key}
    params = {"query": word}
    response = requests.get(base_url, headers=headers, params=params)

    if response.status_code == 200:
        return json.dumps(response.json(), indent=4, ensure_ascii=False)
    else:
        return None

st.title("إجادة")
st.header("مرحبا بكم في تطبيق إجادة")

st.write("يهدف تطبيق إجادة إلى الاستفادة من معجم الرياض في الكشف عن معاني الكلمات في أي نص يتم إدخاله، وذلك في إطار مسابقة برمجان العربية")
#st.button('Hit me')
input0= st.text_input('أدخل كلمة')
st.write(input0)

output0=search_arabic_word(input0)
st.write(output0)

cur_tokens=tok_ar_diac(input0)
annotated_tokens=[]
for token0 in cur_tokens: annotated_tokens.append((token0,"noun"))
annotated_text(annotated_tokens)

annotated_text(
    "This ",
    ("is", "verb"),
    " some ",
    ("annotated", "adj"),
    ("text", "noun"),
    " for those of ",
    ("you", "pronoun"),
    " who ",
    ("like", "verb"),
    " this sort of ",
    ("thing", "noun"),
    "."
)

# num_points = st.slider("Number of points in spiral", 1, 10000, 1100)
# num_turns = st.slider("Number of turns in spiral", 1, 300, 31)

# indices = np.linspace(0, 1, num_points)
# theta = 2 * np.pi * num_turns * indices
# radius = indices

# x = radius * np.cos(theta)
# y = radius * np.sin(theta)

# df = pd.DataFrame({
#     "x": x,
#     "y": y,
#     "idx": indices,
#     "rand": np.random.randn(num_points),
# })

# st.altair_chart(alt.Chart(df, height=700, width=700)
#     .mark_point(filled=True)
#     .encode(
#         x=alt.X("x", axis=None),
#         y=alt.Y("y", axis=None),
#         color=alt.Color("idx", legend=None, scale=alt.Scale()),
#         size=alt.Size("rand", legend=None, scale=alt.Scale(range=[1, 150])),
#     ))

