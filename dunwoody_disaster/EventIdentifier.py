# Import the logging module to enable logging of warnings and other messages.
import logging

# Define a dictionary to hold event identifiers for different scenarios in the application or game.
EVENT_IDENTIFIERS = {
    "boss_defeat": {  # Category for events related to defeating bosses.
        "Joe Axberg": "boss_defeat_joe",  # Map each boss's name to a unique event identifier.
        "LeAnn Simonson": "boss_defeat_leann",
        "Noureen Sajid": "boss_defeat_noureen",
        "Ryan Rengo": "boss_defeat_ryan",
        "Bill Hudson": "boss_defeat_bill",
        "Amalan Pulendran": "boss_defeat_amalan",
        "Matthew Beckler": "boss_defeat_matthew",
    },
    "story_milestone_first_act_complete": "story_milestone_first_act_complete",  # Single event identifier for a specific story milestone.
    "story_milestone_final_act_begin": "story_milestone_final_act_begin",  # Another single event identifier for a different story milestone.
}


# Define a class that will handle the retrieval of event identifiers based on given categories and sub-categories.
class EventIdentifier:
    @staticmethod  # Declare a static method, meaning it can be called on the class without needing an instance of the class.
    def get_event_id(category, sub_category=None):
        # This method retrieves an event identifier based on a category and an optional sub-category.

        # Reassign input parameters to themselves (redundant in Python, used here for clarity).
        category = category
        if sub_category:
            sub_category = sub_category
            # Attempt to retrieve the event ID using the category and sub-category.
            # If the category does not exist, it defaults to an empty dictionary, preventing a KeyError.
            event_id = EVENT_IDENTIFIERS.get(category, {}).get(sub_category)
        else:
            # If no sub-category is provided, retrieve the event ID using just the category.
            event_id = EVENT_IDENTIFIERS.get(category)

        # Check if an event ID was successfully retrieved.
        if event_id is None:
            # If no event ID was found, log a warning message.
            logging.warning(
                f"Event ID not found for category '{category}' and sub_category '{sub_category}'"
            )
            # Return a default event ID to handle cases where no specific ID could be found.
            return "default_event"
        # Return the retrieved event ID.
        return event_id
