# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       jhalloran                                                    #
# 	Created:      10/23/2025, 3:26:18 PM                                       #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *
import time
import math

# misc classes
class Vector2D:
    """A simple 2D vector with useful magic methods and helpers.

    Supports: +, -, unary -, *, / (with scalars), ==, abs() for length,
    iteration, dot, cross, length, normalization, rotation, lerp, etc.
    """
    __slots__ = ("x", "y")

    def __init__(self, x=0.0, y=0.0):
        self.x = float(x)
        self.y = float(y)

    # Representation and conversion
    def __repr__(self):
        return "Vector2D(" + str(self.x) + "," + str(self.y) + ")"

    def to_tuple(self):
        return (self.x, self.y)

    def copy(self):
        return Vector2D(self.x, self.y)

    # Iteration/unpacking support: x, y = v
    def __iter__(self):
        yield self.x
        yield self.y

    # Equality (exact). Use math.isclose externally if tolerance required.
    def __eq__(self, other):
        if not isinstance(other, Vector2D):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    # Unary negation
    def __neg__(self):
        return Vector2D(-self.x, -self.y)

    # Arithmetic
    def __add__(self, other):
        if isinstance(other, Vector2D):
            return Vector2D(self.x + other.x, self.y + other.y)
        return Vector2D(self.x + other, self.y + other)

    def __sub__(self, other):
        if isinstance(other, Vector2D):
            return Vector2D(self.x - other.x, self.y - other.y)
        return self.__add__(-other)

    def __mul__(self, other):
        # scalar multiplication or element-wise with another vector
        if isinstance(other, (int, float)):
            return Vector2D(self.x * other, self.y * other)
        if isinstance(other, Vector2D):
            return Vector2D(self.x * other.x, self.y * other.y)
        return NotImplemented

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            if other == 0:
                raise ZeroDivisionError("division by zero")
            return Vector2D(self.x / other, self.y / other)
        if isinstance(other, Vector2D):
            if other.x == 0 or other.y == 0:
                raise ZeroDivisionError("element-wise division by zero")
            return Vector2D(self.x / other.x, self.y / other.y)
        return NotImplemented

    # Length and normalization
    def length_squared(self):
        return self.x * self.x + self.y * self.y

    def length(self):
        return (self.x**2 + self.y**2)**0.5

    # allow abs(v) to return the vector length
    def __abs__(self):
        return self.length()

    def normalized(self):
        l = self.length()
        if l == 0:
            return Vector2D(0.0, 0.0)
        return Vector2D(self.x / l, self.y / l)

    def normalize(self):
        """In-place normalization. Returns self."""
        l = self.length()
        if l == 0:
            self.x = 0.0
            self.y = 0.0
        else:
            self.x /= l
            self.y /= l
        return self

    # Dot and cross (2D cross returns scalar z-component)
    def dot(self, other):
        if not isinstance(other, Vector2D):
            raise TypeError("dot requires a Vector2D")
        return self.x * other.x + self.y * other.y

    def cross(self, other):
        if not isinstance(other, Vector2D):
            raise TypeError("cross requires a Vector2D")
        # 2D cross product returns a scalar corresponding to the z-component
        return self.x * other.y - self.y * other.x

    # Distance and angle helpers
    def distance_to(self, other):
        if not isinstance(other, Vector2D):
            raise TypeError("distance_to requires a Vector2D")
        dx = self.x - other.x
        dy = self.y - other.y
        return (dx * dx + dy * dy)**0.5

    def angle(self):
        """Angle in radians from the positive x-axis to this vector."""
        return math.atan2(self.y, self.x)

    def rotate(self, angle_radians):
        """Return a new Vector2D rotated by angle_radians around the origin."""
        c = math.cos(angle_radians)
        s = math.sin(angle_radians)
        return Vector2D(self.x * c - self.y * s, self.x * s + self.y * c)

    # Linear interpolation
    def lerp(self, other, t: float):
        """Return the linear interpolation between self and other by t in [0,1]."""
        if not isinstance(other, Vector2D):
            raise TypeError("lerp requires a Vector2D")
        return Vector2D(self.x + (other.x - self.x) * t, self.y + (other.y - self.y) * t)

    # Utility: perpendicular (rotated 90 degrees CCW)
    def perpendicular(self):
        return Vector2D(-self.y, self.x)

