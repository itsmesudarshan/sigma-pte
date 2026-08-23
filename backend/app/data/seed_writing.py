"""Original seed data for the Writing module: 8 Summarize Written Text + 7 Essay."""

SEED_WRITING = [
    # ---------- SUMMARIZE WRITTEN TEXT (8) ----------
    {
        "module": "writing", "q_type": "swt", "difficulty": "medium", "tags": ["technology", "education"],
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
            "combine the convenience of online study with periodic in-person engagement."
        ),
        "content": {"key_points": [
            ["online learning", "online courses", "online education", "e-learning"],
            ["flexibility", "flexible", "own pace", "anywhere"],
            ["working adults", "remote areas", "accessibility", "access"],
            ["self-discipline", "motivation", "independent"],
            ["isolated", "isolation", "lack of interaction", "face-to-face"],
            ["hybrid", "combine", "growing", "enrollment"],
        ]},
        "correct_answer": None,
        "explanation": "A strong summary captures flexibility/accessibility, the self-discipline/isolation trade-off, and the move toward hybrid models — in one sentence, 5-75 words.",
    },
    {
        "module": "writing", "q_type": "swt", "difficulty": "hard", "tags": ["environment", "policy"],
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
            "space preservation, often citing the high cost of land as a barrier."
        ),
        "content": {"key_points": [
            ["green spaces", "parks", "urban green"],
            ["heat island", "temperature", "cooling", "heat"],
            ["air quality", "pollutants", "filtering"],
            ["mental health", "stress", "anxiety"],
            ["developing regions", "construction", "land cost", "commercial"],
        ]},
        "correct_answer": None,
        "explanation": "A strong summary captures the health, cooling, and air-quality benefits of green spaces alongside the construction trade-off in developing cities.",
    },
    {
        "module": "writing", "q_type": "swt", "difficulty": "medium", "tags": ["business"],
        "title": "Summarize: The Four-Day Work Week",
        "passage": (
            "Trials of a four-day work week across several countries have produced results that surprised "
            "many economists. Companies that reduced working hours without cutting pay reported little to "
            "no drop in output, and in some cases even saw productivity rise, as employees returned to work "
            "more rested and focused. Employee wellbeing metrics improved substantially, with participants "
            "reporting lower stress and better work-life balance. However, the model has proven harder to "
            "implement in sectors requiring continuous staffing, such as healthcare and retail, where "
            "reducing hours for one worker simply shifts the burden onto colleagues unless additional staff "
            "are hired, raising costs that smaller businesses may struggle to absorb."
        ),
        "content": {"key_points": [
            ["four-day work week", "reduced hours", "shorter week"],
            ["productivity", "output", "unchanged", "increased"],
            ["wellbeing", "stress", "work-life balance"],
            ["healthcare", "retail", "continuous staffing"],
            ["costs", "hiring", "smaller businesses"],
        ]},
        "correct_answer": None,
        "explanation": "A strong summary notes maintained/improved productivity and wellbeing gains, balanced against implementation difficulty in continuous-staffing sectors.",
    },
    {
        "module": "writing", "q_type": "swt", "difficulty": "medium", "tags": ["science", "health"],
        "title": "Summarize: Gut Bacteria and Mood",
        "passage": (
            "Emerging research suggests that the trillions of bacteria living in the human gut may influence "
            "mood and mental health more than previously understood. These microorganisms produce "
            "neurotransmitters, including a significant portion of the body's serotonin, and communicate "
            "with the brain via the vagus nerve in what scientists now call the gut-brain axis. Studies on "
            "mice have shown that transplanting gut bacteria from anxious individuals into calm ones can "
            "induce anxiety-like behavior in the recipients, hinting at a causal relationship. While human "
            "trials remain limited, some researchers are cautiously optimistic that dietary interventions "
            "targeting gut bacteria could eventually complement traditional treatments for depression and "
            "anxiety, though they stress it is far too early for firm clinical recommendations."
        ),
        "content": {"key_points": [
            ["gut bacteria", "microorganisms", "gut microbiome"],
            ["mood", "mental health", "serotonin"],
            ["gut-brain axis", "vagus nerve", "brain"],
            ["mice", "anxiety", "transplant"],
            ["dietary interventions", "depression", "treatments"],
        ]},
        "correct_answer": None,
        "explanation": "A strong summary links gut bacteria to mood via the gut-brain axis, cites the mouse evidence, and notes the cautious outlook on treatment applications.",
    },
    {
        "module": "writing", "q_type": "swt", "difficulty": "easy", "tags": ["technology"],
        "title": "Summarize: The Decline of Cash Payments",
        "passage": (
            "Cash transactions have declined sharply in many countries over the past ten years as consumers "
            "increasingly turn to debit cards, mobile wallets, and contactless payment methods. Retailers "
            "have embraced this shift because digital payments are faster to process and reduce the security "
            "risks associated with handling large amounts of physical currency. However, the move away from "
            "cash has raised concerns about financial exclusion, since elderly people, low-income households, "
            "and those without reliable internet access may struggle to participate fully in an increasingly "
            "cashless economy. Some governments have responded by requiring businesses to continue accepting "
            "cash as a legal form of payment."
        ),
        "content": {"key_points": [
            ["cash", "decline", "digital payments"],
            ["mobile wallets", "contactless", "debit cards"],
            ["retailers", "faster", "security"],
            ["financial exclusion", "elderly", "low-income"],
            ["governments", "legal", "require"],
        ]},
        "correct_answer": None,
        "explanation": "A strong summary covers the shift to digital payments, retailer benefits, and the financial exclusion concern that prompted government responses.",
    },
    {
        "module": "writing", "q_type": "swt", "difficulty": "hard", "tags": ["economics", "labor"],
        "title": "Summarize: Automation and the Labor Market",
        "passage": (
            "Economists have long debated whether automation destroys more jobs than it creates. Historical "
            "evidence from the industrial revolution suggests that while specific occupations disappeared, "
            "new industries and job categories eventually emerged to absorb displaced workers, though this "
            "transition often took decades and caused significant hardship in the interim. Current research "
            "on robotics and artificial intelligence suggests a similar pattern may be unfolding, but at a "
            "pace that could outstrip workers' ability to retrain. Sectors most exposed to automation, such "
            "as manufacturing and routine data processing, are shedding jobs faster than adjacent growth "
            "sectors like healthcare and renewable energy can absorb the displaced workforce, creating "
            "regional pockets of prolonged unemployment even as national job numbers appear stable."
        ),
        "content": {"key_points": [
            ["automation", "jobs", "destroys", "creates"],
            ["industrial revolution", "historical", "new industries"],
            ["robotics", "artificial intelligence", "pace"],
            ["manufacturing", "data processing", "exposed"],
            ["regional", "unemployment", "retrain"],
        ]},
        "correct_answer": None,
        "explanation": "A strong summary contrasts historical job-market adaptation with the faster, more disruptive pace of current automation and its regional effects.",
    },
    {
        "module": "writing", "q_type": "swt", "difficulty": "medium", "tags": ["culture", "media"],
        "title": "Summarize: The Rise of Podcasting",
        "passage": (
            "Podcasting has grown from a niche hobby into a significant segment of the media industry over "
            "the past fifteen years, driven largely by the low barrier to entry and the intimate, "
            "conversational format that distinguishes it from traditional broadcast radio. Advertisers have "
            "taken notice, with podcast advertising revenue climbing steadily as listeners demonstrate higher "
            "engagement and brand recall compared to other digital media. Major technology companies have "
            "responded by acquiring popular shows and investing heavily in exclusive content, mirroring the "
            "streaming wars that reshaped television. Critics worry this consolidation could eventually "
            "undermine the independent, low-cost production model that made podcasting appealing to both "
            "creators and listeners in the first place."
        ),
        "content": {"key_points": [
            ["podcasting", "niche", "growth"],
            ["low barrier", "conversational", "format"],
            ["advertising", "revenue", "engagement"],
            ["technology companies", "acquiring", "exclusive content"],
            ["consolidation", "independent", "production"],
        ]},
        "correct_answer": None,
        "explanation": "A strong summary traces podcasting's growth, advertiser interest, and the tension between industry consolidation and its independent roots.",
    },
    {
        "module": "writing", "q_type": "swt", "difficulty": "easy", "tags": ["health"],
        "title": "Summarize: Benefits of Walking",
        "passage": (
            "Regular walking, even at a moderate pace, has been shown to provide substantial health benefits "
            "comparable in some respects to more intense forms of exercise. Studies tracking large groups of "
            "adults over several years found that those who walked briskly for at least thirty minutes most "
            "days had significantly lower rates of heart disease, improved mood, and better long-term "
            "cognitive function than sedentary peers. Unlike many fitness routines, walking requires no "
            "special equipment or gym membership, making it one of the most accessible forms of exercise "
            "available. Public health officials increasingly promote walking as a low-cost intervention for "
            "populations at risk of chronic disease."
        ),
        "content": {"key_points": [
            ["walking", "moderate", "health benefits"],
            ["heart disease", "lower rates"],
            ["mood", "cognitive function"],
            ["accessible", "no equipment", "gym"],
            ["public health", "low-cost", "intervention"],
        ]},
        "correct_answer": None,
        "explanation": "A strong summary covers the cardiovascular/cognitive benefits, accessibility, and public-health promotion of walking as exercise.",
    },

    # ---------- ESSAY (7) ----------
    {
        "module": "writing", "q_type": "essay", "difficulty": "medium", "tags": ["technology", "society"],
        "title": "Essay: Should Governments Regulate Artificial Intelligence?",
        "passage": (
            "Some people believe that artificial intelligence should be tightly regulated by governments to "
            "prevent misuse and protect jobs, while others argue that heavy regulation will stifle "
            "innovation and put countries at a competitive disadvantage. Discuss both views and give your "
            "own opinion."
        ),
        "content": {"key_points": [
            ["regulation", "regulate", "government control", "oversight"],
            ["innovation", "stifle", "competitive", "progress"],
            ["jobs", "employment", "automation", "workforce"],
            ["misuse", "safety", "risk", "harm"],
            ["balance", "middle ground", "both views"],
            ["opinion", "believe", "argue", "in my view"],
        ]},
        "correct_answer": None,
        "explanation": "A strong essay presents both the regulation and innovation arguments, develops them with reasoning, and closes with a clear personal position in 200-300 words.",
    },
    {
        "module": "writing", "q_type": "essay", "difficulty": "hard", "tags": ["education", "policy"],
        "title": "Essay: Standardized Testing in University Admissions",
        "passage": (
            "Many universities are reconsidering the role of standardized test scores in admissions "
            "decisions, with some institutions dropping the requirement entirely in favor of a more holistic "
            "review of applicants. To what extent do you agree or disagree that standardized tests should "
            "remain a required part of university admissions?"
        ),
        "content": {"key_points": [
            ["standardized test", "test scores", "exam scores"],
            ["holistic", "well-rounded", "broader review"],
            ["fairness", "equity", "socioeconomic", "access"],
            ["objective", "measure", "comparison", "consistency"],
            ["agree", "disagree", "extent", "position"],
        ]},
        "correct_answer": None,
        "explanation": "A strong essay takes a clear position, supports it with reasoning around fairness/objectivity, acknowledges the opposing view, and stays within 200-300 words.",
    },
    {
        "module": "writing", "q_type": "essay", "difficulty": "medium", "tags": ["environment"],
        "title": "Essay: Individual vs Corporate Responsibility for Climate Change",
        "passage": (
            "Some argue that addressing climate change is primarily the responsibility of individuals, who "
            "should reduce their own consumption and carbon footprint. Others contend that large corporations "
            "and governments bear far greater responsibility given their outsized environmental impact. "
            "Discuss both positions and give your own opinion."
        ),
        "content": {"key_points": [
            ["individual", "responsibility", "consumption", "carbon footprint"],
            ["corporations", "government", "policy"],
            ["outsized impact", "emissions", "industry"],
            ["collective action", "both", "shared"],
            ["opinion", "position", "believe"],
        ]},
        "correct_answer": None,
        "explanation": "A strong essay weighs individual action against corporate/government responsibility, develops each side, and concludes with a clear stance.",
    },
    {
        "module": "writing", "q_type": "essay", "difficulty": "medium", "tags": ["health", "policy"],
        "title": "Essay: Should Junk Food Advertising to Children Be Banned?",
        "passage": (
            "Rising childhood obesity rates have led some countries to propose banning the advertising of "
            "high-sugar and high-fat foods during children's television programming. Supporters say this "
            "would protect children from manipulative marketing, while opponents argue it infringes on "
            "commercial freedom and that parents, not the state, should regulate children's diets. Discuss "
            "both views and give your own opinion."
        ),
        "content": {"key_points": [
            ["childhood obesity", "junk food", "advertising"],
            ["ban", "regulation", "protect children"],
            ["commercial freedom", "business", "industry"],
            ["parental responsibility", "parents", "diet"],
            ["opinion", "both views", "believe"],
        ]},
        "correct_answer": None,
        "explanation": "A strong essay presents the child-protection argument and the parental-responsibility/commercial-freedom counter-argument before giving a clear opinion.",
    },
    {
        "module": "writing", "q_type": "essay", "difficulty": "hard", "tags": ["work", "society"],
        "title": "Essay: The Impact of Remote Work on Urban Centers",
        "passage": (
            "The widespread shift to remote work has led to declining foot traffic in many city centers, "
            "affecting businesses that once relied on daily commuters. Some argue cities must reinvent "
            "themselves around residential and community uses, while others believe commuting patterns will "
            "eventually return closer to pre-pandemic norms. To what extent do you agree that city centers "
            "need to fundamentally change in response to remote work?"
        ),
        "content": {"key_points": [
            ["remote work", "foot traffic", "city centers"],
            ["businesses", "commuters", "decline"],
            ["reinvent", "residential", "community"],
            ["return", "pre-pandemic", "commuting"],
            ["agree", "extent", "fundamentally change"],
        ]},
        "correct_answer": None,
        "explanation": "A strong essay takes a position on whether city centers must transform, supports it with reasoning, and addresses the counter-view that patterns may revert.",
    },
    {
        "module": "writing", "q_type": "essay", "difficulty": "medium", "tags": ["technology", "privacy"],
        "title": "Essay: Balancing Privacy and Security in the Digital Age",
        "passage": (
            "Governments increasingly use digital surveillance tools to combat crime and terrorism, but civil "
            "liberties advocates warn this comes at the cost of individual privacy. Some argue that greater "
            "surveillance is a necessary trade-off for public safety, while others believe it sets a "
            "dangerous precedent for government overreach. Discuss both views and give your own opinion."
        ),
        "content": {"key_points": [
            ["surveillance", "privacy", "digital"],
            ["security", "crime", "terrorism", "safety"],
            ["civil liberties", "overreach", "government"],
            ["trade-off", "necessary", "balance"],
            ["opinion", "both views", "believe"],
        ]},
        "correct_answer": None,
        "explanation": "A strong essay presents the security argument and the civil-liberties counter-argument, then commits to a clear, reasoned personal position.",
    },
    {
        "module": "writing", "q_type": "essay", "difficulty": "easy", "tags": ["education"],
        "title": "Essay: Is a University Degree Still Necessary?",
        "passage": (
            "With the rise of coding bootcamps, online certifications, and companies dropping degree "
            "requirements for many roles, some argue a traditional university degree is becoming less "
            "essential for career success. Others maintain that a university education still offers unique "
            "value beyond job preparation. To what extent do you agree that a university degree is still "
            "necessary today?"
        ),
        "content": {"key_points": [
            ["university degree", "necessary", "essential"],
            ["bootcamps", "certifications", "alternatives"],
            ["career success", "job requirements", "companies"],
            ["unique value", "education", "beyond jobs"],
            ["agree", "extent", "position"],
        ]},
        "correct_answer": None,
        "explanation": "A strong essay takes a clear stance on the continued necessity of a degree, weighing career-focused alternatives against broader educational value.",
    },
]
