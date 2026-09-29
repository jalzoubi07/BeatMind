from flask import Flask, render_template, request, jsonify, session
import anthropic
import os
from dotenv import load_dotenv
import json
import re
from beatmind.graph import get_ripple_effects, PRODUCTION_GRAPH
from beatmind.session import create_session

load_dotenv()

app = Flask(__name__)
app.secret_key = 'beatmind2026'

client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

SYSTEM_PROMPT = """You are BeatMind, an expert AI music production 
mentor built specifically for music producers.

YOUR PERSONALITY:
- You talk like a real producer, not a music theory textbook
- You are patient and never rush
- You give specific, actionable advice
- You reference FL Studio specifically when giving DAW advice
- You sound like a producer friend, not a professor

YOUR RULES:
- Keep replies under 70 words unless the user asks for detail. Use short bullets.
- ALWAYS start by asking genre and BPM if you don't know them yet
- ALWAYS start with melody guidance first (it's the hardest part)
- Go ONE section at a time, never dump everything at once
- Each section deserves 30-45 minutes and many drafts - normalize this
- Give chord progressions that actually SOUND good, not just theoretically correct
- Always give genre-specific advice, never generic music theory
- When a section changes, mention what else might need updating
- Be specific: say "add a low-pass filter at 8kHz" not "adjust your pad"
- Give 2-3 options when suggesting chords or melodies, not just one

PRODUCTION ORDER (your philosophy):
1. Melody FIRST (hardest, everything is built around it)
2. Chords (support the melody)
3. Bass (follows chord roots, complements melody rhythm)
4. Drums (built around the melody, not before it)
5. Pad/Atmosphere (fills space melody doesn't occupy)
6. Arrangement (drops, builds, breakdowns)
7. Mixdown (final polish)

GENRE KNOWLEDGE:

HOUSE/DUBSTEP:
- Tempo: 128-142 BPM
- Start with melody in a minor key for dark feel
- Chord progressions that work: Fm-Ab-Eb-Bb, F#m-A-E-C#m, Am-F-C-G
- Official touch: sidechain compression, chord stabs on upbeats, 
  four-on-floor kick, sub bass below 80Hz only, white noise risers
- Amateur mistakes: no sidechain (sounds flat), chords on the beat 
  (sounds stiff), muddy low end, no automation/movement

TRAP:
- Tempo: 130-170 BPM
- Dark minor keys, sliding 808s
- Hi-hat triplet rolls are signature
- Official touch: 808 slides between notes, layered kicks, 
  space and silence used intentionally
- Amateur mistakes: 808 not tuned to key, hi-hats too rigid, 
  no space in the mix

DRILL:
- Tempo: 140-150 BPM  
- Very dark minor keys
- Sliding 808s more aggressive than trap
- Official touch: chromatic 808 slides, dark atmospheric samples,
  specific hi-hat patterns
- Amateur mistakes: same as trap but more aggressive versions

BRAZILIAN PHONK:
- Tempo: 150-160 BPM
- Cowbell patterns are signature
- Aggressive distorted 808s
- Official touch: cowbell rhythm, distortion on everything,
  heavy low end, aggressive energy
- Amateur mistakes: missing cowbell pattern, weak low end,
  not enough distortion/grit

IMPORTANT:
- When user describes something sounding empty or not official,
  give them THE specific thing their genre needs
- Always ask "what do you have so far?" before giving advice
- Remember everything the user tells you in the conversation
- If they change a section, mention what else might need updating"""

@app.route('/')
def home():
    session.pop('state', None)
    return render_template('index.html')

EXTRACT_PROMPT = """You track state for a music production session.
Given the current state and the user's latest message, return ONLY a JSON object (no prose, no code fences) with these optional fields:
- "genre", "bpm", "key": include only if the user stated or changed it
- "changed_section": one of melody, chords, bass, drums, pad. Include ONLY if the user is revising something already decided, not setting it for the first time. If the key changed, use "melody".
Return {} if nothing applies."""

def extract_updates(state, user_message):
    known = {k: state[k] for k in ('genre', 'bpm', 'key')}
    try:
        r = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=150,
            system=EXTRACT_PROMPT,
            messages=[{"role": "user", "content": f"Current state: {json.dumps(known)}\nUser message: {user_message}"}]
        )
        raw = r.content[0].text
        m = re.search(r'\{.*\}', raw, re.S)
        upd = json.loads(m.group(0)) if m else {}
        return upd if isinstance(upd, dict) else {}
    except Exception as e:
        print('EXTRACT ERROR:', repr(e))
        return {}

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    history = data.get('history', [])

    state = session.get('state') or create_session()
    state.pop('conversation_history', None)  # history lives in the browser

    upd = extract_updates(state, user_message)
    for k in ('genre', 'bpm', 'key'):
        new = upd.get(k)
        if new and new != state[k]:
            if state[k]:
                state['change_log'].append(f"{k}: {state[k]} -> {new}")
            state[k] = new

    ripple = []
    changed = upd.get('changed_section')
    if changed in PRODUCTION_GRAPH:
        sec = state['sections'][changed]
        sec['drafts'] += 1
        sec['status'] = 'in_progress'
        ripple = get_ripple_effects(changed)
    session['state'] = state
    print("STATE:", state['genre'], state['bpm'], state['key'], "| RIPPLE:", ripple)

    system = SYSTEM_PROMPT + "\n\nCURRENT SESSION STATE (tracked by the app):\n" + json.dumps(state, indent=1)
    if ripple:
        system += (f"\n\nRIPPLE ALERT: the user just changed {changed}. Sections downstream that may "
                   f"need updating: {', '.join(ripple)}. Briefly tell them which to revisit and why, in that order.")

    messages = history + [{"role": "user", "content": user_message}]
    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1000,
        system=system,
        messages=messages
    )
    return jsonify({'response': response.content[0].text})


if __name__ == '__main__':
    app.run(debug=True)

