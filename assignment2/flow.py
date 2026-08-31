"""
CSC-128 Assignment 2 starter: conversation logic
Roberto Hermida Lujan

Keep the conversation logic here so it can be tested without Streamlit.
"""

# the conversation logic, no Streamlit imports

DEPARTMENT_KEYWORDS = {
    "advising": "Academic Advising",
    "financing" : "Financial Aid",
    "careers" : "Career Services",
    "tutoring" : "Tutoring"
    # TODO 1: add keywords for Financial Aid, Career Services, and Tutoring
}

SLOTS_BY_DEPARTMENT = {
    "Academic Advising": [
        "Monday 10:00 AM", 
        "Tuesday 2:00 PM"
    ],

    "Financial Aid" : [
        "Wednesday 11:00 AM",
        "Thursday 12:00 PM"
    ],
    "Career Services" : [
        "Monday 9:00 AM",
        "Wednesday 12:00 PM",
        "Friday 2:00 PM"
    ],
    "Tutoring" : [
        "Monday 9:00 AM",
        "Wednesday 12:00 PM",
        "Friday 2:00 PM"
    ]
    # TODO 2: add slots for the other three departments
}

GREETING = "IT Help Desk Bot"


def new_state():
    """TODO 3: return a dict with stage, department, and slot. Name it new_state so it matches the tests.."""
    return {
        "stage" : "choose_department",
        "department" : None,
        "Slot" : None
    }


def find_department(text):
    """TODO 4: return a department name if the message names one."""

    if text == "":
        return None;

    text = text.lower();
    for key, value in DEPARTMENT_KEYWORDS.items():
        if text in key or text in value.lower():
            return key;
    return None


def find_slot(text, options):
    """TODO 5: match a slot by weekday name or by its number in the list."""   
    
    for option in options:
        for word in option.split():
            if text in word.lower():
                return option;

    return None



def handle(text, state):
    """Return (reply, updated_state)."""
    # copy rather than mutate, so a test can replay a whole
    # conversation and inspect the state at every step
    state = dict(state)
    lowered = text.lower()


    if "start over" in lowered:
        state = new_state();

    if state["stage"] == "choose_department":
        selected_department = find_department(lowered);

        if selected_department is None:
            reply = "Please select choose and type the following departments\n";
            for key, value in DEPARTMENT_KEYWORDS.items():
                reply += value + "\n";
            return reply, state

        state["department"] = selected_department;
        state["stage"] = "choose_slot"
        
        department_full_name = DEPARTMENT_KEYWORDS[state["department"]];

        reply = department_full_name + " has ";
        for option in SLOTS_BY_DEPARTMENT[department_full_name]:
            reply += option + ", ";

        return reply, state

    if state["stage"] == "choose_slot":
        department_full_name = DEPARTMENT_KEYWORDS[state["department"]];

        slot_found = find_slot(lowered, SLOTS_BY_DEPARTMENT[department_full_name]);
        #for option in SLOTS_BY_DEPARTMENT[department_full_name]:
        #    if option.split()[0].lower() in lowered:
        #        state["slot"] = option
        #        state["stage"] = "confirm"
        #        return f"Booking {option}. Type yes to confirm.", state

        if (slot_found is None):
            return "I did not recognize that time.", state

        state["slot"] = slot_found;
        state["stage"] = "confirm";
        return f"Booking {slot_found}. Type yes to confirm.", state; 

    if state["stage"] == "confirm":
        if lowered.startswith("y"):
            state["stage"] = "done"
            return f"Confirmed for {state['slot']}.", state
        return "Please answer yes or no.", state

    return "You are already booked. Say start over for a new one.", state