from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import HTMLResponse

app = FastAPI()

class UserInput(BaseModel):
    prompt: str

# -------- Stage 1: Intent Extraction --------
def extract_intent(prompt):
    p = prompt.lower()
    features = []

    if "login" in p: features.append("login")
    if "dashboard" in p: features.append("dashboard")
    if "contact" in p: features.append("contacts")
    if "admin" in p: features.append("admin")

    return {
        "app": "CRM" if "crm" in p else "General App",
        "features": features
    }

# -------- Stage 2: System Design --------
def design_system(intent):
    return {
        "entities": ["User", "Contact"],
        "roles": ["admin", "user"] if "admin" in intent["features"] else ["user"]
    }

# -------- Stage 3: Schema Generation --------
def generate_schema(design):
    return {
        "database": {
            "User": ["id", "email", "password"],
            "Contact": ["id", "name", "phone"]
        },
        "api": {
            "/login": "POST",
            "/contacts": "GET"
        }
    }

# -------- Stage 4: Validation --------
def validate_schema(schema):
    errors = []

    if "database" not in schema:
        errors.append("Missing database")

    if "api" not in schema:
        errors.append("Missing API")

    if "/contacts" in schema.get("api", {}) and "Contact" not in schema.get("database", {}):
        errors.append("Mismatch: API uses contacts but DB missing")

    return errors

# -------- Retry Mechanism --------
def generate_with_retry(design, max_retries=2):
    for attempt in range(max_retries):
        schema = generate_schema(design)
        errors = validate_schema(schema)

        if not errors:
            return schema, errors, attempt + 1

    return schema, errors, max_retries

# -------- MAIN API --------
@app.post("/generate")
def generate_app(data: UserInput):
    intent = extract_intent(data.prompt)
    design = design_system(intent)

    schema, errors, attempts = generate_with_retry(design)

    return {
        "stage_1_intent": intent,
        "stage_2_design": design,
        "stage_3_schema": schema,
        "stage_4_validation": errors,
        "retry_attempts": attempts
    }

# -------- Simple UI --------
@app.get("/ui", response_class=HTMLResponse)
def ui():
    return """
    <html>
    <body>
        <h2>AI App Generator (Reliable Pipeline)</h2>
        <p>This system converts natural language into structured application configs using a multi-stage pipeline with validation and retry logic.</p>

        <textarea id="prompt" rows="4" cols="50">Build CRM with login dashboard contacts admin</textarea><br>
        <button onclick="generate()">Generate</button>

        <h3>Output:</h3>
        <pre id="output"></pre>

        <script>
        async function generate() {
            const prompt = document.getElementById("prompt").value;

            const res = await fetch("/generate", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({prompt})
            });

            const data = await res.json();
            document.getElementById("output").textContent = JSON.stringify(data, null, 2);
        }
        </script>
    </body>
    </html>
    """