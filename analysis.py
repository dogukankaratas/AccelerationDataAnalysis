import streamlit as st

graphContent = st.multiselect("Grafik", ["Tasarım Spektrumu (DD1)", 
                              "Tasarım Spektrumu (DD2)",
                              "Tepki Spektrumu (E-W)",
                              "Tepki Spektrumu (N-E)",
                              ])

if "Tasarım Spektrumu (DD2)" in graphContent:
    st.write("YES")