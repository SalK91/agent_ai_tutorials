## Environment & Package Setup

1. install uv
2. move to the project directory
3. uv init = This creates project structure and enables dependency + environment management.
4. uv venv = create a virtual envroiemtn
5. source .venv/Scripts/activate = activate venv 
6. requirement.txt file create to install libraries
7. uv add -r requirements.txt install packages
8. uv add ipykernel = install ipykernel
9. Create api keys e.g. Google Studio, Groq, Cohere etc and add to .env file
10. Activate kernel
11. uv add langchain-cohere
12. uv add tavily-python
13. uv add langsmith
14. uv add langchain_mcp_adapters
15. uv add mcp 
16. uv add pywintypes

```python -m ipykernel install --user --name=uv_venv --display-name "Python (uv venv)"
```