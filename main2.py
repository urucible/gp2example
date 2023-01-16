import streamlit as st
import pandas as pd

URL = "https://raw.githubusercontent.com/gamba/swiss-geolocation/master/post-codes.csv"                         # Link zu der CSV Datei mit allen PLZ der Schweiz

st.title("Projektarbeit Mike")                                                                                  # Anzeigen des Titels
@st.cache
def load_data():
    df_tmp = pd.read_csv(URL, header=3, dtype={"zip": str})
    df_tmp["DISTRICT"] = df_tmp.apply(lambda row: row.post_district.upper(), axis=1)
    return df_tmp

df = load_data()

place = st.text_input("Ort eingeben:")                                                                         # Text oberhalb vom Suchfeld

df_result = df.query(f"DISTRICT.str.contains('{place.upper()}')", engine='python')

if len(df) == len(df_result):
    st.info("Bitte einen Ort eingeben.")
else:
    if df_result.empty:
        st.warning("Ort nicht gefunden!")
    else:
        df_display = df_result.set_index('zip').rename_axis('PLZ', axis=1)
        df_display = df_display[["town"]]
        df_display.index.name = None
        st.write(df_display.to_html(), unsafe_allow_html=True)