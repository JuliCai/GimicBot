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
import vex
import time
import math

# vector classes
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
    

# Autonomous slot manager for step-based routines
class AutonomousManager:
    """Manages selecting and testing one of five step-based autonomous slots."""
    SLOT_MIN = 1
    SLOT_MAX = 5

    def __init__(self, brain, logger, auton_controller, slot_routines):
        self.brain = brain
        self.logger = logger
        self.auton = auton_controller
        self.slot_routines = slot_routines
        self.selected_slot = self.SLOT_MIN
        self.config_mode = False
        self.playback_mode = False
        self._load_selected_slot()
        self._apply_selected_slot()

    def _get_selected_filepath(self):
        """Get the filepath for the selected slot config."""
        return "selected_auton.txt"

    def _sd_available(self):
        """Check if SD card is inserted."""
        return self.brain.sdcard.is_inserted()

    def _normalize_slot(self, slot):
        if slot < self.SLOT_MIN:
            return self.SLOT_MIN
        if slot > self.SLOT_MAX:
            return self.SLOT_MAX
        return slot

    def _load_selected_slot(self):
        """Load selected slot preference from SD card when available."""
        if not self._sd_available():
            self.logger.warn("No SD card - using slot " + str(self.selected_slot))
            return
        try:
            data = self.brain.sdcard.loadfile(self._get_selected_filepath())
            if data:
                content = bytes(data).decode("utf-8").strip()
                if content.isdigit():
                    loaded_slot = self._normalize_slot(int(content))
                    self.selected_slot = loaded_slot
                    self.logger.log("Loaded auton slot: " + str(loaded_slot))
        except:
            self.logger.log("No saved auton selection, using slot " + str(self.selected_slot))

    def _save_selected_slot(self, slot):
        """Persist selected slot preference to SD card when available."""
        self.selected_slot = self._normalize_slot(slot)
        if not self._sd_available():
            return
        try:
            self.brain.sdcard.savefile(self._get_selected_filepath(), bytearray(str(self.selected_slot), "utf-8"))
        except Exception as e:
            self.logger.error("Failed to save selection: " + str(e))

    def _apply_selected_slot(self):
        routine = self.slot_routines.get(self.selected_slot)
        if routine is None:
            self.logger.warn("Missing step routine for slot " + str(self.selected_slot))
            return False
        self.auton.set_step_routine(routine)
        self.auton.use_steps_mode()
        self.logger.log(
            "Selected slot "
            + str(self.selected_slot)
            + " ("
            + str(len(routine.steps))
            + " steps)"
        )
        return True

    def slot_has_data(self, slot):
        """All 5 slots are step-based and always available."""
        return self.SLOT_MIN <= slot <= self.SLOT_MAX and slot in self.slot_routines

    def start_config_mode(self):
        """Enter config mode for selecting/testing autonomous."""
        self.config_mode = True
        self.logger.log("Config mode: Select auton slot")

    def end_config_mode(self):
        """Exit config mode."""
        self.config_mode = False
        self.playback_mode = False

    def start_playback(self, slot):
        """Start playing back a step autonomous for testing."""
        self.selected_slot = self._normalize_slot(slot)
        self._apply_selected_slot()
        self.playback_mode = True
        self.auton.start()
        self.logger.log("Playing slot " + str(self.selected_slot) + "...")

    def stop_playback(self):
        """Stop autonomous playback."""
        self.playback_mode = False
        self.logger.log("Playback stopped")

    def select_slot(self, slot):
        """Select a slot as the active autonomous for competition."""
        self._save_selected_slot(slot)
        self._apply_selected_slot()


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
    def __init__(self, type, content, x, y, width, height, layer=3, rounded_corners=True, corner_radius=5, font=FontType.MONO15, onclick="", color=None, num_lines=5, onupdate=""):
        if color is None:
            color = Color.WHITE
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
    def remove_element(self, element):
        """Remove an element from the UI."""
        if element in self.elements:
            self.elements.remove(element)
    def clear_elements(self, keep_logger=True):
        """Remove all elements, optionally keeping the logger."""
        if keep_logger:
            self.elements = [e for e in self.elements if e.type == "logger"]
        else:
            self.elements = []
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
        self.controltype = "tank"  # "arcade" or "tank"
        # Tunable inversion flags so field fixes don't require rewiring
        # forward_sign: 1 keeps existing axis3 behavior, -1 flips forward/back
        # turn_sign: 1 keeps existing axis4 behavior, -1 flips turn direction
        # right_side_sign: 1 if motors are mounted/reversed in code, -1 if they need inversion
        self.forward_sign = -1  # flip forward/back to correct the observed inversion
        self.turn_sign = -1     # flip turn direction to restore normal turning
        self.right_side_sign = -1  # preserve prior right-side inversion
        self.front_flipped = False
        # Encoder sign normalization for odometry/velocity models.
        # Goal: forward robot motion should read positive on BOTH sides.
        self.left_encoder_sign = 1.0
        self.right_encoder_sign = -1.0
        # Shared drivetrain model constants (used by velocity + odometry).
        self.wheel_diameter_mm = 83.0
        self.track_width_mm = 315.0
        # External ratio: motor 48T driving wheel 60T => 48/60.
        self.external_gear_ratio = 48.0 / 60.0
        # Per-motor continuous position tracking to handle wrapped encoder angles.
        # Some runtimes return motor.position() modulo 360; unwrapping prevents
        # ±360 jumps that destabilize proportional playback correction.
        self._motor_pos_state = {}

    def get_odometry_constants(self):
        """Return (wheel_diameter_mm, track_width_mm, external_gear_ratio)."""
        return self.wheel_diameter_mm, self.track_width_mm, self.external_gear_ratio

    def get_joystick_input(self):
        # Treat x as the horizontal (turn) axis and y as the forward/back axis.
        # Controller: axis4 is horizontal (left/right), axis3 is vertical (forward/back).
        # Return (turn, forward) so downstream code can use input.x as turn and input.y as forward.
        if self.controltype == "arcade":
            return Vector2D(self.controller.axis4.position(), self.controller.axis3.position())
        elif self.controltype == "tank":
            return Vector2D(self.controller.axis1.position(), self.controller.axis3.position())
        return Vector2D(0, 0)
            
    
    def update_from_controller(self):
        # Arcade drive: axis3 = forward/back, axis4 = turn
        js = self.get_joystick_input()

        # deadzone
        if js.length() < 10:
            js = Vector2D(0, 0)

        forward = self.forward_sign * js.y
        turn = self.turn_sign * js.x

        # In flipped mode, invert both forward and turning inputs so controls
        # remain intuitive from the opposite end of the robot.
        if self.front_flipped:
            forward = -forward
            turn = turn

        left = forward + turn
        right = forward - turn

        # Apply right-side inversion if hardware needs it
        right *= self.right_side_sign

        # clamp to [-100, 100]
        self.left_speed = max(-100, min(100, left))
        self.right_speed = max(-100, min(100, right))
        if self.controller.buttonX.pressing():
            self.left_speed *= 0.5
            self.right_speed *= 0.5
        if self.controller.buttonY.pressing():
            self.left_speed *= 0.25
            self.right_speed *= 0.25

    def toggle_front(self):
        self.front_flipped = not self.front_flipped
        return self.front_flipped
    
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

    def _safe_motor_position_degrees(self, motor):
        """Get motor position in degrees without raising runtime errors."""
        pos = 0
        try:
            pos = motor.position(vex.RotationUnits.DEG)
        except Exception:
            try:
                pos = motor.position(DEGREES)
            except Exception:
                try:
                    pos = motor.position()
                except Exception:
                    pos = 0
        try:
            return int(pos)
        except Exception:
            try:
                return int(float(pos))
            except Exception:
                return 0

    def _continuous_motor_position_degrees(self, motor):
        """Get a continuous (unwrapped) motor position in degrees."""
        raw_pos = self._safe_motor_position_degrees(motor)
        key = id(motor)
        state = self._motor_pos_state.get(key)

        if state is None:
            self._motor_pos_state[key] = {"last_raw": raw_pos, "continuous": raw_pos}
            return raw_pos

        delta = raw_pos - state["last_raw"]
        # Unwrap around 360-degree boundaries.
        if delta > 180:
            delta -= 360
        elif delta < -180:
            delta += 360

        state["continuous"] += delta
        state["last_raw"] = raw_pos
        return state["continuous"]

    def get_drive_positions_degrees(self):
        """Return average left/right drive positions in degrees."""
        left_avg = 0
        right_avg = 0
        if len(self.left_motors) > 0:
            left_avg = sum(self._continuous_motor_position_degrees(motor) for motor in self.left_motors) / len(self.left_motors)
            left_avg *= self.left_encoder_sign
        if len(self.right_motors) > 0:
            right_avg = sum(self._continuous_motor_position_degrees(motor) for motor in self.right_motors) / len(self.right_motors)
            right_avg *= self.right_encoder_sign
        return left_avg, right_avg
    
    def get_motor_speeds(self):
        leftspeedsum = 0
        for motor in self.left_motors:
            try:
                leftspeedsum += motor.velocity(vex.VelocityUnits.DPS)
            except Exception:
                try:
                    leftspeedsum += motor.velocity(vex.VelocityUnits.DPS)
                except Exception:
                    leftspeedsum += 0
        rightspeedsum = 0
        for motor in self.right_motors:
            try:
                rightspeedsum += motor.velocity(vex.VelocityUnits.DPS)
            except Exception:
                try:
                    rightspeedsum += motor.velocity(vex.VelocityUnits.DPS)
                except Exception:
                    rightspeedsum += 0
        leftspeed = 0
        rightspeed = 0
        if len(self.left_motors) > 0:
            leftspeed = leftspeedsum / len(self.left_motors)
            leftspeed *= self.left_encoder_sign
        if len(self.right_motors) > 0:
            rightspeed = rightspeedsum / len(self.right_motors)
            rightspeed *= self.right_encoder_sign
        return leftspeed, rightspeed

    
    def get_velocity_real(self):
        """Estimate current velocity in m/s and z rotation of robot in deg/s based on motor speeds, should be pretty accurate, but will drift over time"""
        wheel_circumference_mm = self.wheel_diameter_mm * math.pi
        left_speed_dps, right_speed_dps = self.get_motor_speeds()
        left_speed_mps = (left_speed_dps / 360) * wheel_circumference_mm / 1000 * self.external_gear_ratio
        right_speed_mps = (right_speed_dps / 360) * wheel_circumference_mm / 1000 * self.external_gear_ratio
        forward_speed = (left_speed_mps + right_speed_mps) / 2
        rotation_z_speed = (right_speed_mps - left_speed_mps) / (self.track_width_mm / 1000) * (180 / math.pi)
        return forward_speed, rotation_z_speed


