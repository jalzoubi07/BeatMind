from collections import deque

# Directed graph - how sections affect each other
PRODUCTION_GRAPH = {
    'melody': ['chords', 'bass', 'drums', 'pad'],
    'chords': ['bass', 'pad'],
    'bass':   ['drums'],
    'drums':  [],
    'pad':    []
}

def get_ripple_effects(changed_section):
    """BFS to find every section affected by a change, nearest first."""
    affected = []
    visited = {changed_section}
    queue = deque([changed_section])
    while queue:
        current = queue.popleft()
        for neighbor in PRODUCTION_GRAPH.get(current, []):
            if neighbor not in visited:
                visited.add(neighbor)
                affected.append(neighbor)
                queue.append(neighbor)
    return affected
