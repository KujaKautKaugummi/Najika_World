"""
Inventory Models
Database models for items and equipment
"""

from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base


class InventoryItem(Base):
    """Inventory item model"""

    __tablename__ = "inventory_items"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Ownership
    character_id = Column(Integer, ForeignKey("characters.id"), nullable=False)

    # Item Info
    item_id = Column(String(100), nullable=False)  # Unique item identifier (e.g., "potion_health_small")
    item_type = Column(String(50), nullable=False)  # "food", "weapon", "armor", "material", "quest"
    name = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)

    # Quantity & Stats
    quantity = Column(Integer, default=1)
    quality = Column(Float, default=1.0)  # 0.0 - 1.0 (durability/freshness)

    # Item Properties
    properties = Column(JSON, default=dict)  # Flexible storage for item-specific data

    # Stack Info
    is_stackable = Column(Boolean, default=True)
    max_stack_size = Column(Integer, default=99)

    # Timestamps
    acquired_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    character = relationship("Character", back_populates="inventory")

    def __repr__(self):
        return f"<InventoryItem(id={self.id}, item_id='{self.item_id}', quantity={self.quantity})>"

    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "item_id": self.item_id,
            "item_type": self.item_type,
            "name": self.name,
            "description": self.description,
            "quantity": self.quantity,
            "quality": self.quality,
            "properties": self.properties,
            "is_stackable": self.is_stackable,
            "acquired_at": self.acquired_at.isoformat() if self.acquired_at else None,
        }


class Equipment(Base):
    """Character equipment/loadout model"""

    __tablename__ = "equipment"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Ownership (One-to-One with Character)
    character_id = Column(Integer, ForeignKey("characters.id"), unique=True, nullable=False)

    # Weapon Slots
    weapon_left = Column(Integer, ForeignKey("inventory_items.id"), nullable=True)
    weapon_right = Column(Integer, ForeignKey("inventory_items.id"), nullable=True)

    # Armor Slots
    armor_head = Column(Integer, ForeignKey("inventory_items.id"), nullable=True)
    armor_chest = Column(Integer, ForeignKey("inventory_items.id"), nullable=True)
    armor_legs = Column(Integer, ForeignKey("inventory_items.id"), nullable=True)
    armor_feet = Column(Integer, ForeignKey("inventory_items.id"), nullable=True)

    # Accessory Slots
    accessory_1 = Column(Integer, ForeignKey("inventory_items.id"), nullable=True)
    accessory_2 = Column(Integer, ForeignKey("inventory_items.id"), nullable=True)

    # Timestamps
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    character = relationship("Character", back_populates="equipment")

    def __repr__(self):
        return f"<Equipment(character_id={self.character_id})>"

    def to_dict(self):
        """Convert to dictionary"""
        return {
            "character_id": self.character_id,
            "weapon_left": self.weapon_left,
            "weapon_right": self.weapon_right,
            "armor_head": self.armor_head,
            "armor_chest": self.armor_chest,
            "armor_legs": self.armor_legs,
            "armor_feet": self.armor_feet,
            "accessory_1": self.accessory_1,
            "accessory_2": self.accessory_2,
        }
