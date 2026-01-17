"""
Personalization Module
Re-selects and re-arranges instruction units based on user preferences.
"""

from typing import List, Dict, Any, Optional
from enum import Enum


class SkillLevel(Enum):
    """User skill levels."""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class InterestCategory(Enum):
    """Categories of user interests."""
    VEHICLES = "vehicles"
    BUILDINGS = "buildings"
    CHARACTERS = "characters"
    TECHNIQUES = "techniques"
    SPEED_BUILD = "speed_build"
    DETAILED_BUILD = "detailed_build"


class UserProfile:
    """Represents a user's preferences and skill level."""
    
    def __init__(self, skill_level: SkillLevel = SkillLevel.BEGINNER):
        self.skill_level = skill_level
        self.interests: List[InterestCategory] = []
        self.preferences = {
            "skip_basics": False,
            "show_techniques": True,
            "pacing": "normal",  # slow, normal, fast
            "interaction_frequency": "medium",  # low, medium, high
        }
    
    def set_skill_level(self, level: SkillLevel):
        """Set user's skill level."""
        self.skill_level = level
    
    def add_interest(self, interest: InterestCategory):
        """Add an interest category."""
        if interest not in self.interests:
            self.interests.append(interest)
    
    def set_preference(self, key: str, value: Any):
        """Set a user preference."""
        self.preferences[key] = value
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert profile to dictionary."""
        return {
            "skill_level": self.skill_level.value,
            "interests": [i.value for i in self.interests],
            "preferences": self.preferences
        }


class InstructionPersonalizer:
    """
    Personalizes instruction sequences based on user profile.
    Re-selects and re-arranges units according to preferences.
    """
    
    def __init__(self, user_profile: Optional[UserProfile] = None):
        self.user_profile = user_profile or UserProfile()
        self.personalized_units = []
    
    def set_user_profile(self, profile: UserProfile):
        """Set the user profile."""
        self.user_profile = profile
    
    def personalize(self, units: List[Any]) -> List[Any]:
        """
        Personalize instruction units based on user profile.
        
        Args:
            units: List of InstructionUnit objects
            
        Returns:
            Personalized list of units
        """
        # Start with all units
        selected_units = units.copy()
        
        # Filter based on skill level
        selected_units = self._filter_by_skill_level(selected_units)
        
        # Filter based on interests
        selected_units = self._filter_by_interests(selected_units)
        
        # Re-arrange based on preferences
        selected_units = self._rearrange_units(selected_units)
        
        # Apply pacing adjustments
        selected_units = self._apply_pacing(selected_units)
        
        self.personalized_units = selected_units
        return selected_units
    
    def _filter_by_skill_level(self, units: List[Any]) -> List[Any]:
        """Filter units based on user's skill level."""
        skill_level = self.user_profile.skill_level
        
        if skill_level == SkillLevel.BEGINNER:
            # Keep all units, especially basics
            return units
        
        elif skill_level == SkillLevel.INTERMEDIATE:
            # Skip very basic units if preference is set
            if self.user_profile.preferences.get("skip_basics", False):
                return [u for u in units if u.difficulty > 1]
            return units
        
        elif skill_level == SkillLevel.ADVANCED:
            # Focus on intermediate and complex units
            return [u for u in units if u.difficulty >= 2]
        
        elif skill_level == SkillLevel.EXPERT:
            # Focus on complex and technique units
            return [u for u in units if u.difficulty >= 3]
        
        return units
    
    def _filter_by_interests(self, units: List[Any]) -> List[Any]:
        """Filter or prioritize units based on user interests."""
        if not self.user_profile.interests:
            return units
        
        # Add scoring based on interests
        scored_units = []
        for unit in units:
            score = 0
            
            # Check if unit matches interests
            if InterestCategory.TECHNIQUES in self.user_profile.interests:
                if "technique" in unit.content.lower() or hasattr(unit, 'unit_type') and str(unit.unit_type).endswith('TECHNIQUE'):
                    score += 10
            
            if InterestCategory.SPEED_BUILD in self.user_profile.interests:
                # Prefer simpler, faster units
                score += (5 - unit.difficulty) * 2
            
            if InterestCategory.DETAILED_BUILD in self.user_profile.interests:
                # Prefer detailed, complex units
                score += unit.difficulty * 2
            
            scored_units.append((unit, score))
        
        # Sort by score (descending) but maintain some original order
        scored_units.sort(key=lambda x: (x[1], -x[0].unit_id), reverse=True)
        
        return [u for u, _ in scored_units]
    
    def _rearrange_units(self, units: List[Any]) -> List[Any]:
        """Re-arrange units based on preferences while respecting prerequisites."""
        # Check for prerequisites
        arranged_units = []
        remaining_units = units.copy()
        completed_ids = set()
        
        while remaining_units:
            # Find units whose prerequisites are met
            available = []
            for unit in remaining_units:
                prereqs = getattr(unit, 'prerequisites', [])
                if all(p in completed_ids for p in prereqs):
                    available.append(unit)
            
            if not available:
                # No prerequisites or circular dependency, add remaining
                arranged_units.extend(remaining_units)
                break
            
            # Add available units
            for unit in available:
                arranged_units.append(unit)
                completed_ids.add(unit.unit_id)
                remaining_units.remove(unit)
        
        return arranged_units
    
    def _apply_pacing(self, units: List[Any]) -> List[Any]:
        """Apply pacing adjustments based on user preferences."""
        pacing = self.user_profile.preferences.get("pacing", "normal")
        
        if pacing == "fast":
            # Skip some intermediate explanatory units
            return [u for i, u in enumerate(units) if i % 3 != 1 or u.difficulty >= 3]
        
        elif pacing == "slow":
            # Keep all units as-is
            return units
        
        # Normal pacing
        return units
    
    def get_personalized_units(self) -> List[Any]:
        """Get the personalized units."""
        return self.personalized_units
    
    def get_difficulty_distribution(self) -> Dict[int, int]:
        """Get distribution of difficulties in personalized units."""
        distribution = {}
        for unit in self.personalized_units:
            difficulty = unit.difficulty
            distribution[difficulty] = distribution.get(difficulty, 0) + 1
        return distribution
    
    def get_estimated_time(self) -> int:
        """Get total estimated time for personalized instructions."""
        return sum(getattr(u, 'estimated_time', 0) for u in self.personalized_units)
