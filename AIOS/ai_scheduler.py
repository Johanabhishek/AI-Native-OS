import numpy as np
from sklearn.linear_model import LinearRegression

# ==========================================
# PART 1: GENERATE FAKE "HISTORY"
# We need to teach the AI what tasks look like.
# ==========================================
print("1. Generating Historical Data")

# Let's pretend we have 3 types of apps:
# Type 0: Background Task (Always fast, ~10ms)
# Type 1: Word Processor (Medium, ~50ms)
# Type 2: Video Game (Heavy, ~100ms)

# We create 1000 random past tasks to train the brain
# Feature: [App_Type_ID]
X_history = np.random.randint(0, 3, (1000, 1)) 

# Target: How long they actually took (with some random noise)
# Logic: If Type is 0 -> 10ms. Type 2 -> 100ms.
y_history = []
for task_type in X_history:
    if task_type == 0: duration = 10 + np.random.normal(0, 2)
    elif task_type == 1: duration = 50 + np.random.normal(0, 5)
    else: duration = 100 + np.random.normal(0, 10)
    y_history.append(duration)

print(f"Generated {len(y_history)} past tasks for training.")


# ==========================================
# PART 2: THE AI "BRAIN"
# We train a simple model to predict duration based on App ID
# ==========================================
print("\n2. Training the AI Brain")
model = LinearRegression()
model.fit(X_history, y_history)
print("AI is trained! It can now guess how long a task will take.")


# ==========================================
# PART 3: THE SIMULATION
# New tasks arrive. We compare "Dumb OS" vs "AI OS"
# ==========================================
print("\n3. Running Simulation")

# 5 new tasks arrive in the queue:
# [Heavy, Fast, Fast, Heavy, Medium]
queue_task_types = np.array([[2], [0], [0], [2], [1]])

# 1. TRADITIONAL OS (First Come, First Served)
# It just runs them in the order they arrived: 2, 0, 0, 2, 1
# The small tasks (0) get stuck behind the big one (2).
total_wait_dumb = 0
current_wait = 0
for task in queue_task_types:
    # Use the AI to cheat and see how long it actually takes
    actual_time = model.predict([task])[0] 
    total_wait_dumb += current_wait
    current_wait += actual_time

print(f"Traditional OS Total Wait Time: {int(total_wait_dumb)} ms")


# 2. AI-NATIVE OS (Shortest Job First)
# The AI predicts the time FIRST, then re-orders the queue.
predictions = model.predict(queue_task_types)

# Combine the Task ID with its Predicted Time
tasks_with_predictions = []
for i in range(len(queue_task_types)):
    tasks_with_predictions.append((queue_task_types[i], predictions[i]))

# SORT by predicted time (Smallest first)
tasks_with_predictions.sort(key=lambda x: x[1])

# Run them in the new order
total_wait_ai = 0
current_wait = 0
for task, predicted_time in tasks_with_predictions:
    actual_time = predicted_time # Simplified for simulation
    total_wait_ai += current_wait
    current_wait += actual_time

print(f"AI-Native OS Total Wait Time:   {int(total_wait_ai)} ms")

print("\n------------------------------------------------")
if total_wait_ai < total_wait_dumb:
    print("SUCCESS: The AI OS was faster because it reorganized the line!")
else:
    print("FAIL: The AI didn't help.")