"""TODO: KalmanFilter class, uses GPS, gyro, and Drivetrain odometry to produce a more accurate position estimate"""
class KalmanFilter:
    """Simple pose filter for x/y/heading using odometry prediction + GPS correction.

    State is treated as three mostly-independent 1D filters:
    - x (mm)
    - y (mm)
    - heading (deg)

    Prediction comes from wheel odometry, correction comes from GPS.
    """
    def __init__(self, gps_sensor=None, drivetrain_controller=None):
        self.gps = gps_sensor
        self.drivetrain = drivetrain_controller

        # x (mm), y (mm), heading (deg)
        self.current_estimate = Vector3D()
        # forward speed (m/s), lateral speed (m/s), yaw rate (deg/s)
        self.current_velocity = Vector3D()

        self._initialized = False
        self._last_left_deg = None
        self._last_right_deg = None

        # Independent covariance terms for x, y, heading.
        # Start large so first GPS readings are trusted.
        self._p_x = 10000.0
        self._p_y = 10000.0
        self._p_h = 400.0

        # Tunable process noise (higher = trust odometry less).
        self._q_pos_per_sec = 20.0
        self._q_heading_per_sec = 5.0

        # Tunable GPS measurement noise (lower = trust GPS more).
        # Increased GPS pull for x/y so position estimate recenters faster.
        self._r_x = 900.0
        self._r_y = 900.0
        self._r_h = 25.0

        # Robot geometry for odometry model.
        self._wheel_diameter_mm = 83.0
        self._track_width_mm = 300.0
        # Physical external gear ratio.
        self._gear_ratio = 48.0 / 60.0
        # Empirical scale for odometry model mismatch (scrub, wheel effective
        # diameter, carpet compression, etc). 1.0 = purely geometric model.
        self._odom_scale_tune = 1.25

        # GPS position correction safeguards (x/y only).
        # Hold GPS position corrections while moving quickly to avoid lag pullback.
        self._gps_position_hold_speed_mmps = 120.0
        # Ignore very large single-frame GPS position jumps as outliers.
        self._gps_outlier_residual_mm = 250.0
        # Cap how much GPS can correct x/y per update (after Kalman gain).
        self._gps_position_correction_cap_mm = 35.0
        # Becomes true after we accept at least one trusted GPS x/y correction.
        self._has_position_lock = False
        # Persistent re-lock gate for rare bad GPS lock states.
        self._gps_relock_residual_mm = 300.0
        self._gps_relock_quality_min = 95
        self._gps_relock_required_streak = 10
        self._gps_relock_streak = 0

        self._timer = Timer()
        self._timer.reset()
        self._last_time_s = self._timer.time(vex.TimeUnits.SECONDS)

    def _wrap_heading(self, heading_deg):
        return heading_deg % 360

    def _angle_residual(self, measurement_deg, estimate_deg):
        """Return shortest signed angle delta in degrees (measurement - estimate)."""
        delta = (measurement_deg - estimate_deg + 180.0) % 360.0 - 180.0
        return delta

    def _field_heading_to_math_radians(self, heading_deg):
        """Convert VEX field heading (0°=up, clockwise+) to math radians (0=+x, CCW+)."""
        return math.radians(90.0 - heading_deg)

    def _try_get_gps(self):
        if self.gps is None:
            return None
        try:
            return self.gps.get_position()
        except Exception:
            return None

    def _try_get_accurate_gps(self):
        if self.gps is None:
            return None
        try:
            if hasattr(self.gps, "get_accurate_reading"):
                return self.gps.get_accurate_reading()
        except Exception:
            return None
        return None

    def _try_get_gps_quality(self):
        if self.gps is None:
            return None
        try:
            return self.gps.get_quality()
        except Exception:
            return None

    def _initialize_if_needed(self):
        if self._initialized:
            return

        # Prefer an averaged GPS reading for the initial estimate.
        gps_pos = self._try_get_accurate_gps()
        if gps_pos is None:
            gps_pos = self._try_get_gps()
        init_quality = self._try_get_gps_quality()
        init_position_valid = (init_quality is None) or (init_quality >= 80)
        if gps_pos is not None and init_position_valid:
            self.current_estimate = Vector3D(gps_pos[0], gps_pos[1], gps_pos[2])
            self._has_position_lock = True

        if self.drivetrain is not None:
            try:
                left_deg, right_deg = self.drivetrain.get_drive_positions_degrees()
                self._last_left_deg = left_deg
                self._last_right_deg = right_deg
            except Exception:
                self._last_left_deg = 0.0
                self._last_right_deg = 0.0
        else:
            self._last_left_deg = 0.0
            self._last_right_deg = 0.0

        self._initialized = True

    def _predict_from_odometry(self, dt_s):
        if self.drivetrain is None:
            return

        try:
            left_deg, right_deg = self.drivetrain.get_drive_positions_degrees()
        except Exception:
            return

        if self._last_left_deg is None or self._last_right_deg is None:
            self._last_left_deg = left_deg
            self._last_right_deg = right_deg
            return

        d_left_deg = left_deg - self._last_left_deg
        d_right_deg = right_deg - self._last_right_deg
        self._last_left_deg = left_deg
        self._last_right_deg = right_deg

        wheel_diameter_mm = self._wheel_diameter_mm
        track_width_mm = self._track_width_mm
        gear_ratio = self._gear_ratio
        if self.drivetrain is not None and hasattr(self.drivetrain, "get_odometry_constants"):
            try:
                wheel_diameter_mm, track_width_mm, gear_ratio = self.drivetrain.get_odometry_constants()
            except Exception:
                pass

        wheel_circumference_mm = wheel_diameter_mm * math.pi
        # Raw geometric odometry from encoder deltas and physical gear ratio.
        raw_d_left_mm = (d_left_deg / 360.0) * wheel_circumference_mm * gear_ratio
        raw_d_right_mm = (d_right_deg / 360.0) * wheel_circumference_mm * gear_ratio

        # Tuned odometry used for state prediction.
        d_left_mm = raw_d_left_mm * self._odom_scale_tune
        d_right_mm = raw_d_right_mm * self._odom_scale_tune

        d_center_mm = (d_left_mm + d_right_mm) / 2.0
        d_heading_deg = ((d_right_mm - d_left_mm) / track_width_mm) * (180.0 / math.pi)

        previous_heading = self.current_estimate.z
        predicted_heading = self._wrap_heading(previous_heading + d_heading_deg)
        # Integrate translation at the midpoint heading over the time step.
        mid_heading = self._wrap_heading(previous_heading + (d_heading_deg * 0.5))
        heading_rad = self._field_heading_to_math_radians(mid_heading)

        self.current_estimate.x += d_center_mm * math.cos(heading_rad)
        self.current_estimate.y += d_center_mm * math.sin(heading_rad)
        self.current_estimate.z = predicted_heading

        # Covariance growth during prediction.
        # Base this on raw motion so very large tune factors don't indirectly
        # force GPS dominance (which can hide tune effects during movement).
        raw_d_center_mm = (raw_d_left_mm + raw_d_right_mm) / 2.0
        raw_d_heading_deg = ((raw_d_right_mm - raw_d_left_mm) / track_width_mm) * (180.0 / math.pi)
        motion_scale = abs(raw_d_center_mm) / 10.0
        turn_scale = abs(raw_d_heading_deg) / 5.0
        self._p_x += self._q_pos_per_sec * dt_s + motion_scale
        self._p_y += self._q_pos_per_sec * dt_s + motion_scale
        self._p_h += self._q_heading_per_sec * dt_s + turn_scale

    def _correct_with_gps(self):
        gps_pos = self._try_get_gps()
        if gps_pos is None:
            return

        gps_x, gps_y, gps_h = gps_pos
        quality = self._try_get_gps_quality()

        # VEX GPS quality guidance:
        # - 100: full valid position + heading
        # - ~90: position can degrade (fallback behavior)
        # - 0-80: only heading is considered valid, position is unreliable
        # Use quality to dynamically scale measurement noise.
        position_valid = True
        heading_valid = True
        r_x = self._r_x
        r_y = self._r_y
        r_h = self._r_h
        speed_mmps = 0.0

        if quality is not None:
            if quality <= 0:
                position_valid = False
                heading_valid = False
            elif quality < 80:
                position_valid = False
                # Heading exists but becomes less trustworthy as quality drops.
                # Scale heading noise up as quality decreases.
                q_scale = max(1.0, (100.0 - quality) / 20.0)
                r_h = self._r_h * q_scale
            elif quality < 90:
                # Keep heading correction; heavily de-weight position correction.
                r_x = self._r_x * 4.0
                r_y = self._r_y * 4.0
                r_h = self._r_h * 1.5
            elif quality < 95:
                # Mildly de-weight GPS correction near the degradation band.
                r_x = self._r_x * 2.0
                r_y = self._r_y * 2.0
                r_h = self._r_h * 1.2

        # GPS position can lag during fast motion. Capture speed for gating.
        if self.drivetrain is not None:
            try:
                v_forward_mps, _ = self.drivetrain.get_velocity_real()
                speed_mmps = abs(v_forward_mps) * 1000.0
            except Exception:
                pass

        # While moving quickly, trust odometry for position and keep GPS for heading.
        if speed_mmps > self._gps_position_hold_speed_mmps:
            position_valid = False

        # Reject obviously bad GPS position jumps.
        x_residual = gps_x - self.current_estimate.x
        y_residual = gps_y - self.current_estimate.y

        # If a large residual persists while stationary with strong signal,
        # treat this as a stale/bad lock and forcibly re-lock to GPS.
        residual_mag = math.sqrt((x_residual * x_residual) + (y_residual * y_residual))
        can_relock = (
            (speed_mmps <= self._gps_position_hold_speed_mmps)
            and (quality is not None)
            and (quality >= self._gps_relock_quality_min)
            and (residual_mag >= self._gps_relock_residual_mm)
        )
        if can_relock:
            self._gps_relock_streak += 1
        else:
            self._gps_relock_streak = 0

        if self._gps_relock_streak >= self._gps_relock_required_streak:
            self.current_estimate.x = gps_x
            self.current_estimate.y = gps_y
            self._p_x = min(self._p_x, self._r_x)
            self._p_y = min(self._p_y, self._r_y)
            self._has_position_lock = True
            self._gps_relock_streak = 0
            x_residual = 0.0
            y_residual = 0.0

        if abs(x_residual) > self._gps_outlier_residual_mm or abs(y_residual) > self._gps_outlier_residual_mm:
            # If we do not yet have a trusted GPS x/y lock, allow one controlled
            # re-lock while stationary with decent signal so startup races do not
            # permanently freeze position correction.
            if (
                (not self._has_position_lock)
                and (speed_mmps <= self._gps_position_hold_speed_mmps)
                and ((quality is None) or (quality >= 90))
            ):
                self.current_estimate.x = gps_x
                self.current_estimate.y = gps_y
                self._p_x = min(self._p_x, self._r_x)
                self._p_y = min(self._p_y, self._r_y)
                self._has_position_lock = True
                position_valid = False
            else:
                position_valid = False

        if position_valid:
            # x update
            kx = self._p_x / (self._p_x + r_x)
            x_correction = kx * x_residual
            if x_correction > self._gps_position_correction_cap_mm:
                x_correction = self._gps_position_correction_cap_mm
            elif x_correction < -self._gps_position_correction_cap_mm:
                x_correction = -self._gps_position_correction_cap_mm
            self.current_estimate.x = self.current_estimate.x + x_correction
            self._p_x = (1.0 - kx) * self._p_x

            # y update
            ky = self._p_y / (self._p_y + r_y)
            y_correction = ky * y_residual
            if y_correction > self._gps_position_correction_cap_mm:
                y_correction = self._gps_position_correction_cap_mm
            elif y_correction < -self._gps_position_correction_cap_mm:
                y_correction = -self._gps_position_correction_cap_mm
            self.current_estimate.y = self.current_estimate.y + y_correction
            self._p_y = (1.0 - ky) * self._p_y
            self._has_position_lock = True

        if heading_valid:
            # heading update with wrapped innovation
            kh = self._p_h / (self._p_h + r_h)
            h_residual = self._angle_residual(gps_h, self.current_estimate.z)
            self.current_estimate.z = self._wrap_heading(self.current_estimate.z + kh * h_residual)
            self._p_h = (1.0 - kh) * self._p_h

    def _update_velocity_estimate(self):
        if self.drivetrain is None:
            return
        try:
            v_forward_mps, v_yaw_dps = self.drivetrain.get_velocity_real()
            self.current_velocity = Vector3D(v_forward_mps, 0.0, v_yaw_dps)
        except Exception:
            # Keep last known velocity.
            pass

    def update(self):
        self._initialize_if_needed()

        now_s = self._timer.time(vex.TimeUnits.SECONDS)
        dt_s = now_s - self._last_time_s
        self._last_time_s = now_s
        if dt_s <= 0:
            dt_s = 0.01

        self._predict_from_odometry(dt_s)
        self._correct_with_gps()
        self._update_velocity_estimate()

    def get_estimate(self):
        return self.current_estimate

    def get_velocity(self):
        return self.current_velocity


