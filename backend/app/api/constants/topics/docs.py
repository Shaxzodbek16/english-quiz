TOPIC_DOCS = {
    "get": {
        "summary": "Retrieve all topics",
        "description": """
        Fetches all available topics from the database.

        Each topic includes:
        - id: Unique identifier of the topic.
        - name: The unique name of the topic.
        - image: (Optional) A URL or path to the topic's associated image.

        This endpoint is useful for retrieving a list of all topics in the system.
        """,
    },
    "get_one": {
        "summary": "Retrieve a specific topic",
        "description": """
        Fetches a single topic by its ID.

        - topic_id: The unique identifier of the topic (must be greater than or equal to 1).

        This endpoint returns the details of a specific topic if it exists.
        """,
    },
    "create": {
        "summary": "Create a new topic",
        "description": """
        Creates a new topic in the system.

        Request body should contain:
        - name: The unique name of the topic.
        - image: (Optional) A URL or path to the topic's associated image.

        Returns the created topic with its unique identifier.
        """,
    },
    "update": {
        "summary": "Update an existing topic",
        "description": """
        Updates an existing topic's information.

        - topic_id: The unique identifier of the topic to be updated.
        - Request body can contain:
          - name: The updated name of the topic.
          - image: (Optional) A new image URL or path.

        Returns the updated topic data.
        """,
    },
    "delete": {
        "summary": "Delete a topic",
        "description": """
        Deletes a topic by its ID.

        - topic_id: The unique identifier of the topic to be deleted.

        This operation permanently removes the topic from the system.
        """,
    },
}
