import chromadb
import ollama

CHROMA_PATH = r"chroma_db"
chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = chroma_client.get_or_create_collection(name="Travel_Germany")

def check_query_completeness(query):
    system_prompt = """
    Analyze the given travel query. Check if it contains all essential details: destination, duration, and budget.
    If any are missing, ask for the missing information in a natural, conversational way.
    If all essential details are present, respond with 'Complete'.
    Format your response as:
    Status: [Incomplete/Complete]
    Response: [Your natural language question or 'None' if complete]
    """
    
    response = ollama.chat(
        model="llama3.1",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query},
        ]
    )
    return response['message']['content']

def parse_llm_response(response):
    lines = response.split('\n')
    result = {}
    for line in lines:
        if ':' in line:
            key, value = line.split(':', 1)
            result[key.strip()] = value.strip()
    return result

def analyze_query(query):
    system_prompt = """
    Analyze the given travel query and determine if it's more suitable for a backpacker or a travel expert. 
    Consider these criteria:
    - Backpacker: Mentions traveling alone, having only a bag, budget constraints, or seeking budget-friendly options.
    - Travel Expert: Mentions traveling with family/friends, seeking luxury experiences, or planning a more complex itinerary.
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

def extract_keywords_and_questions(query):
    system_prompt = """
    Extract key travel-related keywords from the given query. 
    The keywords MUST include at least:
    1. Where (destination, can be as broad as a country)
    2. When (time of travel, can be a season if specific dates aren't given or 'not provided')

    Also, generate five related questions that would help in querying a travel database more effectively.
    
    Return your response in this exact format:
    Keywords: [comma-separated list of keywords]
    Where: [extracted destination]
    When: [extracted time of travel or 'not provided']
    Budget: [extracted budget or 'not provided']
    Sufficiency: [Sufficient/Insufficient]
    Missing Information: [List any missing key information from the three required fields or 'None']
    Related Questions:
    1. [Question 1]
    2. [Question 2]
    3. [Question 3]
    4. [Question 4]
    5. [Question 5]
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
        n_results=2
    )
    return results['documents'][0] if results['documents'] else []

def generate_travel_advice(query_info, db_results, query_type):
    context = "\n".join(db_results)
    
    system_prompt = f"""
    You are a travel advisor. Generate a **detailed day-by-day travel itinerary** for the following traveler.
    Tailor your advice for a {query_type}.
    
    Destination: {query_info['destination']}
    Duration: {query_info['duration']} days
    
    Context:
    {context}
    
    For each day, break down the itinerary into:
    1. Morning activity/attraction
    2. Afternoon activity/attraction
    3. Evening activity/attraction
    
    Also, provide recommendations for:
    - Accommodation based on the traveler type and budget
    - Transportation advice
    - Budget tips and suggestions for saving money
    """
    
    response = ollama.chat(
        model="llama3.1",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Plan a detailed trip to {query_info['destination']} for {query_info['duration']} days with a {query_info['budget']} budget."}
        ]
    )
    
    return response['message']['content']