class Vector3D():
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
    
    def __repr__(self):
        return "Vector3D(" + str(self.x) + "," + str(self.y) + "," + str(self.z) + ")"
    
    def to_tuple(self):
        return (self.x, self.y, self.z)
    
    def __str__(self):
        return "("+str(self.x)+", "+str(self.y)+", "+str(self.z)+")"
    
    def copy(self):
        return Vector3D(self.x, self.y, self.z)
    
    def __eq__(self, other):
        if not isinstance(other, Vector3D):
            return NotImplemented
        return self.x == other.x and self.y == other.y and self.z == other.z
    
    def __add__(self, other):
        if isinstance(other, Vector3D):
            return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)
        return NotImplemented
    
    def __sub__(self, other):
        if isinstance(other, Vector3D):
            return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)
        return NotImplemented
    
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Vector3D(self.x * other, self.y * other, self.z * other)
        if isinstance(other, Vector3D):
            return Vector3D(self.x * other.x, self.y * other.y, self.z * other.z)
        return NotImplemented
    
    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            if other == 0:
                raise ZeroDivisionError("division by zero")
            return Vector3D(self.x / other, self.y / other, self.z / other)
        if isinstance(other, Vector3D):
            if other.x == 0 or other.y == 0 or other.z == 0:
                raise ZeroDivisionError("element-wise division by zero")
            return Vector3D(self.x / other.x, self.y / other.y, self.z / other.z)
        return NotImplemented

    def length_squared(self):
        return self.x * self.x + self.y * self.y + self.z * self.z
    
    def length(self):
        return (self.x**2 + self.y**2 + self.z**2)**0.5
    
    def __abs__(self):
        return self.length()
    
    def normalized(self):
        l = self.length()
        if l == 0:
            return Vector3D(0.0, 0.0, 0.0)
        return Vector3D(self.x / l, self.y / l, self.z / l)
    
    def normalize(self):
        l = self.length()
        if l == 0:
            self.x = 0.0
            self.y = 0.0
            self.z = 0.0
        else:
            self.x /= l
            self.y /= l
            self.z /= l
        return self
    
    def dot(self, other):
        if not isinstance(other, Vector3D):
            raise TypeError("dot requires a Vector3D")
        return self.x * other.x + self.y * other.y + self.z * other.z
    
    def cross(self, other):
        if not isinstance(other, Vector3D):
            raise TypeError("cross requires a Vector3D")
        return Vector3D(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )
    
    def distance_to(self, other):
        if not isinstance(other, Vector3D):
            raise TypeError("distance_to requires a Vector3D")
        dx = self.x - other.x
        dy = self.y - other.y
        dz = self.z - other.z
        return (dx * dx + dy * dy + dz * dz)**0.5
    
    def lerp(self, other, t: float):
        if not isinstance(other, Vector3D):
            raise TypeError("lerp requires a Vector3D")
        return Vector3D(
            self.x + (other.x - self.x) * t,
            self.y + (other.y - self.y) * t,
            self.z + (other.z - self.z) * t
        )
    
    def angle_xy(self):
        return math.atan2(self.y, self.x)

    def angle_xz(self):
        return math.atan2(self.z, self.x)

    def angle_yz(self):
        return math.atan2(self.z, self.y)
    
    def rotate_around_z(self, angle_radians):
        c = math.cos(angle_radians)
        s = math.sin(angle_radians)
        return Vector3D(
            self.x * c - self.y * s,
            self.x * s + self.y * c,
            self.z
        )
    
    def rotate_around_y(self, angle_radians):
        c = math.cos(angle_radians)
        s = math.sin(angle_radians)
        return Vector3D(
            self.x * c + self.z * s,
            self.y,
            -self.x * s + self.z * c
        )
    
    def rotate_around_x(self, angle_radians):
        c = math.cos(angle_radians)
        s = math.sin(angle_radians)
        return Vector3D(
            self.x,
            self.y * c - self.z * s,
            self.y * s + self.z * c
        )
    
    def rotate(self, angle_x_radians, angle_y_radians, angle_z_radians):
        v = self.rotate_around_x(angle_x_radians)
        v = v.rotate_around_y(angle_y_radians)
        v = v.rotate_around_z(angle_z_radians)
        return v
    
    def perpendicular_xy(self):
        return Vector3D(-self.y, self.x, self.z)
    
    def perpendicular_xz(self):
        return Vector3D(-self.z, self.y, self.x)
    
    def perpendicular_yz(self):
        return Vector3D(self.x, -self.z, self.y)
    
    def perpendicular_rotated_plane(self, plane_normal):
        if not isinstance(plane_normal, Vector3D):
            raise TypeError("perpendicular_rotated_plane requires a Vector3D")
        # Project self onto the plane defined by the normal
        n = plane_normal.normalized()
        dot_product = self.dot(n)
        projected = self - n * dot_product
        return projected
    

