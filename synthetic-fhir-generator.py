import streamlit as st
import requests

# Replace 'your-api-key' with your actual OpenRouter API key
openrouter_api_key = st.secrets['openrouter_api_key']
openrouter_api_url = 'https://openrouter.ai/api/v1/chat/completions'

def get_fhir_data(user_input, model):
    headers = {
        'Authorization': f'Bearer {openrouter_api_key}',
        'Content-Type': 'application/json'
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are an assistant that generates verbose synthetic health data as a FHIR bundle. Make sure that your response include only the json object and no additional text."},
            {"role": "user", "content": user_input}
        ]
    }
    response = requests.post(openrouter_api_url, headers=headers, json=payload)
    response.raise_for_status()
    print(response.json())
    return response.json()['choices'][0]['message']['content']

st.title('Synthetic Patient Data Generator')
st.write('Generate synthetic patient records in FHIR format.')

# Model selection
model = st.selectbox('Select Model', ['openai/gpt-3.5-turbo', 'openai/gpt-4o', 'openai/gpt-4', 'anthropic/claude-instant-v1', 'meta-llama/llama-2-70b-chat', 'google/palm-2-chat-bison'])

# User inputs
text_description = st.text_area('Text Description')

# Compose user input for OpenRouter
user_input = f"""
Generate a verbose FHIR bundle resource with the following details:
- Instructions: {text_description}
"""

if st.button('Generate Data'):
    with st.spinner('Generating data...'):
        try:
            fhir_data = get_fhir_data(user_input, model)
            # Parse the FHIR data to JSON to ensure it's valid
            #print(fhir_data)
            st.json(fhir_data)
        except requests.RequestException as e:
            st.error(f"API request failed: {e}")
        except Exception as e:
            st.error(f"An unknown error occurred: {e}")