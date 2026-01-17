"""
Interaction Management Module
Inserts questions, suggestions, and comments to increase user engagement.
"""

import random
from typing import List, Dict, Any, Optional
from enum import Enum


class InteractionType(Enum):
    """Types of interactions."""
    QUESTION = "question"
    SUGGESTION = "suggestion"
    COMMENT = "comment"
    ENCOURAGEMENT = "encouragement"
    TIP = "tip"


class Interaction:
    """Represents an interaction to be inserted between instruction units."""
    
    def __init__(self, interaction_type: InteractionType, content: str, position: int):
        self.interaction_type = interaction_type
        self.content = content
        self.position = position  # Position in sequence where to insert
        self.metadata = {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert interaction to dictionary."""
        return {
            "type": self.interaction_type.value,
            "content": self.content,
            "position": self.position,
            "metadata": self.metadata
        }
    
    def __repr__(self):
        return f"Interaction({self.interaction_type.value}: '{self.content[:30]}...' at pos {self.position})"


class InteractionManager:
    """
    Manages insertion of interactions between instruction units.
    Increases user engagement through questions, tips, and encouragement.
    """
    
    def __init__(self, frequency: str = "medium"):
        """
        Initialize interaction manager.
        
        Args:
            frequency: How often to insert interactions (low, medium, high)
        """
        self.frequency = frequency
        self.interactions: List[Interaction] = []
        self._setup_interaction_templates()
    
    def _setup_interaction_templates(self):
        """Set up templates for different types of interactions."""
        self.questions = [
            "Have you found all the pieces for this step?",
            "Does your build look like the picture?",
            "Are all connections secure?",
            "Ready to move to the next step?",
            "Would you like a hint for this step?",
            "How is your progress so far?",
        ]
        
        self.suggestions = [
            "Try organizing your pieces by color before starting.",
            "Double-check the orientation of each piece.",
            "Take a break if you're feeling frustrated.",
            "Compare your build with the image to verify accuracy.",
            "Consider building on a flat, stable surface.",
            "Keep small pieces in a separate container.",
        ]
        
        self.comments = [
            "This is a tricky part, take your time!",
            "You're making great progress!",
            "This technique is commonly used in many sets.",
            "Notice how the pieces interlock - that's LEGO engineering!",
            "This section adds structural stability.",
            "Pay attention to the color coding in the instructions.",
        ]
        
        self.encouragements = [
            "Great job! Keep going!",
            "You're doing fantastic!",
            "Almost there, don't give up!",
            "Excellent work on that step!",
            "You're a natural builder!",
            "That's the spirit!",
        ]
        
        self.tips = [
            "Pro tip: Press pieces firmly but gently to avoid damage.",
            "Tip: Count your pieces before starting each major section.",
            "Builder's tip: If a piece doesn't fit easily, don't force it.",
            "Quick tip: Use the brick separator tool for stubborn pieces.",
            "Expert tip: Build in good lighting to see details clearly.",
            "Handy tip: Keep the instruction booklet flat to avoid creases.",
        ]
    
    def generate_interactions(self, units: List[Any]) -> List[Interaction]:
        """
        Generate interactions to be inserted among instruction units.
        
        Args:
            units: List of instruction units
            
        Returns:
            List of Interaction objects
        """
        self.interactions = []
        
        if not units:
            return self.interactions
        
        # Determine interaction frequency
        if self.frequency == "low":
            interval = max(5, len(units) // 3)
        elif self.frequency == "high":
            interval = max(2, len(units) // 10)
        else:  # medium
            interval = max(3, len(units) // 6)
        
        # Generate interactions at intervals
        for i in range(0, len(units), interval):
            if i == 0:
                # Welcome message at start
                interaction = Interaction(
                    InteractionType.COMMENT,
                    "Welcome! Let's build something amazing together!",
                    i
                )
                self.interactions.append(interaction)
            
            elif i < len(units) // 4:
                # Early stage - questions and tips
                if random.random() < 0.5:
                    interaction = self._create_question(i)
                else:
                    interaction = self._create_tip(i)
                self.interactions.append(interaction)
            
            elif i < len(units) * 3 // 4:
                # Middle stage - mix of interactions
                choice = random.choice([
                    InteractionType.SUGGESTION,
                    InteractionType.COMMENT,
                    InteractionType.ENCOURAGEMENT
                ])
                interaction = self._create_interaction(choice, i)
                self.interactions.append(interaction)
            
            else:
                # Late stage - encouragement
                interaction = self._create_encouragement(i)
                self.interactions.append(interaction)
        
        # Add completion message
        completion = Interaction(
            InteractionType.ENCOURAGEMENT,
            "Congratulations! You've completed your build! 🎉",
            len(units)
        )
        self.interactions.append(completion)
        
        return self.interactions
    
    def _create_interaction(self, interaction_type: InteractionType, position: int) -> Interaction:
        """Create an interaction of specified type."""
        if interaction_type == InteractionType.QUESTION:
            return self._create_question(position)
        elif interaction_type == InteractionType.SUGGESTION:
            return self._create_suggestion(position)
        elif interaction_type == InteractionType.COMMENT:
            return self._create_comment(position)
        elif interaction_type == InteractionType.ENCOURAGEMENT:
            return self._create_encouragement(position)
        elif interaction_type == InteractionType.TIP:
            return self._create_tip(position)
    
    def _create_question(self, position: int) -> Interaction:
        """Create a question interaction."""
        content = random.choice(self.questions)
        return Interaction(InteractionType.QUESTION, content, position)
    
    def _create_suggestion(self, position: int) -> Interaction:
        """Create a suggestion interaction."""
        content = random.choice(self.suggestions)
        return Interaction(InteractionType.SUGGESTION, content, position)
    
    def _create_comment(self, position: int) -> Interaction:
        """Create a comment interaction."""
        content = random.choice(self.comments)
        return Interaction(InteractionType.COMMENT, content, position)
    
    def _create_encouragement(self, position: int) -> Interaction:
        """Create an encouragement interaction."""
        content = random.choice(self.encouragements)
        return Interaction(InteractionType.ENCOURAGEMENT, content, position)
    
    def _create_tip(self, position: int) -> Interaction:
        """Create a tip interaction."""
        content = random.choice(self.tips)
        return Interaction(InteractionType.TIP, content, position)
    
    def insert_interactions(self, units: List[Any], interactions: Optional[List[Interaction]] = None) -> List[Any]:
        """
        Insert interactions into the instruction sequence.
        
        Args:
            units: List of instruction units
            interactions: Optional list of interactions (uses generated if not provided)
            
        Returns:
            Combined list of units and interactions in sequence
        """
        if interactions is None:
            interactions = self.interactions
        
        if not interactions:
            return units
        
        # Combine units and interactions
        combined = []
        interaction_map = {i.position: i for i in interactions}
        
        for idx, unit in enumerate(units):
            # Add interaction if one exists at this position
            if idx in interaction_map:
                combined.append(interaction_map[idx])
            
            # Add the unit
            combined.append(unit)
        
        # Add any interactions at or after the end
        for pos in sorted(interaction_map.keys()):
            if pos >= len(units):
                combined.append(interaction_map[pos])
        
        return combined
    
    def get_interactions(self) -> List[Interaction]:
        """Get all generated interactions."""
        return self.interactions
    
    def set_frequency(self, frequency: str):
        """Set interaction frequency (low, medium, high)."""
        if frequency in ["low", "medium", "high"]:
            self.frequency = frequency
    
    def get_interaction_stats(self) -> Dict[str, int]:
        """Get statistics about interaction types."""
        stats = {}
        for interaction in self.interactions:
            itype = interaction.interaction_type.value
            stats[itype] = stats.get(itype, 0) + 1
        return stats
