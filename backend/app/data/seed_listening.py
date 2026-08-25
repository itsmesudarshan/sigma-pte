"""
Original seed data for the Listening module — 15 questions across 4 types.

Audio is generated live in-browser via the free Web Speech Synthesis API
from content.audio_text — no audio files, uploads, or recording required.
"""

SEED_LISTENING = [
    # ---------- MULTIPLE CHOICE (5) ----------
    {
        "module": "listening", "q_type": "l_mcq_single", "difficulty": "easy", "tags": ["environment"],
        "title": "Listening MCQ: City Recycling Program",
        "passage": (
            "The city council announced a new recycling program that will provide every household with "
            "a separate bin for food waste starting next month. Officials say the change is expected to "
            "cut landfill waste by nearly thirty percent within the first year."
        ),
        "content": {
            "audio_text": (
                "The city council announced a new recycling program that will provide every household with "
                "a separate bin for food waste starting next month. Officials say the change is expected to "
                "cut landfill waste by nearly thirty percent within the first year."
            ),
            "question": "According to the audio, what is the city hoping to achieve with the new bins?",
            "options": [
                {"id": "A", "text": "Increase recycling company profits"},
                {"id": "B", "text": "Reduce landfill waste by about 30%"},
                {"id": "C", "text": "Replace all household bins with digital sensors"},
                {"id": "D", "text": "Ban food waste entirely"},
            ],
        },
        "correct_answer": {"option": "B"},
        "explanation": "The audio states the change is expected to cut landfill waste by nearly thirty percent.",
    },
    {
        "module": "listening", "q_type": "l_mcq_single", "difficulty": "medium", "tags": ["business"],
        "title": "Listening MCQ: Company Merger",
        "passage": (
            "Two of the region's largest logistics companies announced plans to merge next year, a move "
            "analysts say will create the largest freight operator in the country. The combined company "
            "expects to cut costs by consolidating overlapping warehouse networks, though some employees "
            "have expressed concern about potential job losses during the transition."
        ),
        "content": {
            "audio_text": (
                "Two of the region's largest logistics companies announced plans to merge next year, a move "
                "analysts say will create the largest freight operator in the country. The combined company "
                "expects to cut costs by consolidating overlapping warehouse networks, though some employees "
                "have expressed concern about potential job losses during the transition."
            ),
            "question": "What concern do some employees have about the merger?",
            "options": [
                {"id": "A", "text": "Lower product quality"},
                {"id": "B", "text": "Potential job losses"},
                {"id": "C", "text": "Reduced warehouse space"},
                {"id": "D", "text": "Higher shipping costs"},
            ],
        },
        "correct_answer": {"option": "B"},
        "explanation": "The audio states employees have expressed concern about potential job losses during the transition.",
    },
    {
        "module": "listening", "q_type": "l_mcq_single", "difficulty": "medium", "tags": ["health"],
        "title": "Listening MCQ: Sleep Study Results",
        "passage": (
            "A new study following over two thousand adults found that those who maintained a consistent "
            "sleep schedule, going to bed and waking at the same time daily, reported better overall mood "
            "and concentration than those with irregular sleep patterns, even when total sleep duration was "
            "similar between the two groups."
        ),
        "content": {
            "audio_text": (
                "A new study following over two thousand adults found that those who maintained a consistent "
                "sleep schedule, going to bed and waking at the same time daily, reported better overall mood "
                "and concentration than those with irregular sleep patterns, even when total sleep duration was "
                "similar between the two groups."
            ),
            "question": "What was the key finding of the study?",
            "options": [
                {"id": "A", "text": "Total sleep duration is the only factor that matters"},
                {"id": "B", "text": "Consistent sleep schedules improved mood and concentration"},
                {"id": "C", "text": "Irregular sleepers slept more hours overall"},
                {"id": "D", "text": "Sleep schedule has no effect on mood"},
            ],
        },
        "correct_answer": {"option": "B"},
        "explanation": "The study found consistent schedules linked to better mood and concentration, independent of total sleep duration.",
    },
    {
        "module": "listening", "q_type": "l_mcq_single", "difficulty": "hard", "tags": ["economics"],
        "title": "Listening MCQ: Currency Fluctuation",
        "passage": (
            "Central bank officials cautioned that the recent sharp depreciation of the national currency "
            "was driven primarily by external factors, including rising global interest rates, rather than "
            "domestic economic mismanagement. They noted that similar currencies in the region experienced "
            "comparable declines over the same period, suggesting the trend reflects broader market forces."
        ),
        "content": {
            "audio_text": (
                "Central bank officials cautioned that the recent sharp depreciation of the national currency "
                "was driven primarily by external factors, including rising global interest rates, rather than "
                "domestic economic mismanagement. They noted that similar currencies in the region experienced "
                "comparable declines over the same period, suggesting the trend reflects broader market forces."
            ),
            "question": "What did officials say caused the currency's decline?",
            "options": [
                {"id": "A", "text": "Domestic economic mismanagement"},
                {"id": "B", "text": "External factors like global interest rates"},
                {"id": "C", "text": "A decision to devalue the currency deliberately"},
                {"id": "D", "text": "A drop in national exports"},
            ],
        },
        "correct_answer": {"option": "B"},
        "explanation": "Officials attributed the decline primarily to external factors such as rising global interest rates.",
    },
    {
        "module": "listening", "q_type": "l_mcq_single", "difficulty": "easy", "tags": ["education"],
        "title": "Listening MCQ: School Schedule Change",
        "passage": (
            "Starting in September, the school district will shift its start time for high schools to nine "
            "a.m., an hour later than the current schedule. The decision follows research showing teenagers "
            "benefit academically from later start times due to natural shifts in their sleep cycles."
        ),
        "content": {
            "audio_text": (
                "Starting in September, the school district will shift its start time for high schools to nine "
                "a.m., an hour later than the current schedule. The decision follows research showing teenagers "
                "benefit academically from later start times due to natural shifts in their sleep cycles."
            ),
            "question": "Why is the school district changing the start time?",
            "options": [
                {"id": "A", "text": "To reduce transportation costs"},
                {"id": "B", "text": "Because teenagers benefit academically from later start times"},
                {"id": "C", "text": "To align with elementary school schedules"},
                {"id": "D", "text": "Due to a shortage of teachers"},
            ],
        },
        "correct_answer": {"option": "B"},
        "explanation": "The audio cites research showing teenagers benefit academically from later start times due to sleep-cycle shifts.",
    },

    # ---------- FILL IN THE BLANKS (4) ----------
    {
        "module": "listening", "q_type": "l_fill_blanks", "difficulty": "medium", "tags": ["technology"],
        "title": "Listening Fill in the Blanks: Battery Technology",
        "passage": "Researchers have developed a new battery {1} that charges twice as fast as current models while lasting significantly {2}. The technology could reach consumer devices within {3} years.",
        "content": {
            "audio_text": "Researchers have developed a new battery technology that charges twice as fast as current models while lasting significantly longer. The technology could reach consumer devices within three years.",
            "blank_count": 3,
        },
        "correct_answer": {"blanks": {"1": "technology", "2": "longer", "3": "three"}},
        "explanation": "Listen for: 'battery technology', 'lasting significantly longer', and 'within three years'.",
    },
    {
        "module": "listening", "q_type": "l_fill_blanks", "difficulty": "medium", "tags": ["nature"],
        "title": "Listening Fill in the Blanks: Ocean Currents",
        "passage": "Ocean currents play a crucial role in {1} heat around the planet, moving warm water from the {2} toward the poles. Disruptions to these currents could significantly {3} regional climate patterns.",
        "content": {
            "audio_text": "Ocean currents play a crucial role in distributing heat around the planet, moving warm water from the equator toward the poles. Disruptions to these currents could significantly alter regional climate patterns.",
            "blank_count": 3,
        },
        "correct_answer": {"blanks": {"1": "distributing", "2": "equator", "3": "alter"}},
        "explanation": "Listen for: 'distributing heat', 'warm water from the equator', and 'significantly alter regional climate patterns'.",
    },
    {
        "module": "listening", "q_type": "l_fill_blanks", "difficulty": "hard", "tags": ["business"],
        "title": "Listening Fill in the Blanks: Startup Funding",
        "passage": "The startup secured a new round of {1} led by two venture capital firms, valuing the company at over one billion dollars. The funds will be used to {2} into new international markets and {3} its engineering team.",
        "content": {
            "audio_text": "The startup secured a new round of funding led by two venture capital firms, valuing the company at over one billion dollars. The funds will be used to expand into new international markets and grow its engineering team.",
            "blank_count": 3,
        },
        "correct_answer": {"blanks": {"1": "funding", "2": "expand", "3": "grow"}},
        "explanation": "Listen for: 'round of funding', 'expand into new international markets', and 'grow its engineering team'.",
    },
    {
        "module": "listening", "q_type": "l_fill_blanks", "difficulty": "easy", "tags": ["daily life"],
        "title": "Listening Fill in the Blanks: Community Garden",
        "passage": "The neighborhood association is opening a community {1} where residents can grow their own vegetables. Plots will be available on a {2} basis, and beginners are {3} to attend a free workshop first.",
        "content": {
            "audio_text": "The neighborhood association is opening a community garden where residents can grow their own vegetables. Plots will be available on a first-come basis, and beginners are encouraged to attend a free workshop first.",
            "blank_count": 3,
        },
        "correct_answer": {"blanks": {"1": "garden", "2": "first-come", "3": "encouraged"}},
        "explanation": "Listen for: 'community garden', 'first-come basis', and 'beginners are encouraged'.",
    },

    # ---------- SELECT MISSING WORD (3) ----------
    {
        "module": "listening", "q_type": "select_missing_word", "difficulty": "medium", "tags": ["business"],
        "title": "Select Missing Word: Quarterly Results",
        "passage": "The recording discusses quarterly results and ends abruptly, missing its final word.",
        "content": {
            "audio_text": "This quarter's results show steady growth across all departments, with particularly strong gains in overseas markets. Analysts attribute much of this success to increased",
            "question": "Select the word that completes the recording.",
            "options": [
                {"id": "A", "text": "revenue"},
                {"id": "B", "text": "expenses"},
                {"id": "C", "text": "employees"},
                {"id": "D", "text": "delays"},
            ],
        },
        "correct_answer": {"option": "A"},
        "explanation": "The recording discusses quarterly growth and success, ending on the logical word 'revenue'.",
    },
    {
        "module": "listening", "q_type": "select_missing_word", "difficulty": "easy", "tags": ["weather"],
        "title": "Select Missing Word: Weather Report",
        "passage": "The forecast ends abruptly, missing its final word.",
        "content": {
            "audio_text": "Tomorrow will bring clear skies across most of the region, with temperatures reaching a comfortable twenty-two degrees by",
            "question": "Select the word that completes the recording.",
            "options": [
                {"id": "A", "text": "midnight"},
                {"id": "B", "text": "afternoon"},
                {"id": "C", "text": "January"},
                {"id": "D", "text": "yesterday"},
            ],
        },
        "correct_answer": {"option": "B"},
        "explanation": "A temperature forecast for 'tomorrow' logically refers to a time later that day, such as 'afternoon'.",
    },
    {
        "module": "listening", "q_type": "select_missing_word", "difficulty": "hard", "tags": ["science"],
        "title": "Select Missing Word: Research Announcement",
        "passage": "The recording ends abruptly, missing its final word.",
        "content": {
            "audio_text": "The research team plans to publish their complete findings next year, following further trials designed to confirm the initial results were not due to",
            "question": "Select the word that completes the recording.",
            "options": [
                {"id": "A", "text": "celebration"},
                {"id": "B", "text": "chance"},
                {"id": "C", "text": "funding"},
                {"id": "D", "text": "publicity"},
            ],
        },
        "correct_answer": {"option": "B"},
        "explanation": "Confirming results 'were not due to chance' is standard scientific phrasing for ruling out a random/coincidental result.",
    },

    # ---------- WRITE FROM DICTATION (3) ----------
    {
        "module": "listening", "q_type": "write_from_dictation", "difficulty": "medium", "tags": ["general"],
        "title": "Write From Dictation: Meeting Reschedule",
        "passage": None,
        "content": {"audio_text": "The meeting has been rescheduled to next Thursday afternoon."},
        "correct_answer": {"text": "The meeting has been rescheduled to next Thursday afternoon."},
        "explanation": "Type exactly what you hear, word for word, including correct spelling.",
    },
    {
        "module": "listening", "q_type": "write_from_dictation", "difficulty": "easy", "tags": ["general"],
        "title": "Write From Dictation: Office Supplies",
        "passage": None,
        "content": {"audio_text": "Please order more paper for the printer before Friday."},
        "correct_answer": {"text": "Please order more paper for the printer before Friday."},
        "explanation": "Type exactly what you hear, word for word, including correct spelling.",
    },
    {
        "module": "listening", "q_type": "write_from_dictation", "difficulty": "hard", "tags": ["academic"],
        "title": "Write From Dictation: Research Deadline",
        "passage": None,
        "content": {"audio_text": "The final draft of the research paper is due by the end of the month."},
        "correct_answer": {"text": "The final draft of the research paper is due by the end of the month."},
        "explanation": "Type exactly what you hear, word for word, including correct spelling.",
    },
]
