survey = {
    "title": "title",
    "uuid": "survey001",
    "questions": [
        {
            "uuid": "q1",
            "text": "ИНН или название компании",
            "type": "tin",
            "required": True,
            "answers": [],
            "category": "1"
        },
        {
            "uuid": "q2",
            "text": "text",
            "type": "text",
            "required": False,
            "answers": [],
            "category": "1"
        },
        {
            "uuid": "q3",
            "text": "How would you rate our service?",
            "type": "rating",
            "required": True,
            "answers": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            "category": "1"
        },
        {
            "uuid": "q4",
            "text": "Do you like our product?",
            "type": "bool",
            "required": True,
            "answers": ["yes", "no"],
            "category": "1"
        },
        {
            "uuid": "q5",
            "text": "When does the survey end?",
            "type": "datetime",
            "required": False,
            "answers": [],
            "category": "1"
        },
        {
            "uuid": "q6",
            "text": "what do you like",
            "type": "radio",
            "required": False,
            "answers": ["fruits", "kalans", "home"],
            "category": None
        },
        {
            "uuid": "q7",
            "text": "what do you like",
            "type": "checkbox",
            "required": False,
            "answers": ["fruits", "kalans", "home"],
            "category": None
        }
    ]
}