# logger class
class LogLine():
    def __init__(self, message, type="log"):
        self.message = message
        self.type = type
        self.override_color = None

class Logger():
    def __init__(self, brain, max_lines=100):
        self.logs = []
        self.max_lines = max_lines
        self.brain = brain
    
    def log(self, message):
        self._add_log(message, "log")
    def warn(self, message):
        self._add_log(message, "warn")
    def error(self, message):
        self._add_log(message, "error")
    def custom(self, message, color=None):
        log_line = LogLine(message, "custom")
        log_line.override_color = color
        self._add_log_line(log_line)
    def _add_log(self, message, type):
        log_line = LogLine(message, type)
        self._add_log_line(log_line)
    def _add_log_line(self, log_line):
        self.logs.append(log_line)
        if len(self.logs) > self.max_lines:
            self.logs.pop(0)

    def display(self, x,y, num_lines=5, size_percent = 100):
        self.brain.screen.clear_screen()
        # self.brain.screen.set_font_size(int(12 * (size_percent / 100)))
        start_index = max(0, len(self.logs) - num_lines)
        for i in range(start_index, len(self.logs)):
            log_line = self.logs[i]
            if log_line.type == "log":
                color_to_use = Color.WHITE
            elif log_line.type == "warn":
                color_to_use = Color.YELLOW
            elif log_line.type == "error":
                color_to_use = Color.RED
            elif log_line.type == "custom" and log_line.override_color is not None:
                color_to_use = log_line.override_color
            else:
                color_to_use = Color.WHITE
            self.brain.screen.set_pen_color(color_to_use)
            text_height = self.brain.screen.get_string_height(str(log_line.message))
            self.brain.screen.set_font(FontType.MONO15)
            self.brain.screen.print_at(str(log_line.message), x=x, y=(y + int((i - start_index) * ((text_height + 2) * (size_percent / 100)))))
    def clear(self):
        self.logs = []
# UI classes
class UI_element():
    def __init__(self, type, content, x, y, width, height, layer=3, rounded_corners=True, corner_radius=5, font=FontType.MONO15, onclick="", color=Color.WHITE, num_lines=5, onupdate=""):
        self.type = type # "text", "square", "logger", "button"
        self.num_lines = num_lines
        self.content = content
        self.onupdate = onupdate
        self.x = x
        self.y = y
        self.layer = layer 
        self.width = width
        self.height = height
        self.rounded_corners = rounded_corners
        self.corner_radius = corner_radius
        self.font = font
        self.color = color
        self.onclick = onclick
        self.was_clicked_last_check = False
    def draw(self, brain):
        brain.screen.set_pen_color(Color.WHITE)
        if self.type == "text":
            brain.screen.set_font(self.font)
            brain.screen.print_at(self.content, x=self.x, y=self.y)
        elif self.type == "square":
            if self.rounded_corners:
                # draw rounded rectangle using circles and rectangles (there's no built-in function for rounded rectangles)
                brain.screen.set_pen_color(self.color)
                brain.screen.set_fill_color(self.color)
                brain.screen.draw_circle(self.x + self.corner_radius, self.y + self.corner_radius, self.corner_radius)
                brain.screen.draw_circle(self.x + self.width - self.corner_radius, self.y + self.corner_radius, self.corner_radius)
                brain.screen.draw_circle(self.x + self.corner_radius, self.y + self.height - self.corner_radius, self.corner_radius)
                brain.screen.draw_circle(self.x + self.width - self.corner_radius, self.y + self.height - self.corner_radius, self.corner_radius)
                brain.screen.draw_rectangle(self.x + self.corner_radius, self.y, self.width - 2 * self.corner_radius, self.height)
                brain.screen.draw_rectangle(self.x, self.y + self.corner_radius, self.width, self.height - 2 * self.corner_radius)

            else:
                brain.screen.draw_rectangle(self.x, self.y, self.width, self.height)
        elif self.type == "logger":
            brain.screen.set_pen_color(Color.WHITE)
            brain.screen.set_fill_color(Color.BLACK)
            self.content.display(self.x, self.y, num_lines=self.num_lines, size_percent=100)
        elif self.type == "button":
            brain.screen.set_font(self.font)
            text_width = brain.screen.get_string_width(self.content)
            text_height = brain.screen.get_string_height(self.content)
            padding = 10
            # Use the maximum of configured width and text width + padding so
            # the button is at least the configured width but expands if the
            # label is longer than that width.
            content_width = max(self.width, text_width + padding)
            r = self.corner_radius

            # draw filled rounded rect
            brain.screen.set_pen_color(self.color)
            brain.screen.set_fill_color(self.color)
            if self.rounded_corners and content_width > 2 * r and self.height > 2 * r:
                brain.screen.draw_circle(self.x + r, self.y + r, r)
                brain.screen.draw_circle(self.x + content_width - r, self.y + r, r)
                brain.screen.draw_circle(self.x + r, self.y + self.height - r, r)
                brain.screen.draw_circle(self.x + content_width - r, self.y + self.height - r, r)
                brain.screen.draw_rectangle(self.x + r, self.y, content_width - 2 * r, self.height)
                brain.screen.draw_rectangle(self.x, self.y + r, content_width, self.height - 2 * r)
            else:
                brain.screen.draw_rectangle(self.x, self.y, content_width, self.height)

            # draw centered text
            brain.screen.set_pen_color(Color.WHITE)
            # print_at uses bottom-left, so compute y as: top + (height + text_height)/2
            text_x = self.x + int((content_width - text_width) / 2)
            text_y = self.y + int((self.height + text_height) / 2)
            brain.screen.print_at(self.content, x=text_x, y=text_y)
        # Additional element types can be added here
    def update(self, brain):
        if self.type == "button":
            brain.screen.set_font(self.font)
            text_width = brain.screen.get_string_width(self.content)
            padding = 10
            # Match drawing behavior: use the max so click area covers the
            # displayed button width.
            content_width = max(self.width, text_width + padding)
            is_pressed = brain.screen.pressing()
            if is_pressed and not self.was_clicked_last_check:
                touch_x = brain.screen.x_position()
                touch_y = brain.screen.y_position()
                if (self.x <= touch_x <= self.x + content_width) and (self.y <= touch_y <= self.y + self.height):
                    if self.onclick:
                        try:
                            # Execute the onclick code with access to the element as `self`
                            # and the current `brain` instance while preserving module globals
                            # (so global names like `logger` or `ui` remain available).
                            exec(self.onclick, globals(), {"self": self, "brain": brain})
                        except Exception as e:
                            # Swallow errors to avoid crashing the UI loop; logging
                            # is preferred if a global `logger` exists.
                            try:
                                logger.error(str(e))
                            except Exception:
                                pass
            self.was_clicked_last_check = is_pressed
        if self.onupdate != "":
            try:
                # Run onupdate with the same local scope so scripts can use `self`/`brain`
                exec(self.onupdate, globals(), {"self": self, "brain": brain})
            except Exception as e:
                logger.error(str(e))
