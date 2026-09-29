import { useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [notes, setNotes] = useState("");
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const extractTasks = async () => {
    if (!notes.trim()) {
      setError("Please enter meeting notes.");
      return;
    }

    setLoading(true);
    setError("");
    setTasks([]);

    try {
      const response = await fetch(`${API_URL}/extract`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          notes,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Failed to extract tasks");
      }

      setTasks(data.tasks);
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>AI Meeting Task Extractor</h1>

      <p className="subtitle">
        Convert meeting notes into structured actionable tasks.
      </p>

      <textarea
        value={notes}
        onChange={(event) => setNotes(event.target.value)}
        placeholder="Paste your meeting notes here..."
        rows="10"
      />

      <button onClick={extractTasks} disabled={loading}>
        {loading ? "Extracting..." : "Extract Tasks"}
      </button>

      {error && <p className="error">{error}</p>}

      {tasks.length > 0 && (
        <div className="results">
          <h2>Extracted Tasks</h2>

          {tasks.map((task, index) => (
            <div className="task-card" key={index}>
              <h3>{task.title}</h3>

              <p>
                <strong>Assignee:</strong>{" "}
                {task.assignee || "Not specified"}
              </p>

              <p>
                <strong>Due date:</strong>{" "}
                {task.due_date || "Not specified"}
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default App;