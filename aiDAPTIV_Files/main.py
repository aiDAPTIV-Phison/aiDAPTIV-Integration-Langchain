from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

import os 
import httpx
import time


OPENAI_BASE_URL = os.getenv('OPENAI_BASE_URL', None)
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'EMPTY')
OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'model')
if OPENAI_BASE_URL is None:
    raise ValueError("Please provide a valid `OPENAI_BASE_URL`.")
EXAMPLE_DOCS_FILE_DIR = './Example/Files'
CONTEXT_LENGTH_LIMIT = 40000 # by char size


def count_tokens(text: str) -> int:
    """
    Helper function to count tokens given a text body
    
    Args:
        text: The text to be tokenized and counted
    Returns:
        int: Token count of the text provided
    """
    try:
        payload = {
            'model': OPENAI_MODEL,
            'prompt': text,
        }
        base_url = OPENAI_BASE_URL.replace('/v1', '')
        response = httpx.post(f'{base_url}/tokenize', json=payload)
        response.raise_for_status()
        data = response.json()
        
        return data['count']

    except httpx.HTTPStatusError:
        print(f"Something went wrong when counting text token count. \nPayload: {payload}\nStatus Code: {response.status_code}\nResponse:\n{response.text}")


def load_pdf(file_path: str) -> list[str]:
    """
    Parse PDF into string given a directory/file
    
    Args:
        file_path: The file path to the documents, can be a directory or file path directly to PDF
    Returns:
        list[str]: A list of document string that is parsed from the PDFs
    """
    docs = []
    if os.path.isdir(file_path):
        files = os.listdir(file_path)
    else:
        files = [file_path]

    # parse each PDF to text
    for file in files:
        loader = PyPDFLoader(f"{EXAMPLE_DOCS_FILE_DIR}/{file}")
        parsed = loader.load()

        print(f"Length of documents pages: {len(parsed)}")
        pdf_content = ""
        for page in parsed:
            pdf_content += (page.page_content + "\n\n")
        
        # restrict doc length limit to prevent out of context window
        if len(pdf_content) > CONTEXT_LENGTH_LIMIT:
            pdf_content = pdf_content[:CONTEXT_LENGTH_LIMIT]

        num_tokens = count_tokens(pdf_content)
        print(f"Document tokens: {num_tokens}")
        docs.append(pdf_content)
    
    return docs


def format_context_as_system_msg(context: str) -> SystemMessage:
    """
    Format the system message based on the context given for consistency to ensure prefix cache is aligned

    Args:
        context: The document content to be used as context to answer question
    
    Returns:
        SystemMessage: The system template represented by Langchain SystemMessage object
    """
    if context == "":
        context = "No context given"
    system_msg = SystemMessage(content=f"{context}\nThe above is the context provided to answer the user question. If you do not know how to answer the user question, please specify that you do not know since the context did not contain the relevant information.")
    
    return system_msg


def build_kv_cache(docs: list[str]):
    """
    Get the files in the directory and build KV Cache for accelerated inference
        Did not use asynchronous processing to avoid crashing the LLM server
    
    Args:
        docs: A list of document string (context) to be processed
    """

    llm = ChatOpenAI(
        base_url=OPENAI_BASE_URL,
        api_key=OPENAI_API_KEY,
        model=OPENAI_MODEL,
        temperature=0,
        max_completion_tokens=5, # just to go through prefill to store KV Cache
    )
    
    for index, doc in enumerate(docs):
        tokens_count = count_tokens(doc)
        print(f"Building KV Cache for {tokens_count} tokens")
        system_msg = format_context_as_system_msg(doc)
        human_msg = HumanMessage(content="Hi") # random text to pass the inference
        message = [
            system_msg,
            human_msg,
        ]
        
        start_time = time.perf_counter()
        _ = llm.invoke(message)
        end_time = time.perf_counter()
        
        print(f"Done processing KV Cache for text {index + 1}. Tiem taken: {end_time - start_time:.4f} seconds.")

    print("Finished KV Cache building for all documents")


def main():
    """Main entrypoint to the application"""
    chat_history = []
    docs = load_pdf(EXAMPLE_DOCS_FILE_DIR) 
    llm = ChatOpenAI(
        base_url=OPENAI_BASE_URL,
        api_key=OPENAI_API_KEY,
        model=OPENAI_MODEL,
    )
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("aiDAPTIV Langchain Integration")
        print("Before you asks question, you may upload your PDF files to the `Example/Files/` directory, then restart this application.")
        print("Currently accessed files:")
        for index, file in enumerate(os.listdir(EXAMPLE_DOCS_FILE_DIR)):
            print(f"{index + 1}. {file}")
        print()
        
        print("Actions available:")
        print("1. Build KV Cache (for accelerated inference)")
        print("2. Chat with AI Assistant")
        print("3. Quit")

        try:
            action = input("Please select your action: ").strip()
            if int(action) == 1:
                build_kv_cache(docs) 
            
            elif int(action) == 2:
                # chatting interface
                os.system('cls' if os.name == 'nt' else 'clear')
                
                # print accessed files if there's file inside
                selected_context = ""
                number_of_docs_currently = os.listdir(EXAMPLE_DOCS_FILE_DIR)
                if len(number_of_docs_currently) > 0: 
                    print("Currently accessed files:")
                    for index, file in enumerate(number_of_docs_currently):
                        print(f"{index + 1}. {file}")
                    print()
                
                    selected_file = input('Please select a file to act as reference for your Q&A: ').strip()
                    try:
                        selected_file = int(selected_file)
                        selected_file -= 1
                        if selected_file < 0:
                            print("You have entered invalid choice for file selection.")
                        
                        selected_context = docs[selected_file]
                        
                    except ValueError:
                        print("Invalid input for file selection")
                        continue 
                    
                    except IndexError:
                        print("File does not exists")
                        continue
                
                # chat loop
                first_message = True
                print("=" * 100)
                print("You have entered the chat room, enter \"Q\" to quit this application.")
                print("=" * 100)
                while True:
                    if first_message:
                        system_msg = format_context_as_system_msg(selected_context)
                        chat_history.append(system_msg)
                        print("Assistant:\nHello, how can I help you?\n")
                        first_message = False

                    # detect exit signal
                    user_question = input("User: ").strip()
                    if user_question.lower() == 'q':
                        return 
                    
                    chat_history.append(HumanMessage(content=user_question))

                    # output the response
                    full_response = ""
                    print("Assistant:")
                    for chunk in llm.stream(chat_history):
                        print(chunk.content, end="", flush=True)
                        full_response += chunk.content
                    chat_history.append(AIMessage(content=full_response))
                    
                    print()
                    print("=" * 100, end="")
                    print("\n")
                    
            elif int(action) == 3:
                print("Application exitting...")
                return 
            
            else:
                raise ValueError()
            
        except ValueError:
            print("Your selected action is invalid.")
            continue


if __name__ == '__main__':
    main()
