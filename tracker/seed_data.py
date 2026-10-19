"""Default exercise library and weekly plan. Loaded once by migration 0002."""

# One exercise per line: name | muscle group | equipment | category
EXERCISE_LIBRARY = """
Barbell Bench Press | chest | barbell | compound
Incline Barbell Bench Press | chest | barbell | compound
Decline Barbell Bench Press | chest | barbell | compound
Dumbbell Bench Press | chest | dumbbell | compound
Incline Dumbbell Press | chest | dumbbell | compound
Decline Dumbbell Press | chest | dumbbell | compound
Flat Machine Chest Press | chest | machine | compound
Incline Machine Chest Press | chest | machine | compound
Decline Machine Chest Press | chest | machine | compound
Smith Machine Bench Press | chest | smith | compound
Smith Machine Incline Press | chest | smith | compound
Floor Press | chest | barbell | compound
Dumbbell Floor Press | chest | dumbbell | compound
Spoto Press | chest | barbell | compound
Guillotine Press | chest | barbell | compound
Weighted Push-Up | chest | bodyweight | compound
Push-Up | chest | bodyweight | compound
Incline Push-Up | chest | bodyweight | compound
Decline Push-Up | chest | bodyweight | compound
Wide Push-Up | chest | bodyweight | compound
Archer Push-Up | chest | bodyweight | compound
Ring Push-Up | chest | other | compound
Chest Dip | chest | bodyweight | compound
Dumbbell Fly | chest | dumbbell | isolation
Incline Dumbbell Fly | chest | dumbbell | isolation
Cable Chest Fly | chest | cable | isolation
Low-to-High Cable Fly | chest | cable | isolation
High-to-Low Cable Fly | chest | cable | isolation
Single-Arm Cable Fly | chest | cable | isolation
Pec Deck Fly | chest | machine | isolation
Dumbbell Pullover | chest | dumbbell | isolation
Svend Press | chest | other | isolation
Conventional Deadlift | back | barbell | compound
Sumo Deadlift | back | barbell | compound
Deficit Deadlift | back | barbell | compound
Rack Pull | back | barbell | compound
Snatch-Grip Deadlift | back | barbell | compound
Pull-Up | back | bodyweight | compound
Wide-Grip Pull-Up | back | bodyweight | compound
Neutral-Grip Pull-Up | back | bodyweight | compound
Weighted Pull-Up | back | bodyweight | compound
Chin-Up | back | bodyweight | compound
Weighted Chin-Up | back | bodyweight | compound
Assisted Pull-Up | back | machine | compound
Lat Pulldown | back | cable | compound
Wide-Grip Lat Pulldown | back | cable | compound
Close-Grip Lat Pulldown | back | cable | compound
Neutral-Grip Lat Pulldown | back | cable | compound
Reverse-Grip Lat Pulldown | back | cable | compound
Single-Arm Lat Pulldown | back | cable | compound
Machine Lat Pulldown | back | machine | compound
Straight-Arm Pulldown | back | cable | isolation
Rope Cable Pullover | back | cable | isolation
Machine Pullover | back | machine | isolation
Barbell Bent-Over Row | back | barbell | compound
Pendlay Row | back | barbell | compound
Yates Row | back | barbell | compound
Seal Row | back | barbell | compound
T-Bar Row | back | barbell | compound
Chest-Supported T-Bar Row | back | machine | compound
Landmine Row | back | barbell | compound
Meadows Row | back | barbell | compound
One-Arm Dumbbell Row | back | dumbbell | compound
Kroc Row | back | dumbbell | compound
Chest-Supported Row | back | dumbbell | compound
Renegade Row | back | dumbbell | compound
Seated Cable Row | back | cable | compound
Wide-Grip Seated Cable Row | back | cable | compound
One-Arm Cable Row | back | cable | compound
Machine Row | back | machine | compound
Iso-Lateral Row Machine | back | machine | compound
Inverted Row | back | bodyweight | compound
Ring Row | back | other | compound
Smith Machine Row | back | smith | compound
Back Extension | lower_back | bodyweight | isolation
Weighted Back Extension | lower_back | other | isolation
Superman | lower_back | bodyweight | isolation
Bird Dog | lower_back | bodyweight | isolation
Good Morning | hamstrings | barbell | compound
Jefferson Curl | mobility | barbell | stretch
Barbell Shrug | traps | barbell | isolation
Dumbbell Shrug | traps | dumbbell | isolation
Trap Bar Shrug | traps | trap_bar | isolation
Cable Shrug | traps | cable | isolation
Smith Machine Shrug | traps | smith | isolation
Overhead Shrug | traps | barbell | isolation
Snatch-Grip High Pull | traps | barbell | compound
Standing Barbell Overhead Press | shoulders | barbell | compound
Seated Barbell Shoulder Press | shoulders | barbell | compound
Seated Shoulder Press | shoulders | dumbbell | compound
Standing Dumbbell Shoulder Press | shoulders | dumbbell | compound
Machine Shoulder Press | shoulders | machine | compound
Smith Machine Shoulder Press | shoulders | smith | compound
Arnold Press | shoulders | dumbbell | compound
Push Press | shoulders | barbell | compound
Behind-the-Neck Press | shoulders | barbell | compound
Z Press | shoulders | barbell | compound
Landmine Press | shoulders | barbell | compound
Pike Push-Up | shoulders | bodyweight | compound
Handstand Push-Up | shoulders | bodyweight | compound
Dumbbell Lateral Raises | shoulders | dumbbell | isolation
Cable Lateral Raises | shoulders | cable | isolation
Machine Lateral Raise | shoulders | machine | isolation
Lean-Away Lateral Raise | shoulders | dumbbell | isolation
Seated Lateral Raise | shoulders | dumbbell | isolation
Lu Raise | shoulders | dumbbell | isolation
Dumbbell Front Raise | shoulders | dumbbell | isolation
Cable Front Raise | shoulders | cable | isolation
Plate Front Raise | shoulders | other | isolation
Barbell Upright Row | shoulders | barbell | compound
Cable Upright Row | shoulders | cable | compound
Reverse Pec Deck | shoulders | machine | isolation
Rear Delt Cable Fly | shoulders | cable | isolation
Bent-Over Rear Delt Raise | shoulders | dumbbell | isolation
Rear Delt Row | shoulders | dumbbell | compound
Face Pull | shoulders | cable | isolation
Band Pull-Apart | shoulders | band | isolation
Prone Y-T-W Raise | shoulders | dumbbell | isolation
Cuban Press | shoulders | dumbbell | isolation
Cable External Rotation | shoulders | cable | isolation
Dumbbell External Rotation | shoulders | dumbbell | isolation
Overhead Carry | shoulders | dumbbell | compound
Barbell Curl | biceps | barbell | isolation
EZ-Bar Biceps Curl | biceps | ez_bar | isolation
Dumbbell Curl | biceps | dumbbell | isolation
Alternating Dumbbell Curl | biceps | dumbbell | isolation
Hammer Curl | biceps | dumbbell | isolation
Cross-Body Hammer Curl | biceps | dumbbell | isolation
Incline Dumbbell Curl | biceps | dumbbell | isolation
Preacher Curl | biceps | ez_bar | isolation
Dumbbell Preacher Curl | biceps | dumbbell | isolation
Machine Preacher Curl | biceps | machine | isolation
Concentration Curl | biceps | dumbbell | isolation
Spider Curl | biceps | dumbbell | isolation
Drag Curl | biceps | barbell | isolation
Zottman Curl | biceps | dumbbell | isolation
Barbell 21s | biceps | barbell | isolation
Cable Curl | biceps | cable | isolation
Rope Hammer Curl | biceps | cable | isolation
Bayesian Cable Curl | biceps | cable | isolation
High Cable Curl | biceps | cable | isolation
Band Curl | biceps | band | isolation
Rope Triceps Pushdown | triceps | cable | isolation
Cable Triceps Pushdown | triceps | cable | isolation
Reverse-Grip Triceps Pushdown | triceps | cable | isolation
Single-Arm Cable Pushdown | triceps | cable | isolation
Overhead Cable Triceps Extension | triceps | cable | isolation
Overhead Dumbbell Triceps Extension | triceps | dumbbell | isolation
EZ-Bar Skull Crusher | triceps | ez_bar | isolation
Dumbbell Skull Crusher | triceps | dumbbell | isolation
JM Press | triceps | barbell | compound
Close-Grip Bench Press | triceps | barbell | compound
Diamond Push-Up | triceps | bodyweight | compound
Triceps Dip | triceps | bodyweight | compound
Bench Dip | triceps | bodyweight | compound
Machine Dip | triceps | machine | compound
Dumbbell Triceps Kickback | triceps | dumbbell | isolation
Cable Triceps Kickback | triceps | cable | isolation
Tate Press | triceps | dumbbell | isolation
Machine Triceps Extension | triceps | machine | isolation
Barbell Wrist Curl | forearms | barbell | isolation
Reverse Wrist Curl | forearms | barbell | isolation
Behind-the-Back Wrist Curl | forearms | barbell | isolation
Dumbbell Wrist Curl | forearms | dumbbell | isolation
Reverse Curl | forearms | ez_bar | isolation
Wrist Roller | forearms | other | isolation
Plate Pinch | forearms | other | isolation
Dead Hang | forearms | bodyweight | isolation
Farmer's Walk | forearms | dumbbell | compound
Crunch | abs | bodyweight | isolation
Cable Crunch | abs | cable | isolation
Machine Crunch | abs | machine | isolation
Decline Crunch | abs | bodyweight | isolation
Stability Ball Crunch | abs | other | isolation
Reverse Crunch | abs | bodyweight | isolation
Sit-Up | abs | bodyweight | isolation
V-Up | abs | bodyweight | isolation
Hanging Knee Raise | abs | bodyweight | isolation
Hanging Leg Raise | abs | bodyweight | isolation
Captain's Chair Leg Raise | abs | machine | isolation
Lying Leg Raise | abs | bodyweight | isolation
Toes-to-Bar | abs | bodyweight | isolation
Flutter Kicks | abs | bodyweight | isolation
Plank | abs | bodyweight | isolation
Weighted Plank | abs | other | isolation
RKC Plank | abs | bodyweight | isolation
Ab Wheel Rollout | abs | other | isolation
Dead Bug | abs | bodyweight | isolation
Hollow Body Hold | abs | bodyweight | isolation
Dragon Flag | abs | bodyweight | isolation
L-Sit | abs | bodyweight | isolation
Mountain Climber | abs | bodyweight | cardio
Bicycle Crunch | obliques | bodyweight | isolation
Russian Twist | obliques | medicine_ball | isolation
Side Plank | obliques | bodyweight | isolation
Pallof Press | obliques | cable | isolation
Cable Woodchop | obliques | cable | isolation
Oblique Crunch | obliques | bodyweight | isolation
Dumbbell Side Bend | obliques | dumbbell | isolation
Landmine Rotation | obliques | barbell | compound
Heel Touch | obliques | bodyweight | isolation
Windshield Wipers | obliques | bodyweight | isolation
Suitcase Carry | obliques | dumbbell | compound
Barbell Back Squat | quads | barbell | compound
Front Squat | quads | barbell | compound
Pause Squat | quads | barbell | compound
Box Squat | quads | barbell | compound
Safety Bar Squat | quads | other | compound
Zercher Squat | quads | barbell | compound
Overhead Squat | full_body | barbell | compound
Smith Machine Squat | quads | smith | compound
Hack Squat | quads | machine | compound
Pendulum Squat | quads | machine | compound
Belt Squat | quads | machine | compound
Goblet Squat | quads | dumbbell | compound
Heels-Elevated Goblet Squat | quads | dumbbell | compound
Landmine Squat | quads | barbell | compound
Bodyweight Squat | quads | bodyweight | compound
Pistol Squat | quads | bodyweight | compound
Sissy Squat | quads | bodyweight | isolation
Spanish Squat | quads | band | compound
Wall Sit | quads | bodyweight | isolation
Leg Press | quads | machine | compound
Single-Leg Leg Press | quads | machine | compound
Leg Extension | quads | machine | isolation
Reverse Nordic | quads | bodyweight | isolation
Bulgarian Split Squat | quads | dumbbell | compound
Split Squat | quads | dumbbell | compound
Walking Lunge | quads | dumbbell | compound
Forward Lunge | quads | dumbbell | compound
Reverse Lunge | quads | dumbbell | compound
Smith Machine Lunge | quads | smith | compound
Step-Up | quads | dumbbell | compound
Romanian Deadlift | hamstrings | barbell | compound
Dumbbell Romanian Deadlift | hamstrings | dumbbell | compound
Single-Leg Romanian Deadlift | hamstrings | dumbbell | compound
Stiff-Leg Deadlift | hamstrings | barbell | compound
Seated Leg Curl | hamstrings | machine | isolation
Lying Leg Curl | hamstrings | machine | isolation
Standing Leg Curl | hamstrings | machine | isolation
Nordic Hamstring Curl | hamstrings | bodyweight | isolation
Glute-Ham Raise | hamstrings | machine | isolation
Stability Ball Leg Curl | hamstrings | other | isolation
Sliding Leg Curl | hamstrings | bodyweight | isolation
Hip Thrust | glutes | barbell | compound
Machine Hip Thrust | glutes | machine | compound
Single-Leg Hip Thrust | glutes | bodyweight | compound
B-Stance Hip Thrust | glutes | barbell | compound
Glute Bridge | glutes | bodyweight | isolation
Single-Leg Glute Bridge | glutes | bodyweight | isolation
Frog Pump | glutes | bodyweight | isolation
Cable Pull-Through | glutes | cable | compound
Cable Glute Kickback | glutes | cable | isolation
Glute Kickback Machine | glutes | machine | isolation
Donkey Kick | glutes | bodyweight | isolation
45-Degree Back Extension | glutes | bodyweight | isolation
Reverse Hyperextension | glutes | machine | isolation
Curtsy Lunge | glutes | dumbbell | compound
Sumo Squat | adductors | dumbbell | compound
Lateral Lunge | adductors | dumbbell | compound
Cossack Squat | adductors | bodyweight | compound
Hip Adduction Machine | adductors | machine | isolation
Cable Hip Adduction | adductors | cable | isolation
Copenhagen Plank | adductors | bodyweight | isolation
Hip Abduction Machine | abductors | machine | isolation
Cable Hip Abduction | abductors | cable | isolation
Banded Lateral Walk | abductors | band | isolation
Clamshell | abductors | band | isolation
Side-Lying Leg Raise | abductors | bodyweight | isolation
Fire Hydrant | abductors | bodyweight | isolation
Standing Calf Raise | calves | machine | isolation
Seated Calf Raise | calves | machine | isolation
Smith Machine Calf Raise | calves | smith | isolation
Leg Press Calf Raise | calves | machine | isolation
Single-Leg Calf Raise | calves | dumbbell | isolation
Donkey Calf Raise | calves | machine | isolation
Tibialis Raise | calves | other | isolation
Neck Curl | neck | other | isolation
Neck Extension | neck | other | isolation
Lateral Neck Flexion | neck | other | isolation
Neck Harness Extension | neck | other | isolation
Power Clean | full_body | barbell | compound
Hang Clean | full_body | barbell | compound
Clean and Jerk | full_body | barbell | compound
Snatch | full_body | barbell | compound
Hang Snatch | full_body | barbell | compound
Push Jerk | full_body | barbell | compound
Thruster | full_body | barbell | compound
Trap Bar Deadlift | full_body | trap_bar | compound
Kettlebell Swing | full_body | kettlebell | compound
Kettlebell Clean | full_body | kettlebell | compound
Kettlebell Snatch | full_body | kettlebell | compound
Turkish Get-Up | full_body | kettlebell | compound
Dumbbell Devil Press | full_body | dumbbell | compound
Man Maker | full_body | dumbbell | compound
Wall Ball | full_body | medicine_ball | compound
Sled Push | full_body | other | compound
Sled Pull | full_body | other | compound
Tire Flip | full_body | other | compound
Bear Crawl | full_body | bodyweight | compound
Burpee | full_body | bodyweight | plyometric
Box Jump | quads | bodyweight | plyometric
Jump Squat | quads | bodyweight | plyometric
Jumping Lunge | quads | bodyweight | plyometric
Broad Jump | full_body | bodyweight | plyometric
Tuck Jump | full_body | bodyweight | plyometric
Depth Jump | quads | bodyweight | plyometric
Lateral Bound | glutes | bodyweight | plyometric
Skater Jump | glutes | bodyweight | plyometric
Clap Push-Up | chest | bodyweight | plyometric
Medicine Ball Chest Pass | chest | medicine_ball | plyometric
Medicine Ball Slam | full_body | medicine_ball | plyometric
Treadmill Running | cardio | machine | cardio
Incline Treadmill Walk | cardio | machine | cardio
Outdoor Running | cardio | bodyweight | cardio
Sprint Intervals | cardio | bodyweight | cardio
Brisk Walking | cardio | bodyweight | cardio
Hiking | cardio | bodyweight | cardio
Outdoor Cycling | cardio | other | cardio
Stationary Bike | cardio | machine | cardio
Assault Bike | cardio | machine | cardio
Rowing Machine | cardio | machine | cardio
Ski Erg | cardio | machine | cardio
Elliptical | cardio | machine | cardio
Stair Climber | cardio | machine | cardio
Swimming | cardio | other | cardio
Jump Rope | cardio | other | cardio
Jumping Jacks | cardio | bodyweight | cardio
High Knees | cardio | bodyweight | cardio
Shadow Boxing | cardio | bodyweight | cardio
Battle Ropes | cardio | other | cardio
Hip Flexor Stretch | mobility | bodyweight | stretch
Couch Stretch | mobility | bodyweight | stretch
Pigeon Stretch | mobility | bodyweight | stretch
Standing Hamstring Stretch | mobility | bodyweight | stretch
Standing Quad Stretch | mobility | bodyweight | stretch
Wall Calf Stretch | mobility | bodyweight | stretch
Doorway Chest Stretch | mobility | bodyweight | stretch
Cross-Body Shoulder Stretch | mobility | bodyweight | stretch
Overhead Triceps Stretch | mobility | bodyweight | stretch
Butterfly Stretch | mobility | bodyweight | stretch
Cobra Stretch | mobility | bodyweight | stretch
Child's Pose | mobility | bodyweight | stretch
Downward Dog | mobility | bodyweight | stretch
Cat-Cow | mobility | bodyweight | stretch
World's Greatest Stretch | mobility | bodyweight | stretch
Thoracic Rotation | mobility | bodyweight | stretch
90/90 Hip Switch | mobility | bodyweight | stretch
Deep Squat Hold | mobility | bodyweight | stretch
Ankle Mobility Drill | mobility | bodyweight | stretch
Scapular Wall Slide | mobility | bodyweight | stretch
Band Shoulder Dislocate | mobility | band | stretch
Foam Rolling | mobility | other | stretch
"""

