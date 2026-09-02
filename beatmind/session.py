# Session state management
# Remembers everything about your production session

def create_session():
    return {
        'genre': None,
        'bpm': None,
        'key': None,
        'sections': {
            'melody': {
                'status': 'not_started',
                'notes': [],
                'drafts': 0,
                'feel': None
            },
            'chords': {
                'status': 'not_started',
                'progression': [],
                'drafts': 0
            },
            'bass': {
                'status': 'not_started',
                'drafts': 0
            },
            'drums': {
                'status': 'not_started',
                'drafts': 0
            },
            'pad': {
                'status': 'not_started',
                'drafts': 0
            }
        },
        'change_log': [],
        'conversation_history': []
    }