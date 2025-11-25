# aiDAPTIV Integrations - Langchain

## Installation & Setup

1. Run (or double click) the `setup.bat` script to install and run the application (It may take some time to parse PDFs if there's any uploaded). 
2. Choose `1. Build KV Cache (for accelerated inference)` by typing `1` to enhance the inference speed when conducting Q&A with your documents.
3. Choose `2. Chat with AI Assistant` by typing `2` when you're ready to chat with your assistant.
4. After selecting Option 2, you will be navigated to select which document to be used as context, select 1 document, then you can start chatting to get insights from the document selected.

## Example Flow
1. Start by building KV Cache to enhance the inference speed.

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
Building KV Cache for 10413 tokens
Done processing KV Cache for text 1. Time taken: X seconds.
Building KV Cache for 11152 tokens
Done processing KV Cache for text 2. Time taken: X seconds.
Building KV Cache for 11075 tokens
Done processing KV Cache for text 3. Time taken: X seconds.
Building KV Cache for 10433 tokens
Done processing KV Cache for text 4. Time taken: X seconds.
```

2. You may now start chatting with your assistant with accelerated speed. First, select the document you want to know more about.

```bash
Currently accessed files:
1. Biology-2-2.pdf
2. Biology-2-3.pdf
3. Biology-2-4.pdf
4. Biology-2-1.pdf

Please select a file to act as reference for your Q&A: 4
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
1. Biology-2-2.pdf
2. Biology-2-3.pdf
3. Biology-2-4.pdf
4. Biology-2-1.pdf

Please select a file to act as reference for your Q&A: 4
====================================================================================================
You have entered the chat room, enter "Q" to quit this application.
====================================================================================================
Assistant:
Hello, how can I help you?

User: What is this document about?
Assistant:
This document is about cellular respiration, which is described in Chapter 7. It covers the production of energy through cellular respiration, the types of cellular respiration (including aerobic respiration and fermentation), and conducts experiments to study these processes. Specifically, it discusses the breakdown of glucose in the presence or absence of oxygen to produce energy, and examines different scenarios such as fermentation in yeast, human muscle cells, and plants.
====================================================================================================
```
4. You can ask more questions about your documents. Type `q` or `Q` in the chat to exit the application. If that doesn't work you may try pressing `CTRL + C` to terminate the application.