# Form guides for the exercises in the default plan: (steps, mistakes to avoid)
INSTRUCTIONS = {
    "Incline Dumbbell Press": (
        ["Set the bench to 30° and sit back with a dumbbell on each thigh",
         "Kick the dumbbells up and lie back, shoulder blades pinned back and down",
         "Lower slowly until the dumbbells are beside your upper chest, elbows 45-60° from your body",
         "Press up and slightly in until your arms are straight over your shoulders"],
        ["Bench too steep (turns it into a shoulder press)", "Bouncing the dumbbells off the chest"]),
    "Flat Machine Chest Press": (
        ["Adjust the seat so the handles line up with mid-chest",
         "Sit tall with your back flat on the pad and feet planted",
         "Press the handles forward until your arms are almost straight",
         "Bring them back over 2-3 seconds until you feel a chest stretch"],
        ["Shoulders rolling forward at the end", "Short partial reps"]),
    "Cable Chest Fly": (
        ["Set both pulleys at shoulder height or slightly above and step forward into a split stance",
         "Start with arms wide and a fixed slight bend in the elbows",
         "Bring your hands together in front of your chest in a hugging arc",
         "Squeeze 1 second, then open slowly until you feel the stretch"],
        ["Turning it into a press by bending the elbows", "Going too heavy and losing the stretch"]),
    "Seated Shoulder Press": (
        ["Set the bench upright and keep your back fully on the pad",
         "Start with the dumbbells at about chin level, palms forward",
         "Press up and slightly in front of your face until arms are straight",
         "Lower back to chin level under control"],
        ["Arching off the pad", "Flaring the elbows straight out to the sides"]),
    "Dumbbell Lateral Raises": (
        ["Stand tall with a slight forward lean, dumbbells at your sides",
         "Raise your arms out to the side, leading with the elbows",
         "Stop at shoulder height with a slight bend in the elbows",
         "Lower slowly over 2 seconds"],
        ["Swinging with the body", "Shrugging the traps up"]),
    "Rope Triceps Pushdown": (
        ["Attach a rope to a high pulley and lean forward slightly",
         "Pin your elbows to your sides",
         "Push down until your arms are straight and pull the rope apart at the bottom",
         "Let your hands rise back to chest level without moving the elbows"],
        ["Elbows drifting forward", "Leaning over to push with body weight"]),
    "Overhead Cable Triceps Extension": (
        ["Face away from the cable stack in a staggered stance, rope behind your head",
         "Keep your upper arms beside your head, pointing forward and up",
         "Straighten your arms fully overhead",
         "Let the rope go deep behind your head for a full stretch"],
        ["Elbows flaring wide", "Cutting the stretch short"]),
    "Lat Pulldown": (
        ["Lock your thighs under the pad and grip slightly wider than your shoulders",
         "Lean back a little with your chest up",
         "Drive your elbows down to your ribs, pulling the bar to your upper chest",
         "Let the bar rise until your arms are fully stretched"],
        ["Pulling behind the neck", "Big body swing to move the weight"]),
    "Chest-Supported Row": (
        ["Lie chest-down on an incline bench with dumbbells hanging straight down",
         "Keep your chest on the pad the whole set",
         "Row the weights towards your lower ribs",
         "Squeeze your shoulder blades for 1 second, then lower fully"],
        ["Lifting your chest off the pad", "Shrugging instead of rowing"]),
    "Seated Cable Row": (
        ["Sit with feet on the platform and a slight knee bend",
         "Reach forward and let your shoulders stretch",
         "Sit tall and pull the handle to your belly button",
         "Return slowly to the stretch without rounding your lower back"],
        ["Rocking the torso back and forth", "Rounding the lower back"]),
    "Straight-Arm Pulldown": (
        ["Face a high pulley, hinge slightly at the hips, arms nearly straight",
         "Sweep the bar down in an arc towards your thighs",
         "Squeeze your lats at the bottom",
         "Let your arms rise back up slowly"],
        ["Bending your elbows into a pushdown", "Using momentum"]),
    "Reverse Pec Deck": (
        ["Sit facing the pad with the handles at shoulder height",
         "Grab the handles with arms almost straight",
         "Move your arms out wide in an arc, like pushing your hands to the walls",
         "Return slowly until your hands are close together"],
        ["Squeezing shoulder blades hard (shifts work to traps)", "Going too heavy"]),
    "EZ-Bar Biceps Curl": (
        ["Stand tall holding the EZ bar at the angled grips",
         "Keep your elbows by your sides",
         "Curl the bar up and squeeze at the top",
         "Lower over 2-3 seconds to straight arms"],
        ["Swinging the hips", "Elbows drifting forward"]),
    "Incline Dumbbell Curl": (
        ["Set the bench to 45-60° and lie back",
         "Let your arms hang straight down behind your torso",
         "Curl the dumbbells up without moving your upper arms",
         "Lower all the way to a full stretch"],
        ["Shoulders rolling forward", "Partial reps at the bottom"]),
    "Hammer Curl": (
        ["Stand holding dumbbells with palms facing each other",
         "Keep your elbows by your sides",
         "Curl up with thumbs pointing up",
         "Lower under control to straight arms"],
        ["Body swing", "Rushing the lowering"]),
    "Hack Squat": (
        ["Stand on the platform with feet shoulder width, shoulders under the pads",
         "Release the safety handles and brace your core",
         "Lower until your thighs are at least parallel, knees tracking over your toes",
         "Drive up through your whole foot without locking your knees hard"],
        ["Heels lifting off the platform", "Knees caving in", "Lower back leaving the pad"]),
    "Barbell Back Squat": (
        ["Bar on your upper back, feet shoulder width, toes slightly out",
         "Take a deep breath and brace your core",
         "Sit down and back, knees tracking over your toes, as deep as you can with a neutral spine",
         "Drive up through your whole foot to standing"],
        ["Heels lifting", "Knees caving in", "Lower back rounding at the bottom"]),
    "Romanian Deadlift": (
        ["Stand tall holding the bar in front of your thighs, knees soft",
         "Push your hips back and let the bar slide down close to your legs",
         "Stop when your hips stop moving back (usually mid-shin) and you feel your hamstrings stretch",
         "Squeeze your glutes and drive your hips forward to stand"],
        ["Rounding the back", "Turning it into a squat"]),
    "Leg Press": (
        ["Sit back with feet shoulder width in the middle of the platform",
         "Release the safeties and lower until your knees are near 90° or deeper",
         "Keep your lower back flat on the pad",
         "Press back up without locking your knees hard"],
        ["Lower back peeling off the pad", "Bouncing at the bottom"]),
    "Seated Leg Curl": (
        ["Set the lower pad just above your heels and lock the thigh pad down",
         "Lean slightly forward for a bigger stretch",
         "Curl your heels down and back as far as you can",
         "Pause, then let your legs straighten slowly"],
        ["Lifting the hips", "Fast, jerky reps"]),
    "Leg Extension": (
        ["Line up your knee with the machine pivot, pad on your lower shins",
         "Hold the handles and keep your hips down",
         "Straighten your legs and squeeze 1 second at the top",
         "Lower under control"],
        ["Kicking the weight up", "Hips lifting off the seat"]),
    "Standing Calf Raise": (
        ["Balls of your feet on the step, shoulders under the pads",
         "Keep your knees straight but not locked",
         "Drop your heels and pause 2 seconds at the deep stretch",
         "Rise all the way onto your toes"],
        ["Bouncing out of the bottom", "Short half reps"]),
    "Incline Machine Chest Press": (
        ["Adjust the seat so the handles are at upper-chest height",
         "Keep shoulder blades back and down",
         "Press up and forward until your arms are almost straight",
         "Lower for 2-3 seconds until you feel a chest stretch"],
        ["Shoulders shrugging up", "Locking out aggressively"]),
    "Neutral-Grip Lat Pulldown": (
        ["Use the close neutral handle with palms facing each other",
         "Lock your thighs under the pad and lean back slightly",
         "Drive your elbows down and slightly back to your upper chest",
         "Let your arms go fully straight at the top"],
        ["Leaning way back", "Cutting the top stretch short"]),
    "One-Arm Cable Row": (
        ["Hold a single handle and brace with your free hand",
         "Reach forward for a full stretch",
         "Pull your elbow back towards your hip",
         "Return slowly without twisting"],
        ["Twisting the torso to move the weight", "Shrugging"]),
    "Pec Deck Fly": (
        ["Set the seat so the handles are at mid-chest",
         "Sit tall with a slight elbow bend and chest proud",
         "Bring the handles together in front of you and squeeze 1 second",
         "Open slowly until you feel the stretch"],
        ["Shoulders rolling forward", "Letting the stack slam"]),
    "Cable Lateral Raises": (
        ["Set the pulley low and stand side-on to the stack",
         "Hold the handle with your arm across your body",
         "Raise your arm out to the side up to shoulder height",
         "Lower slowly, keeping tension on the cable"],
        ["Swinging", "Raising above shoulder height with the traps"]),
    "Rear Delt Cable Fly": (
        ["Set both pulleys at shoulder height and grab the opposite cables, arms crossed",
         "Keep your arms nearly straight",
         "Pull your arms out wide in an arc",
         "Return slowly to the crossed position"],
        ["Rowing with the elbows", "Too heavy, losing the arc"]),
    "Preacher Curl": (
        ["Sit with your armpits snug over the top of the pad",
         "Start with arms nearly straight",
         "Curl the bar up and squeeze",
         "Lower slowly to nearly straight arms"],
        ["Dropping fast at the bottom (elbow stress)", "Lifting the elbows off the pad"]),
    "Cable Triceps Pushdown": (
        ["Use a straight or angled bar on a high pulley",
         "Tuck your elbows at your sides",
         "Push down to a full lockout every rep",
         "Control the bar back up to chest level"],
        ["Elbows moving forward and back", "Shoulders rolling over the bar"]),
    "Goblet Squat": (
        ["Hold a dumbbell vertically against your chest, feet shoulder width",
         "Keep your chest tall",
         "Sit down between your knees with a smooth tempo",
         "Stand up by driving through your whole foot"],
        ["Rushing reps", "Heels lifting"]),
    "Bulgarian Split Squat": (
        ["Rear foot laces-down on a bench, front foot about a stride ahead",
         "Hold dumbbells at your sides",
         "Lower straight down until your back knee nearly touches the floor",
         "Push through the front foot to stand"],
        ["Pushing off the back leg", "Front knee caving in"]),
    "Lying Leg Curl": (
        ["Lie face down with the pad just above your heels",
         "Press your hips into the bench and hold the handles",
         "Curl your heels towards your glutes",
         "Lower over 2-3 seconds"],
        ["Hips lifting off the bench", "Partial range"]),
    "Hip Thrust": (
        ["Upper back on the bench edge, bar over your hips, feet flat",
         "Tuck your chin and keep your ribs down",
         "Drive through your heels until your hips are level with your knees",
         "Pause 1 second at the top, then lower"],
        ["Arching the lower back at lockout", "Feet too far out (shifts work to hamstrings)"]),
    "Seated Calf Raise": (
        ["Sit with the pad on your lower thighs and balls of your feet on the step",
         "Lower your heels to a deep stretch and pause 2 seconds",
         "Rise all the way onto your toes",
         "Lower slowly"],
        ["Bouncing", "Short range"]),
    "Hanging Knee Raise": (
        ["Hang from a bar with your shoulders active",
         "Raise your knees towards your chest",
         "Curl your pelvis up at the top",
         "Lower slowly without swinging"],
        ["Swinging for momentum", "Only lifting the knees without tilting the pelvis"]),
    "Cable Crunch": (
        ["Kneel facing a high pulley, rope held beside your head",
         "Keep your hips still",
         "Crunch your ribs down towards your hips",
         "Return slowly to upright"],
        ["Pulling with the arms", "Sitting back on the heels"]),
}

