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
    

# Recording class - writes directly to SD card in binary format
class MoveRecorder:
    """Records controller inputs directly to SD card for playback.
    
    Binary format (MR3): 4-byte header "MR3:" + 6 bytes per frame
    Each frame: left, right, intake, outtake, matchloader, pneumatic
    Values stored as unsigned bytes with +128 offset (so -100 = 28, 0 = 128, 100 = 228)
    """
    
    TEMP_FILE = "recording_temp.bin"
    
    def __init__(self, brain):
        self.brain = brain
        self.recording = False
        self.frame_count = 0
        self.frame_buffer = bytearray()  # Small buffer to batch writes
        self.buffer_size = 60  # Write every 10 frames (60 bytes)
    
    def start_recording(self):
        """Start recording - creates temp file with header."""
        self.recording = True
        self.frame_count = 0
        self.frame_buffer = bytearray()
        # Write header to temp file
        self.brain.sdcard.savefile(self.TEMP_FILE, bytearray("MR3:", "utf-8"))
    
    def stop_recording(self):
        """Stop recording - flush remaining buffer."""
        self.recording = False
        # Flush any remaining frames in buffer
        if len(self.frame_buffer) > 0:
            self.brain.sdcard.appendfile(self.TEMP_FILE, self.frame_buffer)
            self.frame_buffer = bytearray()
        return self.frame_count
    
    def record_frame(self, left, right, intake_speed, outtake_speed, matchloader_speed, pneumatic_state):
        """Record a single frame - buffers and writes to SD periodically."""
        if not self.recording:
            return
        
        # Convert signed values (-100 to 100) to unsigned bytes (28 to 228) with offset 128
        def to_byte(val):
            clamped = max(-128, min(127, int(round(val))))
            return (clamped + 128) & 0xFF
        
        # Add frame to buffer (6 bytes)
        self.frame_buffer.append(to_byte(left))
        self.frame_buffer.append(to_byte(right))
        self.frame_buffer.append(to_byte(intake_speed))
        self.frame_buffer.append(to_byte(outtake_speed))
        self.frame_buffer.append(to_byte(matchloader_speed))
        self.frame_buffer.append(1 if pneumatic_state else 0)
        
        self.frame_count += 1
        
        # Write buffer to SD when full
        if len(self.frame_buffer) >= self.buffer_size:
            self.brain.sdcard.appendfile(self.TEMP_FILE, self.frame_buffer)
            self.frame_buffer = bytearray()
    
    def get_temp_file(self):
        """Get the temp file path for saving to a slot."""
        return self.TEMP_FILE
    
    @staticmethod
    def load_frames(brain, filepath):
        """Load frames from a binary recording file."""
        if not brain.sdcard.exists(filepath):
            return []
        
        data = brain.sdcard.loadfile(filepath)
        if not data:
            return []
        
        # Check header
        if len(data) < 4:
            return []
        
        header = data[0:4]
        try:
            header_str = bytes(header).decode("utf-8")
        except:
            header_str = ""
        
        if header_str == "MR3:":
            return MoveRecorder._parse_mr3(data)
        elif header_str == "MR2:":
            # Legacy text format
            try:
                return MoveRecorder._parse_mr2(bytes(data).decode("utf-8"))
            except:
                return []
        elif header_str == "MS1:":
            # Legacy compressed format
            try:
                return MoveRecorder._parse_ms1(bytes(data).decode("utf-8"))
            except:
                return []
        
        return []
    
    @staticmethod
    def _parse_mr3(data):
        """Parse MR3 binary format."""
        frames = []
        # Skip 4-byte header, read 6 bytes per frame
        idx = 4
        while idx + 6 <= len(data):
            # Convert unsigned bytes back to signed values
            def from_byte(b):
                return b - 128
            
            frame = (
                from_byte(data[idx]),
                from_byte(data[idx + 1]),
                from_byte(data[idx + 2]),
                from_byte(data[idx + 3]),
                from_byte(data[idx + 4]),
                data[idx + 5]  # pneumatic is 0/1, no offset
            )
            frames.append(frame)
            idx += 6
        
        return frames
    
    @staticmethod
    def _parse_mr2(move_string):
        """Parse MR2 (text) format for backwards compatibility."""
        data = move_string[4:]  # Remove "MR2:" header
        if not data:
            return []
        
        frames = []
        segments = data.split(";")
        
        for segment in segments:
            if not segment:
                continue
            parts = segment.split(",")
            if len(parts) == 6:
                frame = (int(parts[0]), int(parts[1]), int(parts[2]), int(parts[3]), int(parts[4]), int(parts[5]))
                frames.append(frame)
        
        return frames
    
    @staticmethod
    def _parse_ms1(move_string):
        """Parse MS1 (legacy compressed) format for backwards compatibility."""
        data = move_string[4:]
        if not data:
            return []
        
        b62 = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        
        def decode_num(s):
            if not s:
                return 0
            sign = 1
            if s[0] == '-':
                sign = -1
                s = s[1:]
            result = 0
            for c in s:
                result = result * 62 + b62.index(c)
            return sign * result
        
        def decode_frame(s):
            parts = s.split(",")
            return tuple(decode_num(p) for p in parts)
        
        frames = []
        segments = data.split(";")
        prev_frame = (0, 0, 0, 0, 0, 0)
        first = True
        
        for segment in segments:
            if not segment:
                continue
            if "*" in segment:
                frame_part, count_part = segment.rsplit("*", 1)
                count = decode_num(count_part)
            else:
                frame_part = segment
                count = 1
            delta = decode_frame(frame_part)
            for _ in range(count):
                if first:
                    frame = delta
                    first = False
                else:
                    frame = tuple(prev_frame[i] + delta[i] for i in range(6))
                frames.append(frame)
                prev_frame = frame
        
        return frames


