import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
import numpy as np

# Create figure and axis
fig, ax = plt.subplots(1, 1, figsize=(20, 16))
ax.set_xlim(0, 24)
ax.set_ylim(0, 18)
ax.axis('off')

# Define entities with their positions and sizes
entities = [
    # User Management
    ('Account', 2, 15, 5, 2.5),
    ('UserProfile', 10, 15, 5, 2.5),
    
    # Product Management
    ('Category', 2, 12, 5, 2.5),
    ('Product', 10, 12, 5, 2.5),
    ('Variation', 18, 12, 5, 2.5),
    ('ProductGallery', 2, 9, 5, 2.5),
    
    # Review System
    ('ReviewRating', 10, 9, 5, 2.5),
    
    # Shopping Cart
    ('Cart', 18, 9, 5, 2.5),
    ('CartItem', 2, 6, 5, 2.5),
    
    # Order Management
    ('Payment', 10, 6, 5, 2.5),
    ('Order', 18, 6, 5, 2.5),
    ('OrderProduct', 2, 3, 5, 2.5),
]

# Draw entities
for name, x, y, w, h in entities:
    # Create rounded rectangle
    box = FancyBboxPatch(
        (x, y), w, h,
        boxstyle='round,pad=0.1',
        facecolor='lightblue',
        edgecolor='darkblue',
        linewidth=2
    )
    ax.add_patch(box)
    
    # Add entity name
    ax.text(x + w/2, y + h/2, name, 
            ha='center', va='center', 
            fontsize=11, fontweight='bold',
            color='darkblue')

# Define relationships with their positions and labels
relationships = [
    # User Management
    ((4.5, 16.25), (10, 16.25), '1:1', 'Account ↔ UserProfile'),
    
    # Product Management
    ((4.5, 13.25), (10, 13.25), '1:N', 'Category → Product'),
    ((12.5, 13.25), (18, 13.25), '1:N', 'Product → Variation'),
    ((4.5, 10.25), (10, 10.25), '1:N', 'Product → ProductGallery'),
    
    # Review System
    ((12.5, 10.25), (10, 10.25), '1:N', 'Product → ReviewRating'),
    ((7, 15.25), (12.5, 10.25), '1:N', 'Account → ReviewRating'),
    
    # Shopping Cart
    ((12.5, 10.25), (20.5, 10.25), '1:N', 'Product → CartItem'),
    ((7, 15.25), (4.5, 7.25), '1:N', 'Account → CartItem'),
    ((20.5, 10.25), (4.5, 7.25), '1:N', 'Cart → CartItem'),
    
    # Order Management
    ((7, 15.25), (12.5, 7.25), '1:N', 'Account → Payment'),
    ((7, 15.25), (20.5, 7.25), '1:N', 'Account → Order'),
    ((12.5, 7.25), (20.5, 7.25), '1:1', 'Payment → Order'),
    ((20.5, 7.25), (4.5, 4.25), '1:N', 'Order → OrderProduct'),
    ((12.5, 7.25), (4.5, 4.25), '1:N', 'Payment → OrderProduct'),
    ((7, 15.25), (4.5, 4.25), '1:N', 'Account → OrderProduct'),
    ((12.5, 10.25), (4.5, 4.25), '1:N', 'Product → OrderProduct'),
]

# Draw relationships
for (x1, y1), (x2, y2), rel_type, label in relationships:
    # Draw arrow
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', lw=2, color='red'))
    
    # Add relationship label
    ax.text((x1 + x2)/2, (y1 + y2)/2, rel_type, 
            ha='center', va='center', fontsize=9, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.8))

# Add title and subtitle
ax.text(12, 17.5, 'Hawashmart E-Commerce Database Schema', 
        ha='center', va='center', fontsize=18, fontweight='bold', color='darkblue')
ax.text(12, 17, 'Entity Relationship Diagram (ERD)', 
        ha='center', va='center', fontsize=14, color='gray')

# Add legend
legend_elements = [
    patches.Patch(color='lightblue', label='Entities'),
    patches.Patch(color='red', label='Relationships'),
    patches.Patch(color='yellow', label='Cardinality')
]
ax.legend(handles=legend_elements, loc='upper right', fontsize=10)

# Add section labels
ax.text(3.5, 16.5, 'User Management', ha='center', va='center', 
        fontsize=12, fontweight='bold', color='darkgreen')
ax.text(3.5, 13.5, 'Product Management', ha='center', va='center', 
        fontsize=12, fontweight='bold', color='darkgreen')
ax.text(3.5, 10.5, 'Content & Reviews', ha='center', va='center', 
        fontsize=12, fontweight='bold', color='darkgreen')
ax.text(3.5, 7.5, 'Shopping Cart', ha='center', va='center', 
        fontsize=12, fontweight='bold', color='darkgreen')
ax.text(3.5, 4.5, 'Order Management', ha='center', va='center', 
        fontsize=12, fontweight='bold', color='darkgreen')

plt.tight_layout()
plt.savefig('database_schema.png', dpi=300, bbox_inches='tight', facecolor='white')
print('Database schema diagram generated as database_schema.png') 