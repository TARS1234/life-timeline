THE 4 STEP PROCESS — CODE PRESERVATION IS PARAMOUNT

When implementing changes you MUST follow these steps:

🎯 Step 1: ANALYZE THE COMPLETE ORIGINAL FILE
    •    Read and understand EVERY line of the original working code
    •    Identify the existing architecture, methods, imports, and logic flow
    •    95%+ of this code works perfectly and must be preserved exactly as-is
    •    Note: This is NOT a rewrite — this is surgical modification of working production code

🎯 Step 2: IDENTIFY THE SPECIFIC CHANGES NEEDED
    •    Pinpoint the EXACT lines/methods that need modification
    •    Identify what new methods/imports need to be ADDED (not replaced)
    •    Goal: Minimal surgical changes, maximum code preservation

🎯 Step 3: MAKE SURGICAL CHANGES TO ORIGINAL CODE
    •    Keep the original file structure, variable names, and logic intact
    •    Add new functionality without breaking existing working systems
    •    Preserve all existing comments, logging, and error handling
    •    Make only the specific targeted fixes needed

🎯 Step 4: PRESENT COMPLETE FILE READY FOR COPY/PASTE
    •    Deliver the FULL original file with surgical changes integrated
    •    This should be: YOUR WORKING CODE + TARGETED FIXES
    •    Ready to drop-in replace the existing file
    •    Never say "I can't provide the full file" — always deliver the complete working result

---

CRITICAL REMINDERS:
    •    SURGICAL FIXES ONLY — Not rewrites or major restructuring
    •    PRESERVE the original working code — If it works, leave it alone. Only add/remove what is necessary
    •    FULL FILE DELIVERY — Always provide complete ready-to-use result
    •    CODE PRESERVATION IS PARAMOUNT — This cannot be overstated
•Make sure you understand the correct paths and dependencies so you don't break working systems.

---

🚨 VERY IMPORTANT — TINY HELPER RULE 🚨
    •    If new functionality is requested, FIRST consider adding it as a tiny helper function or class inside an existing module.
    •    A tiny helper = a small, specialized function/class for a single, narrowly defined purpose (e.g., formatting, validation, parsing).
    •    This keeps the system modular, avoids unnecessary new files, and reduces risk of breaking working pipelines.
    •    Only create a new file if the new functionality is large, standalone, and truly cannot fit as a helper in an existing module.

🚨 SIGNAL RULE 🚨
    •    When adding any new helper, method, or function, also add a signal or log so that if it fails, we know exactly where the failure occurred for debugging.

# ==========================================================================
#  Tiny Helper Template
#  Used for adding small, specialized functions
#  IMPORTANT: Always include a signal/log for debugging when failures occur
# ==============================================================================================================

import logging

# Configure logging (if not already configured in project)
logger = logging.getLogger(__name__)

def tiny_helper_example(input_value: str) -> str:
    """
    Tiny helper function template.
    Purpose: Perform one very small, specific task (e.g., formatting, validation).

    Args:
        input_value (str): The value to process

    Returns:
        str: Processed value

    Raises:
        ValueError: If the input_value is invalid
    """
    try:
        # Example logic: strip whitespace and uppercase
        processed = input_value.strip().upper()

        # Debug signal/log
        logger.info("[TinyHelper] Successfully processed input in tiny_helper_example")
        return processed

    except Exception as e:
        # Failure signal/log
        logger.error(f"[TinyHelper ERROR] tiny_helper_example failed: {e}")
        raise

_____________________________________________________________________________________________
