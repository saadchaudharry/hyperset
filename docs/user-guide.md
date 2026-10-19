# User guide

The app has five tabs: **Today**, **Plan**, **Exercises**, **Coach** and **Profile**. On a phone they sit in the bottom bar; on a computer they're in the top bar.

## Today: log your workout

Today shows the workout your plan has for that weekday. Use the arrows, the date picker or the week strip to open another day. A dot on a day in the week strip means you completed at least one exercise.

The tiles at the top show calories and protein against your targets, exercises done and sets logged.

<p>
  <img src="screenshots/03-today.png" width="240" alt="Today screen">
  <img src="screenshots/04-log-sets.png" width="240" alt="Logging sets">
</p>

For each exercise:

1. Enter **reps** and **weight (kg)** for each set. The placeholders show the target rep range.
2. Tap **+ Set** to add more sets.
3. Tick **Completed** when you're done, then tap **Save**.
4. Tap **How to do it** for the form steps and mistakes to avoid.

### Exercises that aren't in the plan

Use **Not in the plan? Add an exercise** near the top. Search the library, tap **Add**, and log it like any other exercise. It's labelled **Extra** and has an **×** button to remove it from that day. Rest days work the same way.

<img src="screenshots/05-extra-exercise.png" width="240" alt="Extra exercise card">

## Food

Scroll down Today to **Food**.

1. Pick the meal.
2. Describe what you ate, with amounts if you know them: "3 rotis, 1 katori dal, 150 g paneer bhurji".
3. Tap **Add food**. Gemini estimates calories, protein, carbs and fat, and explains the breakdown. The entry is marked **AI**.

If you already know the numbers, open **I know the calories** and type them in; no AI is used then. Tap **×** to delete an entry.

<img src="screenshots/06-food.png" width="240" alt="Food log">

## Plan: your weekly template

Every day on Today uses this template.

- Change a day's **title** and **focus** and tap **Save day**.
- Change an exercise's **sets**, **reps** (text such as `8-12` or `45 s`) and **rest**, then tap **Save**.
- Reorder with **↑ ↓** and remove with **×**.
- Add exercises with the search box at the bottom of each day.

A day with no exercises is a rest day.

<img src="screenshots/07-plan.png" width="240" alt="Weekly plan">

## Exercises: the library

Search by name and filter by muscle group and equipment. Tap an exercise to see its form guide, a link to form videos, which plan days use it, and your history for it. Use **Edit exercise** to change its details or instructions, and **+ Add a new exercise** on the list page to create your own.

<p>
  <img src="screenshots/08-exercises.png" width="240" alt="Exercise library">
  <img src="screenshots/09-exercise-detail.png" width="240" alt="Exercise detail">
</p>

## Coach: AI guidance

Ask anything about training, food or recovery, or tap a quick question:

- **Rest of today's food**: what to eat to reach today's calories and protein.
- **Review my week**: what you did, missed, and should do next.
- **Next workout targets**: weights and reps to aim for.
- **Am I on track?**: a check on the last 14 days.

The coach looks up your profile, plan, food, workouts and body weight itself before answering. **Clear chat** starts a new conversation.

<img src="screenshots/10-coach.png" width="240" alt="AI coach">

## Profile: your stats and report

At the top: weight, height, age and BMI. Expand **Basic info and targets** to update them. Saving logs today's weight and waist.

Below is a report for the last **7, 30 or 90 days**:

- **Insights**, marked *On track* or *Needs attention*:
  - weekly weight gain against the 0.1-0.25 kg lean-gain target
  - waist growing too fast
  - average calories against your target
  - how many days you hit your protein target
  - workout consistency and which planned workouts you missed
  - your best strength gain, and lifts that have stalled for 3 sessions
- **Summary tiles**: workouts, average calories and protein, weight change, sets and volume, days with food logged.
- **Charts**: calories and protein per day (darker bars reached the target), body weight, and weekly training volume. Tap a bar or point to see its value.
- **Sets per muscle group**, with sets per week.
- **Strength progress**: each exercise's latest best set against its first in the period.

<p>
  <img src="screenshots/11-profile.png" width="200" alt="Profile">
  <img src="screenshots/13-insights.png" width="200" alt="Insights">
  <img src="screenshots/14-charts.png" width="200" alt="Charts">
  <img src="screenshots/15-strength.png" width="200" alt="Strength progress">
</p>

## Logging in and out

Every page needs a login. **Log out** is in the top bar. **Forgot password?** on the login screen emails a reset link (see [configuration](configuration.md#password-reset-emails) for email setup).

## Settings (admin)

**Settings** opens the Django admin, where you can:

- set the Gemini API key and model (**AI settings**)
- edit your profile and targets (**Profile**)
- fix any record directly: exercises, plan days, workout logs, food entries, body measurements and coach messages
- add users (**Users**). All users share the same data; the app is built for one person.
