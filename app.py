
# Imports

import streamlit as st
from faqs import faqs
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk

try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")

# Page Config

st.set_page_config(
    page_title="College Admission FAQ Chatbot",
    page_icon="🎓",
    layout="centered"
)

# Session State

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# CSS    

st.markdown("""
<h1 style="
text-align:center;
color:#2F5D50;
font-size:38px;
margin-bottom:5px;
">
🎓 College Admission FAQ Chatbot
</h1>
""", unsafe_allow_html=True)

st.markdown("""
<p style="
text-align:center;
color:#6A7F75;
font-size:17px;
margin-bottom:30px;
">
Ask your admission-related questions and receive instant AI-powered answers.
</p>
""", unsafe_allow_html=True)

# Sidebar

st.sidebar.markdown("""
<div style="
background:#FFFFFF;
border:2px solid #D5E8DA;
border-radius:18px;
padding:20px;
text-align:center;
margin-bottom:20px;
">

<div style="font-size:50px;">🎓</div>

<h2 style="
color:#2F5D50;
margin-top:10px;
margin-bottom:5px;
">
Admission Bot
</h2>

<p style="
color:#5B756B;
font-size:15px;
margin:0;
">
Smart • Fast • Accurate
</p>

</div>
""", unsafe_allow_html=True)

st.markdown("""
<style>

/* Main Background */
[data-testid="stAppViewContainer"]{
    background:#F8FAF7;
}

/* Sidebar */
section[data-testid="stSidebar"]{
    background:#EAF4EC;
    border-right:2px solid #D5E8DA;
}

/* Headings */
h1{
    color:#2F5D50;
    text-align:center;
}

h2,h3{
    color:#3F6F63;
}

/* Button */
.stButton>button{
    background:#6FAF8F;
    color:white;
    border:none;
    border-radius:12px;
    height:52px;
    font-size:17px;
    font-weight:bold;
    transition:0.3s;
}

.stButton>button:hover{
    background:#5C9C7B;
    color:white;
}

/* Input Box */
.stTextInput input{
    border-radius:12px;
    border:2px solid #D5E8DA;
    background:white;
    padding:10px;
}

/* Statistics Card */
[data-testid="stMetric"]{
    background:white;
    border:2px solid #D5E8DA;
    border-radius:12px;
    padding:12px;
}

</style>
""", unsafe_allow_html=True)



