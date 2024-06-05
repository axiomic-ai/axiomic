

import os
import inspect


def second_caller_filename():
    # Get the current stack trace
    stack = inspect.stack()
    
    if len(stack) < 3:
        return None

    # Get the second stack frame
    frame = stack[2]
    
    # Get the filename of the second stack frame
    filename = frame.filename
    
    # Return the filename
    return filename



    
