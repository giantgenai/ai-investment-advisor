import pickle
import streamlit as st
import time
from llama_index.core import VectorStoreIndex, StorageContext, SimpleDirectoryReader, load_index_from_storage
from llama_index.vector_stores.faiss import FaissVectorStore
from streamlit_chat import message
from openai import OpenAI
import faiss

from investment_utils import get_industry_tickers, get_news_with_summary


# Initialize both OpenAI and Ollama clients
openai_client = OpenAI()
ollama_client = OpenAI(
    base_url='http://localhost:11434/v1',
    api_key='ollama'
)

# Set page config
st.set_page_config(page_title="Investment Advisor Pro", page_icon="📈", layout="wide")

# Custom CSS to improve the app's appearance
st.markdown("""
    <style>
    .big-font {
        font-size:30px !important;
        font-weight: bold;
    }
    .medium-font {
        font-size:20px !important;
    }
    .small-font {
        font-size:14px !important;
    }
    .highlight {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data(ttl=3600)
def get_industry_data(industry):
    tickers = get_industry_tickers(industry)
    news_summaries = get_news_with_summary(tickers)
    return tickers, news_summaries

# Load the index
news_dir = "./data"

# Load documents
documents = SimpleDirectoryReader(news_dir).load_data()

# Create a FAISS index
d = 1536  # dimensions of text-embedding-ada-002
faiss_index = faiss.IndexFlatL2(d)
vector_store = FaissVectorStore(faiss_index=faiss_index)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# Create the index
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)

# # Save the FAISS index separately
# faiss.write_index(faiss_index, "./saved_index/faiss.index")

# # Save the rest of the index
# index.storage_context.persist(persist_dir="./saved_index")

# # Save the vector store separately
# with open("./saved_index/vector_store.pkl", "wb") as f:
#     pickle.dump(vector_store, f)

# print("Index saved successfully")

# vector_store = FaissVectorStore.from_persist_dir("./saved_index")
# storage_context = StorageContext.from_defaults(
#     vector_store=vector_store, persist_dir="./saved_index"
# )
# index = load_index_from_storage(storage_context=storage_context)

# Create a query engine
query_engine = index.as_query_engine()

def get_relevant_news(industry: str, company: str) -> str:
    query = f"What are the recent developments in the {industry} industry, particularly related to {company}?"
    response = query_engine.query(query)
    return str(response)

def recommend_investment(industry: str, tickers: str, news_summaries: str, model_choice: str="gpt-4o-mini") -> str:

    relevant_news = ""
    for ticker in tickers.split(", "):
        relevant_news += get_relevant_news(industry, ticker) + "\n\n"
    
    prompt = f"""
    Based on the following news summaries and relevant news for companies in the {industry} industry, 
    analyze the information and recommend the best company for investment. 
    Consider factors such as positive developments, growth potential, and market trends.

    Industry: {industry}
    Tickers: {tickers}
    News Summaries:
    {news_summaries}
    Relevant News:
    {relevant_news}

    Please structure your response as follows:
    1. Start with "Recommendation:" followed by the ticker symbol of the recommended company.
    2. Then, provide an "Explanation:" section with a detailed analysis of why this company is recommended.
    3. Include 3-4 key points supporting your recommendation.
    4. Briefly mention why the other companies were not chosen.

    Your response should look like this:

    Recommendation: [TICKER]

    Explanation:
    [Your detailed explanation here, structured in paragraphs or bullet points]

    Do not include any other sections or repeat the recommendation and explanation.
    """

    if model_choice == "gpt-4o-mini":
        client = openai_client
        model = "gpt-4o-mini"
    else:
        client = ollama_client
        model = "llama3.3:latest"  

    # Make the API call to OpenAI's GPT-4 model
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a financial assistant specialized in investment analysis."},
            {"role": "user", "content": prompt}
        ],
        temperature=0  # This makes the output more deterministic
    )
    
    # Return the response content
    return response.choices[0].message.content.strip()


# Initialize session state variables
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []
if 'messages' not in st.session_state:
    st.session_state['messages'] = []
if 'recommendation' not in st.session_state:
    st.session_state['recommendation'] = ""

def generate_response(prompt, recommendation, model_choice="gpt-4o-mini"):
    st.session_state['messages'].append({"role": "user", "content": prompt})

    
    if model_choice == "gpt-4o-mini":
        client = openai_client
        model = "gpt-4o-mini"
    else:
        client = ollama_client
        model = "llama3.3:latest"  
    
    response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that provides information about the investment recommendation. Refer to the recommendation when answering questions."},
                {"role": "assistant", "content": f"Here's the investment recommendation: {recommendation}"},
                *st.session_state['messages']
    ])
    
    bot_response = response.choices[0].message.content
    st.session_state['messages'].append({"role": "assistant", "content": bot_response})
    
    return bot_response

def main():
    st.markdown("<p class='big-font'>Investment Advisor Pro</p>", unsafe_allow_html=True)
    st.markdown("<p class='medium-font'>Get AI-powered investment recommendations based on latest industry news</p>", unsafe_allow_html=True)

    st.sidebar.image("./logo/investment_recommendation_logo.webp", width=200)  
    st.sidebar.markdown("## About")
    st.sidebar.info("Investment Advisor Pro uses advanced AI to analyze recent news and provide investment recommendations for various industries.")
    st.sidebar.markdown("## How to use")
    st.sidebar.markdown("1. Enter an industry name")
    st.sidebar.markdown("2. Click 'Get Recommendation'")
    st.sidebar.markdown("3. Review the AI-generated advice")

    # Add model selection dropdown
    model_choice = st.selectbox(
        "Choose Language Model",
        ["gpt-4o-mini", "llama3.3"],
        help="Select which language model to use for generating responses"
    )

    industry = st.text_input("Enter an industry name:", help="e.g., Technology, Healthcare, Finance")

    if st.button("Get Recommendation", key="recommend"):
        if industry:
            with st.spinner(f"Analyzing the {industry} industry..."):
                start_time = time.time()
                
                # Create placeholder elements
                ticker_placeholder = st.empty()
                progress_bar = st.progress(0)
                recommendation_placeholder = st.empty()
                explanation_placeholder = st.empty()
                news_placeholder = st.empty()
                
                # Fetch data
                tickers, news_summaries = get_industry_data(industry)
                ticker_placeholder.markdown(f"<p class='highlight'><b>Analyzed tickers:</b> {tickers}</p>", unsafe_allow_html=True)
                progress_bar.progress(50)
                
                # Generate recommendation
                recommendation = recommend_investment(industry, tickers, news_summaries, model_choice=model_choice)
                st.session_state['recommendation'] = recommendation
                progress_bar.progress(100)
                
                end_time = time.time()
                
                # Split the recommendation into parts
                recommendation_parts = recommendation.split("Explanation:", 1)
                recommendation_text = recommendation_parts[0].strip()
                explanation = recommendation_parts[1].strip() if len(recommendation_parts) > 1 else ""

                # Display recommendation
                recommendation_placeholder.markdown(f"<p class='highlight'><b>{recommendation_text}</b></p>", unsafe_allow_html=True)

                # Display explanation
                # if explanation:
                explanation_placeholder.markdown("<p class='medium-font'><b>Explanation:</b></p>", unsafe_allow_html=True)
                explanation_placeholder.write(explanation)
                
                # Display news summaries
                news_placeholder.markdown("<p class='medium-font'><b>Recent News Summaries:</b></p>", unsafe_allow_html=True)
                for company_news in news_summaries.split('\n\n'):
                    st.markdown("---")  # Add a separator between companies
                    lines = company_news.split('\n')
                    if lines:
                        st.markdown(f"**{lines[0]}**")  # Company name or ticker
                        for line in lines[1:]:
                            if line.startswith('- '):
                                title, date = line[2:].rsplit(' (Published:', 1)
                                st.write(f"• {title}")
                                st.caption(f"Published: {date.rstrip(')')}")
                            elif line.startswith('  Summary:'):
                                st.info(line[10:])  # Display summary if available
                            elif line.strip():
                                st.write(line)  # Any other information
                
                st.success(f"Analysis completed in {end_time - start_time:.2f} seconds!")
                
        else:
            st.warning("Please enter an industry name.")

    st.markdown("<p class='small-font'>Disclaimer: This tool provides recommendations based on AI analysis of recent news. It should not be considered as financial advice. Always consult with a qualified financial advisor before making investment decisions.</p>", unsafe_allow_html=True)
    
    # Chat interface
    st.subheader("Ask follow-up questions")

    # Display chat history
    if st.session_state['generated']:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
            message(st.session_state["generated"][i], key=str(i))
    
    # Input box for user questions
    user_input = st.text_input("Your question:", key="input")
    
    if user_input:
        output = generate_response(user_input, st.session_state['recommendation'], model_choice=model_choice)
        st.session_state.past.append(user_input)
        st.session_state.generated.append(output)


if __name__ == "__main__":
    main()