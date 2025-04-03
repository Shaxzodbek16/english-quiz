OPTIONS_DOCS = {
    "get": {
        "summary": "Retrieve all options",
        "description": """
        Fetches all available options from the database.

        Each option includes:
        - id: Unique identifier of the option.
        - options: The text representation of the option.
        - is_correct: A boolean indicating whether the option is correct.
        - created_at: The timestamp when the option was created.
        - updated_at: The timestamp when the option was last updated.

        This endpoint is useful for retrieving all options associated with different questions.
        """,
    },
    "get_one": {
        "summary": "Retrieve a specific option",
        "description": """
        Fetches a single option by its ID.

        - option_id: The unique identifier of the option (must be greater than or equal to 1).

        Returns the details of a specific option if it exists.
        """,
    },
    "create": {
        "summary": "Create a new option",
        "description": """
        Creates a new option in the system.

        Request body should contain:
        - options: The text of the option.
        - is_correct: (Optional, default: False) A boolean indicating whether the option is the correct answer.

        Returns the created option with its unique identifier.
        """,
    },
    "update": {
        "summary": "Update an existing option",
        "description": """
        Updates an existing option's information.

        - option_id: The unique identifier of the option to be updated.
        - Request body can contain:
          - options: The updated text of the option.
          - is_correct: A boolean indicating whether the option is correct.

        Returns the updated option data.
        """,
    },
    "delete": {
        "summary": "Delete an option",
        "description": """
        Deletes an option by its ID.

        - option_id: The unique identifier of the option to be deleted.

        This operation permanently removes the option from the system.
        """,
    },
}