class UI():
    def __init__(self, brain):
        self.elements = []
        self.brain = brain
    def add_element(self, element):
        self.elements.append(element)
    def add_logger(self, logger, x, y, width, height, layer=2, rounded_corners=True, corner_radius=5, num_lines=5):
        element = UI_element("logger", logger, x, y, width, height, layer, rounded_corners, corner_radius, num_lines=num_lines)
        self.add_element(element)
    def draw(self):
        # Sort elements by layer
        for layer in range(0, 6):
            for element in self.elements:
                if element.layer == layer:
                    element.draw(self.brain)
        self.brain.screen.render()
    def update(self):
        for element in self.elements:
            element.update(self.brain)


# DriveController class
class DriveController():
    def __init__(self, left_motors, right_motors, controller):
        self.left_motors = left_motors
        self.right_motors = right_motors
        self.controller = controller
        self.left_speed = 0
        self.right_speed = 0

    def get_joystick_input(self):
        # Treat x as the horizontal (turn) axis and y as the forward/back axis.
        # Controller: axis4 is horizontal (left/right), axis3 is vertical (forward/back).
        # Return (turn, forward) so downstream code can use input.x as turn and input.y as forward.
        return Vector2D(self.controller.axis4.position(), self.controller.axis3.position())
    
    def update_from_controller(self):
        # Standard arcade/differential mapping:
        # forward = input.y, turn = input.x
        # left = forward + turn
        # right = forward - turn
        js = self.get_joystick_input()
        forward = js.length()
        if js.y <0:
            forward = 0-forward
        turn = js.x*-2
        

        left = forward + turn
        right = forward - turn
        right = 0-right

        # clamp to [-100, 100]
        self.left_speed = max(-100, min(100, left))
        self.right_speed = max(-100, min(100, right))
        if self.controller.buttonL1.pressing():
            self.left_speed *= 0.5
            self.right_speed *= 0.5
        if self.controller.buttonY.pressing():
            self.left_speed *= 0.25
            self.right_speed *= 0.25
    
    def update_manually(self, left, right):
        self.left_speed = max(-100, min(100, left))
        self.right_speed = max(-100, min(100, right))

    def update_motor_speeds(self):
        for left_motor in self.left_motors:
            left_motor.spin(FORWARD)
            left_motor.set_velocity(self.left_speed, VelocityUnits.PERCENT)
        for right_motor in self.right_motors:
            right_motor.set_velocity(self.right_speed, VelocityUnits.PERCENT)
            right_motor.spin(FORWARD)

