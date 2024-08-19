import chromadb
import ollama

CHROMA_PATH = r"chroma_db"
chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = chroma_client.get_or_create_collection(name="Travel_Germany")

def analyze_query(query):
    system_prompt = """
    Analyze the given travel query and determine if it's more suitable for a backpacker or a travel expert. 
    Consider factors like duration, number of people, and any specific requests.
    Return your analysis in this format:
    Type: [Backpacker/Travel Expert]
    Reasoning: [Brief explanation]
    """
    
    response = ollama.chat(
        model="llama3.1",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query},
        ]
    )
    return response['message']['content']

def extract_keywords(query, travelType):
    system_prompt = f"""
        Extract key travel-related keywords from the given query. 
    Tailor the related questions based on the type of traveler: {travelType}.
    
    - For a backpacker, focus on budget-friendly options, solo travel, and accessible activities.
    - For a travel expert, focus on luxury experiences, group travel, and detailed itineraries.

    Generate ten related questions that would help in querying a travel database more effectively.

    Return your response in this format:
    Keywords: [comma-separated list of keywords]
    Related Questions:
    1. [First related question]
    2. [Second related question]
    3. [Third related question]
    4. [Four related question]
    5. [Fifth related question]
    6. [Sixth related question]
    7. [Seventh related question]
    8. [Eighth related question]
    9. [Ninth related question]
    10. [Ten related question]
    """
    
    response = ollama.chat(
        model="llama3.1",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query},
        ]
    )
    return response['message']['content']

def select_top_questions(questions, query):
    system_prompt = f"""
    Given the user query: "{query}"
    And the following related questions:
    {questions}
    
    Select the top 3 most relevant questions. Rank them based on how well they would help gather more useful information for travel planning.
    Return only the top 3 questions in order of relevance.
    """
    
    response = ollama.chat(
        model="llama3.1",
        messages=[
            {"role": "system", "content": system_prompt},
        ]
    )
    return response['message']['content'].split('\n')

def query_database(keywords):
    results = collection.query(
        query_texts=[keywords],
        n_results=5, 
        # include_metadata=True
    )

    # print(results)

    # Flatten the nested list of documents
    flattened_documents = [item for sublist in results['documents'] for item in sublist]
    
    # Join all the flattened document content into one string
    combined_results = ' '.join(flattened_documents)

    # print(combined_results)
     # If no documents are returned, return an empty string
    return combined_results if combined_results else ''

def generate_travel_advice(query, db_results, query_type, top_questions):
    context = "\n".join(db_results)
    system_prompt = f"""
    You are a travel advisor. Generate travel advice based on the user's query and the following context.
    Tailor your advice for a {query_type} and {top_questions}.
    
    User Query: {query}
    
    Context:
    {context}
    
    Provide a comprehensive travel plan including:
    1. Travel destination'outline & general information include trip roadmap.
    2. A day-by-day itinerary for the duration of the trip. For each day, break down the itinerary into:
        a. Morning activity/attraction
        b. Afternoon activity/attraction
        c. Evening activity/attraction  
    3. Suggestions for accommodation suitable for the traveler type and budget.
    4. Recommended activities and attractions.
    5. Transportation advice.
    6. Budget considerations and money-saving tips.
    7. Any specific considerations based on the query type and the provided information.

    Format your response clearly with headers for each section.
    """
    
    response = ollama.chat(
        model="llama3.1",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query},
        ]
    )
    return response['message']['content']

def generate_related_questions_from_advice(travel_advice):
    system_prompt = f"""
    Based on the following detailed travel advice:
    "{travel_advice}"

    Generate five related questions that the user might ask based on the advice provided. Tailor the questions to the user's preferences (e.g., backpacker or travel expert), and ensure the questions are specific to the itinerary, activities, or accommodations mentioned.

    Return the response in this format:
    Related Questions:
    1. [First question]
    2. [Second question]
    3. [Third question]
    4. [Fourth question]
    5. [Fifth question]
    """
    
    response = ollama.chat(
        model="llama3.1",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": travel_advice},
        ]
    )
    return response['message']['content']

def main():
    user_query = input("What are your travel plans?\n")
    
    # Step 1: Analyze Query
    analysis = analyze_query(user_query)
    print("\nQuery Analysis:")
    print(analysis)
    query_type = analysis.split("\n")[0].split(": ")[1]
    
    # Step 2: Extract Keywords and Generate Related Questions
    keyword_info = extract_keywords(user_query, query_type)
    keyword_lines = keyword_info.split('\n')

    # Check if the expected format is present before splitting
    # Handling the potential * or other unexpected characters before Keywords:
    for line in keyword_lines:
        if "Keywords" in line:
            # Clean any unexpected characters like * and then split
            clean_line = line.replace('*', '').strip()  # Remove any * and strip spaces
            if ": " in clean_line:
                keywords = clean_line.split(": ")[1].strip()
            else:
                keywords = "No keywords found"
            break
    else:
        keywords = "No keywords found"

    print("\nKeyword Extraction and Related Questions:")
    print(keyword_info)
    # keywords = keyword_info.split("\n")[0].split(": ")[1]

    # Display Related Questions for User
    all_questions = keyword_lines[3:]  # Skip the first three lines
    print(all_questions)
    top_questions = select_top_questions("\n".join(all_questions), user_query)
    
    # Step 3: Query Database
    db_results = query_database(keywords)
    print("\nDatabase Query Results:")
    print(db_results)
    
    # Step 4: Generate Travel Advice
    travel_advice = generate_travel_advice(user_query, db_results, query_type, top_questions)
    print("\n\nTravel Advice:")
    print(travel_advice)
    
    # Step 5: Generate Related Questions Based on Travel Advice
    related_questions = generate_related_questions_from_advice(travel_advice)
    
    print("\nWould you like to know more about:")
    for question in related_questions.split("\n"):
        if question.startswith("Related Questions:"):
            continue
        print(question.strip())

if __name__ == "__main__":
    main()