"""
Example new version of a Python module with breaking changes for testing AST diff analyzer.
"""

def calculate_sum(a, b, c=0):
    """Calculate the sum of two or three numbers."""
    return a + b + c

# process_data function was removed - BREAKING CHANGE

def process_items(items):
    """Process a list of items (renamed from process_data)."""
    return [x * 3 for x in items]

class DataProcessor:
    """A class for processing data."""
    
    def __init__(self, multiplier=1, offset=0):  # Added new parameter
        self.multiplier = multiplier
        self.offset = offset  # New attribute
    
    def transform(self, value):
        """Transform a single value."""
        return (value * self.multiplier) + self.offset  # Changed implementation
    
    # batch_transform method was removed - BREAKING CHANGE
    
    def parallel_transform(self, values):
        """Transform values in parallel (new method)."""
        return [self.transform(v) for v in values]

class AdvancedProcessor(DataProcessor):
    """New class that extends DataProcessor."""
    
    def advanced_transform(self, value):
        """Advanced transformation."""
        return self.transform(value) ** 2

# Module-level constant value changed - POTENTIALLY BREAKING
DEFAULT_MULTIPLIER = 3

# Module-level variable
current_version = "2.0.0"

# New module-level variable
api_version = "v2" 