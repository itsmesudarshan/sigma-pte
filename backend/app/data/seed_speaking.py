"""Original seed data for the Speaking module: 5 Read Aloud, 5 Repeat Sentence, 5 Answer Short Question."""

SEED_SPEAKING = [
    # ---------- READ ALOUD (5) ----------
    {
        "module": "speaking", "q_type": "read_aloud", "difficulty": "easy", "tags": ["business"],
        "title": "Read Aloud: Workplace Flexibility",
        "passage": "Many companies now offer employees the choice to work from home several days a week. This shift has changed how teams communicate and collaborate on shared projects.",
        "content": {"prep_seconds": 25, "record_seconds": 40},
        "correct_answer": None,
        "explanation": "Read the text aloud clearly at a natural pace, matching the words and order shown exactly.",
    },
    {
        "module": "speaking", "q_type": "read_aloud", "difficulty": "medium", "tags": ["science"],
        "title": "Read Aloud: Renewable Energy",
        "passage": "Wind and solar power have become increasingly affordable over the past decade, prompting many countries to set ambitious targets for reducing their reliance on fossil fuels.",
        "content": {"prep_seconds": 30, "record_seconds": 40},
        "correct_answer": None,
        "explanation": "Focus on clear pronunciation of technical terms like 'renewable' and steady, even pacing.",
    },
    {
        "module": "speaking", "q_type": "read_aloud", "difficulty": "easy", "tags": ["travel"],
        "title": "Read Aloud: Airport Announcement",
        "passage": "Passengers travelling to Chicago should proceed to gate fourteen, where boarding will begin shortly. Please have your travel documents ready for inspection.",
        "content": {"prep_seconds": 25, "record_seconds": 35},
        "correct_answer": None,
        "explanation": "Read with clear enunciation of place names and numbers, at an even, announcement-style pace.",
    },
    {
        "module": "speaking", "q_type": "read_aloud", "difficulty": "hard", "tags": ["medicine"],
        "title": "Read Aloud: Medical Research Findings",
        "passage": "The clinical trial demonstrated a statistically significant reduction in symptoms among participants receiving the experimental treatment, compared with those given a placebo.",
        "content": {"prep_seconds": 35, "record_seconds": 45},
        "correct_answer": None,
        "explanation": "Pay close attention to multisyllabic words like 'statistically' and 'experimental', maintaining natural sentence stress.",
    },
    {
        "module": "speaking", "q_type": "read_aloud", "difficulty": "medium", "tags": ["culture"],
        "title": "Read Aloud: Museum Exhibition",
        "passage": "The new exhibition explores three centuries of maritime history through paintings, artifacts, and personal letters recovered from shipwrecks along the coast.",
        "content": {"prep_seconds": 30, "record_seconds": 40},
        "correct_answer": None,
        "explanation": "Focus on smooth linking between words and clear pronunciation of 'maritime' and 'artifacts'.",
    },

    # ---------- REPEAT SENTENCE (5) ----------
    {
        "module": "speaking", "q_type": "repeat_sentence", "difficulty": "easy", "tags": ["general"],
        "title": "Repeat Sentence: Library Hours",
        "passage": "The library will be closed for renovations starting next Monday.",
        "content": {"record_seconds": 15},
        "correct_answer": None,
        "explanation": "Repeat the sentence exactly as heard, preserving word order and content.",
    },
    {
        "module": "speaking", "q_type": "repeat_sentence", "difficulty": "medium", "tags": ["business"],
        "title": "Repeat Sentence: Quarterly Report",
        "passage": "The quarterly report shows a significant increase in overseas sales figures.",
        "content": {"record_seconds": 15},
        "correct_answer": None,
        "explanation": "Repeat the sentence exactly as heard, preserving word order and content.",
    },
    {
        "module": "speaking", "q_type": "repeat_sentence", "difficulty": "easy", "tags": ["daily life"],
        "title": "Repeat Sentence: Weather Forecast",
        "passage": "It is expected to rain heavily throughout the afternoon and evening.",
        "content": {"record_seconds": 12},
        "correct_answer": None,
        "explanation": "Repeat the sentence exactly as heard, preserving word order and content.",
    },
    {
        "module": "speaking", "q_type": "repeat_sentence", "difficulty": "hard", "tags": ["academic"],
        "title": "Repeat Sentence: Research Methodology",
        "passage": "The researchers controlled for several confounding variables before analyzing the results.",
        "content": {"record_seconds": 16},
        "correct_answer": None,
        "explanation": "Repeat the sentence exactly as heard, preserving word order and content, including technical vocabulary.",
    },
    {
        "module": "speaking", "q_type": "repeat_sentence", "difficulty": "medium", "tags": ["transportation"],
        "title": "Repeat Sentence: Train Delay",
        "passage": "The train service has been delayed due to unexpected signal failures.",
        "content": {"record_seconds": 14},
        "correct_answer": None,
        "explanation": "Repeat the sentence exactly as heard, preserving word order and content.",
    },

    # ---------- ANSWER SHORT QUESTION (5) ----------
    {
        "module": "speaking", "q_type": "answer_short_question", "difficulty": "easy", "tags": ["general knowledge"],
        "title": "Answer Short Question: Seasons",
        "passage": "What is the season right before winter called?",
        "content": {"acceptable_answers": ["autumn", "fall"], "record_seconds": 10},
        "correct_answer": None,
        "explanation": "Expected answer: 'autumn' or 'fall'.",
    },
    {
        "module": "speaking", "q_type": "answer_short_question", "difficulty": "easy", "tags": ["general knowledge"],
        "title": "Answer Short Question: Reading Material",
        "passage": "What do you call a place where you can borrow books for free?",
        "content": {"acceptable_answers": ["library"], "record_seconds": 10},
        "correct_answer": None,
        "explanation": "Expected answer: 'library'.",
    },
    {
        "module": "speaking", "q_type": "answer_short_question", "difficulty": "medium", "tags": ["science"],
        "title": "Answer Short Question: Planets",
        "passage": "Which planet in our solar system is known as the Red Planet?",
        "content": {"acceptable_answers": ["mars"], "record_seconds": 10},
        "correct_answer": None,
        "explanation": "Expected answer: 'Mars'.",
    },
    {
        "module": "speaking", "q_type": "answer_short_question", "difficulty": "easy", "tags": ["daily life"],
        "title": "Answer Short Question: Timepieces",
        "passage": "What instrument do you use to tell the time?",
        "content": {"acceptable_answers": ["clock", "watch"], "record_seconds": 10},
        "correct_answer": None,
        "explanation": "Expected answer: 'clock' or 'watch'.",
    },
    {
        "module": "speaking", "q_type": "answer_short_question", "difficulty": "medium", "tags": ["nature"],
        "title": "Answer Short Question: Insects",
        "passage": "What is the name of the insect known for producing honey?",
        "content": {"acceptable_answers": ["bee", "honeybee"], "record_seconds": 10},
        "correct_answer": None,
        "explanation": "Expected answer: 'bee' or 'honeybee'.",
    },

    # ---------- DESCRIBE IMAGE (5) — original chart data, no real photos ----------
    {
        "module": "speaking", "q_type": "describe_image", "difficulty": "medium", "tags": ["business"],
        "title": "Describe Image: Quarterly Sales",
        "passage": "Describe the bar chart, including the trend it shows and any notable figures.",
        "content": {
            "prep_seconds": 25, "record_seconds": 40,
            "chart_type": "bar", "chart_title": "Quarterly Sales ($M)",
            "chart_data": [
                {"label": "Q1", "value": 12}, {"label": "Q2", "value": 18},
                {"label": "Q3", "value": 15}, {"label": "Q4", "value": 24},
            ],
            "key_points": [
                ["bar chart", "graph", "chart"], ["quarterly", "quarter", "q1", "q2", "q3", "q4"],
                ["sales", "revenue"], ["increase", "rise", "growth", "highest"],
                ["q3", "decline", "drop", "dip"], ["overall", "trend", "upward"],
            ],
        },
        "correct_answer": None,
        "explanation": "A strong response names the chart type, walks through the quarterly figures, notes the Q3 dip, and summarizes the overall upward trend.",
    },
    {
        "module": "speaking", "q_type": "describe_image", "difficulty": "medium", "tags": ["environment"],
        "title": "Describe Image: Renewable Energy Mix",
        "passage": "Describe the pie chart, including the largest and smallest segments.",
        "content": {
            "prep_seconds": 25, "record_seconds": 40,
            "chart_type": "pie", "chart_title": "Energy Sources (%)",
            "chart_data": [
                {"label": "Solar", "value": 35}, {"label": "Wind", "value": 30},
                {"label": "Hydro", "value": 20}, {"label": "Other", "value": 15},
            ],
            "key_points": [
                ["pie chart", "chart", "graph"], ["solar", "largest", "biggest"],
                ["wind", "second"], ["hydro"], ["other", "smallest"], ["percent", "percentage", "share"],
            ],
        },
        "correct_answer": None,
        "explanation": "A strong response identifies the chart type, names each segment with its approximate share, and highlights solar as the largest and 'other' as the smallest.",
    },
    {
        "module": "speaking", "q_type": "describe_image", "difficulty": "hard", "tags": ["demographics"],
        "title": "Describe Image: Population Growth Trend",
        "passage": "Describe the line graph, including how the trend changes over time.",
        "content": {
            "prep_seconds": 25, "record_seconds": 40,
            "chart_type": "line", "chart_title": "City Population (thousands)",
            "chart_data": [
                {"label": "2000", "value": 120}, {"label": "2010", "value": 180},
                {"label": "2020", "value": 210}, {"label": "2025", "value": 215},
            ],
            "key_points": [
                ["line graph", "chart", "graph"], ["population", "grow", "growth", "increase"],
                ["2000", "2010", "2020", "2025"], ["steady", "steep", "sharp"],
                ["plateau", "slow", "leveling", "flatten"],
            ],
        },
        "correct_answer": None,
        "explanation": "A strong response describes the steady rise from 2000-2020 and notes the growth flattening between 2020 and 2025.",
    },
    {
        "module": "speaking", "q_type": "describe_image", "difficulty": "easy", "tags": ["education"],
        "title": "Describe Image: Student Enrollment by Subject",
        "passage": "Describe the bar chart comparing enrollment across subjects.",
        "content": {
            "prep_seconds": 25, "record_seconds": 40,
            "chart_type": "bar", "chart_title": "Enrollment by Subject",
            "chart_data": [
                {"label": "Science", "value": 320}, {"label": "Arts", "value": 180},
                {"label": "Business", "value": 260}, {"label": "Engineering", "value": 300},
            ],
            "key_points": [
                ["bar chart", "graph", "chart"], ["science", "highest", "most"],
                ["arts", "lowest", "least"], ["business", "engineering"], ["subject", "enrollment", "students"],
            ],
        },
        "correct_answer": None,
        "explanation": "A strong response names the chart type, compares the four subjects, and identifies Science as highest and Arts as lowest.",
    },
    {
        "module": "speaking", "q_type": "describe_image", "difficulty": "hard", "tags": ["health"],
        "title": "Describe Image: Hospital Wait Times",
        "passage": "Describe the line graph showing wait time changes across the day.",
        "content": {
            "prep_seconds": 25, "record_seconds": 40,
            "chart_type": "line", "chart_title": "Average Wait Time (minutes)",
            "chart_data": [
                {"label": "8am", "value": 15}, {"label": "12pm", "value": 45},
                {"label": "4pm", "value": 60}, {"label": "8pm", "value": 25},
            ],
            "key_points": [
                ["line graph", "chart", "graph"], ["wait time", "waiting"],
                ["morning", "8am", "lowest", "shortest"], ["afternoon", "4pm", "peak", "highest", "longest"],
                ["evening", "8pm", "decrease", "drop"],
            ],
        },
        "correct_answer": None,
        "explanation": "A strong response traces the rise from morning to a mid-afternoon peak, then the drop by evening, naming approximate values.",
    },
]
