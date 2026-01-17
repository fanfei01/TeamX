"""
Example usage of the Lego Instruction Personalizer API.
Demonstrates all four main features of the system.
"""

from lego_instructor import (
    PDFRecognizer,
    InstructionDecomposer,
    InstructionPersonalizer,
    InteractionManager,
)
from lego_instructor.pdf_recognizer import InstructionStep
from lego_instructor.personalizer import UserProfile, SkillLevel, InterestCategory


def create_example_steps():
    """Create example instruction steps."""
    return [
        InstructionStep(1, "Welcome! Sort all your LEGO pieces by color and size.", page_number=1),
        InstructionStep(2, "Step 1: Take 4 red 2x4 bricks and 2 blue 2x2 bricks.", page_number=1),
        InstructionStep(3, "Step 2: Connect the red bricks in a rectangular base.", page_number=2),
        InstructionStep(4, "Step 3: Advanced technique: Add the turntable mechanism for rotating features.", page_number=2),
        InstructionStep(5, "Step 4: Build the walls using alternating brick colors.", page_number=3),
        InstructionStep(6, "Step 5: Create the roof structure with angled plates.", page_number=3),
        InstructionStep(7, "Step 6: Add decorative elements and finishing touches.", page_number=4),
        InstructionStep(8, "Final step: Display your completed masterpiece!", page_number=4),
    ]


def example_1_basic_workflow():
    """Example 1: Complete workflow from steps to personalized instructions."""
    print("\n" + "="*60)
    print("EXAMPLE 1: Basic Workflow")
    print("="*60)
    
    # Get instruction steps
    steps = create_example_steps()
    print(f"✓ Created {len(steps)} example instruction steps")
    
    # Decompose into minimal units
    decomposer = InstructionDecomposer()
    units = decomposer.decompose(steps)
    print(f"✓ Decomposed into {len(units)} minimal units")
    
    # Create a beginner user profile
    profile = UserProfile(skill_level=SkillLevel.BEGINNER)
    print(f"✓ Created beginner user profile")
    
    # Personalize
    personalizer = InstructionPersonalizer(profile)
    personalized = personalizer.personalize(units)
    print(f"✓ Personalized to {len(personalized)} units")
    
    # Add interactions
    interaction_mgr = InteractionManager(frequency="medium")
    interactions = interaction_mgr.generate_interactions(personalized)
    final = interaction_mgr.insert_interactions(personalized, interactions)
    print(f"✓ Added {len(interactions)} interactions")
    print(f"✓ Final sequence has {len(final)} items")


def example_2_advanced_user():
    """Example 2: Advanced user with specific interests."""
    print("\n" + "="*60)
    print("EXAMPLE 2: Advanced User with Interests")
    print("="*60)
    
    steps = create_example_steps()
    decomposer = InstructionDecomposer()
    units = decomposer.decompose(steps)
    
    # Create advanced user with specific interests
    profile = UserProfile(skill_level=SkillLevel.ADVANCED)
    profile.add_interest(InterestCategory.TECHNIQUES)
    profile.add_interest(InterestCategory.SPEED_BUILD)
    profile.set_preference("skip_basics", True)
    profile.set_preference("pacing", "fast")
    
    print(f"✓ User profile:")
    print(f"  - Skill: {profile.skill_level.value}")
    print(f"  - Interests: {[i.value for i in profile.interests]}")
    print(f"  - Skip basics: {profile.preferences['skip_basics']}")
    
    # Personalize
    personalizer = InstructionPersonalizer(profile)
    personalized = personalizer.personalize(units)
    
    difficulty_dist = personalizer.get_difficulty_distribution()
    estimated_time = personalizer.get_estimated_time()
    
    print(f"✓ Personalized sequence:")
    print(f"  - Units: {len(personalized)}")
    print(f"  - Difficulty distribution: {difficulty_dist}")
    print(f"  - Estimated time: {estimated_time // 60} min {estimated_time % 60} sec")


def example_3_custom_interactions():
    """Example 3: Custom interaction frequency and analysis."""
    print("\n" + "="*60)
    print("EXAMPLE 3: Custom Interaction Patterns")
    print("="*60)
    
    steps = create_example_steps()
    decomposer = InstructionDecomposer()
    units = decomposer.decompose(steps)
    
    # Test different interaction frequencies
    for frequency in ["low", "medium", "high"]:
        interaction_mgr = InteractionManager(frequency=frequency)
        interactions = interaction_mgr.generate_interactions(units)
        stats = interaction_mgr.get_interaction_stats()
        
        print(f"\n{frequency.upper()} frequency:")
        print(f"  - Total interactions: {len(interactions)}")
        print(f"  - By type: {stats}")


def example_4_unit_filtering():
    """Example 4: Filtering units by type and difficulty."""
    print("\n" + "="*60)
    print("EXAMPLE 4: Unit Filtering and Analysis")
    print("="*60)
    
    steps = create_example_steps()
    decomposer = InstructionDecomposer()
    units = decomposer.decompose(steps)
    
    # Get units by type
    from lego_instructor.instruction_decomposer import UnitType
    
    basic_units = decomposer.get_units_by_type(UnitType.BASIC)
    technique_units = decomposer.get_units_by_type(UnitType.TECHNIQUE)
    
    print(f"✓ Unit classification:")
    print(f"  - Basic units: {len(basic_units)}")
    print(f"  - Technique units: {len(technique_units)}")
    
    # Get units by difficulty
    easy_units = decomposer.get_units_by_difficulty(1, 2)
    hard_units = decomposer.get_units_by_difficulty(4, 5)
    
    print(f"✓ Difficulty filtering:")
    print(f"  - Easy units (1-2): {len(easy_units)}")
    print(f"  - Hard units (4-5): {len(hard_units)}")
    
    # Show some details
    if technique_units:
        print(f"\n✓ Example technique unit:")
        unit = technique_units[0]
        print(f"  - ID: {unit.unit_id}")
        print(f"  - Type: {unit.unit_type.value}")
        print(f"  - Difficulty: {unit.difficulty}")
        print(f"  - Content: {unit.content[:80]}...")


def main():
    """Run all examples."""
    print("\n" + "="*60)
    print("  LEGO INSTRUCTION PERSONALIZER - API EXAMPLES")
    print("="*60)
    
    example_1_basic_workflow()
    example_2_advanced_user()
    example_3_custom_interactions()
    example_4_unit_filtering()
    
    print("\n" + "="*60)
    print("All examples completed successfully!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
