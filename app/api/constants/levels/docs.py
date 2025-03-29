LEVEL_DOCS = {
    "get": {
        "summary": "Retrieve all levels",
        "description": """
        Fetches all available levels from the database.

        Each level includes:
        - id: Unique identifier of the level.
        - name: The unique name of the level.
        - image: (Optional) A URL or path to the level's associated image.

        This endpoint is useful for retrieving a list of all levels in the system.
        """,
    },
    "get_one": {
        "summary": "Retrieve a specific level",
        "description": """
        Fetches a single level by its ID.

        - level_id: The unique identifier of the level (must be greater than or equal to 1).

        This endpoint returns the details of a specific level if it exists.
        """,
    },
    "create": {
        "summary": "Create a new level",
        "description": """
        Creates a new level in the system.

        Request body should contain:
        - name: The unique name of the level.
        - image: (Optional) A URL or path to the level's associated image.

        Returns the created level with its unique identifier.
        """,
    },
    "update": {
        "summary": "Update an existing level",
        "description": """
        Updates an existing level's information.

        - level_id: The unique identifier of the level to be updated.
        - Request body can contain:
          - name: The updated name of the level.
          - image: (Optional) A new image URL or path.

        Returns the updated level data.
        """,
    },
    "delete": {
        "summary": "Delete a level",
        "description": """
        Deletes a level by its ID.

        - level_id: The unique identifier of the level to be deleted.

        This operation permanently removes the level from the system.
        """,
    },
}