st.sidebar.markdown("""
<p style="
text-align:center;
color:#5B756B;
font-size:13px;
margin-top:5px;
margin-bottom:15px;
">
✨ CodeAlpha AI Internship
</p>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

st.sidebar.markdown("""
<div style="
background:#FFFFFF;
border:2px solid #D5E8DA;
border-radius:15px;
padding:16px;
margin-bottom:15px;
box-shadow:0 3px 10px rgba(0,0,0,0.05);
">

<h4 style="
color:#2F5D50;
margin-top:0;
margin-bottom:12px;
">
✨ Features
</h4>

<p style="color:#5B756B;">🎓 Admission FAQs</p>
<p style="color:#5B756B;">🤖 Smart Matching</p>
<p style="color:#5B756B;">🧠 NLP Processing</p>
<p style="color:#5B756B;">💬 Chat History</p>

</div>
""", unsafe_allow_html=True)

# Sidebar Tip

st.sidebar.markdown("---")

st.sidebar.markdown("""
<div style="
background:#F4FAF5;
border-left:5px solid #6FAF8F;
border-radius:12px;
padding:12px;
margin:15px 0;
">

<p style="
color:#3F6F63;
font-size:14px;
margin:0;
">
💡 <b>Tip:</b><br>
Type your admission-related question below and press
<b>Get Answer</b>.
</p>

</div>
""", unsafe_allow_html=True)

# Statistics Placeholder
statistics_placeholder = st.sidebar.empty()


st.sidebar.markdown("---")

st.sidebar.markdown("""
<div style="
background:#FFFFFF;
border:2px solid #D5E8DA;
border-radius:15px;
padding:15px;
margin-bottom:15px;
">

<h4 style="color:#2F5D50;">💡 Suggested Questions</h4>

<p>• What courses are offered?</p>
<p>• How can I apply?</p>
<p>• Is hostel facility available?</p>
<p>• What documents are required?</p>

</div>
""", unsafe_allow_html=True)

# Main Title

st.markdown("""
<div style="
background:#FFFFFF;
border:2px solid #D5E8DA;
border-radius:18px;
padding:22px;
margin-bottom:25px;
text-align:center;
box-shadow:0 4px 12px rgba(0,0,0,0.08);
">

<h3 style="color:#2F5D50;margin-bottom:10px;">
👋 Welcome!
</h3>

<p style="color:#5B756B;font-size:16px;">
Ask any college admission question and receive an instant AI-powered response.
</p>

</div>
""", unsafe_allow_html=True)

# AI Logic

user_question = st.text_input(
    "💬 Ask Your Question",
    placeholder="Example: What courses are offered?",
    help="Type any admission-related question here."
)

questions = [faq["question"] for faq in faqs]
answers = [faq["answer"] for faq in faqs]

vectorizer = TfidfVectorizer(
    stop_words="english",
    ngram_range=(1, 2),
    sublinear_tf=True
)
question_vectors = vectorizer.fit_transform(questions)

if st.button("🤖 Get Answer", use_container_width=True):

    if user_question.strip():

        user_vector = vectorizer.transform([user_question])

        similarity = cosine_similarity(user_vector, question_vectors)

        best_match = similarity.argmax()

        score = similarity[0][best_match]

        if score >= 0.15:
            answer = answers[best_match]
        else:
            answer = """
❌ Sorry, I couldn't find an answer to that question.

💡 You can ask questions like:

• What courses are offered?
• How can I apply?
• What documents are required?
• Is hostel facility available?
• What is the admission fee?
"""

        st.session_state.chat_history.append(
            {
                "question": user_question,
                "answer": answer
            }
        )

    else:
        st.warning("Please enter a question.")
        
# Update Statistics

statistics_placeholder.markdown(f"""
<div style="
background:#FFFFFF;
border:2px solid #D5E8DA;
border-radius:15px;
padding:16px;
margin-bottom:15px;
box-shadow:0 3px 10px rgba(0,0,0,0.05);
">

<h4 style="
color:#2F5D50;
margin-top:0;
margin-bottom:12px;
">
📊 Statistics
</h4>

<p style="
color:#5B756B;
font-size:14px;
margin-bottom:5px;
">
Questions Asked
</p>

<h2 style="
color:#2F5D50;
margin-top:0;
margin-bottom:12px;
">
{len(st.session_state.chat_history)}
</h2>

<p style="
color:#5B756B;
font-size:14px;
margin-bottom:5px;
">
Available FAQs
</p>

<h2 style="
color:#2F5D50;
margin-top:0;
">
{len(faqs)}
</h2>

</div>
""", unsafe_allow_html=True)

# Conversation

st.markdown("---")



st.markdown("""
<h2 style="
color:#2F5D50;
margin-top:25px;
margin-bottom:20px;
">
💬 Conversation
</h2>
""", unsafe_allow_html=True)

if st.session_state.chat_history:

    for chat in st.session_state.chat_history:

        # User Message

        st.markdown(f"""
<div style="
background:#EAF4FF;
border:1px solid #C8DFF8;
border-left:6px solid #64B5F6;
border-radius:18px 18px 5px 18px;
padding:16px 18px;
margin:10px 0 12px 30px;
box-shadow:0 4px 12px rgba(0,0,0,0.06);
">

<div style="
color:#2F5D50;
font-size:14px;
font-weight:bold;
margin-bottom:8px;
">
🧑 You
</div>

<div style="
color:#344A43;
font-size:15px;
line-height:1.6;
">
{chat['question']}
</div>

</div>
""", unsafe_allow_html=True)

        # Bot Message

        st.markdown(f"""
<div style="
background:#EDF8EF;
border:1px solid #CFE8D5;
border-left:6px solid #6FAF8F;
border-radius:18px 18px 18px 5px;
padding:16px 18px;
margin:10px 30px 25px 0;
box-shadow:0 4px 12px rgba(0,0,0,0.06);
">

<div style="
color:#2F5D50;
font-size:14px;
font-weight:bold;
margin-bottom:8px;
">
🤖 Admission Bot
</div>

<div style="
color:#344A43;
font-size:15px;
line-height:1.6;
">
{chat['answer']}
</div>

</div>
""", unsafe_allow_html=True)

else:

    st.info("👋 Start chatting with the Admission Bot!")

    #footer

    st.markdown("---")

st.markdown(
    """
<div style="text-align:center;color:#6A7F75;font-size:14px;">
Made with Asfa Mushtaq❤️ using Streamlit | CodeAlpha AI Internship
</div>
""",
unsafe_allow_html=True
)