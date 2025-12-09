from main.models import FAQ
from users.models import Skill

# Create FAQ entries
faqs = [
    {
        'question': 'How do I offer a skill?',
        'answer': 'After signing up, go to your profile and click "Update Skills". Select the skills you can teach or offer from the list.',
        'category': 'general',
        'order': 1
    },
    {
        'question': 'How do I request a skill?',
        'answer': 'In the same "Update Skills" section, select the skills you want to learn in the "Skills Needed" section.',
        'category': 'general',
        'order': 2
    },
    {
        'question': 'Is SkillBridge free?',
        'answer': 'Yes! SkillBridge is completely free to use. We believe in creating accessible opportunities for everyone.',
        'category': 'general',
        'order': 3
    },
    {
        'question': 'How do I contact another user?',
        'answer': 'Find users on the Explore page and click "View Profile". You can send them a connection request from their profile.',
        'category': 'communication',
        'order': 4
    },
    {
        'question': 'Can I update my skills later?',
        'answer': 'Yes! You can update your offered and needed skills at any time from your profile page.',
        'category': 'profile',
        'order': 5
    },
    {
        'question': 'How are matches made?',
        'answer': 'Our algorithm finds users whose offered skills match your needed skills and vice versa.',
        'category': 'matching',
        'order': 6
    },
    {
        'question': 'Is SkillBridge safe to use?',
        'answer': 'We encourage users to verify each other\'s skills and meet in public places for initial exchanges.',
        'category': 'safety',
        'order': 7
    },
]

# Create initial skills
skills = [
    {'name': 'Web Development', 'category': 'tech'},
    {'name': 'Graphic Design', 'category': 'creative'},
    {'name': 'Mathematics Tutoring', 'category': 'academic'},
    {'name': 'Cooking', 'category': 'home'},
    {'name': 'Gardening', 'category': 'home'},
    {'name': 'Yoga Instruction', 'category': 'health'},
    {'name': 'Spanish Language', 'category': 'language'},
    {'name': 'Car Repair', 'category': 'trade'},
    {'name': 'Photography', 'category': 'creative'},
    {'name': 'Business Consulting', 'category': 'business'},
    {'name': 'Tailoring', 'category': 'trade'},
    {'name': 'Music Lessons', 'category': 'creative'},
    {'name': 'Farming Techniques', 'category': 'trade'},
    {'name': 'Data Analysis', 'category': 'tech'},
    {'name': 'First Aid Training', 'category': 'health'},
]

# Run this in Django shell
for faq_data in faqs:
    FAQ.objects.create(**faq_data)

for skill_data in skills:
    Skill.objects.create(**skill_data)