class GPSSensor:
    def __init__(self, sensor, heading_offset_deg=0.0):
        self.sensor = sensor
        self.heading_offset_deg = float(heading_offset_deg)
        self.last_valid_position = None
        self.last_valid_heading = 0.0
        self.last_valid_gyro_z = 0
        self.last_valid_quality = None

    def _normalize_heading(self, heading):
        return heading % 360

    def _average_heading(self, sin_total, cos_total):
        if sin_total == 0 and cos_total == 0:
            return self.last_valid_heading
        avg_heading = math.degrees(math.atan2(sin_total, cos_total))
        return self._normalize_heading(avg_heading)

    def get_position(self):
        try:
            x = self.sensor.x_position(vex.DistanceUnits.MM)
            y = self.sensor.y_position(vex.DistanceUnits.MM)
            heading = self._normalize_heading(self.sensor.heading() + self.heading_offset_deg)
            position = (x, y, heading)
            self.last_valid_position = position
            self.last_valid_heading = heading
            return position
        except Exception:
            return None

    def get_heading(self):
        try:
            heading = self._normalize_heading(self.sensor.heading() + self.heading_offset_deg)
            self.last_valid_heading = heading
            return heading
        except Exception:
            return self.last_valid_heading

    def set_heading_offset(self, heading_offset_deg):
        """Set heading correction for mounting orientation mismatch."""
        try:
            self.heading_offset_deg = float(heading_offset_deg)
            return True
        except Exception:
            return False

    def get_internal_gyro_z(self):
        """get internal stuff with gps_sensor.orientation(axis, units)"""
        try:
            orientation = self.sensor.orientation(vex.OrientationType.YAW, vex.RotationUnits.DEG)
            self.last_valid_gyro_z = orientation
            return orientation
        except Exception:
            return self.last_valid_gyro_z

    def get_quality(self):
        """Get current GPS signal quality percentage (0-100)."""
        try:
            quality = self.sensor.quality()
            self.last_valid_quality = quality
            return quality
        except Exception:
            return self.last_valid_quality

    def set_origin(self, x, y, distance_units=vex.DistanceUnits.MM):
        """Set the GPS sensor reference point offset on the robot."""
        try:
            self.sensor.set_origin(x, y, distance_units)
            return True
        except Exception:
            return False

    def get_accurate_reading(self, samples=5, delay_ms=100):
        """Get an averaged GPS reading (x, y, heading) to reduce noise; best while stationary."""
        x_total = 0
        y_total = 0
        heading_sin_total = 0
        heading_cos_total = 0
        valid_samples = 0
        for _ in range(samples):
            pos = self.get_position()
            if pos is not None:
                x, y, heading = pos
                x_total += x
                y_total += y
                heading_radians = math.radians(heading)
                heading_sin_total += math.sin(heading_radians)
                heading_cos_total += math.cos(heading_radians)
                valid_samples += 1
            vex.sleep(delay_ms)
        if valid_samples == 0:
            return self.last_valid_position
        avg_heading = self._average_heading(heading_sin_total, heading_cos_total)
        averaged = (x_total / valid_samples, y_total / valid_samples, avg_heading)
        self.last_valid_position = averaged
        self.last_valid_heading = avg_heading
        return averaged