# weekday: (title, focus, [(exercise, sets, reps, rest), ...]). Weekdays without an entry are rest days.
DEFAULT_PLAN = {
    0: ("Push", "Upper chest and wider shoulders.", [
        ("Incline Dumbbell Press", 3, "8-12", "2-3 min"),
        ("Flat Machine Chest Press", 3, "8-12", "2 min"),
        ("Cable Chest Fly", 3, "12-15", "60-90 s"),
        ("Seated Shoulder Press", 3, "8-12", "2 min"),
        ("Dumbbell Lateral Raises", 4, "12-20", "60 s"),
        ("Rope Triceps Pushdown", 3, "10-15", "60-90 s"),
        ("Overhead Cable Triceps Extension", 2, "12-15", "60-90 s"),
    ]),
    1: ("Pull", "Back width, thickness, and biceps development.", [
        ("Lat Pulldown", 3, "8-12", "2 min"),
        ("Chest-Supported Row", 3, "8-12", "2 min"),
        ("Seated Cable Row", 3, "10-12", "90 s"),
        ("Straight-Arm Pulldown", 2, "12-15", "60-90 s"),
        ("Reverse Pec Deck", 3, "12-20", "60 s"),
        ("EZ-Bar Biceps Curl", 3, "8-12", "90 s"),
        ("Incline Dumbbell Curl", 3, "10-15", "60-90 s"),
        ("Hammer Curl", 2, "10-15", "60 s"),
    ]),
    2: ("Legs", "Complete leg development and strength.", [
        ("Hack Squat", 3, "6-10", "2-3 min"),
        ("Romanian Deadlift", 3, "8-12", "2-3 min"),
        ("Leg Press", 3, "10-15", "2 min"),
        ("Seated Leg Curl", 3, "10-15", "60-90 s"),
        ("Leg Extension", 2, "12-15", "60-90 s"),
        ("Standing Calf Raise", 4, "12-20", "60 s"),
    ]),
    4: ("Upper Body", "Train chest, back, shoulders and arms a second time this week.", [
        ("Incline Machine Chest Press", 3, "8-12", "2 min"),
        ("Neutral-Grip Lat Pulldown", 3, "8-12", "2 min"),
        ("One-Arm Cable Row", 3, "10-12", "90 s"),
        ("Pec Deck Fly", 2, "12-15", "60-90 s"),
        ("Cable Lateral Raises", 3, "12-20", "60 s"),
        ("Rear Delt Cable Fly", 2, "12-20", "60 s"),
        ("Preacher Curl", 3, "10-15", "60-90 s"),
        ("Cable Triceps Pushdown", 3, "10-15", "60-90 s"),
    ]),
    5: ("Lower Body + Abs", "Balanced legs, glutes, and abdominal strength.", [
        ("Goblet Squat", 3, "10-12", "2 min"),
        ("Bulgarian Split Squat", 2, "8-12 / leg", "90 s"),
        ("Lying Leg Curl", 3, "10-15", "60-90 s"),
        ("Hip Thrust", 3, "8-12", "2 min"),
        ("Seated Calf Raise", 4, "12-20", "60 s"),
        ("Hanging Knee Raise", 3, "12-15", "60 s"),
        ("Cable Crunch", 3, "12-15", "60 s"),
    ]),
}


