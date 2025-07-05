"""
Example old version of a Python module for testing AST diff analyzer.
"""

def calculate_sum(a, b):
    """Calculate the sum of two numbers."""
    return a + b

def process_data(data):
    """Process a list of data."""
    return [x * 2 for x in data]

class DataProcessor:
    """A class for processing data."""
    
    def __init__(self, multiplier=1):
        self.multiplier = multiplier
    
    def transform(self, value):
        """Transform a single value."""
        return value * self.multiplier
    
    def batch_transform(self, values):
        """Transform a batch of values."""
        return [self.transform(v) for v in values]

# Module-level constant
DEFAULT_MULTIPLIER = 2

# Module-level variable
current_version = "1.0.0" 