class PIDController:
    """general purpose PID controller, always useful"""
    def __init__(self, kp, ki, kd, setpoint=0, output_limits=(None, None)):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.setpoint = setpoint
        self.output_limits = output_limits
        self._last_error = 0
        self._integral = 0

    def reset(self):
        self._last_error = 0
        self._integral = 0
    
    def compute(self, measurement, dt=None):
        if dt is None or dt <= 0:
            dt = 1.0
        error = self.setpoint - measurement
        self._integral += error * dt
        derivative = (error - self._last_error) / dt
        output = (self.kp * error) + (self.ki * self._integral) + (self.kd * derivative)
        
        # Apply output limits
        min_output, max_output = self.output_limits
        if min_output is not None:
            output = max(min_output, output)
        if max_output is not None:
            output = min(max_output, output)
        
        self._last_error = error
        return output

# Intake class
class Intake:
    def __init__(self, controller, motor):
        self.controller=controller
        self.motor = motor
        self.speed = 100
    def _apply_speed(self, speed):
        if speed == 0:
            self.motor.stop()
            return
        direction = FORWARD if speed > 0 else REVERSE
        self.motor.set_velocity(abs(speed), VelocityUnits.PERCENT)
        self.motor.spin(direction)
    def update_from_controller(self):
        if self.controller.buttonR1.pressing():
            self._apply_speed(self.speed)
        else:
            if self.controller.buttonR2.pressing():
                self._apply_speed(0-self.speed)
            else:
                self._apply_speed(0)
    def update_manually(self, speed):
        self._apply_speed(speed)

class ButtonControlledMotor:
    def __init__(self, buttonforward, buttonbackward, motor, speed=100, mode = "direct", params=None):
        self.buttonforward = buttonforward
        self.buttonbackward = buttonbackward
        self.motor = motor 
        self.speed = speed
        self.mode = mode
        self.params = params or {}
        self.toggle_state = None
        if self.mode == "toggle":
            position_a = self.params.get("position_a")
            position_b = self.params.get("position_b")
            if position_a is None or position_b is None:
                raise ValueError("toggle mode requires position_a and position_b params")
            initial_state = self.params.get("initial_state", "b")
            self.toggle_state = Toggled(position_a, position_b, initial_state)
            self._apply_toggle_target()
    def _apply_speed(self, speed):
        if speed == 0:
            self.motor.stop()
            return
        direction = FORWARD if speed > 0 else REVERSE
        self.motor.set_velocity(abs(speed), VelocityUnits.PERCENT)
        self.motor.spin(direction)
    def _apply_toggle_target(self):
        if self.toggle_state is None:
            return
        target = self.toggle_state.get_value()
        self.motor.spin_to_position(target, RotationUnits.DEG, self.speed, VelocityUnits.PERCENT, wait=False)
    def set_toggle_state(self, state, force=False):
        if self.mode != "toggle" or self.toggle_state is None:
            raise RuntimeError("set_toggle_state is only available in toggle mode")
        changed = self.toggle_state.set_state(state)
        if changed or force:
            self._apply_toggle_target()
    def update_from_controller(self):
        if self.mode == "direct":
            if self.buttonforward.pressing():
                self._apply_speed(self.speed)
            else:
                if self.buttonbackward.pressing():
                    self._apply_speed(0 - self.speed)
                else:
                    self._apply_speed(0)
        if self.mode == "toggle" and self.toggle_state is not None:
            if self.buttonforward.pressing():
                if self.toggle_state.set_state("a"):
                    self._apply_toggle_target()
            if self.buttonbackward.pressing():
                if self.toggle_state.set_state("b"):
                    self._apply_toggle_target()
    def update_manually(self, speed):
        self._apply_speed(speed)

