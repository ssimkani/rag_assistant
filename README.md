# RAG Assistant

## Description

This Chatbot is a RAG Assistant using Gemini 2.5 Flash to answer user queries based on personalized notes. Delivers well-structured and accurate answers and uses relevant information from a dedicated notes section.

## Features

- [Gemini 2.5 Flash](https://aistudio.google.com/welcome?utm_source=google&utm_medium=cpc&utm_campaign=FY25-global-DR-gsem-BKWS-1710442&utm_content=text-ad-none-any-DEV_c-CRE_726057516126-ADGP_Hybrid%20%7C%20BKWS%20-%20EXA%20%7C%20Txt-Gemini-Gemini%20API-KWID_2262542020022-kwd-2262542020022&utm_term=KW_google%20gemini%20api-ST_google%20gemini%20api&gclsrc=aw.ds&gad_source=1&gad_campaignid=20866959509&gbraid=0AAAAACn9t67mGVo7Hugjw-mjdHUOQc419&gclid=CjwKCAiAjc7KBhBvEiwAE2BDOf4LW3f38f4RUV9IeE91tkVvPBI3onikXjcEOMsJNaJTI54SCFg-hBoC8SQQAvD_BwE) under the hood
- Retrieval-Augmented Generation (RAG) pipeline using [Pinecone](pinecone.io) as a vector database
- User authentication using [Firebase](firebase.google.com) to personalize notes
- [Streamlit UI](https://streamlit.io/) for ease of use

## Website

The link for the website is here: [RAG Assistant](https://assistant-llm.streamlit.app/)

## How RAG Works

[Image](https://media.geeksforgeeks.org/wp-content/uploads/20250210190608027719/How-Rag-works.webp) of how RAG works.

------------------------------------------------------------------------------------------------

When the user submits their notes and clicks save, The notes are split into chunks which are embedded into vector representations and stored in a vector database (Pinecone). Then, when the user send a new query, the chatbot retrieves the most semantically relevant chunks from the vector database and generates a response based on these chunks. The length of chunks and the amount used in a single response is pre-configured to optimize response quality.
