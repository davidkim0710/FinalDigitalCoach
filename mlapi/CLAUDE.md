# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands
- Run server: `python main.py`
- Run all tests: `pytest`
- Run single test: `pytest tests/test_file.py::test_function_name`
- Type check: `mypy .`
- Formatting: `ruff format .`

## Code Style
- **Imports**: Group standard lib > third-party > local; use absolute imports
- **Typing**: Use pydantic for data structures; annotate all function returns
- **Naming**: snake_case for functions/variables, PascalCase for classes/types
- **Error handling**: Use Optional types for nullable fields
- **Formatting**: Follow PEP 8 guidelines
- **Documentation**: Include docstrings for classes and functions
- **Python version**: >=3.12
- Keep files around 200 to 300 lines and with a clear single purpose and structure. 
- Always make sure to check if a functionality is already implemented and that it is well understood before implementing. You can make one-off scripts to test however always make sure to delete after using. 
- Always prefer simple solutions. 
- Only implement features that are well understood. If the feature is not well understood, think before implementing. 


## Project Structure
- routes/: FastAPI endpoints
- schemas/: Type definitions using pydantic
- tasks/: Background task implementation
- redisStore/: Redis queue management
- utils/: Helper functions

## Redis
- Use Redis for queue mannagement and rq workers for background tasks. 

