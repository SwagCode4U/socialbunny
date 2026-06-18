from app.database import SessionLocal
from app.models import Topic

sample_topics = [
    {
        "title": "Introduction to React Hooks",
        "author": "Hani",
        "content": """React Hooks were introduced in React 16.8.
They let you use state and other React features without writing a class.

useState:
useState is the most basic hook. It returns a pair: the current state value
and a function that lets you update it.

useEffect:
useEffect lets you perform side effects in function components.
It serves the same purpose as componentDidMount, componentDidUpdate,
and componentWillUnmount in React classes.

useContext:
useContext lets you subscribe to React context without introducing nesting.

useReducer:
useReducer is usually preferable to useState when you have complex
state logic that involves multiple sub-values or when the next state
depends on the previous one.

Custom Hooks:
Building your own Hooks lets you extract component logic into reusable
functions. A custom Hook is a JavaScript function whose name starts
with "use" and that may call other Hooks.

Rules of Hooks:
1. Only call Hooks at the top level.
2. Only call Hooks from React functions.

Hooks are fully backward-compatible and are the recommended way to
write React components going forward.""",
    },
    {
        "title": "Python FastAPI vs Flask",
        "author": "Hani",
        "content": """FastAPI is a modern web framework for building APIs with Python.

Key Differences:

1. Performance:
FastAPI is based on Starlette and is async-native, making it faster
than Flask for I/O-bound operations.

2. Type Hints:
FastAPI uses Python type hints for automatic request validation
and serialization. Flask requires manual validation.

3. Auto Documentation:
FastAPI generates OpenAPI/Swagger docs automatically.
Flask needs Flasgger or similar extensions.

4. Async Support:
FastAPI has built-in async support. Flask requires Quart for async.

5. Community:
Flask has a larger community and more extensions.
FastAPI is newer but growing rapidly.

6. When to use Flask:
Simple applications, smaller teams, need maximum flexibility.

7. When to use FastAPI:
API-heavy applications, need performance, want automatic docs,
using async operations.

8. Database Integration:
Both work with SQLAlchemy. FastAPI's dependency injection
makes database sessions cleaner.

9. Testing:
Both support pytest. FastAPI's TestClient is intuitive.

10. Deployment:
Both can run behind uvicorn/gunicorn. FastAPI is natively
compatible with ASGI servers.""",
    },
]

db = SessionLocal()
for s in sample_topics:
    exists = db.query(Topic).filter(Topic.title == s["title"]).first()
    if exists:
        print(f"  Skipping: {s['title']}")
        continue
    topic = Topic(title=s["title"], content=s["content"], author=s["author"])
    db.add(topic)
    db.commit()
    print(f"  Added: {s['title']}")

db.close()
print("Done.")