class Intake:
    def __init__(self, controller, motor):
        self.controller=controller
        self.motor = motor
        self.speed = 100
    def update_from_controller(self):
        if self.controller.buttonR1.pressing():
            self.motor.spin(FORWARD)
            self.motor.set_velocity(self.speed, VelocityUnits.PERCENT)
        else:
            if self.controller.buttonR2.pressing():
                self.motor.spin(FORWARD)
                self.motor.set_velocity(0-self.speed, VelocityUnits.PERCENT)
            else:
                self.motor.spin(FORWARD)
                self.motor.set_velocity(0, VelocityUnits.PERCENT)
    def update_manually(self, speed):
        self.speed = speed
        self.motor.spin(FORWARD)
        self.motor.set_velocity(self.speed, VelocityUnits.PERCENT)
class AutonomousStep:
    def __init__(self, left, right, intake_speed, duration):
        self.left = left
        self.right = right
        self.intake_speed = intake_speed
        self.duration = duration


class AutonomousController:
    def __init__(self, drivecontroller, intake, brain, logger):
        self.drivecontroller = drivecontroller
        self.intake = intake
        self.brain = brain
        self.logger = logger
        self.steps = []
        self.timer = Timer()
        self.currentstepidx = 0
        self.completesteptime = 0

    def add_step(self, step):
        self.steps.append(step)
    
    def start(self):
        self.timer.reset()

    def update(self):
        if self.currentstepidx >= len(self.steps):
            # finished
            self.drivecontroller.update_manually(0, 0)
            self.intake.update_manually(0)
            return
        if self.timer.time() >= self.completesteptime:
            self.completesteptime += self.steps[self.currentstepidx].duration
            self.currentstepidx += 1
        
        self.drivecontroller.update_manually(self.steps[self.currentstepidx].left, self.steps[self.currentstepidx].right)
        self.intake.update_manually(self.steps[self.currentstepidx].intake_speed)


        

def autonomous_start():
    auton.start()
    logger.log("Autonomous started.")

def usercontrol_start():
    logger.log("User control started.")
        

# Brain should be defined by default
brain=Brain()
controller = Controller()
brain.screen.set_pen_color(Color.WHITE)
brain.screen.render()
logger = Logger(brain, max_lines=50)
logger.log("Logger initialized.")
motor1 = Motor(Ports.PORT1)
intake = Intake(controller,Motor(Ports.PORT5))
competition = Competition(usercontrol_start, autonomous_start)
drivetrain = DriveController([Motor(Ports.PORT1),Motor(Ports.PORT2)],[Motor(Ports.PORT3),Motor(Ports.PORT4)],controller)
auton = AutonomousController(drivetrain, intake, brain, logger)
auton.add_step(AutonomousStep(70, 70, 100, 1.5))

# setup UI
ui = UI(brain)
ui.add_logger(logger, x=10, y=50, width=480, height=35, num_lines=7)
ui.add_element(UI_element("button", "VEX Logger UI Demo", x=0, y=0, width=200, height=35, layer=3, font=FontType.MONO20, color=Color.BLUE, rounded_corners=False, onclick='logger.log("Button clicked!")'))
ui.add_element(UI_element("button", "", x=200, y=0, width=280, height=35, layer=3, font=FontType.MONO20, color=Color.BLUE, rounded_corners=False, onupdate='self.content = "batt:"+str("brain.battery.capacity()")+"%"'))
logger.log("UI initialized.")
ui.draw()



target_framerate = 10
screenupdatetimer = Timer()
screenupdatetimer.reset()
while True:
    if screenupdatetimer.time() > 1/target_framerate:
        screenupdatetimer.reset()
        ui.update()
        ui.draw()
    if competition.is_enabled() or not(competition.is_competition_switch()):
        if competition.is_autonomous():
            auton.update()
            drivetrain.update_motor_speeds()
        else:
            drivetrain.update_from_controller()
            drivetrain.update_motor_speeds()
            intake.update_from_controller()
    else:
        drivetrain.update_manually(0,0)
        drivetrain.update_motor_speeds()
        intake.update_manually(0)
    time.sleep(0.01) # Sleep to prevent 100% CPU usage