class ButtonControlledPneumatic:
    def __init__(self, buttontoggle, digital_out, inverted=False):
        self.buttontoggle = WrappedButton(buttontoggle)
        self.digital_out = digital_out
        self.isinverted = inverted
        self.toggle_state = Toggled("a", "b", initial_state="b")
        if self.toggle_state.state == "a":
            self.digital_out.set(True)  # extend
        else:
            self.digital_out.set(False)  # retract 
    def update_from_controller(self):
        self.buttontoggle.update_state()
        if self.buttontoggle.pressed():
            new_state = self.toggle_state.toggle()
            if new_state == "a":
                self.digital_out.set(True)  # extend
            else:
                self.digital_out.set(False)  # retract
    def update_manually(self, value):
        """Set pneumatic state from a value (for autonomous playback).
        Positive values = extend (state a), zero or negative = retract (state b)."""
        new_state = "a" if value > 0 else "b"
        if self.toggle_state.set_state(new_state):
            self.digital_out.set(new_state == "a")

# Autonomous classes
class AutonomousStep:
    def __init__(self, left, right, intake_speed, outtake_speed, matchloader_speed, duration, matchloader_toggle_state=None):
        self.left = left
        self.right = right
        self.intake_speed = intake_speed
        self.outtake_speed = outtake_speed
        self.matchloader_speed = matchloader_speed
        self.duration = duration
        self.matchloader_toggle_state = matchloader_toggle_state


class StepAutonomousRoutine:
    """Container for step-based autonomous sequences."""
    def __init__(self, name="Steps", steps=None):
        self.name = name
        self.steps = list(steps) if steps is not None else []

    def add_step(self, left, right, intake_speed, outtake_speed, matchloader_speed, duration, matchloader_toggle_state=None):
        self.steps.append(
            AutonomousStep(left, right, intake_speed, outtake_speed, matchloader_speed, duration, matchloader_toggle_state)
        )
        return self

    def clear(self):
        self.steps = []


