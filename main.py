from document_loader import load_documents
from semantic_search import semantic_search
from answer_generator import generate_answer

# Load documents from the folder
documents = load_documents("documents")

print("Dobby AI Ready!")

while True:
    query = input("\nAsk a question: ")

    # Exit condition
    if query.lower() == "exit":
        print("Goodbye!")
        break

    # Step 1: Find relevant sentences using semantic search
    results = semantic_search(query, documents)

    if results:
        print("\nSearching documents...\n")

        # Step 2: Combine sentences into context for AI
        context = ""

        for filename, sentence in results:
            context += sentence + " "

        # Step 3: Generate AI answer
        answer = generate_answer(query, context)

        print("AI Answer:\n")
        print(answer)

    else:
        print("No relevant information found.")
