import streamlit as st
import pandas as pd
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt

st.title("🧠 AI-Based Log Analyzer System")

# Upload file
file = st.file_uploader("Upload log file")

if file:
    logs = file.read().decode("utf-8").split("\n")
    
    df = pd.DataFrame(logs, columns=["log"])
    
    # Create feature
    df["length"] = df["log"].apply(len)
    
    # AI model
    model = IsolationForest(contamination=0.2)
    df["anomaly"] = model.fit_predict(df[["length"]])
    
    # Log type detection
    def get_type(log):
        log = log.lower()
        if "error" in log:
            return "Error"
        elif "warning" in log:
            return "Warning"
        else:
            return "Normal"
    
    df["type"] = df["log"].apply(get_type)
    
    # Show all logs
    st.subheader("📄 All Logs")
    st.dataframe(df)
    
    # Show anomalies
    st.subheader("🚨 Anomalies Detected")
    st.dataframe(df[df["anomaly"] == -1])
    
    # Show types
    st.subheader("📌 Log Types")
    st.write(df[["log", "type"]])
    
    # Graph
    st.subheader("📊 Log Length Graph")
    fig, ax = plt.subplots()
    ax.hist(df["length"])
    st.pyplot(fig)

else:
    st.write("Please upload a log file")