class AutonomousController:
    def __init__(self, drivecontroller, intake, outtake, matchloader, brain, logger, descore=None, pose_filter=None, game_state=None):
        self.drivecontroller = drivecontroller
        self.intake = intake
        self.outtake = outtake
        self.brain = brain
        self.logger = logger
        self.step_routine = StepAutonomousRoutine("Steps")
        self.steps = self.step_routine.steps
        self.timer = Timer()
        self.currentstepidx = 0
        self.completesteptime = 0
        self.matchloader = matchloader
        self.descore = descore
        self.pose_filter = pose_filter
        self.game_state = game_state

        # Target navigation state
        self.target_active = False
        self.arrived_at_target = False
        self.target_q4 = None
        self.target_world = None
        self.target_angle = None
        self._target_phase = "idle"

        # Navigation tuning
        self.target_tolerance_mm = 15.0
        self.target_heading_tolerance_deg = 3.0
        self._target_settle_frames = 3
        self._target_max_drive_speed = 60.0
        self._target_min_drive_speed = 8.0
        self._target_max_turn_speed = 40.0
        self._target_min_turn_speed = 6.0
        self._target_max_steer_speed = 16.0
        # Acceleration limits for motion-profiled commands.
        # Units are in "command-percent per second^2".
        self._target_drive_accel = 180.0
        self._target_turn_accel = 220.0
        self._target_slew_per_update = 4.0
        self._target_align_tolerance_deg = 3.5
        self._target_realign_threshold_deg = 18.0
        self._target_required_in_tolerance_count = self._target_settle_frames
        self._target_in_tolerance_count = 0
        self._target_drive_sign = 1.0
        self._target_choose_direction_on_align = True
        self._target_align_start_error_deg = 0.0
        self._target_drive_start_distance_mm = 0.0
        self._target_final_turn_start_error_deg = 0.0
        self._target_phase_entry_heading_error_deg = 0.0
        self._last_left_command = 0.0
        self._last_right_command = 0.0
        self._right_motor_sign = 1.0
        try:
            if hasattr(self.drivecontroller, "right_side_sign"):
                self._right_motor_sign = float(self.drivecontroller.right_side_sign)
        except Exception:
            pass

        self._target_timer = Timer()
        self._target_timer.reset()
        self._target_last_time_s = self._target_timer.time(vex.TimeUnits.SECONDS)

        self._distance_pid = PIDController(
            kp=0.06,
            ki=0.0,
            kd=0.005,
            setpoint=0,
            output_limits=(0, self._target_max_drive_speed),
        )
        self._path_heading_pid = PIDController(
            kp=0.30,
            ki=0.0,
            kd=0.03,
            setpoint=0,
            output_limits=(-self._target_max_steer_speed, self._target_max_steer_speed),
        )
        self._final_heading_pid = PIDController(
            kp=0.65,
            ki=0.0,
            kd=0.08,
            setpoint=0,
            output_limits=(-self._target_max_turn_speed, self._target_max_turn_speed),
        )

        """TODO: Add GPS Sensor PID control"""

    def add_step(self, step):
        self.step_routine.steps.append(step)

    def set_step_routine(self, routine):
        """Set the active step-based autonomous routine."""
        self.step_routine = routine
        self.steps = self.step_routine.steps

    def use_steps_mode(self):
        return

    def _wrap_heading(self, heading_deg):
        return heading_deg % 360

    def _angle_residual(self, measurement_deg, estimate_deg):
        return (measurement_deg - estimate_deg + 180.0) % 360.0 - 180.0

    def _heading_to_field_vector(self, heading_deg):
        radians = math.radians(self._wrap_heading(heading_deg))
        # VEX field heading convention:
        # 0 deg = +Y, 90 deg = +X, clockwise positive
        return math.sin(radians), math.cos(radians)

    def _field_vector_to_heading(self, x_component, y_component):
        heading = math.degrees(math.atan2(x_component, y_component))
        return self._wrap_heading(heading)

    def _heading_from_target_vector(self, dx, dy):
        # Convert math angle to VEX field heading.
        return self._wrap_heading(90.0 - math.degrees(math.atan2(dy, dx)))

    def _apply_quadrant_mirror(self, x_mm, y_mm, heading_deg):
        quadrant = None
        if self.game_state is not None:
            quadrant = self.game_state.quadrant

        mirror_x = False
        mirror_y = False
        if quadrant in (GameState.QUADRANT_BLUE_RIGHT, GameState.QUADRANT_BLUE_LEFT):
            mirror_x = True
        if quadrant in (GameState.QUADRANT_BLUE_RIGHT, GameState.QUADRANT_RED_RIGHT):
            mirror_y = True

        tx = -x_mm if mirror_x else x_mm
        ty = -y_mm if mirror_y else y_mm

        transformed_heading = heading_deg
        if heading_deg is not None:
            hvx, hvy = self._heading_to_field_vector(heading_deg)
            if mirror_x:
                hvx = -hvx
            if mirror_y:
                hvy = -hvy
            transformed_heading = self._field_vector_to_heading(hvx, hvy)

        return tx, ty, transformed_heading

    def _target_dt(self):
        now = self._target_timer.time(vex.TimeUnits.SECONDS)
        dt = now - self._target_last_time_s
        self._target_last_time_s = now
        if dt <= 0:
            return 0.02
        if dt > 0.25:
            return 0.25
        return dt

    def _clamp_speed(self, value):
        return max(-100, min(100, value))

    def _slew(self, current, target, max_delta):
        delta = target - current
        if delta > max_delta:
            delta = max_delta
        elif delta < -max_delta:
            delta = -max_delta
        return current + delta

    def _command_drive_smoothed(self, left, right):
        self._last_left_command = self._slew(self._last_left_command, left, self._target_slew_per_update)
        self._last_right_command = self._slew(self._last_right_command, right, self._target_slew_per_update)
        self.drivecontroller.update_manually(self._last_left_command, self._last_right_command)

    def _mix_robot_drive(self, linear, turn):
        """Convert robot-relative linear/turn into motor commands."""
        left = linear + turn
        right = linear - turn
        right *= self._right_motor_sign
        return self._clamp_speed(left), self._clamp_speed(right)

    def _profile_speed(self, traveled, remaining, accel, max_speed, min_speed, hold_min=True):
        """Kinematic trapezoid/triangle speed profile.

        Returns a non-negative command magnitude that:
        - accelerates using distance already traveled,
        - decelerates using distance remaining,
        - cruises at max speed when path is long enough.
        """
        traveled = max(0.0, traveled)
        remaining = max(0.0, remaining)
        accel = max(1e-6, accel)

        accel_limited = math.sqrt(2.0 * accel * traveled) if traveled > 0.0 else 0.0
        decel_limited = math.sqrt(2.0 * accel * remaining) if remaining > 0.0 else 0.0

        magnitude = min(max_speed, accel_limited, decel_limited)
        if hold_min and remaining > 0.0 and magnitude < min_speed:
            magnitude = min_speed
        return max(0.0, min(max_speed, magnitude))

    def _signed_from_error(self, error, magnitude):
        if error > 0:
            return magnitude
        if error < 0:
            return -magnitude
        return 0.0

    def _enter_align_phase(self, current_heading, heading_to_target):
        self._target_phase = "align"
        if self._target_choose_direction_on_align:
            self._target_drive_sign = self._choose_drive_sign(current_heading, heading_to_target)
            self._target_choose_direction_on_align = False
        self._target_in_tolerance_count = 0
        heading_error = self._heading_error_for_drive_sign(current_heading, heading_to_target, self._target_drive_sign)
        self._target_align_start_error_deg = max(abs(heading_error), self._target_align_tolerance_deg)
        self._target_phase_entry_heading_error_deg = heading_error
        self._final_heading_pid.reset()

    def _enter_drive_phase(self, distance_mm):
        self._target_phase = "drive"
        self._target_in_tolerance_count = 0
        self._target_drive_start_distance_mm = max(distance_mm, self.target_tolerance_mm)
        self._path_heading_pid.reset()

    def _enter_final_turn_phase(self, current_heading):
        self._target_phase = "final_turn"
        self._target_in_tolerance_count = 0
        heading_error = self._angle_residual(self.target_angle, current_heading)
        self._target_final_turn_start_error_deg = max(abs(heading_error), self.target_heading_tolerance_deg)
        self._target_phase_entry_heading_error_deg = heading_error
        self._final_heading_pid.reset()

    def _choose_drive_sign(self, current_heading, heading_to_target):
        front_error = self._angle_residual(heading_to_target, current_heading)
        back_heading = self._wrap_heading(current_heading + 180.0)
        back_error = self._angle_residual(heading_to_target, back_heading)
        # Hysteresis margin prevents indecisive front/back flips near the
        # 90-degree boundary.
        hysteresis_deg = 8.0
        if abs(back_error) + hysteresis_deg < abs(front_error):
            return -1.0
        return 1.0

    def _heading_error_for_drive_sign(self, current_heading, heading_to_target, drive_sign):
        if drive_sign < 0:
            return self._angle_residual(heading_to_target, self._wrap_heading(current_heading + 180.0))
        return self._angle_residual(heading_to_target, current_heading)

    def _mark_target_complete(self):
        self.target_active = False
        self.arrived_at_target = True
        self._target_phase = "done"
        self._last_left_command = 0.0
        self._last_right_command = 0.0
        self.drivecontroller.update_manually(0, 0)

    def set_target(self, x_mm, y_mm, target_angle=None):
        """Set movement target using quadrant-4 coordinates, mirrored to startup quadrant."""
        transformed_x, transformed_y, transformed_heading = self._apply_quadrant_mirror(x_mm, y_mm, target_angle)

        self.target_q4 = (x_mm, y_mm, target_angle)
        self.target_world = (transformed_x, transformed_y)
        self.target_angle = transformed_heading
        self.arrived_at_target = False
        self.target_active = True
        self._target_phase = "align"
        self._target_in_tolerance_count = 0
        self._target_drive_sign = 1.0
        self._target_choose_direction_on_align = True
        self._target_align_start_error_deg = 0.0
        self._target_drive_start_distance_mm = 0.0
        self._target_final_turn_start_error_deg = 0.0
        self._target_phase_entry_heading_error_deg = 0.0

        self._distance_pid.reset()
        self._path_heading_pid.reset()
        self._final_heading_pid.reset()

        self._target_timer.reset()
        self._target_last_time_s = self._target_timer.time(vex.TimeUnits.SECONDS)
        self._last_left_command = 0.0
        self._last_right_command = 0.0

        self.logger.log(
            "Target set (q4): ("
            + str(int(x_mm))
            + ", "
            + str(int(y_mm))
            + ") -> ("
            + str(int(transformed_x))
            + ", "
            + str(int(transformed_y))
            + ")"
        )

    def target_update(self):
        """Three-phase target navigation.

        1) align: rotate to face toward/away from target (shortest wrapped error)
        2) drive: move straight with heading PID correction
        3) final_turn: rotate to desired final heading (optional)
        """
        if not self.target_active or self.target_world is None:
            return
        if self.pose_filter is None:
            self.logger.error("Target mode needs pose filter")
            self.target_active = False
            return

        pose = self.pose_filter.get_estimate()
        if pose is None:
            return

        dt = self._target_dt()
        target_x, target_y = self.target_world

        dx = target_x - pose.x
        dy = target_y - pose.y
        distance_mm = math.sqrt(dx * dx + dy * dy)
        current_heading = self._wrap_heading(pose.z)
        if distance_mm > 1e-6:
            heading_to_target = self._heading_from_target_vector(dx, dy)
        else:
            heading_to_target = current_heading

        if self._target_phase == "align":
            self._enter_align_phase(current_heading, heading_to_target)

        if self._target_phase == "align":
            heading_error = self._heading_error_for_drive_sign(current_heading, heading_to_target, self._target_drive_sign)
            abs_error = abs(heading_error)

            if abs_error <= self._target_align_tolerance_deg:
                self._target_in_tolerance_count += 1
            else:
                self._target_in_tolerance_count = 0

            if self._target_in_tolerance_count >= self._target_settle_frames:
                self._enter_drive_phase(distance_mm)
                self._command_drive_smoothed(0.0, 0.0)
                return

            turned = max(0.0, self._target_align_start_error_deg - abs_error)
            turn_mag = self._profile_speed(
                traveled=turned,
                remaining=abs_error,
                accel=self._target_turn_accel,
                max_speed=self._target_max_turn_speed,
                min_speed=self._target_min_turn_speed,
                hold_min=True,
            )
            turn_cmd = self._signed_from_error(heading_error, turn_mag)
            left_cmd, right_cmd = self._mix_robot_drive(0.0, turn_cmd)
            self._command_drive_smoothed(left_cmd, right_cmd)
            return

        if self._target_phase == "drive":
            if distance_mm <= self.target_tolerance_mm:
                self._target_in_tolerance_count += 1
            else:
                self._target_in_tolerance_count = 0

            if self._target_in_tolerance_count >= self._target_required_in_tolerance_count:
                self._command_drive_smoothed(0, 0)
                if self.target_angle is None:
                    self._mark_target_complete()
                else:
                    self._enter_final_turn_phase(current_heading)
                return

            heading_error = self._heading_error_for_drive_sign(current_heading, heading_to_target, self._target_drive_sign)

            if abs(heading_error) > self._target_realign_threshold_deg:
                # Keep current direction unless a full re-choose is requested.
                self._target_choose_direction_on_align = False
                self._enter_align_phase(current_heading, heading_to_target)
                self._command_drive_smoothed(0, 0)
                return

            traveled = max(0.0, self._target_drive_start_distance_mm - distance_mm)
            drive_mag = self._profile_speed(
                traveled=traveled,
                remaining=distance_mm,
                accel=self._target_drive_accel,
                max_speed=self._target_max_drive_speed,
                min_speed=self._target_min_drive_speed,
                hold_min=(distance_mm > self.target_tolerance_mm),
            )

            self._path_heading_pid.setpoint = 0
            steering = self._path_heading_pid.compute(-heading_error, dt=dt)
            steer_cap = min(self._target_max_steer_speed, max(6.0, drive_mag * 0.4))
            steering = max(-steer_cap, min(steer_cap, steering))

            linear = self._target_drive_sign * drive_mag
            left_cmd, right_cmd = self._mix_robot_drive(linear, steering)
            self._command_drive_smoothed(left_cmd, right_cmd)
            return

        if self._target_phase == "final_turn":
            if self.target_angle is None:
                self._mark_target_complete()
                return

            heading_error = self._angle_residual(self.target_angle, current_heading)
            abs_error = abs(heading_error)

            if abs_error <= self.target_heading_tolerance_deg:
                self._target_in_tolerance_count += 1
            else:
                self._target_in_tolerance_count = 0

            if self._target_in_tolerance_count >= self._target_settle_frames:
                self._mark_target_complete()
                return

            turned = max(0.0, self._target_final_turn_start_error_deg - abs_error)
            turn_mag = self._profile_speed(
                traveled=turned,
                remaining=abs_error,
                accel=self._target_turn_accel,
                max_speed=self._target_max_turn_speed,
                min_speed=self._target_min_turn_speed,
                hold_min=True,
            )
            turn_cmd = self._signed_from_error(heading_error, turn_mag)
            left_cmd, right_cmd = self._mix_robot_drive(0.0, turn_cmd)
            self._command_drive_smoothed(left_cmd, right_cmd)
            return

    def _stop_all_outputs(self):
        self.drivecontroller.update_manually(0, 0)
        self.intake.update_manually(0)
        self.outtake.update_manually(0)
        self.matchloader.update_manually(0)

    def is_finished(self):
        return self.currentstepidx >= len(self.steps)
    
    def start(self):
        self.timer.reset()
        self.currentstepidx = 0
        if self.steps:
            self.completesteptime = self.steps[0].duration
        else:
            self.completesteptime = 0

    def update(self):
        if self.target_active:
            self.target_update()
        else:
            self._update_steps()
    
    def _update_steps(self):
        """Run the active step-based autonomous routine."""
        if self.currentstepidx >= len(self.steps):
            # finished
            self._stop_all_outputs()
            return

        # VEX Timer.time defaults to milliseconds, so ask for seconds to match
        # the step durations we store.
        if self.timer.time(vex.TimeUnits.SECONDS) >= self.completesteptime:
            self.completesteptime += self.steps[self.currentstepidx].duration
            self.currentstepidx += 1

            if self.currentstepidx >= len(self.steps):
                # finished
                self._stop_all_outputs()
                return

        step = self.steps[self.currentstepidx]
        self.drivecontroller.update_manually(step.left, step.right)
        self.intake.update_manually(step.intake_speed)
        self.outtake.update_manually(step.outtake_speed)
        if step.matchloader_toggle_state is not None and getattr(self.matchloader, "mode", None) == "toggle":
            try:
                self.matchloader.set_toggle_state(step.matchloader_toggle_state)
            except RuntimeError:
                self.matchloader.update_manually(step.matchloader_speed)
        else:
            self.matchloader.update_manually(step.matchloader_speed)

