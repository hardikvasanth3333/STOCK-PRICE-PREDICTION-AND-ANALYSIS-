import pandas as pd
from alpha_vantage.timeseries import TimeSeries
import plotly.graph_objs as go
import time
import pyttsx3
import speech_recognition as sr
import webbrowser

larynx=pyttsx3.init('sapi5')
voices=larynx.getProperty('voices')
larynx.setProperty('voice',voices[1].id)


def speak(audio):
    larynx.say(audio)
    larynx.runAndWait()
    
def takecommand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("listening...")
        r.pause_threshold=1
        audio=r.listen(source)
        
    try:
        print("wait for few moment")
        query=r.recognize_google(audio,language='en-in')
        print("user said:", query)
    
    
    except Exception as e:
        print(e)
        query="nothing"
    return query

if __name__ == "__main__":
    speak("hi , welcome sir")
    while True:
        query=takecommand().lower()
        
        if "stock" in query:
            speak("opening stocks")

            api_key = "5OA09BO39DZST9QS"
            ts = TimeSeries(key=api_key, output_format="pandas")
            data, meta_data = ts.get_intraday(symbol="MSFT", interval="1min", outputsize="full")
            data.columns = data.columns.str.strip()
            print(data.head())

            close_data = data["4. close"]
            percentage_change = close_data.pct_change()
            last_change = percentage_change[-1]
            if abs(last_change) > 0.0004:
                print(f"MSFT alert: {last_change}")

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=data.index, y=close_data, mode='lines', name="Close Price"))
            fig.add_trace(go.Scatter(x=data.index, y=percentage_change, mode='lines', name="Percentage Change", line=dict(dash='dash')))

            fig.update_layout(
                title="MSFT Stock Data with Percentage Change",
                xaxis_title="Timestamp",
                yaxis_title="Price / Percentage Change",
                template="plotly_dark"
            )

            fig.show()