   📘 **Smart Task Analyzer**

### Intelligent Task Prioritization System (Django REST API + HTML/JavaScript Frontend)

## 📌 **Overview**

**Smart Task Analyzer** is an intelligent task ranking and recommendation system that identifies which task should be completed first—and explains why.
It evaluates tasks using a weighted scoring algorithm based on:

* **Urgency** (due date / overdue days)
* **Importance** (impact value from 1–10)
* **Effort** (estimated hours — quick wins score higher)
* **Dependencies** (tasks blocking other tasks)

The project includes:

* A fully functional **Django REST API backend**
* A clean, responsive **HTML + JavaScript frontend**
* Real-time prioritization
* Multiple scoring strategies
* Detailed explanations for every score

This project is ideal for internship assignments, portfolio showcases, and real-world productivity tools.

---

# 🚀 **Features**

## 🔧 **Backend (Django REST Framework)**

### ✔ `/api/tasks/analyze/` — *POST*

Analyzes a list of tasks and returns:

* Computed **priority score**
* Detailed explanation:

  * urgency
  * importance
  * effort impact
  * dependency weight
* Tasks sorted by priority
* Circular dependency detection

### ✔ `/api/tasks/suggest/?strategy=` — *GET*

Returns **Top 3 recommended tasks**.

Supported strategies:

| Strategy     | Behavior                           |
| ------------ | ---------------------------------- |
| `smart`      | Backend weighted scoring (default) |
| `fastest`    | Shortest estimated hours           |
| `highimpact` | Highest importance                 |
| `deadline`   | Earliest due date                  |

---

# 🎨 **Frontend (HTML + JavaScript)**

* Manual task input
* Paste JSON task lists
* Analyze using **Smart Balance (backend)**
* Client-side strategies:

  * Fastest Wins
  * High Impact First
  * Earliest Deadline
* Task cards with:

  * Score
  * Explanation
  * Priority sorting
* Top 3 task suggestions
* Responsive, minimal UI

---

# 🏗 **Tech Stack**

### **Backend**

* Python 3.10+
* Django 4.x
* Django REST Framework

### **Frontend**

* HTML5
* CSS3
* JavaScript (Fetch API)

---

# 📂 **Project Structure**

```
Smart-Task-Analyzer/
│
├── backend/
│   ├── manage.py
│   ├── task_analyzer/
│   └── api/
│       ├── views.py
│       ├── urls.py
│       └── utils.py
│
├── frontend/
│   ├── index.html
│   ├── script.js
│   ├── styles.css
│
├── documentation/
│   ├── ChatGPT_Usage_Notes.txt
│
└── README.md
```

---

# ⚙️ **Installation & Running**

## 1️⃣ Clone Repository

```
git clone https://github.com/your-username/Smart-Task-Analyzer.git
cd Smart-Task-Analyzer
```

---

## 2️⃣ Create & Activate Virtual Environment

```
python -m venv env
env\Scripts\activate
```

---

## 3️⃣ Install Dependencies

```
pip install -r requirements.txt
```

---

## 4️⃣ Run Django Backend

```
cd backend
python manage.py runserver
```

API is available at:

```
http://127.0.0.1:8000/api/tasks/analyze/
```

---

# 🌐 **Running the Frontend (IMPORTANT)**

Do **NOT** open index.html like this:

```
file:///C:/.../index.html
```

This causes:

❌ *NetworkError when attempting to fetch resource*

Because browsers block local file → HTTP requests.

---

## ✅ FIX — Start a Local Web Server

Inside the `frontend/` folder:

```
python -m http.server 5500
```

Now open:

```
http://127.0.0.1:5500/index.html
```

Frontend + backend will work perfectly.

---

# 🧪 **API Documentation**

---

## 🔥 POST `/api/tasks/analyze/`

### Request Body Example

```json
{
  "tasks": [
    {
      "id": "1",
      "title": "Fix critical bug",
      "due_date": "2025-02-02",
      "estimated_hours": 2,
      "importance": 9
    },
    {
      "id": "2",
      "title": "Prepare slides",
      "due_date": "2025-02-05",
      "estimated_hours": 3,
      "importance": 7
    }
  ]
}
```

---

## 🔥 Example Response

```json
{
  "tasks": [
    {
      "id": "1",
      "title": "Fix critical bug",
      "score": 8.21,
      "explanation": [
        "urgency: 10.00 (overdue by 3 day(s))",
        "importance: 9.00",
        "effort: 3.33",
        "dependency: 0.00"
      ]
    }
  ]
}
```

---

## 🔥 GET `/api/tasks/suggest/?strategy=smart`

Returns top 3 tasks based on selected strategy.

---

# 🧠 **Smart Scoring Algorithm**

```
final_score =
(urgency × 0.35) +
(importance × 0.35) +
(effort_score × 0.15) +
(dependency_score × 0.15)
```

### Factors:

* Urgency → overdue tasks get highest weight
* Importance → higher importance = higher priority
* Effort → small tasks get a "quick win" boost
* Dependencies → tasks blocking others get priority

---

# 📚 **Sample JSON for Frontend Testing**

```json
[
  {
    "id": "1",
    "title": "Fix critical bug",
    "due_date": "2025-02-02",
    "estimated_hours": 2,
    "importance": 9
  },
  {
    "id": "2",
    "title": "Prepare meeting slides",
    "due_date": "2025-02-05",
    "estimated_hours": 3,
    "importance": 7
  },
  {
    "id": "3",
    "title": "Email client",
    "due_date": "2025-02-01",
    "estimated_hours": 1,
    "importance": 5
  }
]
```

---

# 🧩 **Error Handling**

The system gracefully handles:

* Invalid JSON
* Missing fields
* Wrong data types
* Circular dependencies
* Empty task list
* Unsupported strategies

All errors return clear messages.


# 🏁 **Conclusion**

The **Smart Task Analyzer** is a complete, production-ready task prioritization system with:

* A powerful REST backend
* Interactive modern frontend
* Detailed scoring algorithm
* Multiple prioritization strategies
* Clean architecture
* Clear documentation

