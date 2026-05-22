import { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";
const WS_URL = "ws://127.0.0.1:8000/ws";

function App() {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("all");
  const [connectionStatus, setConnectionStatus] = useState("Disconnected");

  async function fetchTasks() {
    try {
      const response = await axios.get(`${API_URL}/tasks`);
      setTasks(response.data);
    } catch (error) {
      console.error("Error fetching tasks:", error);
    } finally {
      setLoading(false);
    }
  }

  async function updateTaskStatus(taskId, newStatus) {
    try {
      await axios.patch(`${API_URL}/tasks/${taskId}`, {
        status: newStatus,
      });
    } catch (error) {
      console.error("Error updating task:", error);
      alert("Could not update task.");
    }
  }

  async function deleteTask(taskId) {
    const confirmed = confirm("Are you sure you want to delete this task?");

    if (!confirmed) return;

    try {
      await axios.delete(`${API_URL}/tasks/${taskId}`);
    } catch (error) {
      console.error("Error deleting task:", error);
      alert("Could not delete task.");
    }
  }

  useEffect(() => {
    fetchTasks();

    const socket = new WebSocket(WS_URL);

    socket.onopen = () => {
      setConnectionStatus("Connected");
      console.log("WebSocket connected");
    };

    socket.onmessage = (event) => {
      console.log("WebSocket message:", event.data);
      fetchTasks();
    };

    socket.onclose = () => {
      setConnectionStatus("Disconnected");
      console.log("WebSocket disconnected");
    };

    socket.onerror = (error) => {
      setConnectionStatus("Error");
      console.error("WebSocket error:", error);
    };

    return () => {
      socket.close();
    };
  }, []);

  const filteredTasks =
    filter === "all"
      ? tasks
      : tasks.filter((task) => task.status === filter);

  const pendingCount = tasks.filter((task) => task.status === "pending").length;
  const inProgressCount = tasks.filter(
    (task) => task.status === "in_progress"
  ).length;
  const completedCount = tasks.filter(
    (task) => task.status === "completed"
  ).length;

  return (
    <div className="app">
      <header className="header">
        <h1>AI Task Bot Dashboard</h1>
        <p>Manage tasks created from Telegram or API.</p>
        <p className="connection">Realtime: {connectionStatus}</p>
      </header>

      <section className="stats">
        <div className="stat-card">
          <h3>Total</h3>
          <p>{tasks.length}</p>
        </div>

        <div className="stat-card">
          <h3>Pending</h3>
          <p>{pendingCount}</p>
        </div>

        <div className="stat-card">
          <h3>In Progress</h3>
          <p>{inProgressCount}</p>
        </div>

        <div className="stat-card">
          <h3>Completed</h3>
          <p>{completedCount}</p>
        </div>
      </section>

      <section className="toolbar">
        <button onClick={fetchTasks}>Refresh</button>

        <select value={filter} onChange={(e) => setFilter(e.target.value)}>
          <option value="all">All tasks</option>
          <option value="pending">Pending</option>
          <option value="in_progress">In Progress</option>
          <option value="completed">Completed</option>
        </select>
      </section>

      {loading ? (
        <p>Loading tasks...</p>
      ) : filteredTasks.length === 0 ? (
        <p>No tasks found.</p>
      ) : (
        <div className="task-grid">
          {filteredTasks.map((task) => (
            <div className="task-card" key={task.id}>
              <div className="task-top">
                <span className="task-id">#{task.id}</span>
                <span className={`status ${task.status}`}>
                  {task.status}
                </span>
              </div>

              <h2>{task.title}</h2>

              {task.description && <p>{task.description}</p>}

              <div className="task-meta">
                <span>Source: {task.source}</span>
                <span>
                  Created: {new Date(task.created_at).toLocaleString()}
                </span>
              </div>

              <div className="actions">
                <button onClick={() => updateTaskStatus(task.id, "pending")}>
                  Pending
                </button>

                <button onClick={() => updateTaskStatus(task.id, "in_progress")}>
                  In Progress
                </button>

                <button onClick={() => updateTaskStatus(task.id, "completed")}>
                  Completed
                </button>

                <button className="delete" onClick={() => deleteTask(task.id)}>
                  Delete
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default App;