import streamlit as st
import pickle
import re
import fitz
import warnings

warnings.filterwarnings('ignore')

st.header('Resume Categorizer App')
upload = st.file_uploader('Upload PDF resume', type='pdf')
st.write('Click the button below to find the resume category.')

vect = pickle.load(open('vect.pkl','rb'))
model = pickle.load(open('model.pkl','rb'))

def extracted_text(uploaded_file):
    text = ''
    with fitz.open(stream = uploaded_file.read(), filetype='pdf') as doc:
        for txt in doc:
            text = text + txt.get_text()
    return text

exttext = extracted_text(upload)

def clean_Text(text):
    cleanedText = re.sub(r'http\S+\s', ' ',text)
    cleanedText = re.sub(r'RT|cc', ' ',cleanedText)
    cleanedText = re.sub(r'#\S+\s', ' ',cleanedText)
    cleanedText = re.sub(r'@\S+', ' ',cleanedText)
    cleanedText = re.sub(r'[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\\]^_'{|}~"""), ' ', cleanedText)
    cleanedText = re.sub(r'[^\x00-\x7f]', ' ',cleanedText)
    cleanedText = re.sub(r'\s+', ' ',cleanedText)    
    return cleanedText

cleaned_text = clean_Text(exttext)

def predicted(t_ext):  
    vectText = vect.transform([t_ext])
    Prediction = model.predict(vectText)[0]
    return Prediction

Predicted_category = predicted(cleaned_text) 

but = st.button('Predict')

if upload is not None:
    if but:
        st.success(f"Category of the resume: {Predicted_category}")
else:
    st.write('Please upload PDF file.')

