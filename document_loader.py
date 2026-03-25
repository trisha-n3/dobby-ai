# document_loader.py
import os
import fitz  # PyMuPDF

def load_documents(folder_path="documents"):
    documents = []

    # Load from folder as before
    if os.path.exists(folder_path):
        for filename in os.listdir(folder_path):
            filepath = os.path.join(folder_path, filename)

            if filename.endswith(".txt"):
                with open(filepath, "r", encoding="utf-8") as f:
                    text = f.read()
                documents.append({"text": text, "source": filename})

            elif filename.endswith(".pdf"):
                doc = fitz.open(filepath)
                text = ""
                for page in doc:
                    text += page.get_text()
                documents.append({"text": text, "source": filename})

    return documents


def load_uploaded_file(uploaded_file):
    # This handles files uploaded directly from Streamlit UI
    if uploaded_file.name.endswith(".pdf"):
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        return {"text": text, "source": uploaded_file.name}

    elif uploaded_file.name.endswith(".txt"):
        text = uploaded_file.read().decode("utf-8")
        return {"text": text, "source": uploaded_file.name}

    return None