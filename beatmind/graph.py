# Production relationship graph
# Ripple effect engine using BFS

# Directed graph - how sections affect each other
PRODUCTION_GRAPH = {
    'melody': ['chords', 'bass', 'drums', 'pad'],
    'chords': ['bass', 'pad'],
    'bass':   ['drums'],
    'drums':  [],
    'pad':    []
}

def get_ripple_effects(changed_section):
    """
    BFS traversal to find all sections
    affected by a change
    """
    affected = []
    visited = set()
    queue = [changed_section]
    
    while queue:
        current = queue.pop(0)
        if current in visited:
            continue
        visited.add(current)
        
        for neighbor in PRODUCTION_GRAPH.get(current, []):
            if neighbor not in visited:
                affected.append(neighbor)
                queue.append(neighbor)
    
    return affected