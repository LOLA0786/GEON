import streamlit as st
from scrape import scrape_website , split_dom_content , clean_body_content , extract_body_content
from parse import parse_with_gemini

st.title("AI Web Scraper")
url = st.text_input("Enter Website Url")


if st.button("Scrape Site"):
    st.write("Scrapping the website")
    result = scrape_website(url)
    body_content = extract_body_content(result)
    cleaned_content = clean_body_content(body_content)

    st.session_state.dom_content = cleaned_content

    with st.expander("View DOM Content"):
        st.text_area("DOM Content" , cleaned_content, height=300)


if "dom_content" in st.session_state:
    parse_description = st.text_area("Describe what you want to parse?")
    # print("0")
    if st.button("Parse Content"):
        if parse_description:
            st.write("Parsing the content")
            # print("1")
            dom_chunks = split_dom_content(st.session_state.dom_content)
            # print(dom_chunks)
            # print("2")
            result = parse_with_gemini(st.session_state.dom_content , parse_description)
            # print(result)
            st.write(result)