"""Original seed data for the Reading module question bank — 15 questions, 3 per type."""

SEED_QUESTIONS = [
    # ---------- MCQ SINGLE (3) ----------
    {
        "module": "reading", "q_type": "mcq_single", "difficulty": "easy", "tags": ["environment", "energy"],
        "title": "Solar Power Adoption",
        "passage": (
            "Over the past decade, the cost of solar panels has fallen by more than seventy percent, "
            "making solar energy one of the cheapest sources of electricity in many parts of the world. "
            "Governments in South Asia have begun offering subsidies to households that install rooftop "
            "solar systems, hoping to reduce dependence on imported fuel and ease pressure on aging power "
            "grids. Even so, adoption remains uneven: wealthier urban households install panels quickly, "
            "while rural communities often lack access to financing or reliable installation services."
        ),
        "content": {
            "question": "What does the passage identify as the main barrier to solar adoption in rural areas?",
            "options": [
                {"id": "A", "text": "Lack of sunlight in rural regions"},
                {"id": "B", "text": "Limited access to financing and installation services"},
                {"id": "C", "text": "Government bans on rural solar use"},
                {"id": "D", "text": "Higher electricity demand in cities"},
            ],
        },
        "correct_answer": {"option": "B"},
        "explanation": "The passage states rural communities 'often lack access to financing or reliable installation services.'",
    },
    {
        "module": "reading", "q_type": "mcq_single", "difficulty": "medium", "tags": ["business", "workplace"],
        "title": "Remote Work Productivity",
        "passage": (
            "A three-year study tracking over four thousand employees across twelve companies found that "
            "productivity, measured by completed tasks per week, remained statistically unchanged when staff "
            "moved from office-based to fully remote work. However, self-reported measures of collaboration "
            "quality declined noticeably, particularly among teams working on projects requiring frequent "
            "creative problem-solving. Researchers suggest that while remote work preserves individual output, "
            "it may quietly erode the informal exchanges that fuel innovation."
        ),
        "content": {
            "question": "According to the study, what aspect of work was most negatively affected by remote arrangements?",
            "options": [
                {"id": "A", "text": "Individual task completion"},
                {"id": "B", "text": "Employee salaries"},
                {"id": "C", "text": "Collaboration on creative problem-solving"},
                {"id": "D", "text": "Number of hours worked"},
            ],
        },
        "correct_answer": {"option": "C"},
        "explanation": "The passage notes collaboration quality declined, especially for creative problem-solving tasks.",
    },
    {
        "module": "reading", "q_type": "mcq_single", "difficulty": "hard", "tags": ["psychology"],
        "title": "The Paradox of Choice",
        "passage": (
            "Conventional economic theory holds that more options make consumers better off, since choice "
            "allows people to select the alternative that best matches their preferences. Yet a series of "
            "experiments found that shoppers presented with a smaller selection of jams were more likely to "
            "make a purchase, and reported greater satisfaction with their choice, than those presented with "
            "a much larger selection. Psychologists attribute this to decision fatigue and the fear of "
            "having chosen incorrectly when too many alternatives are available, a phenomenon now widely "
            "referred to as the paradox of choice."
        ),
        "content": {
            "question": "What did the jam experiment demonstrate?",
            "options": [
                {"id": "A", "text": "Consumers always prefer more options regardless of context"},
                {"id": "B", "text": "Smaller selections led to higher purchase rates and satisfaction"},
                {"id": "C", "text": "Larger selections reduced decision fatigue"},
                {"id": "D", "text": "Jam quality was the main factor in purchase decisions"},
            ],
        },
        "correct_answer": {"option": "B"},
        "explanation": "Shoppers with fewer options bought more and reported greater satisfaction, contradicting the assumption that more choice is always better.",
    },

    # ---------- MCQ MULTI (3) ----------
    {
        "module": "reading", "q_type": "mcq_multi", "difficulty": "medium", "tags": ["health", "science"],
        "title": "Sleep and Memory",
        "passage": (
            "Neuroscientists have long known that sleep plays a role in memory consolidation, but recent "
            "research clarifies which stages matter most. Deep, slow-wave sleep appears critical for "
            "transferring factual information from short-term to long-term storage, while REM sleep seems "
            "more closely tied to consolidating procedural skills, such as playing an instrument or riding a "
            "bicycle. Interestingly, the studies found no significant link between total sleep duration alone "
            "and memory performance; two people sleeping the same number of hours can show very different "
            "recall abilities depending on how much time they spend in each sleep stage."
        ),
        "content": {
            "question": "Which TWO statements are supported by the passage? (Select all that apply)",
            "options": [
                {"id": "A", "text": "Slow-wave sleep helps consolidate factual memory."},
                {"id": "B", "text": "REM sleep is linked to procedural skill consolidation."},
                {"id": "C", "text": "Total sleep duration alone predicts memory performance."},
                {"id": "D", "text": "People who sleep the same number of hours always recall equally well."},
            ],
        },
        "correct_answer": {"options": ["A", "B"]},
        "explanation": "The passage links slow-wave sleep to factual memory and REM sleep to procedural skills, and explicitly rejects C and D.",
    },
    {
        "module": "reading", "q_type": "mcq_multi", "difficulty": "medium", "tags": ["economics"],
        "title": "Inflation and Consumer Behavior",
        "passage": (
            "When inflation rises sharply, consumers often accelerate planned purchases, anticipating that "
            "prices will only continue climbing — a behavior economists call inflationary expectations at "
            "work. At the same time, discretionary spending on non-essential goods tends to decline as "
            "households redirect income toward necessities like food and housing. Central banks watch these "
            "shifting patterns closely, since a widespread rush to buy now can itself worsen inflation by "
            "increasing demand, creating a self-reinforcing cycle that is difficult to break through interest "
            "rate policy alone."
        ),
        "content": {
            "question": "Which TWO consumer behaviors does the passage associate with sharp inflation? (Select all that apply)",
            "options": [
                {"id": "A", "text": "Accelerating planned purchases"},
                {"id": "B", "text": "Reduced spending on non-essential goods"},
                {"id": "C", "text": "Increased saving in long-term investments"},
                {"id": "D", "text": "Complete avoidance of all purchases"},
            ],
        },
        "correct_answer": {"options": ["A", "B"]},
        "explanation": "The passage describes consumers buying sooner (A) while cutting discretionary spending (B); C and D are not mentioned.",
    },
    {
        "module": "reading", "q_type": "mcq_multi", "difficulty": "hard", "tags": ["biology"],
        "title": "Migratory Bird Navigation",
        "passage": (
            "How migratory birds navigate thousands of kilometers with remarkable precision has puzzled "
            "scientists for decades. Current research points to multiple mechanisms working in tandem: many "
            "species appear to sense the Earth's magnetic field through specialized proteins in their eyes, "
            "allowing them to perceive magnetic orientation almost as a visual overlay. Others rely partly on "
            "the position of the sun and stars as directional cues, recalibrating this internal compass at "
            "dawn and dusk. Notably, experiments show that when magnetic cues and celestial cues conflict, "
            "young birds on their first migration tend to prioritize the magnetic signal, while experienced "
            "birds increasingly rely on learned landmarks."
        ),
        "content": {
            "question": "Which TWO navigation mechanisms are described in the passage? (Select all that apply)",
            "options": [
                {"id": "A", "text": "Sensing Earth's magnetic field via eye proteins"},
                {"id": "B", "text": "Using the sun and stars as directional cues"},
                {"id": "C", "text": "Detecting changes in air pressure"},
                {"id": "D", "text": "Following scent trails left by other birds"},
            ],
        },
        "correct_answer": {"options": ["A", "B"]},
        "explanation": "The passage describes magnetic field sensing and celestial cues; air pressure and scent trails are not mentioned.",
    },

    # ---------- FILL IN THE BLANKS (word bank, 3) ----------
    {
        "module": "reading", "q_type": "fill_blanks", "difficulty": "easy", "tags": ["technology"],
        "title": "The Rise of Cloud Computing",
        "passage": (
            "Cloud computing allows businesses to rent computing power instead of {1} it. This shift has "
            "made it far {2} for small startups to launch products, since they no longer need to invest "
            "heavily in physical servers. As demand for a service grows, companies can {3} their resources "
            "almost instantly, paying only for what they actually use."
        ),
        "content": {"blank_count": 3, "word_bank": ["owning", "cheaper", "scale", "expensive", "reduce", "purchasing"]},
        "correct_answer": {"blanks": {"1": "owning", "2": "cheaper", "3": "scale"}},
        "explanation": "Context clues: 'rent...instead of {owning}', 'far {cheaper} for small startups', 'can {scale} their resources'.",
    },
    {
        "module": "reading", "q_type": "fill_blanks", "difficulty": "medium", "tags": ["environment"],
        "title": "Coral Reef Bleaching",
        "passage": (
            "When ocean temperatures rise even slightly above normal, coral polyps expel the colourful algae "
            "living in their tissues, a process known as {1}. Without these algae, the coral loses both its "
            "colour and a major source of {2}, leaving it vulnerable to disease. If temperatures return to "
            "normal quickly, reefs can sometimes {3}, but prolonged heat stress often causes permanent damage."
        ),
        "content": {"blank_count": 3, "word_bank": ["bleaching", "nutrition", "recover", "erosion", "collapse", "photosynthesis"]},
        "correct_answer": {"blanks": {"1": "bleaching", "2": "nutrition", "3": "recover"}},
        "explanation": "The passage defines 'bleaching', links algae loss to 'nutrition', and describes reefs that 'recover' if temperatures normalize.",
    },
    {
        "module": "reading", "q_type": "fill_blanks", "difficulty": "hard", "tags": ["linguistics"],
        "title": "How Languages Borrow Words",
        "passage": (
            "Languages rarely evolve in isolation; contact between cultures through trade, conquest, or "
            "migration routinely leads to {1}, where one language absorbs vocabulary from another. English, "
            "for instance, has {2} thousands of words from French following the Norman Conquest. Linguists "
            "note that borrowed words often {3} subtle shifts in meaning as they adapt to the sound patterns "
            "and grammar of the host language."
        ),
        "content": {"blank_count": 3, "word_bank": ["borrowing", "absorbed", "undergo", "isolation", "rejected", "prevent"]},
        "correct_answer": {"blanks": {"1": "borrowing", "2": "absorbed", "3": "undergo"}},
        "explanation": "Context: 'leads to {borrowing}', English has '{absorbed} thousands of words', borrowed words '{undergo} subtle shifts'.",
    },

    # ---------- R&W FILL IN THE BLANKS (dropdown, 3) ----------
    {
        "module": "reading", "q_type": "rw_fill_blanks", "difficulty": "medium", "tags": ["history", "economics"],
        "title": "The Silk Road's Legacy",
        "passage": (
            "For centuries, the network of trade routes known as the Silk Road did more than {1} goods "
            "between East and West; it also served as a conduit for ideas, religions, and technologies. "
            "Merchants travelling these routes {2} not only silk and spices but also papermaking techniques "
            "and astronomical knowledge. Historians now argue that the Silk Road's greatest {3} was not "
            "economic but cultural, reshaping how distant civilizations understood one another."
        ),
        "content": {
            "blank_count": 3,
            "dropdown_options": {
                "1": ["transport", "transported", "transports", "transporting"],
                "2": ["carry", "carried", "carries", "carrying"],
                "3": ["contribution", "contributes", "contributed", "contributing"],
            },
        },
        "correct_answer": {"blanks": {"1": "transport", "2": "carried", "3": "contribution"}},
        "explanation": "Grammar and meaning: 'did more than transport', past-tense narrative 'carried', and noun form 'greatest contribution'.",
    },
    {
        "module": "reading", "q_type": "rw_fill_blanks", "difficulty": "medium", "tags": ["science"],
        "title": "Vaccines and Herd Immunity",
        "passage": (
            "When a sufficient proportion of a population becomes {1} to an infectious disease, either "
            "through vaccination or prior infection, the pathogen struggles to {2} because it encounters "
            "fewer susceptible hosts. This protective effect, known as herd immunity, {3} even those who "
            "cannot be vaccinated for medical reasons, since the disease has fewer opportunities to spread."
        ),
        "content": {
            "blank_count": 3,
            "dropdown_options": {
                "1": ["immune", "immunity", "immunize", "immunizing"],
                "2": ["spread", "spreads", "spreading", "spread's"],
                "3": ["shields", "shield", "shielding", "shielded"],
            },
        },
        "correct_answer": {"blanks": {"1": "immune", "2": "spread", "3": "shields"}},
        "explanation": "Adjective form 'becomes immune', base verb after 'struggles to spread', present-tense verb 'shields'.",
    },
    {
        "module": "reading", "q_type": "rw_fill_blanks", "difficulty": "hard", "tags": ["philosophy"],
        "title": "The Ship of Theseus",
        "passage": (
            "The ancient thought experiment known as the Ship of Theseus {1} whether an object that has had "
            "all its components gradually replaced remains fundamentally the same object. If every plank of "
            "a ship is {2} over time, is the fully restored vessel still the original ship, or has it {3} "
            "into something new entirely? Philosophers continue to debate what this puzzle reveals about "
            "identity and continuity."
        ),
        "content": {
            "blank_count": 3,
            "dropdown_options": {
                "1": ["questions", "question", "questioning", "questioned"],
                "2": ["replaced", "replace", "replacing", "replaces"],
                "3": ["transformed", "transform", "transforming", "transforms"],
            },
        },
        "correct_answer": {"blanks": {"1": "questions", "2": "replaced", "3": "transformed"}},
        "explanation": "Subject-verb agreement 'experiment questions', passive construction 'is replaced', and 'has it transformed'.",
    },

    # ---------- RE-ORDER PARAGRAPHS (3) ----------
    {
        "module": "reading", "q_type": "reorder", "difficulty": "hard", "tags": ["science", "history"],
        "title": "The Discovery of Penicillin",
        "passage": None,
        "content": {
            "paragraphs": [
                {"id": "P1", "text": "In 1928, Alexander Fleming returned from a holiday to find that mould had contaminated one of his bacterial culture plates."},
                {"id": "P2", "text": "Rather than discarding it immediately, he noticed something unusual: the bacteria surrounding the mould had been destroyed."},
                {"id": "P3", "text": "This chance observation led Fleming to isolate the substance responsible, which he named penicillin after the Penicillium mould that produced it."},
                {"id": "P4", "text": "It would take another decade, and the work of chemists Howard Florey and Ernst Chain, before penicillin was purified and mass-produced for medical use."},
            ],
        },
        "correct_answer": {"order": ["P1", "P2", "P3", "P4"]},
        "explanation": "The paragraphs follow chronological cause and effect: contamination, observation, isolation, then large-scale development.",
    },
    {
        "module": "reading", "q_type": "reorder", "difficulty": "medium", "tags": ["business"],
        "title": "How a Startup Pivoted",
        "passage": None,
        "content": {
            "paragraphs": [
                {"id": "P1", "text": "The company originally built software for restaurant table reservations, but growth stalled after the first year."},
                {"id": "P2", "text": "While reviewing usage data, the founders noticed that many restaurants were using the messaging feature far more than the booking tool itself."},
                {"id": "P3", "text": "Acting on this insight, the team rebuilt the product around customer messaging, rebranding it as a communication platform for small businesses."},
                {"id": "P4", "text": "Within eighteen months, the pivot had tripled the company's user base and attracted its first round of institutional funding."},
            ],
        },
        "correct_answer": {"order": ["P1", "P2", "P3", "P4"]},
        "explanation": "The sequence moves from initial problem, to insight from data, to strategic pivot, to eventual outcome.",
    },
    {
        "module": "reading", "q_type": "reorder", "difficulty": "medium", "tags": ["history"],
        "title": "The Printing Press and Literacy",
        "passage": None,
        "content": {
            "paragraphs": [
                {"id": "P1", "text": "Before the fifteenth century, books were copied by hand, a slow process that kept literature scarce and expensive."},
                {"id": "P2", "text": "Johannes Gutenberg's development of the movable-type printing press dramatically reduced the time and cost required to reproduce a text."},
                {"id": "P3", "text": "As books became more affordable, literacy rates began climbing across Europe, no longer confined mainly to clergy and nobility."},
                {"id": "P4", "text": "This wider access to the written word is often credited with accelerating the spread of new scientific and political ideas in the centuries that followed."},
            ],
        },
        "correct_answer": {"order": ["P1", "P2", "P3", "P4"]},
        "explanation": "Sequence: the problem (scarce books), the invention that solved it, its immediate effect on literacy, then its longer-term consequence.",
    },
]
