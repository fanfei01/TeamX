"""
Instruction Decomposition Module
Decomposes building instruction sequences into minimal units with certain rules.
"""

from typing import List, Dict, Any, Optional
from enum import Enum


class UnitType(Enum):
    """Types of instruction units."""
    BASIC = "basic"  # Simple single-piece addition
    INTERMEDIATE = "intermediate"  # Multiple pieces, clear sequence
    COMPLEX = "complex"  # Complex assembly, multiple sub-steps
    TECHNIQUE = "technique"  # Special building technique


class InstructionUnit:
    """Represents a minimal unit of building instruction."""
    
    def __init__(self, unit_id: int, content: str, unit_type: UnitType = UnitType.BASIC):
        self.unit_id = unit_id
        self.content = content
        self.unit_type = unit_type
        self.pieces_count = 0
        self.difficulty = 1  # 1-5 scale
        self.prerequisites = []  # List of unit_ids that should come before
        self.images = []
        self.tags = []
        self.estimated_time = 0  # in seconds
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert unit to dictionary representation."""
        return {
            "unit_id": self.unit_id,
            "content": self.content,
            "unit_type": self.unit_type.value,
            "pieces_count": self.pieces_count,
            "difficulty": self.difficulty,
            "prerequisites": self.prerequisites,
            "tags": self.tags,
            "estimated_time": self.estimated_time
        }
    
    def __repr__(self):
        return f"InstructionUnit(id={self.unit_id}, type={self.unit_type.value}, difficulty={self.difficulty})"


class DecompositionRule:
    """Defines rules for decomposing instructions."""
    
    def __init__(self, name: str, condition: callable, action: callable):
        self.name = name
        self.condition = condition  # Function that returns bool
        self.action = action  # Function that performs decomposition
    
    def applies(self, step: Any) -> bool:
        """Check if this rule applies to the given step."""
        return self.condition(step)
    
    def apply(self, step: Any) -> List[InstructionUnit]:
        """Apply the decomposition rule."""
        return self.action(step)


class InstructionDecomposer:
    """
    Decomposes building instructions into minimal units based on rules.
    """
    
    def __init__(self):
        self.units: List[InstructionUnit] = []
        self.rules: List[DecompositionRule] = []
        self._setup_default_rules()
    
    def _setup_default_rules(self):
        """Set up default decomposition rules."""
        
        # Rule 1: Split by explicit step numbers
        def has_step_numbers(step):
            text = step.text if hasattr(step, 'text') else str(step)
            return any(marker in text.lower() for marker in ["step", "étape", "schritt"])
        
        def split_by_steps(step):
            units = []
            text = step.text if hasattr(step, 'text') else str(step)
            # Simple split by newlines or step markers
            lines = text.split('\n')
            for idx, line in enumerate(lines):
                if line.strip():
                    unit = InstructionUnit(idx + 1, line.strip())
                    units.append(unit)
            return units
        
        self.rules.append(DecompositionRule(
            "split_by_step_numbers",
            has_step_numbers,
            split_by_steps
        ))
        
        # Rule 2: Split by sentence for long text
        def is_long_text(step):
            text = step.text if hasattr(step, 'text') else str(step)
            return len(text) > 200
        
        def split_by_sentences(step):
            units = []
            text = step.text if hasattr(step, 'text') else str(step)
            sentences = text.replace('!', '.').replace('?', '.').split('.')
            for idx, sentence in enumerate(sentences):
                if sentence.strip():
                    unit = InstructionUnit(idx + 1, sentence.strip())
                    units.append(unit)
            return units
        
        self.rules.append(DecompositionRule(
            "split_long_text",
            is_long_text,
            split_by_sentences
        ))
    
    def add_rule(self, rule: DecompositionRule):
        """Add a custom decomposition rule."""
        self.rules.append(rule)
    
    def decompose(self, steps: List[Any]) -> List[InstructionUnit]:
        """
        Decompose instruction steps into minimal units.
        
        Args:
            steps: List of instruction steps (from PDFRecognizer)
            
        Returns:
            List of InstructionUnit objects
        """
        self.units = []
        unit_id = 1
        
        for step in steps:
            # Try to apply rules
            decomposed = False
            
            for rule in self.rules:
                if rule.applies(step):
                    step_units = rule.apply(step)
                    # Assign proper IDs
                    for unit in step_units:
                        unit.unit_id = unit_id
                        unit_id += 1
                    self.units.extend(step_units)
                    decomposed = True
                    break
            
            # If no rule applies, create a basic unit
            if not decomposed:
                text = step.text if hasattr(step, 'text') else str(step)
                unit = InstructionUnit(unit_id, text)
                
                # Copy metadata if available
                if hasattr(step, 'images'):
                    unit.images = step.images
                
                self.units.append(unit)
                unit_id += 1
        
        # Analyze and classify units
        self._classify_units()
        
        return self.units
    
    def _classify_units(self):
        """Classify units by type and difficulty."""
        for unit in self.units:
            # Simple heuristics for classification
            content_lower = unit.content.lower()
            
            # Determine unit type
            if any(word in content_lower for word in ["technique", "method", "special"]):
                unit.unit_type = UnitType.TECHNIQUE
            elif len(unit.content) > 100 or len(unit.images) > 2:
                unit.unit_type = UnitType.COMPLEX
            elif len(unit.content) > 50 or len(unit.images) > 1:
                unit.unit_type = UnitType.INTERMEDIATE
            else:
                unit.unit_type = UnitType.BASIC
            
            # Estimate difficulty (1-5 scale)
            if unit.unit_type == UnitType.BASIC:
                unit.difficulty = 1
            elif unit.unit_type == UnitType.INTERMEDIATE:
                unit.difficulty = 2
            elif unit.unit_type == UnitType.COMPLEX:
                unit.difficulty = 4
            elif unit.unit_type == UnitType.TECHNIQUE:
                unit.difficulty = 5
            
            # Estimate time (in seconds)
            unit.estimated_time = unit.difficulty * 30
            
            # Add tags
            if "brick" in content_lower or "piece" in content_lower:
                unit.tags.append("assembly")
            if "connect" in content_lower or "attach" in content_lower:
                unit.tags.append("connection")
    
    def get_units(self) -> List[InstructionUnit]:
        """Get the list of decomposed units."""
        return self.units
    
    def get_units_by_type(self, unit_type: UnitType) -> List[InstructionUnit]:
        """Get units filtered by type."""
        return [u for u in self.units if u.unit_type == unit_type]
    
    def get_units_by_difficulty(self, min_difficulty: int, max_difficulty: int) -> List[InstructionUnit]:
        """Get units filtered by difficulty range."""
        return [u for u in self.units if min_difficulty <= u.difficulty <= max_difficulty]