class WrappedButton:
    def __init__(self, button):
        self.button = button
        self.last_state = False
        self.state = False
    def pressing(self):
        return self.state
    def releasing(self):
        return not self.state
    def pressed(self):
        return self.state and not self.last_state
    def released(self):
        return not self.state and self.last_state
    def raw_pressing(self):
        return self.button.pressing()
    def update_state(self):
        self.last_state = self.state
        self.state = self.button.pressing()

class Toggled:
    """Utility to keep a two-state value in sync across subsystems."""
    def __init__(self, value_a, value_b, initial_state="a"):
        self.value_a = value_a
        self.value_b = value_b
        self.state = self._normalize_state(initial_state)

    def _normalize_state(self, state):
        if isinstance(state, bool):
            return "a" if state else "b"
        if isinstance(state, str):
            lowered = state.lower()
            if lowered in ("a", "b"):
                return lowered
        raise ValueError("Toggle state must be 'a', 'b', True, or False")

    def set_state(self, state):
        normalized = self._normalize_state(state)
        changed = normalized != self.state
        self.state = normalized
        return changed

    def toggle(self):
        next_state = "b" if self.state == "a" else "a"
        self.state = next_state
        return self.state

    def get_value(self):
        return self.value_a if self.state == "a" else self.value_b

    def get_state(self):
        return self.state


class GameState:
    """Tracks detected startup field quadrant.

    Quadrant mapping:
    1 = blue right
    2 = blue left
    3 = red right
    4 = red left
    """
    QUADRANT_BLUE_RIGHT = 1
    QUADRANT_BLUE_LEFT = 2
    QUADRANT_RED_RIGHT = 3
    QUADRANT_RED_LEFT = 4

    def __init__(self):
        self.quadrant = None

    def set_from_position(self, x_mm, y_mm):
        # Color from x sign: x+ = blue, x- = red
        # Side from y sign: y+ = right, y- = left
        if x_mm > 0:
            self.quadrant = self.QUADRANT_BLUE_RIGHT if y_mm >= 0 else self.QUADRANT_BLUE_LEFT
        elif x_mm < 0:
            self.quadrant = self.QUADRANT_RED_RIGHT if y_mm >= 0 else self.QUADRANT_RED_LEFT
        else:
            self.quadrant = None
        return self.quadrant

    def get_label(self):
        if self.quadrant == self.QUADRANT_BLUE_RIGHT:
            return "blue right"
        if self.quadrant == self.QUADRANT_BLUE_LEFT:
            return "blue left"
        if self.quadrant == self.QUADRANT_RED_RIGHT:
            return "red right"
        if self.quadrant == self.QUADRANT_RED_LEFT:
            return "red left"
        return "unknown"
        
def autonomous_start():
    # Q4-referenced target; set_target mirrors for detected startup quadrant.
    auton.set_target(-1200, -900, None)
    logger.log("Autonomous started.")

def usercontrol_start():
    logger.log("User control started.")
        

"""
===========================================================
----------------------Configuration------------------------
===========================================================
"""

# Brain should be defined by default
brain=Brain()
controller = Controller()
brain.screen.set_pen_color(Color.WHITE)
brain.screen.render()
logger = Logger(brain, max_lines=50)
logger.log("Logger initialized.")
descore = ButtonControlledPneumatic(controller.buttonUp, DigitalOut(brain.three_wire_port.a))
intake = Intake(controller, Motor(Ports.PORT9))
outtake = ButtonControlledMotor(controller.buttonL1, controller.buttonL2, Motor(Ports.PORT7), speed=100)
matchloader = ButtonControlledPneumatic(controller.buttonDown, DigitalOut(brain.three_wire_port.b))
heightadjuster = ButtonControlledPneumatic(controller.buttonB, DigitalOut(brain.three_wire_port.c))
competition = Competition(usercontrol_start, autonomous_start)
# GPS mounting relative to robot center:
# +x = right, +y = forward. Rear-left mount => negative x and y.
GPS_MOUNT_X_MM = 105
GPS_MOUNT_Y_MM = 68
# If sensor/device orientation is flipped 180° relative to robot forward,
# keep this at 180.0. If heading is already correct, set to 0.0.
GPS_HEADING_OFFSET_DEG = 180.0

GPS = GPSSensor(Gps(Ports.PORT10), heading_offset_deg=GPS_HEADING_OFFSET_DEG)
GPS.set_origin(GPS_MOUNT_X_MM, GPS_MOUNT_Y_MM)
drivetrain = DriveController(
    [Motor(Ports.PORT4), Motor(Ports.PORT5), Motor(Ports.PORT6)],
    [Motor(Ports.PORT1), Motor(Ports.PORT2), Motor(Ports.PORT3)],
    controller,
)
Filter = KalmanFilter(GPS, drivetrain)

