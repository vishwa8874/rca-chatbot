import streamlit as st
import os
import pandas as pd
import google.generativeai as genai



genai.configure(api_key="AIzaSyB2zb_SGPmqT28ZUUDXXJcL7aks5oGh8N8")


def get_gemini_response(input_text, description_text, prompt):
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content([input_text, description_text, prompt])
        return response.text
    except Exception as e:
        st.error(f"An error occurred while generating the content: {e}")
        return None


def find_description_by_summary(df, summary):
    
    if 'Summary' in df.columns and 'Description' in df.columns:
        
        filtered_df = df[df['Summary'].str.contains(summary, case=False, na=False)]

        if not filtered_df.empty:
            
            return " ".join(filtered_df['Description'].fillna(""))
        else:
            st.warning("No matching descriptions found for the provided summary.")
            return None
    else:
        st.error("The uploaded CSV file must contain both 'Summary' and 'Description' columns.")
        return None


st.set_page_config(page_title="Root Cause Analyzer")

st.header("Chatbot for Root Cause Analysis")



input_text = st.text_input("Summary of the Error:", key="summary_input")
uploaded_file = st.file_uploader("Upload your Docs (CSV)...", type=["csv"])


submit_analysis = st.button("Root Cause Analysis")
submit_suggestions = st.button("Suggest Alternative Approaches")



input_prompt1 = """
To perform a thorough root cause analysis (RCA) of the problem or incident described in the given description. The goal is to identify the underlying causes and propose actionable solutions to prevent recurrence.

Instructions:

Document Review:

Carefully read the uploaded document.
Note key details about the problem or incident, including when it occurred, where it occurred, and its impact.
Problem Description:

Clearly describe the problem or incident in your own words.
Specify the nature of the issue, its symptoms, and its scope.
Data Collection:

Identify and gather relevant data from the document and any other sources provided.
Focus on facts, figures, and evidence that can help in understanding the problem.
Identify Possible Causes:

Use one or more RCA techniques (e.g., 5 Whys, Fishbone Diagram, FMEA) to brainstorm possible causes of the problem.
Consider factors such as processes, people, equipment, materials, environment, and management.
Analyze Causes:

Analyze the identified causes to determine which are the root causes.
Use additional data or evidence to support your analysis.
Propose Solutions:

Suggest actionable solutions or corrective actions for each root cause.
Ensure that the solutions address the root causes effectively and can be implemented feasibly.
Documentation:

Document your findings and analysis clearly and concisely.
Include visual aids (e.g., diagrams, charts) where applicable to enhance understanding.
Deliverables:

A detailed report summarizing the root cause analysis.
A list of identified root causes with supporting evidence.
Proposed solutions for each root cause with implementation steps.
Tools and Techniques:
You may use any of the following RCA techniques:

5 Whys
Fishbone Diagram (Ishikawa)
Failure Mode and Effects Analysis (FMEA)
Fault Tree Analysis (FTA)
Pareto Analysis
Root Cause Mapping
Change Analysis
Kepner-Tregoe Problem Analysis
Current Reality Tree (CRT)
8D Problem Solving
"""

input_prompt2 = """
To receive insightful suggestions and recommendations for alternative solutions to address the root causes identified in the attached root cause analysis (RCA) document. The goal is to explore diverse approaches to effectively resolve the issue and prevent its recurrence.

Instructions:

Review Root Cause Analysis:

Carefully read the attached RCA document.
Understand the identified root causes and the proposed solutions.
Evaluate Proposed Solutions:

Analyze the effectiveness, feasibility, and potential impact of the proposed solutions.
Consider any limitations or potential challenges associated with the proposed solutions.
Suggest Alternate Solutions:

Provide at least three alternative solutions for each identified root cause.
Ensure that the suggested solutions are actionable and practical.
Consider different perspectives, innovative approaches, and best practices.
Detail Each Suggestion:

For each alternative solution, include the following details:
Description: A clear and concise explanation of the solution.
Implementation Steps: A step-by-step plan for how to implement the solution.
Advantages: Benefits and positive impacts of the solution.
Potential Challenges: Any potential challenges or obstacles and how to mitigate them.
Provide Supporting Evidence:

Include any relevant data, case studies, or examples that support the effectiveness of the suggested solutions.
Use visual aids (e.g., diagrams, charts) where applicable to enhance understanding.
Deliverables:

A comprehensive report with alternative solutions for each root cause.
Detailed descriptions, implementation steps, advantages, and potential challenges for each suggested solution.
Supporting evidence and visual aids to substantiate the recommendations.
"""



description_text = ""
if uploaded_file is not None:
    st.write("CSV Uploaded Successfully")
    df = pd.read_csv(uploaded_file)
    description_text = find_description_by_summary(df, input_text)


if submit_analysis:
    if description_text:
        response = get_gemini_response(input_text, description_text, input_prompt1)
        if response:
            st.subheader("Analysis Response")
            st.write(response)
    else:
        st.write("Please upload a CSV file and provide a valid summary to proceed.")

elif submit_suggestions:
    if description_text:
        response = get_gemini_response(input_text, description_text, input_prompt2)
        if response:
            st.subheader("Suggestions Response")
            st.write(response)
    else:
        st.write("Please upload a CSV file and provide a valid summary to proceed.")


    
