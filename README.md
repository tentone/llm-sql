# LLM SQL
 - LLM connected with a SQL database for natural language query
 - Ask SQL for any information about its content
 - Basic Safeguards agains update/delete operations.

<img src="./readme.gif">

## How It Works
 - The LLM model is teached to understand the database schema and generate SQL queries based on natural language input.
 - The environment uses Microsoft SQL Server as an example but can be easily adapted to other databases.
 - The LLM can execute the following operations when queried:
   - `text` - Returns a text response based on the query.
   - `sql` - Returns a SQL to be presented to the user.

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

## Database Structure
 - The system automatically generates a database schema stored in the `structure.txt` file
 - Schema includes the tables, column and relational keys
 - After being generated the schema can be edited to remove unecessary information (keep schema to the minimum).
 - Mark any important fields with * and add comments to the columns when necessary (e.g. enum values, description)

```txt
team:
	- id (uniqueidentifier)
	- *name (varchar)
	- *description (varchar)

team_user:
	- user_id (uniqueidentifier) - fk - user(id)
	- team_id (uniqueidentifier) - fk - team(id)

user:
	- id (uniqueidentifier)
	- *email (nvarchar)
	- *phone_number (varchar)
	- *name (varchar)
	- notes (varchar)
	- active (bit)
	- company_id (uniqueidentifier) - fk - company(id)
```

## License
 - The project is licensed under the MIT License.
 - See the [LICENSE](LICENSE.md) file for details.

