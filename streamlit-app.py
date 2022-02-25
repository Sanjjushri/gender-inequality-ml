# Global Import
import streamlit as st
import pandas as pd

# Local import
import similar_countries_4_criteria as simi

def main():
    
    st.title("Countries with similar gender inquality rate Estimator")

    html_temp = """
    <div style = "background-color:blue; padding:10px">
    <h5 style  = "color:white"; text-align:center; "> Find Countries with similar GII Rank </h5>
    </div>
    """

    st.markdown(html_temp, unsafe_allow_html = True)

    name   = st.text_input("Country", "Type Here")
    
    if st.button("Predict"):

        result = simi.find_similar_student(name)
        data = pd.DataFrame.from_dict(result)

        st.table(data)
    
if __name__ == "__main__":
    main()