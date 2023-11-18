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

def exact_search_arabic_word(word):
    api_key = "470deac4-36a4-482c-a2e7-7dd97a88135a"
    base_url = "https://siwar.ksaa.gov.sa/api/alriyadh/exact-search"
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

# output0=search_arabic_word(input0)
# st.write(output0)

cur_tokens=tok_ar_diac(input0)
annotated_tokens=[]
table_items=[]
cur_headers=["الكلمة","موجودة؟","المدخل","الترجمة","النوع","الجمع"]
for token0 in cur_tokens: 
  if len(token0)<2: continue
  
  try:
    token_output0=exact_search_arabic_word(token0)
    out_parsed=json.loads(token_output0)
    for test in out_parsed: 
      #print(test)        
      form0=test["lemma"]['formRepresentations'][0]["form"]
      translation0=test["senses"][0]['translations'][0]["form"]
      broken_plural0=test["extras"]['senseDetails'][0]['BrokenPlural']
      broken_plural_str0=", ".join(broken_plural0)
      pos0=test["pos"]
      row_items=[token0,'✅',form0,translation0,pos0,broken_plural_str0]
      # st.write(form0)
      # st.write(translation0)
      # st.write(", ".join(broken_plural0))
      # st.write(pos0)
      # st.write("----")
    
    #st.json(json.loads(token_output0))
  except:
    row_items=[token0,'❌',"","","",""]
    # st.write(f'هذه الكلمة غير موجودة في المعجم: ' )
    # st.write(token0)
    # st.write("----")
  table_items.append(row_items)
    

table_df=pd.DataFrame(table_items, columns = cur_headers)
st.table(table_df)

  #annotated_tokens.append((token0,"noun"))
#annotated_text(annotated_tokens)

# annotated_text(
#     "This ",
#     ("is", "verb"),
#     " some ",
#     ("annotated", "adj"),
#     ("text", "noun"),
#     " for those of ",
#     ("you", "pronoun"),
#     " who ",
#     ("like", "verb"),
#     " this sort of ",
#     ("thing", "noun"),
#     "."
# )

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