def format_instructions(steps, avoid):
    lines = ["How to do it:"]
    lines += [f"{i}. {step}" for i, step in enumerate(steps, 1)]
    lines += ["", "Avoid:"]
    lines += [f"- {item}" for item in avoid]
    return "\n".join(lines)


def seed(apps, schema_editor):
    Exercise = apps.get_model("tracker", "Exercise")
    WorkoutDay = apps.get_model("tracker", "WorkoutDay")
    TemplateExercise = apps.get_model("tracker", "TemplateExercise")

    exercises = {}
    for line in EXERCISE_LIBRARY.strip().splitlines():
        name, muscle, equipment, category = [part.strip() for part in line.split("|")]
        instructions = ""
        if name in INSTRUCTIONS:
            instructions = format_instructions(*INSTRUCTIONS[name])
        exercises[name] = Exercise.objects.create(
            name=name, muscle_group=muscle, equipment=equipment, category=category, instructions=instructions
        )

    for weekday in range(7):
        title, focus, items = DEFAULT_PLAN.get(weekday, ("Rest", "Recover: sleep, walk, eat your protein.", []))
        day = WorkoutDay.objects.create(weekday=weekday, title=title, focus=focus)
        for order, (name, sets, reps, rest) in enumerate(items):
            TemplateExercise.objects.create(
                day=day, exercise=exercises[name], order=order, sets=sets, reps=reps, rest=rest
            )
