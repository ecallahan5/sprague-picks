import numpy as np
import pandas as pd
import streamlit as st


df = pd.read_csv("picks.csv", index_col = False)

wc_winners = ["2 BUF", "3 CIN", "4 JAX", "2 SF", "5 DAL", "6 NYG"]
div_winners = ["1 PHI", "2 SF", "1 KC", "3 CIN"]

cin_hel = "https://content.sportslogos.net/logos/7/154/full/ftn3942al0p6xnzh9lv9v11hl.png"
kc_hel = "https://content.sportslogos.net/logos/7/162/full/mbtef36mxmdxosrpvl4hf3e8i.png"
phi_hel = "https://content.sportslogos.net/logos/7/167/full/58p6tm0b3zr4dsrhevp12uva4.png"
sf_hel = "https://content.sportslogos.net/logos/7/179/full/vj3mzax8z0hvgafjtsccwcqde.png"

df["wc_pts"] = np.where(df["WC1"].str.strip().isin(wc_winners),1,0) + np.where(df["WC2"].str.strip().isin(wc_winners),1,0) + np.where(df["WC3"].str.strip().isin(wc_winners),1,0)  +\
               np.where(df["WC4"].str.strip().isin(wc_winners),1,0) + np.where(df["WC5"].str.strip().isin(wc_winners),1,0) + np.where(df["WC6"].str.strip().isin(wc_winners),1,0) 
df["div_pts"] = np.where(df["D1"].str.strip().isin(div_winners),2,0) + np.where(df["D2"].str.strip().isin(div_winners),2,0) +\
                 np.where(df["D3"].str.strip().isin(div_winners),2,0) + np.where(df["D4"].str.strip().isin(div_winners),2,0)
df["Total"] = df["wc_pts"] + df["div_pts"]  

st.header('Current Standings')
current_standings = df[["Name", "Total"]].sort_values(by=['Total'], ascending=False).set_index(["Name"])
st.dataframe(current_standings, use_container_width=True)

st.markdown("""<hr style="height:10px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)

st.header('Let\'s Play What If!')

afc_select = st.selectbox(
    "AFC Champ",
    ('Who Wins?', '3 CIN', '1 KC'))

if afc_select == '3 CIN':
    df["Simulated Total a"] = np.where(df["AFC"].str.strip() == '3 CIN', df["Total"] + 4, df["Total"])
elif afc_select == '1 KC':
    df["Simulated Total a"] = np.where(df["AFC"].str.strip() == '1 KC', df["Total"] + 4, df["Total"])
else:
    df["Simulated Total a"] = df["Total"]

nfc_select = st.selectbox(
    "NFC Champ",
    ('Who Wins?', '2 SF', '1 PHI'))

if nfc_select == '2 SF':
    df["Simulated Total n"] = np.where(df["NFC"].str.strip() == '2 SF', df["Simulated Total a"] + 4, df["Simulated Total a"])
elif nfc_select == '1 PHI':
    df["Simulated Total n"] = np.where(df["NFC"].str.strip() == '1 PHI', df["Simulated Total a"] + 4, df["Simulated Total a"])
else:  
    df["Simulated Total n"] = df["Simulated Total a"]

pb_select = st.selectbox(
    "Pro Bowl Winner",
    ('Who Wins?', 'AFC', 'NFC', 'Tie'))

if pb_select == 'NFC':
    df["Simulated Total p"] = np.where(df["PB"].str[:3] == 'NFC', df["Simulated Total n"] + 1, df["Simulated Total n"])
elif pb_select == 'AFC':
    df["Simulated Total p"] = np.where(df["PB"].str[:3] == 'AFC', df["Simulated Total n"] + 1, df["Simulated Total n"])
elif pb_select == 'Tie':
    df["Simulated Total p"] = np.where(df["PB"].str[:3] == 'Tie', df["Simulated Total n"] + 1, df["Simulated Total n"])
else:  
    df["Simulated Total p "] = df["Simulated Total n"]

sb_select = st.selectbox(
    "Super Bowl Champion",
    ('Who Wins?', nfc_select, afc_select))

if sb_select == nfc_select:
    df["Simulated Total"] = np.where(df["SB"].str.strip() == nfc_select, df["Simulated Total p"] + 6, df["Simulated Total p"])
elif sb_select == afc_select:
    df["Simulated Total"] = np.where(df["SB"].str.strip() == afc_select, df["Simulated Total p"] + 6, df["Simulated Total p"])
else:  
    df["Simulated Total"] = df["Simulated Total p"]

if sb_select == '3 CIN':
    st.image(cin_hel)
elif sb_select == '1 PHI':
    st.image(phi_hel)
elif sb_select == '1 KC':
    st.image(kc_hel)
elif sb_select == '2 SF':
    st.image(sf_hel)


sim_standings = df[["Name", "Total", "Simulated Total"]].sort_values(by=['Simulated Total'], ascending=False).set_index(["Name"])
st.dataframe(sim_standings, use_container_width=True)
# col1, col2, col3, col4 = st.columns(4)

# with col1:
#    st.header("A cat")
#    st.image("https://static.streamlit.io/examples/cat.jpg")

# with col2:
#    st.header("A dog")
#    st.image("https://static.streamlit.io/examples/dog.jpg")

# with col3:
#    st.header("An owl")
#    st.image("https://static.streamlit.io/examples/owl.jpg")