def main():
    user_query = input("What are your travel plans?\n")
    
    # Extract Keywords and Generate Related Questions
    keyword_info = extract_keywords_and_questions(user_query)
    keyword_lines = keyword_info.split('\n')

    print(keyword_lines)
    # Parse the keyword information
    keywords = next((line.split(": ")[1] for line in keyword_lines if line.startswith("Keywords:")), "")
    where = next((line.split(": ")[1] for line in keyword_lines if line.startswith("Where:")), "")
    when = next((line.split(": ")[1] for line in keyword_lines if line.startswith("When:")), "")
    # budget = next((line.split(": ")[1] for line in keyword_lines if line.startswith("Budget:")), "")
    sufficiency = next((line.split(": ")[1] for line in keyword_lines if line.startswith("Sufficiency:")), "Insufficient")
    missing_info = next((line.split(": ")[1] for line in keyword_lines if line.startswith("Missing Information:")), "")
    return 

    # If information is insufficient, ask for missing details
    while sufficiency == "Insufficient":
        print(f"I need more information. {missing_info}")
        additional_info = input("Please provide the missing details: ")
        user_query += " " + additional_info
        keyword_info = extract_keywords_and_questions(user_query)
        keyword_lines = keyword_info.split('\n')
        keywords = next((line.split(": ")[1] for line in keyword_lines if line.startswith("Keywords:")), "")
        where = next((line.split(": ")[1] for line in keyword_lines if line.startswith("Where:")), "")
        when = next((line.split(": ")[1] for line in keyword_lines if line.startswith("When:")), "")
        # budget = next((line.split(": ")[1] for line in keyword_lines if line.startswith("Budget:")), "")
        sufficiency = next((line.split(": ")[1] for line in keyword_lines if line.startswith("Sufficiency:")), "Insufficient")
        missing_info = next((line.split(": ")[1] for line in keyword_lines if line.startswith("Missing Information:")), "")

        # If information is insufficient, but the user has already stated they don't know details like dates, skip asking
        if missing_info == 'None' or ('When' in missing_info and 'not provided' in when):
            sufficiency = 'Sufficient'
        
        if sufficiency == "Sufficient":
            print("Proceeding with the trip plan...")
            # Proceed with querying the database and generating the plan
            db_results = query_database(keywords)
            travel_advice = generate_travel_advice({"destination": where, "duration": "5", "budget": budget}, db_results, "backpacker")
            print("\nTravel Advice:")
            print(travel_advice)
        else:
            print(f"I still need more information: {missing_info}")

    print("\nKeyword Extraction and Related Questions:")
    print(keyword_info)
    print("\n\n---------------------\n\n")

    # Analyze Query
    analysis = analyze_query(user_query)
    query_type = analysis.split("\n")[0].split(": ")[1]
    print("\nQuery Analysis:")
    print(analysis)
    print("\n\n---------------------\n\n")

    # Determine if we can provide a specific or general trip plan
    plan_type_prompt = f"""
    Based on the following information, determine if we should provide a specific or general trip plan:
    User Query: {user_query}
    Extracted Keywords: {keywords}
    Keyword Sufficiency: {sufficiency}
    Query Type: {query_type}

    If the information is sufficient for a specific plan, respond with 'Specific'.
    If the information is only sufficient for a general plan, respond with 'General'.
    Include a brief explanation for your decision.

    Format your response as:
    Plan Type: [Specific/General]
    Explanation: [Your explanation]
    """
    
    plan_type_response = ollama.chat(
        model="llama3.1",
        messages=[
            {"role": "system", "content": plan_type_prompt},
        ]
    )
    
    # Parse the response manually to handle potential inconsistencies
    response_content = plan_type_response['message']['content']
    plan_type = 'General'  # Default to General if we can't determine
    if 'Plan Type:' in response_content:
        plan_type = response_content.split('Plan Type:')[1].split('\n')[0].strip()
    
    # Query Database
    print(keyword_info)
    db_results = query_database(keyword_info)
    print("\nDatabase Query Results:")
    print(db_results)
    print("\n\n---------------------\n\n")
    
    # Generate Travel Advice
    if plan_type.lower() == 'specific':
        travel_advice = generate_specific_travel_advice(user_query, db_results, query_type)
    else:
        travel_advice = generate_general_travel_advice(user_query, db_results, query_type)
    
    print("\nTravel Advice:")
    print(travel_advice)
    print("\n\n---------------------\n\n")
    
    # Display Related Questions for User
    all_questions = keyword_lines[3:]  # Skip the first three lines
    top_questions = select_top_questions("\n".join(all_questions), user_query)
    
    print("\nWould you like to know more about:")
    for question in top_questions:
        print(question)

def generate_specific_travel_advice(query, db_results, query_type):
    context = "\n".join(db_results)
    system_prompt = f"""
    You are a travel advisor. Generate specific travel advice based on the following query and context.
    Tailor your advice for a {query_type}.
    
    User Query: {query}
    
    Context:
    {context}
    
    Provide a comprehensive travel plan including:
    1. A day-by-day itinerary for the duration of the trip.
    2. Suggestions for accommodation suitable for the traveler type and budget.
    3. Recommended activities and attractions.
    4. Transportation advice.
    5. Budget considerations and money-saving tips.
    6. Any specific considerations based on the query type and the provided information.

    Format your response clearly with headers for each section.
    """
    
    response = ollama.chat(
        model="llama3.1",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ]
    )
    return response['message']['content']

def generate_general_travel_advice(query, db_results, query_type):
    context = "\n".join(db_results)
    system_prompt = f"""
    You are a travel advisor. Generate general travel advice based on the following query and context.
    Tailor your advice for a {query_type}.
    
    User Query: {query}
    
    Context:
    {context}
    
    Provide a general travel plan including:
    1. Suggested regions or cities to visit.
    2. General activities and attractions suitable for the timeframe mentioned (if any).
    3. General transportation advice.
    4. Budget considerations and money-saving tips.
    5. Any specific considerations based on the query type and the provided information.

    Format your response clearly with headers for each section.
    """
    
    response = ollama.chat(
        model="llama3.1",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ]
    )
    return response['message']['content']

if __name__ == "__main__":
    main()