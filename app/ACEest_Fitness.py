# app/ACEest_Fitness.py
# Headless-friendly version: GUI (Tkinter) only if available, plus a Flask API for deployments.

# ---- Try Tkinter (desktop GUI); skip gracefully in containers ----
GUI_AVAILABLE = True
try:
    import tkinter as tk
    from tkinter import messagebox
except Exception:
    GUI_AVAILABLE = False
    tk = None
    messagebox = None

# ---- Flask API (used in Docker/Kubernetes) ----
from flask import Flask, jsonify, request

app = Flask(__name__)

# Simple in-memory store (shared by GUI and API)
workouts = []  # each item: {"workout": str, "duration": int}

@app.get("/")
def index():
    return (
        "<h1>ACEest Fitness API</h1>"
        f"<p>Status: OK</p>"
        f"<p>Workouts logged: {len(workouts)}</p>"
        "<p>Use <code>GET /api/workouts</code> and <code>POST /api/workouts</code></p>"
    )

@app.get("/health")
def health():
    return jsonify(status="ok", service="aceest-fitness")

@app.get("/api/workouts")
def list_workouts():
    return jsonify(workouts=workouts)

@app.post("/api/workouts")
def add_workout():
    data = request.get_json(silent=True) or {}
    workout = (data.get("workout") or "").strip()
    duration = data.get("duration")

    if not workout or duration is None:
        return jsonify(error="Please provide 'workout' and 'duration'"), 400

    try:
        duration = int(duration)
        if duration <= 0:
            raise ValueError
    except Exception:
        return jsonify(error="'duration' must be a positive integer"), 400

    workouts.append({"workout": workout, "duration": duration})
    return jsonify(message="Added", workout=workout, duration=duration), 201


# ---- Desktop GUI (only defined/run if Tkinter is available) ----
if GUI_AVAILABLE:
    class FitnessTrackerApp:
        def __init__(self, master):
            self.master = master
            master.title("ACEestFitness and Gym")

            # Labels and Entries
            self.workout_label = tk.Label(master, text="Workout:")
            self.workout_label.grid(row=0, column=0, padx=5, pady=5)
            self.workout_entry = tk.Entry(master)
            self.workout_entry.grid(row=0, column=1, padx=5, pady=5)

            self.duration_label = tk.Label(master, text="Duration (minutes):")
            self.duration_label.grid(row=1, column=0, padx=5, pady=5)
            self.duration_entry = tk.Entry(master)
            self.duration_entry.grid(row=1, column=1, padx=5, pady=5)

            # Buttons
            self.add_button = tk.Button(master, text="Add Workout", command=self.add_workout)
            self.add_button.grid(row=2, column=0, columnspan=2, pady=10)

            self.view_button = tk.Button(master, text="View Workouts", command=self.view_workouts)
            self.view_button.grid(row=3, column=0, columnspan=2, pady=5)

        def add_workout(self):
            workout = self.workout_entry.get().strip()
            duration_str = self.duration_entry.get().strip()

            if not workout or not duration_str:
                messagebox.showerror("Error", "Please enter both workout and duration.")
                return

            try:
                duration = int(duration_str)
                if duration <= 0:
                    raise ValueError
                workouts.append({"workout": workout, "duration": duration})
                messagebox.showinfo("Success", f"'{workout}' added successfully!")
                self.workout_entry.delete(0, tk.END)
                self.duration_entry.delete(0, tk.END)
            except ValueError:
                messagebox.showerror("Error", "Duration must be a positive number.")

        def view_workouts(self):
            if not workouts:
                messagebox.showinfo("Workouts", "No workouts logged yet.")
                return
            workout_list = "Logged Workouts:\n"
            for i, entry in enumerate(workouts, start=1):
                workout_list += f"{i}. {entry['workout']} - {entry['duration']} minutes\n"
            messagebox.showinfo("Workouts", workout_list)

# ---- Entrypoint ----
if __name__ == "__main__":
    if GUI_AVAILABLE:
        # Run the desktop GUI locally
        root = tk.Tk()
        app_gui = FitnessTrackerApp(root)
        root.mainloop()
    else:
        # Fallback: run Flask dev server if Tk isn't available
        app.run(host="0.0.0.0", port=5000)
