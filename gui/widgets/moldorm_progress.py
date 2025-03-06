from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap, QImage, QColor
import os
import math

class MoldormProgress(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(900, 50)  # Simple fixed size
        
        # Get sprite directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        sprite_dir = os.path.normpath(os.path.join(current_dir, "..", "assets", "Moldorm"))
        
        self.segments = []
        self.base_positions = []  # Store original y positions
        self.animation_time = 0
        
        # Small > +13 > Medium > +20 > Large > +27 > Medium > +23 > Small
        self.moldorm_structure = [
            ("tail.png", 0),    # Start with tail
            ("body3.png", 12),  # Small body 
            ("body2.png", 25),  # Medium body
            ("body1.png", 45), # Large body
            ("body2.png", 72),  # Medium body
            ("body3.png", 95),  # Small body 
            ("body2.png", 108),  # Medium body 
            ("body1.png", 128), # Large body
            ("body2.png", 155),  # Medium body 
            ("body3.png", 178),  # Small body
            ("body2.png", 191),  # Medium body 
            ("body1.png", 211), # Large body
            ("body2.png", 238),  # Medium body
            ("body3.png", 261),  # Small body 
            ("body2.png", 274),  # Medium body 
            ("body1.png", 294), # Large body
            ("body2.png", 321),  # Medium body 
            ("body3.png", 344),  # Small body
            ("body2.png", 357),  # Medium body 
            ("body1.png", 377), # Large body
            ("body2.png", 404),  # Medium body
            ("body3.png", 427),  # Small body 
            ("body2.png", 440),  # Medium body 
            ("body1.png", 460), # Large body
            ("body2.png", 487),  # Medium body 
            ("body3.png", 510),  # Small body
            ("body2.png", 523),  # Medium body 
            ("body1.png", 543), # Large body
            ("head.png", 570),  # End with head
        ]
        
        # Create all segments
        for filename, x_pos in self.moldorm_structure:
            full_path = os.path.join(sprite_dir, filename)
            
            # Load sprite
            pixmap = QPixmap(full_path)
            if pixmap.isNull():
                continue
                
            # Calculate vertical center position for this sprite
            y_pos = (self.height() - pixmap.height()) // 2
            self.base_positions.append(y_pos)  # Store the base y position
                
            # Create darkened version
            dark_pixmap = self.create_darkened_pixmap(pixmap)
            
            # Create labels
            dark_label = QLabel(self)
            dark_label.setPixmap(dark_pixmap)
            dark_label.move(x_pos, y_pos)
            dark_label.show()
            
            normal_label = QLabel(self)
            normal_label.setPixmap(pixmap)
            normal_label.move(x_pos, y_pos)
            normal_label.hide()
            
            self.segments.append((dark_label, normal_label))
            
        # Setup animation timer
        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self.update_animation)
        self.animation_timer.start(50)  # Update every 50ms (20fps)
    
    def create_darkened_pixmap(self, original_pixmap):
        """Create a darkened version of the pixmap"""
        image = original_pixmap.toImage()
        
        for x in range(image.width()):
            for y in range(image.height()):
                color = image.pixelColor(x, y)
                if color.alpha() > 0:
                    color.setRed(color.red() // 2)
                    color.setGreen(color.green() // 2)
                    color.setBlue(color.blue() // 2)
                    image.setPixelColor(x, y, color)
                    
        return QPixmap.fromImage(image)
        
    def update_animation(self):
        """Update the wave animation"""
        self.animation_time += 0.2
        
        for i, ((dark_label, normal_label), base_y) in enumerate(zip(self.segments, self.base_positions)):
            phase = (len(self.segments) - 1 - i) * 0.25  # Reversed index
            amplitude = 10
            
            # Calculate new y position using sine wave
            offset = math.sin(self.animation_time - phase) * amplitude
            new_y = int(base_y + offset)
            
            # Update both labels' positions
            dark_label.move(dark_label.x(), new_y)
            normal_label.move(normal_label.x(), new_y)
        
    def set_progress(self, value):
        """Update progress (0-100) by showing/hiding normal segments"""
        progress = min(100, max(0, value))
        segments_to_activate = int((progress / 100.0) * len(self.segments))
        
        for i, (dark_label, normal_label) in enumerate(self.segments):
            if i < segments_to_activate:
                dark_label.hide()
                normal_label.show()
            else:
                dark_label.show()
                normal_label.hide()
