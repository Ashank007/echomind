import streamlit as st
import requests
import os

st.set_page_config(
    page_title="EchoMind - Personal Memory Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

API_URL = os.getenv("API_URL", "http://localhost:8000")

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #2c3e50;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
    .memory-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 5px solid #1f77b4;
    }
    .stButton>button {
        background-color: #1f77b4;
        color: white;
        border-radius: 5px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }
    .stButton>button:hover {
        background-color: #155a8a;
    }
    .stTextInput>div>div>input, .stTextArea>div>textarea {
        border-radius: 5px;
        border: 1px solid #ddd;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🧠 EchoMind - Personal Memory Assistant</div>', unsafe_allow_html=True)

# Sidebar for information
with st.sidebar:
    st.header("ℹ️ About")
    st.write("EchoMind helps you store and retrieve personal memories using AI-powered embeddings.")
    st.write("**Features:**")
    st.write("- Add new memories")
    st.write("- Search similar memories")
    st.write("- Manage stored memories")
    st.markdown("---")
    st.write("**API Status:**")
    try:
        response = requests.get(f"{API_URL}/all_memories")
        if response.status_code == 200:
            st.success("✅ Connected")
        else:
            st.error("❌ Disconnected")
    except:
        st.error("❌ Disconnected")

# Main content with tabs
tab1, tab2, tab3 = st.tabs(["📝 Add Memory", "🔍 Search Memories", "📚 Manage Memories"])

with tab1:
    st.markdown('<div class="section-header">Add a New Memory</div>', unsafe_allow_html=True)
    with st.container():
        memory_text = st.text_area("Enter your memory or note:", height=150, placeholder="Write something meaningful to remember...")
        col1, col2, col3 = st.columns([1, 1, 3])
        with col1:
            add_button = st.button("➕ Add Memory", use_container_width=True)
        with col2:
            clear_button = st.button("🗑️ Clear", use_container_width=True)

        if clear_button:
            memory_text = ""
            st.rerun()

        if add_button:
            if memory_text.strip():
                with st.spinner("Storing memory..."):
                    response = requests.post(f"{API_URL}/ingest", json={"text": memory_text})
                if response.status_code == 200:
                    data = response.json()
                    st.success(f"✅ Memory stored successfully! ID: {data.get('id')}")
                    memory_text = ""
                else:
                    st.error("❌ Failed to store memory. Please try again.")
            else:
                st.warning("⚠️ Please enter some text before adding.")

with tab2:
    st.markdown('<div class="section-header">Search Your Memories</div>', unsafe_allow_html=True)
    with st.container():
        query_text = st.text_input("Enter your search query:", placeholder="What are you looking for?")
        col1, col2 = st.columns([1, 5])
        with col1:
            search_button = st.button("🔎 Search", use_container_width=True)

        if search_button:
            if query_text.strip():
                with st.spinner("Searching memories..."):
                    response = requests.post(
                        f"{API_URL}/context",
                        json={"query": query_text, "top_k": 5},
                    )
                if response.status_code == 200:
                    data = response.json()
                    contexts = data.get("context", [])
                    if contexts:
                        st.markdown("### 📋 Found Memories:")
                        for i, doc in enumerate(contexts, 1):
                            st.markdown(f'<div class="memory-card"><strong>{i}.</strong> {doc}</div>', unsafe_allow_html=True)
                    else:
                        st.info("ℹ️ No matching memories found. Try a different query.")
                else:
                    st.error("❌ Search failed. Please check your connection.")
            else:
                st.warning("⚠️ Please enter a search query.")

with tab3:
    st.markdown('<div class="section-header">Manage Your Memories</div>', unsafe_allow_html=True)
    with st.container():
        if st.button("🔄 Refresh Memories"):
            st.rerun()

        response = requests.get(f"{API_URL}/all_memories")
        if response.status_code == 200:
            data = response.json()
            documents = data.get("documents", [])
            ids = data.get("ids", [])
            if documents and ids:
                st.markdown(f"### 📚 All Memories ({len(documents)} total)")
                for i, (doc, doc_id) in enumerate(zip(documents, ids), 1):
                    with st.expander(f"Memory {i}: {doc[:50]}..."):
                        st.write(doc)
                        col1, col2 = st.columns([4, 1])
                        with col2:
                            if st.button("🗑️ Delete", key=f"del-{doc_id}"):
                                with st.spinner("Deleting..."):
                                    del_res = requests.delete(f"{API_URL}/delete", json={"id": doc_id})
                                if del_res.status_code == 200:
                                    st.success("✅ Memory deleted successfully!")
                                    st.rerun()
                                else:
                                    st.error("❌ Failed to delete memory.")
            else:
                st.info("ℹ️ No memories stored yet. Add some in the 'Add Memory' tab!")
        else:
            st.error("❌ Failed to fetch memories. Please check your connection.")


