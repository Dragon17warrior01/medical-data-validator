import re

# Sample medical records dataset with intentionally mixed formatting
# (e.g., mixed case IDs, gender casing) to test the validator
medical_records = [
    {
        'patient_id': 'P1001',
        'age': 34,
        'gender': 'Female',
        'diagnosis': 'Hypertension',
        'medications': ['Lisinopril'],
        'last_visit_id': 'V2301',
    },
    {
        'patient_id': 'p1002',
        'age': 47,
        'gender': 'male',
        'diagnosis': 'Type 2 Diabetes',
        'medications': ['Metformin', 'Insulin'],
        'last_visit_id': 'v2302',
    },
    {
        'patient_id': 'P1003',
        'age': 29,
        'gender': 'female',
        'diagnosis': 'Asthma',
        'medications': ['Albuterol'],
        'last_visit_id': 'v2303',
    },
    {
        'patient_id': 'p1004',
        'age': 56,
        'gender': 'Male',
        'diagnosis': 'Chronic Back Pain',
        'medications': ['Ibuprofen', 'Physical Therapy'],
        'last_visit_id': 'V2304',
    }
]

def find_invalid_records(
    patient_id, age, gender, diagnosis, medications, last_visit_id
):
    """
    Checks each field of a patient record against expected format rules.
    Returns a list of field names that failed validation.
    If all fields are valid, returns an empty list.
    """

    # Each key maps to a boolean: True = valid, False = invalid
    # patient_id must be a string matching pattern 'P' or 'p' followed by digits
    # age must be an integer and at least 18
    # gender must be 'male' or 'female' (case-insensitive)
    # diagnosis can be a string or None (unknown diagnosis is allowed)
    # medications must be a list where every item is a string
    # last_visit_id must be a string matching pattern 'V' or 'v' followed by digits
    constraints = {
        'patient_id': isinstance(patient_id, str)
        and re.fullmatch('p\d+', patient_id, re.IGNORECASE),
        'age': isinstance(age, int) and age >= 18,
        'gender': isinstance(gender, str) and gender.lower() in ('male', 'female'),
        'diagnosis': isinstance(diagnosis, str) or diagnosis is None,
        'medications': isinstance(medications, list)
        and all([isinstance(i, str) for i in medications]),
        'last_visit_id': isinstance(last_visit_id, str)
        and re.fullmatch('v\d+', last_visit_id, re.IGNORECASE)
    }

    # Return only the keys whose value is False (i.e., failed the constraint)
    return [key for key, value in constraints.items() if not value]


def validate(data):
    """
    Validates the overall structure and content of a medical records dataset.
    Expects a list or tuple of dictionaries, each with the required fields.
    Prints descriptive messages for any issues found.
    Returns True if all records are valid, False if any issues were found.
    """

    # Top-level check: data must be a list or tuple
    is_sequence = isinstance(data, (list, tuple))
    if not is_sequence:
        print('Invalid format: expected a list or tuple.')
        return False

    # Flag to track if any record fails validation
    is_invalid = False

    # The exact set of keys every record dictionary must have
    key_set = set(
        ['patient_id', 'age', 'gender', 'diagnosis', 'medications', 'last_visit_id']
    )

    for index, dictionary in enumerate(data):

        # Each item in the list must itself be a dictionary
        if not isinstance(dictionary, dict):
            print(f'Invalid format: expected a dictionary at position {index}.')
            is_invalid = True
            continue  # Skip further checks for this item

        # Check that the dictionary has exactly the required keys — no more, no less
        if set(dictionary.keys()) != key_set:
            print(
                f'Invalid format: {dictionary} at position {index} has missing and/or invalid keys.'
            )
            is_invalid = True
            continue  # Skip field-level checks since keys are wrong

        # Unpack the dictionary and check each field's value format
        invalid_records = find_invalid_records(**dictionary)

        # Report each field that failed its constraint
        for key in invalid_records:
            print(f"Unexpected format '{key}: {dictionary[key]}' at position {index}.")
            is_invalid = True

    # If no issues were found throughout, confirm valid format
    if is_invalid:
        return False
    print('Valid format.')
    return True


# Run validation on the sample dataset
validate(medical_records)