# Autonomous file manager for SD card save/load
class AutonomousManager:
    """Manages saving, loading, and selecting autonomous routines from SD card."""
    
    def __init__(self, brain, logger, auton_controller):
        self.brain = brain
        self.logger = logger
        self.auton = auton_controller
        self.selected_slot = 1  # Default to slot 1
        self.config_mode = False
        self.save_mode = False  # True when showing save slot buttons
        self.playback_mode = False  # True when playing back in config mode
        self._load_selected_slot()
    
    def _get_auton_filepath(self, slot):
        """Get the filepath for an autonomous slot."""
        return "auton_" + str(slot) + ".bin"
    
    def _get_selected_filepath(self):
        """Get the filepath for the selected slot config."""
        return "selected_auton.txt"
    
    def _sd_available(self):
        """Check if SD card is inserted."""
        return self.brain.sdcard.is_inserted()
    
    def _load_selected_slot(self):
        """Load the selected autonomous slot from SD card."""
        if not self._sd_available():
            self.logger.warn("No SD card - using defaults")
            return
        try:
            data = self.brain.sdcard.loadfile(self._get_selected_filepath())
            if data:
                content = bytes(data).decode("utf-8").strip()
                if content.isdigit():
                    slot = int(content)
                    if 1 <= slot <= 4:
                        self.selected_slot = slot
                        self.logger.log("Loaded auton slot: " + str(slot))
                        self._load_auton_from_slot(slot)
        except:
            self.logger.log("No saved auton selection, using slot 1")
    
    def _save_selected_slot(self, slot):
        """Save the selected autonomous slot to SD card."""
        if not self._sd_available():
            self.logger.error("No SD card!")
            return
        try:
            self.brain.sdcard.savefile(self._get_selected_filepath(), bytearray(str(slot), "utf-8"))
            self.selected_slot = slot
            self.logger.log("Saved auton selection: slot " + str(slot))
        except Exception as e:
            self.logger.error("Failed to save selection: " + str(e))
    
    def _load_auton_from_slot(self, slot):
        """Load an autonomous routine from a slot file."""
        if not self._sd_available():
            self.logger.error("No SD card!")
            return False
        filepath = self._get_auton_filepath(slot)
        if not self.brain.sdcard.exists(filepath):
            return False
        frames = MoveRecorder.load_frames(self.brain, filepath)
        if frames:
            self.auton.set_frames(frames)
            self.auton.set_mode("movestring")
            self.logger.log("Loaded slot " + str(slot) + " (" + str(len(frames)) + " frames)")
            return True
        return False
    
    def save_to_slot(self, slot, temp_file):
        """Copy the temp recording file to a slot file."""
        if not self._sd_available():
            self.logger.error("No SD card!")
            return False
        if not self.brain.sdcard.exists(temp_file):
            self.logger.error("No recording to save!")
            return False
        try:
            # Load temp file and save to slot
            data = self.brain.sdcard.loadfile(temp_file)
            if data:
                filepath = self._get_auton_filepath(slot)
                result = self.brain.sdcard.savefile(filepath, data)
                if result and result > 0:
                    self.logger.log("Saved to slot " + str(slot))
                    return True
            self.logger.error("Save failed!")
            return False
        except Exception as e:
            self.logger.error("Save failed: " + str(e))
            return False
    
    def slot_has_data(self, slot):
        """Check if a slot has a saved autonomous."""
        if not self._sd_available():
            return False
        filepath = self._get_auton_filepath(slot)
        return self.brain.sdcard.exists(filepath)
    
    def start_save_mode(self):
        """Enter save mode after recording."""
        self.save_mode = True
        self.logger.log("Choose slot 1-4 or Trash")
    
    def end_save_mode(self):
        """Exit save mode."""
        self.pending_movestring = None
        self.save_mode = False
    
    def start_config_mode(self):
        """Enter config mode for selecting/testing autonomous."""
        self.config_mode = True
        self.logger.log("Config mode: Select auton slot")
    
    def end_config_mode(self):
        """Exit config mode."""
        self.config_mode = False
        self.playback_mode = False
    
    def start_playback(self, slot):
        """Start playing back an autonomous for testing."""
        if self._load_auton_from_slot(slot):
            self.playback_mode = True
            self.auton.start()
            self.logger.log("Playing slot " + str(slot) + "...")
        else:
            self.logger.warn("Cannot play empty slot")
    
    def stop_playback(self):
        """Stop autonomous playback."""
        self.playback_mode = False
        self.logger.log("Playback stopped")
    
    def select_slot(self, slot):
        """Select a slot as the active autonomous for competition."""
        self._save_selected_slot(slot)
        self._load_auton_from_slot(slot)


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

    def get_joystick_input(self):
        # Treat x as the horizontal (turn) axis and y as the forward/back axis.
        # Controller: axis4 is horizontal (left/right), axis3 is vertical (forward/back).
        # Return (turn, forward) so downstream code can use input.x as turn and input.y as forward.
        if self.controltype == "arcade":
            return Vector2D(self.controller.axis4.position(), self.controller.axis3.position())
        elif self.controltype == "tank":
            return Vector2D(self.controller.axis1.position(), self.controller.axis3.position())
            
    
    def update_from_controller(self):
        # Arcade drive: axis3 = forward/back, axis4 = turn
        js = self.get_joystick_input()
        forward = self.forward_sign * js.y
        turn = self.turn_sign * js.x

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
        """Set pneumatic state from a value (for autonomous/recording playback).
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


class AutonomousController:
    def __init__(self, drivecontroller, intake, outtake, matchloader, brain, logger, descore=None):
        self.drivecontroller = drivecontroller
        self.intake = intake
        self.outtake = outtake
        self.brain = brain
        self.logger = logger
        self.steps = []
        self.timer = Timer()
        self.currentstepidx = 0
        self.completesteptime = 0
        self.matchloader = matchloader
        self.descore = descore
        # Playback mode: "steps" for step-based, "movestring" for recorded playback
        self.mode = "steps"
        self.playback_frames = []
        self.playback_idx = 0
        self.playback_timer = Timer()
        self.frame_duration = 0.01  # 10ms per frame (100 FPS recording)

    def add_step(self, step):
        self.steps.append(step)
    
    def set_frames(self, frames):
        """Set playback frames directly (from binary file)."""
        self.playback_frames = frames
        self.mode = "movestring"
    
    def set_mode(self, mode):
        """Set autonomous mode: 'steps' or 'movestring'."""
        self.mode = mode
    
    def start(self):
        self.timer.reset()
        self.currentstepidx = 0
        self.playback_idx = 0
        self.playback_timer.reset()
        if self.mode == "steps" and self.steps:
            self.completesteptime = self.steps[0].duration
        else:
            self.completesteptime = 0

    def update(self):
        if self.mode == "movestring":
            self._update_movestring()
        else:
            self._update_steps()
    
    def _update_movestring(self):
        """Playback recorded frames - one frame per update call for 1:1 timing."""
        if self.playback_idx >= len(self.playback_frames):
            # Finished playback
            self.drivecontroller.update_manually(0, 0)
            self.intake.update_manually(0)
            self.outtake.update_manually(0)
            self.matchloader.update_manually(0)
            return
        
        # Get current frame and apply it
        frame = self.playback_frames[self.playback_idx]
        left, right, intake_spd, outtake_spd, matchloader_spd, pneumatic_state = frame
        
        self.drivecontroller.update_manually(left, right)
        self.intake.update_manually(intake_spd)
        self.outtake.update_manually(outtake_spd)
        self.matchloader.update_manually(matchloader_spd)
        
        # Playback pneumatic states
        if self.descore is not None:
            self.descore.update_manually(1 if pneumatic_state else 0)
        
        # Advance to next frame
        self.playback_idx += 1
    
    def _update_steps(self):
        """Original step-based autonomous."""
        if self.currentstepidx >= len(self.steps):
            # finished
            self.drivecontroller.update_manually(0, 0)
            self.intake.update_manually(0)
            self.outtake.update_manually(0)
            self.matchloader.update_manually(0)
            return

        # VEX Timer.time defaults to milliseconds, so ask for seconds to match
        # the step durations we store.
        if self.timer.time(vex.TimeUnits.SECONDS) >= self.completesteptime:
            self.completesteptime += self.steps[self.currentstepidx].duration
            self.currentstepidx += 1

            if self.currentstepidx >= len(self.steps):
                # finished
                self.drivecontroller.update_manually(0, 0)
                self.intake.update_manually(0)
                self.outtake.update_manually(0)
                self.matchloader.update_manually(0)
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
        
def autonomous_start():
    auton.start()
    logger.log("Autonomous started.")

def usercontrol_start():
    logger.log("User control started.")
        

# Brain should be defined by default
brain=Brain()
controller = Controller()
record_button = WrappedButton(controller.buttonLeft)  # Left arrow to toggle recording
brain.screen.set_pen_color(Color.WHITE)
brain.screen.render()
logger = Logger(brain, max_lines=50)
logger.log("Logger initialized.")
move_recorder = MoveRecorder(brain)  # For recording controller inputs - needs brain for SD card
descore = ButtonControlledPneumatic(controller.buttonUp, DigitalOut(brain.three_wire_port.a))
intake = Intake(controller, Motor(Ports.PORT9))
outtake = ButtonControlledMotor(controller.buttonL1, controller.buttonL2, Motor(Ports.PORT7), speed=100)
matchloader = ButtonControlledPneumatic(controller.buttonDown, DigitalOut(brain.three_wire_port.b))
competition = Competition(usercontrol_start, autonomous_start)
drivetrain = DriveController(
    [Motor(Ports.PORT4), Motor(Ports.PORT5), Motor(Ports.PORT6)],
    [Motor(Ports.PORT1), Motor(Ports.PORT2), Motor(Ports.PORT3)],
    controller,
)

auton = AutonomousController(drivetrain, intake, outtake, matchloader, brain, logger, descore)
# autonomous steps. Format: left, right, intake speed, outtake speed, matchloader speed, duration (seconds)
auton.add_step(AutonomousStep(-30, -30, 100, 50, 0, 2, matchloader_toggle_state="b"))
auton.add_step(AutonomousStep(0, 0, 100, 50, 0, 5, matchloader_toggle_state="b"))

# Autonomous manager for SD card save/load
auton_manager = AutonomousManager(brain, logger, auton)

# Config button (right arrow)
config_button = WrappedButton(controller.buttonRight)

# To use a recorded MoveString instead of steps, uncomment and paste your MoveString:
# auton.set_movestring("MS1:your_movestring_here")
# 
# To switch back to step-based autonomous:
# auton.set_mode("steps")  # Commented out - auton_manager handles this now

# setup UI
ui = UI(brain)
ui.add_logger(logger, x=10, y=50, width=480, height=35, num_lines=7)
ui.add_element(UI_element("button", "Grayson Gimic Bot", x=0, y=0, width=200, height=35, layer=3, font=FontType.MONO20, color=Color.BLUE, rounded_corners=False, onclick='logger.log("Button clicked!")'))
ui.add_element(UI_element("button", "", x=200, y=0, width=280, height=35, layer=3, font=FontType.MONO20, color=Color.BLUE, rounded_corners=False, onupdate='self.content = "batt:" + str(brain.battery.capacity()) + "%"'))

# Store references to dynamically added UI elements
save_slot_buttons = []
config_slot_buttons = []

def show_save_slot_ui():
    """Show the save slot selection buttons."""
    global save_slot_buttons
    clear_save_slot_ui()
    
    button_width = 90
    button_height = 40
    start_x = 10
    start_y = 180
    spacing = 5
    
    # Create slot buttons 1-4
    for i in range(1, 5):
        has_data = auton_manager.slot_has_data(i)
        color = Color.ORANGE if has_data else Color.GREEN
        label = "Slot " + str(i) + ("*" if has_data else "")
        btn = UI_element("button", label, 
                        x=start_x + (i-1) * (button_width + spacing), 
                        y=start_y,
                        width=button_width, height=button_height,
                        layer=4, font=FontType.MONO15, color=color,
                        onclick='save_to_slot(' + str(i) + ')')
        save_slot_buttons.append(btn)
        ui.add_element(btn)
    
    # Trash button
    trash_btn = UI_element("button", "Trash",
                          x=start_x + 4 * (button_width + spacing),
                          y=start_y,
                          width=button_width, height=button_height,
                          layer=4, font=FontType.MONO15, color=Color.RED,
                          onclick='trash_recording()')
    save_slot_buttons.append(trash_btn)
    ui.add_element(trash_btn)

def clear_save_slot_ui():
    """Remove save slot buttons from UI."""
    global save_slot_buttons
    for btn in save_slot_buttons:
        ui.remove_element(btn)
    save_slot_buttons = []

def save_to_slot(slot):
    """Save pending recording to a slot."""
    auton_manager.save_to_slot(slot, move_recorder.get_temp_file())
    auton_manager.end_save_mode()
    clear_save_slot_ui()

def trash_recording():
    """Discard the pending recording."""
    logger.log("Recording discarded")
    auton_manager.end_save_mode()
    clear_save_slot_ui()

def show_config_ui():
    """Show the config mode UI for selecting/testing autonomous."""
    global config_slot_buttons
    clear_config_ui()
    
    button_width = 90
    button_height = 35
    start_x = 10
    start_y = 180
    spacing = 5
    
    # Create slot buttons 1-4 for selection
    for i in range(1, 5):
        has_data = auton_manager.slot_has_data(i)
        is_selected = auton_manager.selected_slot == i
        if is_selected:
            color = Color.CYAN
            label = "[" + str(i) + "]"
        elif has_data:
            color = Color.GREEN
            label = "Slot " + str(i)
        else:
            color = Color(50, 50, 50)
            label = "Empty " + str(i)
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

# Dedicated timer for consistent recording/playback frame rate
# Both record and playback advance one frame per FRAME_INTERVAL so timing stays 1:1
FRAME_INTERVAL = 0.02  # 20ms per frame = 50 FPS
frame_timer = Timer()
frame_timer.reset()

# Helper variables for tracking motor states during recording
last_intake_speed = 0
last_outtake_speed = 0
last_matchloader_speed = 0
last_pneumatic_state = False

while True:
    if screenupdatetimer.time() > 1/target_framerate:
        screenupdatetimer.reset()
        ui.update()
        ui.draw()
        record_button.update_state()
        config_button.update_state()
        
        if config_button.pressed() and not auton_manager.save_mode:
            if auton_manager.config_mode:
                exit_config_mode()
            else:
                auton_manager.start_config_mode()
                show_config_ui()
        
        if record_button.pressed() and not auton_manager.config_mode and not auton_manager.save_mode:
            if move_recorder.recording:
                frame_count = move_recorder.stop_recording()
                logger.log("Recording stopped. " + str(frame_count) + " frames.")
                # Show save slot selection UI
                auton_manager.start_save_mode()
                show_save_slot_ui()
            else:
                move_recorder.start_recording()
                frame_timer.reset()
                logger.log("Recording started! Press left arrow to stop.")
    
    # Check if a consistent frame tick has elapsed for recording/playback
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
            if auton.mode == "movestring" and auton.playback_idx >= len(auton.playback_frames):
                auton_manager.stop_playback()
                logger.log("Playback complete")
        else:
            drivetrain.update_from_controller()
            drivetrain.update_motor_speeds()
            intake.update_from_controller()
            outtake.update_from_controller()
            matchloader.update_from_controller()
            descore.update_from_controller()
            
            if move_recorder.recording and frame_tick:
                if controller.buttonR1.pressing():
                    current_intake = intake.speed
                elif controller.buttonR2.pressing():
                    current_intake = -intake.speed
                else:
                    current_intake = 0
                
                if controller.buttonL1.pressing():
                    current_outtake = outtake.speed
                elif controller.buttonL2.pressing():
                    current_outtake = -outtake.speed
                else:
                    current_outtake = 0
                
                current_matchloader = 100 if matchloader.toggle_state.state == "a" else 0
                
                current_pneumatic = descore.toggle_state.state == "a"
                
                move_recorder.record_frame(
                    drivetrain.left_speed,
                    drivetrain.right_speed,
                    current_intake,
                    current_outtake,
                    current_matchloader,
                    current_pneumatic
                )
    else:
        drivetrain.update_manually(0,0)
        drivetrain.update_motor_speeds()
        intake.update_manually(0)
        outtake.update_manually(0)
        matchloader.update_manually(0)
    time.sleep(0.01) # Sleep to prevent unnecessary 100% CPU usage