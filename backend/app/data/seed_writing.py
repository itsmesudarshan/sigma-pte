"""
Original seed data for the Writing module: Summarize Written Text and Essay.

key_points: list of "ideas" the response should touch on. Each idea is a
list of acceptable keyword/synonym variants — used for the keyword-coverage
heuristic that blends with (or substitutes for) AI scoring.
"""

SEED_WRITING = [
    {
        "module": "writing",
        "q_type": "swt",
        "difficulty": "medium",
        "tags": ["technology", "education"],
        "title": "Summarize: The Shift to Online Learning",
        "passage": (
            "The rapid expansion of online learning platforms over the past decade has fundamentally "
            "changed how many students access education. Unlike traditional classrooms, which require "
            "physical attendance at fixed times, online courses allow learners to study at their own pace, "
            "often from anywhere in the world. This flexibility has proven especially valuable for working "
            "adults and people in remote areas who previously had limited access to quality instruction. "
            "However, critics point out that online learning also demands a level of self-discipline and "
            "independent motivation that not every student possesses, and that the lack of face-to-face "
            "interaction can leave some learners feeling isolated. Despite these concerns, enrollment in "
            "online courses continues to grow steadily each year, suggesting that the benefits of "
            "accessibility and flexibility are, for many, outweighing the drawbacks of reduced personal "
            "contact. Educational institutions are increasingly investing in hybrid models that attempt to "
            "combine the convenience of online study with periodic in-person engagement, aiming to capture "
            "the advantages of both approaches while mitigating their respective weaknesses."
        ),
        "content": {
            "key_points": [
                ["online learning", "online courses", "online education", "e-learning"],
                ["flexibility", "flexible", "own pace", "anywhere"],
                ["working adults", "remote areas", "accessibility", "access"],
                ["self-discipline", "motivation", "independent"],
                ["isolated", "isolation", "lack of interaction", "face-to-face"],
                ["hybrid", "combine", "growing", "enrollment"],
            ],
        },
        "correct_answer": None,
        "explanation": (
            "A strong summary is a single sentence, 5-75 words, capturing that online learning offers "
            "flexibility and accessibility but requires self-discipline and can feel isolating, with "
            "institutions now moving toward hybrid models."
        ),
    },
    {
        "module": "writing",
        "q_type": "swt",
        "difficulty": "hard",
        "tags": ["environment", "policy"],
        "title": "Summarize: Urban Green Spaces",
        "passage": (
            "City planners around the world are increasingly recognizing the value of urban green spaces, "
            "not merely as aesthetic additions but as essential infrastructure for public health and "
            "environmental resilience. Parks, tree-lined streets, and community gardens have been shown to "
            "reduce urban heat island effects, where concrete and asphalt absorb and radiate heat, making "
            "cities significantly warmer than surrounding rural areas. Beyond temperature regulation, green "
            "spaces improve air quality by filtering pollutants and provide measurable mental health "
            "benefits, with studies linking regular access to nature with reduced stress and anxiety levels "
            "among city residents. Despite this growing body of evidence, many rapidly expanding cities in "
            "developing regions continue to prioritize commercial and residential construction over green "
            "space preservation, often citing the high cost of land as a barrier. Some urban planners argue "
            "that this short-term economic reasoning ultimately proves costly, since the public health and "
            "climate adaptation expenses associated with green-space-poor cities frequently exceed the "
            "value of the land that would have been set aside."
        ),
        "content": {
            "key_points": [
                ["green spaces", "parks", "urban green"],
                ["heat island", "temperature", "cooling", "heat"],
                ["air quality", "pollutants", "filtering"],
                ["mental health", "stress", "anxiety"],
                ["developing regions", "construction", "land cost", "commercial"],
                ["long-term", "costly", "climate adaptation", "public health expenses"],
            ],
        },
        "correct_answer": None,
        "explanation": (
            "A strong summary captures that urban green spaces provide health, cooling, and air-quality "
            "benefits, yet are often sacrificed for construction in developing cities despite the long-term "
            "costs of that trade-off."
        ),
    },
    {
        "module": "writing",
        "q_type": "essay",
        "difficulty": "medium",
        "tags": ["technology", "society"],
        "title": "Essay: Should Governments Regulate Artificial Intelligence?",
        "passage": (
            "Some people believe that artificial intelligence should be tightly regulated by governments to "
            "prevent misuse and protect jobs, while others argue that heavy regulation will stifle "
            "innovation and put countries at a competitive disadvantage. Discuss both views and give your "
            "own opinion."
        ),
        "content": {
            "key_points": [
                ["regulation", "regulate", "government control", "oversight"],
                ["innovation", "stifle", "competitive", "progress"],
                ["jobs", "employment", "automation", "workforce"],
                ["misuse", "safety", "risk", "harm"],
                ["balance", "middle ground", "both views"],
                ["opinion", "believe", "argue", "in my view"],
            ],
        },
        "correct_answer": None,
        "explanation": (
            "A strong essay presents the regulation argument (safety, job protection) and the "
            "innovation/competitiveness counter-argument, develops both with specific reasoning or "
            "examples, and closes with a clear, well-supported personal position — in 200-300 words across "
            "clear paragraphs with a variety of connective devices."
        ),
    },
    {
        "module": "writing",
        "q_type": "essay",
        "difficulty": "hard",
        "tags": ["education", "policy"],
        "title": "Essay: Standardized Testing in University Admissions",
        "passage": (
            "Many universities are reconsidering the role of standardized test scores in admissions "
            "decisions, with some institutions dropping the requirement entirely in favor of a more holistic "
            "review of applicants. To what extent do you agree or disagree that standardized tests should "
            "remain a required part of university admissions?"
        ),
        "content": {
            "key_points": [
                ["standardized test", "test scores", "exam scores"],
                ["holistic", "well-rounded", "broader review"],
                ["fairness", "equity", "socioeconomic", "access"],
                ["objective", "measure", "comparison", "consistency"],
                ["agree", "disagree", "extent", "position"],
                ["universities", "admissions", "applicants"],
            ],
        },
        "correct_answer": None,
        "explanation": (
            "A strong essay takes a clear position on whether standardized tests should remain required, "
            "supports it with reasoning around fairness, objectivity, or access, acknowledges the opposing "
            "view, and stays within 200-300 words with a coherent four-paragraph structure."
        ),
    },
]
