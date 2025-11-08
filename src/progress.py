# src/progress.py
import json
import os

PROGRESS_FILE = "progress.json"


class ProgressTracker:
    """Tracks which levels are unlocked."""

    def __init__(self):
        self.unlocked_levels = self.load_progress()

    def load_progress(self):
        """Load progress from file, or return default if file doesn't exist."""
        if os.path.exists(PROGRESS_FILE):
            try:
                with open(PROGRESS_FILE, 'r') as f:
                    data = json.load(f)
                    return set(data.get('unlocked_levels', [1]))
            except:
                return {1}  # Default: only level 1 unlocked
        return {1}

    def save_progress(self):
        """Save progress to file."""
        with open(PROGRESS_FILE, 'w') as f:
            json.dump({'unlocked_levels': list(self.unlocked_levels)}, f)

    def unlock_level(self, level_number):
        """Unlock a specific level."""
        self.unlocked_levels.add(level_number)
        self.save_progress()

    def is_level_unlocked(self, level_number):
        """Check if a level is unlocked."""
        return level_number in self.unlocked_levels

    def complete_level(self, level_number):
        """Mark a level as complete and unlock the next one."""
        self.unlock_level(level_number + 1)


# Global progress tracker instance
progress = ProgressTracker()