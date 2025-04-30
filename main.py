import streamlit as st
import pandas as pd
import joblib

pipeline = joblib.load("notebook/pipeline.joblib")


def predict_results(sep_len, sep_wid, pet_len, pet_wid):
    # Convert the results to dataframe
    inputs = [
        {
            "sepal_length": sep_len,
            "sepal_width": sep_wid,
            "petal_length": pet_len,
            "petal_width": pet_wid,
        }
    ]
    xnew = pd.DataFrame(inputs)
    preds = pipeline.predict(xnew)
    probs = pipeline.predict_proba(xnew).flatten()
    classes = pipeline.classes_
    probs_dict = dict(zip(classes, probs.round(4)))
    return preds[0], probs_dict


def main():
    # Set page config
    st.set_page_config(page_title="Iris Project")

    # Add title to the app
    st.title("Iris End to End ML Project")

    # Adding subheader author name
    st.subheader("By Utkarsh Gaikwad")

    # Take inputs from user
    sep_len = st.number_input("Sepal Length : ", min_value=0.00, step=0.01)
    sep_wid = st.number_input("Sepal Width : ", min_value=0.00, step=0.01)
    pet_len = st.number_input("Petal Length : ", min_value=0.00, step=0.01)
    pet_wid = st.number_input("Petal Width : ", min_value=0.00, step=0.01)

    # Create a button for prediction
    submit = st.button("Predict", type="primary")

    # If button pressed
    if submit:
        preds, prob_dict = predict_results(sep_len, sep_wid, pet_len, pet_wid)
        st.subheader(f"Predictions : {preds}")
        for c, prob in prob_dict.items():
            st.subheader(f"Species : {c}, Probability : {prob}")
            st.progress(prob)


if __name__ == "__main__":
    main()
