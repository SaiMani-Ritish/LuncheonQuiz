"""
Quiz questions for the Luncheon Quiz application.
Each question has: text, options (list of 4), and correct_answer (index 0-3).
"""

QUESTIONS = [
    # Seattle / Seattle City Facts (6 questions)
    {
        "text": "What is Seattle's most famous nickname?",
        "options": [
            "The Windy City",
            "The Emerald City",
            "The City of Angels",
            "The Big Apple"
        ],
        "correct_answer": 1
    },
    {
        "text": "Which iconic structure was built for the 1962 World's Fair in Seattle?",
        "options": [
            "Pike Place Market",
            "Columbia Center",
            "Space Needle",
            "Seattle Great Wheel"
        ],
        "correct_answer": 2
    },
    {
        "text": "Which major tech company was founded in Seattle in 1994?",
        "options": [
            "Microsoft",
            "Apple",
            "Amazon",
            "Google"
        ],
        "correct_answer": 2
    },
    {
        "text": "What body of water borders Seattle to the west?",
        "options": [
            "Lake Washington",
            "Puget Sound",
            "Pacific Ocean",
            "Columbia River"
        ],
        "correct_answer": 1
    },
    {
        "text": "Which Seattle market is one of the oldest continuously operated public farmers' markets in the US?",
        "options": [
            "Ballard Farmers Market",
            "University District Farmers Market",
            "Pike Place Market",
            "Capitol Hill Farmers Market"
        ],
        "correct_answer": 2
    },
    {
        "text": "What is the name of Seattle's NFL football team?",
        "options": [
            "Seattle Mariners",
            "Seattle Sounders",
            "Seattle Storm",
            "Seattle Seahawks"
        ],
        "correct_answer": 3
    },
    # MBA Common Knowledge (2 questions)
    {
        "text": "What does ROI stand for in business?",
        "options": [
            "Rate of Inflation",
            "Return on Investment",
            "Risk of Insolvency",
            "Revenue of Industry"
        ],
        "correct_answer": 1
    },
    {
        "text": "Which framework analyzes a company's Strengths, Weaknesses, Opportunities, and Threats?",
        "options": [
            "Porter's Five Forces",
            "PESTLE Analysis",
            "SWOT Analysis",
            "BCG Matrix"
        ],
        "correct_answer": 2
    },
    # MSCS / Computer Science Basics (2 questions)
    {
        "text": "What is the time complexity of binary search on a sorted array?",
        "options": [
            "O(n)",
            "O(n²)",
            "O(log n)",
            "O(1)"
        ],
        "correct_answer": 2
    },
    {
        "text": "Which data structure operates on a Last-In-First-Out (LIFO) principle?",
        "options": [
            "Queue",
            "Stack",
            "Linked List",
            "Binary Tree"
        ],
        "correct_answer": 1
    }
]

def get_questions():
    """Return the list of quiz questions."""
    return QUESTIONS

def get_question_count():
    """Return the total number of questions."""
    return len(QUESTIONS)
