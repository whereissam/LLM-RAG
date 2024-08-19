# Travel Agent

## Pre-request

1. Go to [Ollama](https://ollama.com/), install it.
2. Run `ollama run llama3.1`
3. Run `ollama serve`

## Install

```bash
pip install -r requirements.txt
```

## Create Database

```bash
python3 fill_db.py
```

## Run Query

```bash
python3 ask1.py
```

## Test

```bash
What are your travel plans?
I want to visit Germany for five days alone. My bedget is low. Can you provide a plan?

Query Analysis:
Type: Backpacker
Reasoning: The query indicates that the traveler has a limited budget, plans to travel solo, and wants a trip of relatively short duration (five days). This profile aligns with typical backpacker characteristics who tend to seek affordable accommodations and transportation. A travel expert might require more detailed information or guidance on navigating complex logistics like public transport systems, cultural nuances, and specific activities tailored to the traveler's interests.

Keyword Extraction and Related Questions:
Based on your query, I've extracted the following key travel-related keywords:

Keywords: budget, solo, backpacker, Germany, 5-day trip

As a backpacker, I'll focus on providing you with budget-friendly options for solo travel in Germany.

Travel Advice:
Germany can be an affordable destination if planned carefully. Here's a suggested 5-day itinerary for solo travel in Germany on a low budget:

**Day 1: Arrival in Berlin**

* Fly into Berlin Schönefeld Airport (SXF) or Tegel Airport (TXL)
* Take the public transportation ( buses or trains) to your accommodation ( approx. €2-3)
* Check-in at a hostel or guesthouse like Meininger Berlin (from €15/night) or Generator Berlin Prenzlauer Berg (from €20/night)
* Explore the city and visit the Brandenburg Gate, which is free to visit
* Grab a traditional German currywurst from a street food stall for around €3

**Day 2: Berlin**

* Visit the Berlin Wall Memorial (free admission) at Bernauer Strasse
* Take a stroll along the Spree River and explore the trendy neighborhoods of Kreuzberg or Neukölln
* Visit the Museum Island, which is free to visit on Sundays or with a museum pass ( approx. €18/ person for 5 days)
* Enjoy a traditional German dinner at a restaurant like Curry 36 (from €10)

**Day 3: Travel to Dresden**

* Take an early train from Berlin Hauptbahnhof to Dresden Hauptbahnhof (approx. €30-40, depending on the type of train and seat selection)
* Check-in at a hostel or guesthouse like Meininger Dresden (from €15/night) or A&O Dresden (from €20/night)
* Visit the Zwinger Palace and Gardens (free admission), which is one of the most beautiful baroque palaces in Germany
* Explore the historic city center, including the famous Frauenkirche

**Day 4: Dresden**

* Visit the Semperoper opera house (approx. €10-15 for a guided tour)
* Take a stroll along the Elbe River and enjoy the scenic views of the city
* Visit the Albertinum museum (free admission), which features an impressive collection of European art from the 19th and early 20th centuries
* Enjoy a traditional German dinner at a restaurant like Restaurant Wenzel (from €15)

**Day 5: Return to Berlin or Explore More**

* Take the train back to Berlin or continue exploring Dresden's surroundings, such as the picturesque Saxon Switzerland National Park

Budget Breakdown:

* Flights from your location to Berlin and back (approx. €100-200)
* Accommodation for 4 nights (€60-80)
* Transportation (trains and public transportation): approx. €50-70
* Food: around €20-30 per day, for a total of €100-150
* Attractions and activities: around €20-30 per person, for a total of €100-150

Total estimated cost for the 5-day trip: around €410-630

Tips:

* Consider purchasing a German Rail Pass (approx. €50-70) if you plan to take multiple trains during your trip
* Book your accommodation and transportation in advance to get the best prices
* Look for free walking tours or guided tours that offer discounted admission fees
* Enjoy traditional German food and drinks, but be mindful of your budget

This itinerary should give you a good taste of Germany's culture, history, and natural beauty while keeping costs relatively low.

Would you like to know more about:
1. What are the best options for accommodation in Dresden, considering I'm on a tight budget?
2. Can I get a German Rail Pass that covers the entire country or is it limited to specific regions?
3. Are there any free walking tours or guided tours available in Berlin and Dresden that can help me save money on attractions?
4. How do I get from Berlin Hauptbahnhof to Tegel Airport (TXL) if I have a flight departing from there?
5. Can you recommend some alternative activities or attractions in the Saxon Switzerland National Park, as it might be too long of a day trip from Dresden?
```
