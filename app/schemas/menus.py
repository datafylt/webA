"""
Menu Schema - Minimal version for admin.py MenuType dependency
"""

from enum import Enum


class MenuType(str, Enum):
    """Menu type enumeration"""
    CATALOG = "catalog"   # Catalogue/Directory
    MENU = "menu"         # Menu item
    BUTTON = "button"     # Button/Action
