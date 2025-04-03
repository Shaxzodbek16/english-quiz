DOCS: dict = {
    "get": {
        "summary": "Retrieve all test types",
        "description": "Fetch a list of all available test types. This endpoint provides an overview of all test categories stored in the system. It does not require any parameters and returns a paginated list of test types if applicable.",
    },
    "get_all": {
        "summary": "Retrieve all test types (alternative)",
        "description": "Similar to the 'get' endpoint, this endpoint retrieves all available test types. It serves as an alternative method for fetching test types, potentially used in different parts of the system.",
    },
    "create": {
        "summary": "Create a new test type",
        "description": "Allows the user to create a new test type by providing the necessary details. The request body must include the test type name and an optional description. The response returns the created test type along with metadata such as timestamps.",
    },
    "update": {
        "summary": "Modify an existing test type",
        "description": "Updates an existing test type based on the provided data. The request should include the test type ID and the fields that need to be modified. If successful, the response returns the updated test type details.",
    },
    "delete": {
        "summary": "Remove a test type by ID",
        "description": "Deletes a specific test type using its unique identifier. This action is irreversible and permanently removes the test type from the system. If the ID does not exist, an error response is returned.",
    },
}
