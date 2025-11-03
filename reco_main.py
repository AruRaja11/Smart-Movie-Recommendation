import numpy as np
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
import re
import os 
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")


# importing antecedents and consequents from the dataset
def load_data(data_path):
    return pd.read_csv(data_path)

def clean_name(movie):
    if movie == None:
        return None

    movie = re.findall(r"[a-zA-Z\s]", movie)
    movie = "".join(movie)
    movie = movie.strip()
    movie = movie.lower()
    return movie

def get_suggestion(movie, data):
    movie = clean_name(movie)
    result = []
    for i in range(len(data)):
        if movie == data['antecedents'][i]:
            result.append(data['consequents'][i])
        else:
            continue
    print(result)
    return result



# creating a AI Agent

def content_generation(input):

    prompt = f"""
        You are an expert communication bot specializing in presenting information in a helpful and natural conversational style.

    Your task is to receive a list of movie titles and present them to the user in a single, fluent, and helpful sentence. This sentence must act as a recommendation based on a shared, underlying theme (which you will mention is the "type").

    Input
    You will receive a single, variable-length list of movie names as the input:

    {input}

    Core Rule & Output Format
    Format: The entire output must be a single, complete sentence.

    Persona: The sentence must use a recommending tone (e.g., "I recommend you to watch...").

    Content: Include every movie name from the input list, separated by commas.

    Justification: Conclude the sentence with a justification for the recommendation, specifically stating, based on what you think about the recommendations.
    Note: if the input is none or nothing then say that i couldn't recommend for this movie
    """

    response = model.generate_content(prompt)
    return response.text


def suggest_movie(movie):
    data = load_data("movies_recommendation.csv")
    result = get_suggestion(movie, data)
    return content_generation(result)

if __name__ == "__main__":
    print(suggest_movie("aliens"))
