# LLM SQL
 - LLM connected with a SQL database for natural language query
 - Ask SQL for any information about its content
 - Safeguards agains update/delete operations by analysing transaction before commit.

## How It Works
 - The LLM model is teached to understand the database schema and generate SQL queries based on natural language input.
 - The environment uses SQLServer as an example but can be easily adapted to other databases.
 - The LLM can execute the following operations when queried:
   - `RESPONSE_TEXT` - Returns a text response based on the query.
   - `RESPONSE_SQL` - Returns a SQL to be presented to the user.
   - `INTERNAL_SQL` - Query to the database with result being returned to the LLM for further analysis and actions (the LLM can perform as many of these as required until a response is prepared).
 - Diagram
 - ``````mermaid
   graph TD;
       A[User Input] -->|Natural Language| B[LLM]
       B -->|SQL Query| C[Database]
       C -->|Result Set| B
       B -->|Response Text| D[User Output]
       B -->|Response SQL| E[SQL Output]
       E -->|Execute SQL| C
       C -->|Result Set| B
       B -->|Internal SQL| C
       C -->|Result Set| B
   ```
 
## Setup
 - Get a API key from [OpenAI](https://platform.openai.com/signup)
 - Clone the repository and install [Poetry](https://python-poetry.org/docs/#installation)
 - Install dependencies with Poetry
   ```bash
   poetry install
   ```
 - Run the application with Poetry
    ```bash
    poetry run python app.py
    ```
 - Open the application in your browser at `http://localhost:5000`

## License
 - The project is licensed under the MIT License.
 - See the [LICENSE](LICENSE.md) file for details.

