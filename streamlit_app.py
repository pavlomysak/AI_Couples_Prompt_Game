import streamlit as st
import google.generativeai as genai

st.title("Couples AI Prompt Game")
st.write("""Deepen your connection and have fun exploring your relationship with this interactive game. What makes this game special? It’s completely personalized to your unique dynamic as a couple, powered by AI.

Here’s how it works:

1.) Start by answering a few questions together.
         
2.) Then, each partner will answer their own set of questions individually.
         
3.) Finally, hit "Generate Cards" to create custom prompts tailored just for you.
         
Get ready to laugh, reflect, and discover new things about each other!"""
)

google_api = st.secrets["API_KEY"]
genai.configure(api_key = google_api)
model = genai.GenerativeModel("gemini-1.5-pro")

# Input fields first
partner1 = st.text_input(label = "Name",
                         key = "Partner 1 Name")
partner2 = st.text_input(label = "Name",
                         key = "Partner 2 Name")


# Ensure inputs are filled before initializing tabs
if partner1 and partner2:
    both_partners, partner1_tab, partner2_tab, launch = st.tabs(["Intro Survey",
                                                                f"{partner1} Survey",
                                                                f"{partner2} Survey",
                                                                "Generate Cards"])

    with both_partners:

        time_together = st.text_input(label = "How long have you been together?")
        
        living_situation = st.selectbox(label = "What is your current living situation?",
                                        options = ["Living together",
                                                    "Living Separately but nearby",
                                                    "Long-Distance"])
        
        communication = st.selectbox(label = "Which best describes your communication style as a couple?",
                                    options = ["Calm and thoughtful",
                                                "Playful and humorous",
                                                "Direct and to the point",
                                                "Mixed, depends on the situation"])
        
        adventure = st.slider(label = "How adventurous are you as a couple? (Scale: 1 = prefer routines, 10 = love spontaneity)",
                            min_value = 1,
                            max_value = 10)

        anniversary = st.selectbox(label = "Do you celebrate an anniversary or specific milestones?",
                                    options = ["Yearly",
                                            "Occasionally (every few years)",
                                            "No, not really"])

        personality_similarity = st.selectbox(label = "Do you have similar or contrasting personalities?",
                                            options = ["Very similar",
                                                        "Somewhat similar",
                                                        "Very different"])
        
        plan_date = st.selectbox(label = "Who tends to plan dates or activities?",
                                options = ["One person always plans",
                                            "One person usually plans",
                                            "It's shared equally",
                                            "We rarely plan ahead"])

        shared_friends = st.selectbox("Do you have shared friends or separate friend groups?",
                                    options = ["Mostly shared",
                                                "Mostly separate",
                                                "A mix of both"])

        goals = st.selectbox("Are your long-term goals aligned?",
                            options = ["Yes, we agree on most things",
                                        "Somewhat aligned",
                                        "Not very aligned"])
        
        card_tone = st.segmented_control(label = "Preffered card tone",
                                        options = ["Thoughtful and deep",
                                                    "Lighthearted and playful",
                                                    "Romantic and intimate",
                                                    "A mix of all tones"])
        if card_tone == "A mix of all tones":
            card_tone = "A mix of thoughtful, deep, playful, lighthearted, romantic and intimate"

    # Initializing questions for partner 1

    with partner1_tab:
        
        occupation_1 = st.text_input(label = "Your occupation:",
                                    key = "Occupation_Partner1")
        
        hours_worked_1 = st.slider(label = "How many hours do you typically work in a week?", 
                                min_value = 0,
                                max_value = 60,
                                key = "Hours_Worked_Partner1")
        
        priorities_1 = st.multiselect("Which of these are priorities for you?",
                                    options = ["Career advancement",
                                                "Building a home and family",
                                                "Traveling and exploring",
                                                "Financial stability",
                                                "Pursuing hobbies or passions"],
                                                key = "Priorities_Partner1")

    # Initializing questions for partner 2

    with partner2_tab:
        
        occupation_2 = st.text_input(label = "Your occupation:",
                                    key = "Ocupation_Partner2")
        
        hours_worked_2 = st.slider(label = "How many hours do you typically work in a week?", 
                                min_value = 0,
                                max_value = 60,
                                key = "Hours_Worked_Partner2")
        
        priorities_2 = st.multiselect("Which of these are priorities for you?",
                                    options = ["Career advancement",
                                                "Building a home and family",
                                                "Traveling and exploring",
                                                "Financial stability",
                                                "Pursuing hobbies or passions"],
                                                key = "Priorities_Partner2")

    # Initializing function to generate personalized cards

    def generate_cards():
        
        prompt = f"""Create a personalized couples question game based on the following information about {partner1} and {partner2}:
                                        
                    - Relationship length: {time_together}
                    - Living situation: {living_situation}
                    - Communication style: {communication}
                    - Adventure/Spontaneity scale (1-10): {adventure}
                    - Anniversary celebration style: {anniversary}
                    - Personality similarity: {personality_similarity}
                    - Date planning habits: {plan_date}
                    - Shared friends: {shared_friends}
                    - Life goals: {goals}

                    {partner1}:
                    - Occupation: {occupation_1}
                    - Weekly hours worked: {hours_worked_1}
                    - Priorities: {priorities_1}
                                        
                    {partner2}:
                    - Occupation: {occupation_2}
                    - Weekly hours worked: {hours_worked_2}
                    - Priorities: {priorities_2}
                                        
                    Tailor the questions to deepen their relationship, foster communication, and address their unique dynamics. Use creative and insightful prompts. For example:
                                        
                    1. If one partner works long hours in a demanding field like investment banking, you might ask:  
                        *"What’s one thing [partner name] can do to make you feel more supported, even during their busiest weeks?"*
                                        
                    2. If the couple rates high on adventure/spontaneity, you might ask:  
                        *"What’s one spontaneous thing you’d love to plan together that neither of you has done before?"*
                                        
                    Generate questions in the tone of {card_tone} and return in a python list in the format rotating between partners:
                        
                    ```python
                    [
                        "Question for {partner1}: ...", 
                        "Question for {partner2}: ...",
                        "Question for {partner1}: ...",
                        "Question for {partner2}: ..."
                    ]
                """
        
        response = model.generate_content(prompt,
                                        generation_config = genai.GenerationConfig(response_mime_type = "application/json",
                                                                                response_schema = list[str])
                                        )
        
        return eval(response.text)

    # Initialize session state variables
    if "cards" not in st.session_state:
        st.session_state.cards = []  # Holds generated cards
    if "question_index" not in st.session_state:
        st.session_state.question_index = 0  # Tracks which card to display

    # Function to generate cards and store them in session state
    def handle_generate_cards():
        st.session_state.cards = generate_cards()
        st.session_state.question_index = 0  # Reset index to start at the first card

    # Function to go to the next question
    def handle_next_question():
        if st.session_state.question_index < len(st.session_state.cards) - 1:
            st.session_state.question_index += 1

    with launch:

        # Button to generate cards
        st.button(
            label="Click to Generate Cards",
            on_click=handle_generate_cards
        )

        # Display the current question
        if st.session_state.cards:
            st.write(st.session_state.cards[st.session_state.question_index])

            # Button to display the next card
            st.button(
                label="Next Card",
                on_click=handle_next_question
            )
        else:
            st.write("Click the button above to generate cards.")

else:
    st.warning("Please enter both partner names before continuing.")
