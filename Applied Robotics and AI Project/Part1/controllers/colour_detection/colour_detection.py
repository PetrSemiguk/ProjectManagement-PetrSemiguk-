from controller import Robot, Camera


TIME_STEP = 64
MAX_SPEED = 11
COLOR_THRESHOLD = 50
DISTANCE_THRESHOLD = 80

detected_list = []

robot = Robot()


camera = robot.getDevice("camera")
camera.enable(TIME_STEP)


left_motor = robot.getDevice("left wheel motor")
right_motor = robot.getDevice("right wheel motor")
left_motor.setPosition(float('inf'))
right_motor.setPosition(float('inf'))
left_motor.setVelocity(0)
right_motor.setVelocity(0)


ps = []
for i in range(8):
    sensor = robot.getDevice(f'ps{i}')
    sensor.enable(TIME_STEP)
    ps.append(sensor)

detected_colors = set()

def get_dominant_color(image):
    width = camera.getWidth()
    height = camera.getHeight()
    r_total, g_total, b_total = 0, 0, 0
    count = 0

    for x in range(width // 3, 2 * width // 3):
        for y in range(height // 3, 2 * height // 3):
            r = camera.imageGetRed(image, width, x, y)
            g = camera.imageGetGreen(image, width, x, y)
            b = camera.imageGetBlue(image, width, x, y)
            r_total += r
            g_total += g
            b_total += b
            count += 1

    r_avg = r_total // count
    g_avg = g_total // count
    b_avg = b_total // count

    if r_avg > g_avg + COLOR_THRESHOLD and r_avg > b_avg + COLOR_THRESHOLD:
        return "red"
    elif g_avg > r_avg + COLOR_THRESHOLD and g_avg > b_avg + COLOR_THRESHOLD:
        return "green"
    elif b_avg > r_avg + COLOR_THRESHOLD and b_avg > g_avg + COLOR_THRESHOLD:
        return "blue"
    else:
        return None


while robot.step(TIME_STEP) != -1:
    ps_values = [sensor.getValue() for sensor in ps]

    right_obstacle = ps_values[0] > DISTANCE_THRESHOLD or ps_values[1] > DISTANCE_THRESHOLD
    left_obstacle = ps_values[6] > DISTANCE_THRESHOLD or ps_values[7] > DISTANCE_THRESHOLD
    front_obstacle = ps_values[0] > DISTANCE_THRESHOLD or ps_values[7] > DISTANCE_THRESHOLD

    if front_obstacle or left_obstacle or right_obstacle:
        if left_obstacle:
            left_speed = 0.5 * MAX_SPEED
            right_speed = -0.2 * MAX_SPEED
        elif right_obstacle:
            left_speed = -0.2 * MAX_SPEED
            right_speed = 0.5 * MAX_SPEED
        else:
            left_speed = 0.5 * MAX_SPEED
            right_speed = -0.5 * MAX_SPEED
    else:
        
        left_speed = 0.5 * MAX_SPEED
        right_speed = 0.48 * MAX_SPEED

    left_motor.setVelocity(left_speed)
    right_motor.setVelocity(right_speed)

    image = camera.getImage()
    color = get_dominant_color(image)

    if color and color not in detected_colors:
        print(f"I see {color}")
        detected_colors.add(color)
        detected_list.append({color})
        print("I detected colours:", detected_list)