# Detect startup field quadrant from GPS x/y position.
# x > 0 = blue, x < 0 = red
# y > 0 = right, y < 0 = left
game_state = GameState()
startup_position = GPS.get_accurate_reading(samples=5, delay_ms=40)
if startup_position is not None:
    startup_x, startup_y, _ = startup_position
    quadrant = game_state.set_from_position(startup_x, startup_y)
    if quadrant is not None:
        logger.log("Detected startup quadrant: " + str(quadrant) + " (" + game_state.get_label() + ")")
    else:
        logger.warn("Detected startup quadrant: unknown")
else:
    logger.warn("Detected startup quadrant: unknown")

auton = AutonomousController(
    drivetrain,
    intake,
    outtake,
    matchloader,
    brain,
    logger,
    descore,
    pose_filter=Filter,
    game_state=game_state,
)
# Five autonomous step slots. Format:
# left, right, intake speed, outtake speed, matchloader speed, duration (seconds)
slot_routines = {
    1: StepAutonomousRoutine("Steps Slot 1"),
    2: StepAutonomousRoutine("Steps Slot 2"),
    3: StepAutonomousRoutine("Steps Slot 3"),
    4: StepAutonomousRoutine("Steps Slot 4"),
    5: StepAutonomousRoutine("Steps Slot 5"),
}

# Default sample routine in slot 5
slot_routines[5].add_step(-30, -30, 100, 50, 0, 2, matchloader_toggle_state="b")
slot_routines[5].add_step(0, 0, 100, 50, 0, 5, matchloader_toggle_state="b")

# Autonomous manager for selecting/testing step slots
auton_manager = AutonomousManager(brain, logger, auton, slot_routines)

# Config button (right arrow)
config_button = WrappedButton(controller.buttonRight)
flipfront_button = WrappedButton(controller.buttonA)

# setup UI
ui = UI(brain)
ui.add_logger(logger, x=10, y=50, width=480, height=35, num_lines=7)
ui.add_element(UI_element("button", "Grayson Gimic Bot", x=0, y=0, width=200, height=35, layer=3, font=FontType.MONO20, color=Color.BLUE, rounded_corners=False, onclick='logger.log("Button clicked!")'))
ui.add_element(UI_element("button", "", x=200, y=0, width=280, height=35, layer=3, font=FontType.MONO20, color=Color.BLUE, rounded_corners=False, onupdate='self.content = "batt:" + str(brain.battery.capacity()) + "%"'))

# Store references to dynamically added UI elements
config_slot_buttons = []

def show_config_ui():
    """Show the config mode UI for selecting/testing autonomous."""
    global config_slot_buttons
    clear_config_ui()
    
    button_width = 90
    button_height = 35
    start_x = 10
    start_y = 180
    spacing = 5
    
    # Create slot buttons 1-5 for step autonomous selection
    for i in range(auton_manager.SLOT_MIN, auton_manager.SLOT_MAX + 1):
        is_selected = auton_manager.selected_slot == i
        has_data = auton_manager.slot_has_data(i)

        if is_selected:
            color = Color.CYAN
            label = "[" + str(i) + "]"
        elif has_data:
            color = Color.GREEN
            label = "Slot " + str(i)
        else:
            color = Color(50, 50, 50)
            label = "Slot " + str(i)
        btn = UI_element("button", label,
                        x=start_x + (i-1) * (button_width + spacing),
                        y=start_y,
                        width=button_width, height=button_height,
                        layer=4, font=FontType.MONO15, color=color,
                        onclick='select_auton_slot(' + str(i) + ')')
        config_slot_buttons.append(btn)
        ui.add_element(btn)
    
    play_btn = UI_element("button", "Play",
                         x=start_x,
                         y=start_y + button_height + spacing,
                         width=button_width, height=button_height,
                         layer=4, font=FontType.MONO15, color=Color.YELLOW,
                         onclick='play_selected_auton()')
    config_slot_buttons.append(play_btn)
    ui.add_element(play_btn)
    
    stop_btn = UI_element("button", "Stop",
                         x=start_x + button_width + spacing,
                         y=start_y + button_height + spacing,
                         width=button_width, height=button_height,
                         layer=4, font=FontType.MONO15, color=Color.RED,
                         onclick='stop_auton_playback()')
    config_slot_buttons.append(stop_btn)
    ui.add_element(stop_btn)
    
    exit_btn = UI_element("button", "Exit",
                         x=start_x + 3 * (button_width + spacing),
                         y=start_y + button_height + spacing,
                         width=button_width, height=button_height,
                         layer=4, font=FontType.MONO15, color=Color.PURPLE,
                         onclick='exit_config_mode()')
    config_slot_buttons.append(exit_btn)
    ui.add_element(exit_btn)

def clear_config_ui():
    """Remove config mode buttons from UI."""
    global config_slot_buttons
    for btn in config_slot_buttons:
        ui.remove_element(btn)
    config_slot_buttons = []

def select_auton_slot(slot):
    """Select an autonomous slot and refresh the UI."""
    auton_manager.select_slot(slot)
    # Refresh to show new selection
    show_config_ui()

def play_selected_auton():
    """Play the currently selected autonomous for testing."""
    auton_manager.start_playback(auton_manager.selected_slot)

def stop_auton_playback():
    """Stop autonomous playback."""
    auton_manager.stop_playback()
    # Stop all motors
    drivetrain.update_manually(0, 0)
    drivetrain.update_motor_speeds()
    intake.update_manually(0)
    outtake.update_manually(0)
    matchloader.update_manually(0)

def exit_config_mode():
    """Exit config mode."""
    auton_manager.end_config_mode()
    clear_config_ui()
    logger.log("Exited config mode")

logger.log("UI initialized.")
ui.draw()



target_framerate = 10
screenupdatetimer = Timer()
screenupdatetimer.reset()

# Dedicated timer for consistent autonomous playback frame rate
# Autonomous playback advances one step update per FRAME_INTERVAL.
FRAME_INTERVAL = 0.02  # 20ms per frame = 50 FPS
frame_timer = Timer()
frame_timer.reset()

"""
=====================================================================
---------------------- Main control loop ----------------------------
=====================================================================
"""
while True:
    if screenupdatetimer.time() > 1/target_framerate:
        screenupdatetimer.reset()
        ui.update()
        ui.draw()
        config_button.update_state()
        flipfront_button.update_state()
        
        if config_button.pressed():
            if auton_manager.config_mode:
                exit_config_mode()
            else:
                auton_manager.start_config_mode()
                show_config_ui()

        if flipfront_button.pressed() and not auton_manager.config_mode:
            flipped = drivetrain.toggle_front()
            logger.log("Front flipped" if flipped else "Front normal")
    
    # Check if a consistent frame tick has elapsed for autonomous playback
    frame_tick = frame_timer.time(vex.TimeUnits.SECONDS) >= FRAME_INTERVAL
    if frame_tick:
        frame_timer.reset()

    if competition.is_enabled() or not(competition.is_competition_switch()):
        if competition.is_autonomous():
            if frame_tick:
                auton.update()
            drivetrain.update_motor_speeds()
        elif auton_manager.playback_mode:
            if frame_tick:
                auton.update()
            drivetrain.update_motor_speeds()
            if auton.is_finished():
                auton_manager.stop_playback()
                logger.log("Playback complete")
        else:
            drivetrain.update_from_controller()
            drivetrain.update_motor_speeds()
            intake.update_from_controller()
            outtake.update_from_controller()
            matchloader.update_from_controller()
            descore.update_from_controller()
            heightadjuster.update_from_controller()
        Filter.update() # update position estimate
    else:
        drivetrain.update_manually(0,0)
        drivetrain.update_motor_speeds()
        intake.update_manually(0)
        outtake.update_manually(0)
        matchloader.update_manually(0)
    time.sleep(0.01) # Sleep to prevent unnecessary 100% CPU usage