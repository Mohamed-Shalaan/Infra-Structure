import streamlit as st
from datetime import datetime, timedelta, time

# Backend Functions
def calculate_sleep_time(wake_up_time, bedtime):
    if wake_up_time:
        bedtime = wake_up_time - timedelta(hours=8)  # Default to 8 hours
    elif bedtime:
        wake_up_time = bedtime + timedelta(hours=8)
    return wake_up_time, bedtime

def schedule_meals(wake_up_time, bedtime, num_meals):
    total_time = bedtime - wake_up_time
    interval = total_time / (num_meals + 1)
    meal_times = [wake_up_time + interval * (i + 1) for i in range(num_meals)]
    return meal_times

def calculate_free_slots(fixed_obligations, wake_up_time, bedtime):
    free_slots = []
    fixed_obligations.sort()  # Sort by start time
    previous_end = wake_up_time
    for obligation in fixed_obligations:
        # Convert obligation times to datetime.datetime using today's date
        obligation_start = datetime.combine(datetime.today(), obligation[0])
        obligation_end = datetime.combine(datetime.today(), obligation[1])
        
        if obligation_start > previous_end:
            free_slots.append((previous_end, obligation_start))
        previous_end = obligation_end
    if previous_end < bedtime:
        free_slots.append((previous_end, bedtime))
    return free_slots

def schedule_workout(free_slots, workout_duration):
    for slot in free_slots:
        if slot[1] - slot[0] >= workout_duration:
            return (slot[0], slot[0] + workout_duration)
    return None

# Streamlit App
st.title("Personalized Daily/Weekly Schedule Planner")

# User Inputs
st.sidebar.header("User Inputs")
wake_up_time = st.sidebar.time_input("Wake-up Time", time(7, 0))
bedtime = st.sidebar.time_input("Bedtime", time(22, 0))
num_meals = st.sidebar.number_input("Number of Meals", min_value=1, max_value=6, value=3)
workout_duration = st.sidebar.number_input("Workout Duration (minutes)", min_value=15, max_value=120, value=60)

# Fixed Obligations
st.sidebar.header("Fixed Obligations")
num_obligations = st.sidebar.number_input("Number of Obligations", min_value=0, max_value=10, value=2)
fixed_obligations = []
for i in range(num_obligations):
    start_time = st.sidebar.time_input(f"Obligation {i+1} Start Time", key=f"start_{i}")
    end_time = st.sidebar.time_input(f"Obligation {i+1} End Time", key=f"end_{i}")
    fixed_obligations.append((start_time, end_time))

# Convert wake_up_time and bedtime to datetime.datetime
wake_up_time = datetime.combine(datetime.today(), wake_up_time)
bedtime = datetime.combine(datetime.today(), bedtime)

# Calculate Schedule
wake_up_time, bedtime = calculate_sleep_time(wake_up_time, bedtime)
meal_times = schedule_meals(wake_up_time, bedtime, num_meals)
free_slots = calculate_free_slots(fixed_obligations, wake_up_time, bedtime)
workout_time = schedule_workout(free_slots, timedelta(minutes=workout_duration))

# Display Schedule
st.header("Your Schedule")
st.write(f"**Wake-up Time:** {wake_up_time.strftime('%H:%M')}")
st.write(f"**Bedtime:** {bedtime.strftime('%H:%M')}")
st.write("**Meal Times:**")
for i, meal_time in enumerate(meal_times):
    st.write(f"Meal {i+1}: {meal_time.strftime('%H:%M')}")
if workout_time:
    st.write(f"**Workout Time:** {workout_time[0].strftime('%H:%M')} - {workout_time[1].strftime('%H:%M')}")
else:
    st.write("**Workout Time:** No available slot found.")
st.write("**Free Time Slots:**")
for slot in free_slots:
    st.write(f"{slot[0].strftime('%H:%M')} - {slot[1].strftime('%H:%M')}")