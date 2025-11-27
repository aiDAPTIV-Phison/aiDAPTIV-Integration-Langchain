# aiDAPTIV Integrations - Langchain

## Dependencies
The python dependencies are listed as follows:
```
langchain
langchain-community
langchain-openai
pypdf
```

## Pre-requisites
1. Make sure that the aiDAPTIV server is hosted on `http://localhost:8000/v1` so that the application can work properly.

## Installation & Setup

1. Run (or double click) the `Langchain_Installer_1.0.0.exe` script to install and run the application (It may take some time to parse PDFs if there's any uploaded).
2. Choose `1. Build KV Cache (for accelerated inference)` by typing `1` to enhance the inference speed when conducting Q&A with your documents.
3. Choose `2. Chat with AI Assistant` by typing `2` when you're ready to chat with your assistant.
4. After selecting Option 2, you will be navigated to select which document to be used as context, select 1 document, then you can start chatting to get insights from the document selected.

## Example Flow
1. Start by building KV Cache to enhance the inference speed. (This may take a few minutes to process large documents)

```bash
Before you asks question, you may upload your PDF files to the `Example/Files/` directory, then restart this application.
Currently accessed files:
1. Biology-2-2.pdf
2. Biology-2-3.pdf
3. Biology-2-4.pdf
4. Biology-2-1.pdf

Actions available:
1. Build KV Cache (for accelerated inference)
2. Chat with AI Assistant
3. Quit
Please select your action: 1
Building KV Cache for 0 tokens
Done processing KV Cache for text 1. Time taken: X seconds.
Building KV Cache for 0 tokens
Finished KV Cache building for all documents, navigating back to the main menu...
```

2. You may now start chatting with your assistant with accelerated speed. First, select the document you want to know more about.

```bash
Currently accessed files:
1. Biology-2-1.pdf
2. Biology-2-2.pdf

Please select a file to act as reference for your Q&A: 1
====================================================================================================
You have entered the chat room, enter "Q" to quit this application.
====================================================================================================
Assistant:
Hello, how can I help you?

User:
```
3. Afterwards, you should start seeing the response being streamed after you type your question.

```bash
Currently accessed files:
1. Biology-2-1.pdf
2. Biology-2-2.pdf

Please select a file to act as reference for your Q&A: 1
====================================================================================================
You have entered the chat room, enter "Q" to quit this application.
====================================================================================================
Assistant:
Hello, how can I help you?

User: What is this document about?
Assistant:
This document is about cellular respiration, specifically covering the production of energy through cellular respiration, aerobic respiration, and fermentation. It includes definitions, explanations, and experiments related to these topics.
====================================================================================================
```
4. You can ask more questions about your documents. Type `q` or `Q` in the chat to exit the application. If that doesn't work you may try pressing `CTRL + C` to terminate the application.
