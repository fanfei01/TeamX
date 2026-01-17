#!/usr/bin/env python3
"""
Command-line interface for Lego Instruction Personalizer.
Demonstrates the complete workflow from PDF to personalized instructions.
"""

import argparse
import json
import sys
from pathlib import Path

from lego_instructor import (
    PDFRecognizer,
    InstructionDecomposer,
    InstructionPersonalizer,
    InteractionManager,
)
from lego_instructor.personalizer import UserProfile, SkillLevel, InterestCategory


def print_banner():
    """Print welcome banner."""
    print("=" * 60)
    print("   LEGO INSTRUCTION PERSONALIZER")
    print("   Personalized Building Experience")
    print("=" * 60)
    print()


def create_sample_instructions():
    """Create sample instruction steps for demo when no PDF is available."""
    from lego_instructor.pdf_recognizer import InstructionStep
    
    steps = [
        InstructionStep(1, "Welcome to your LEGO building experience! Gather all pieces from the box.", page_number=1),
        InstructionStep(2, "Step 1: Find 4 red 2x4 bricks. Connect them in a square formation.", page_number=1),
        InstructionStep(3, "Step 2: Add 2 blue 1x2 plates on top of the red bricks.", page_number=2),
        InstructionStep(4, "Step 3: Attach the special technique piece - the turntable base. This allows rotation.", page_number=2),
        InstructionStep(5, "Step 4: Connect 6 yellow 1x1 round bricks around the turntable.", page_number=3),
        InstructionStep(6, "Step 5: Place the flat tile pieces on top to create a smooth surface.", page_number=3),
        InstructionStep(7, "Step 6: Attach the decorative elements - windows and door pieces.", page_number=4),
        InstructionStep(8, "Final step: Add the roof pieces to complete your build!", page_number=4),
    ]
    
    return steps


def process_pdf(pdf_path: str):
    """Process a PDF file and return recognized steps."""
    print(f"📄 Loading PDF: {pdf_path}")
    recognizer = PDFRecognizer()
    
    if not Path(pdf_path).exists():
        print(f"❌ Error: PDF file not found: {pdf_path}")
        return None
    
    steps = recognizer.recognize_instructions(pdf_path)
    metadata = recognizer.get_metadata()
    
    print(f"✓ Recognized {len(steps)} instruction steps from {metadata.get('num_pages', 0)} pages")
    return steps


def decompose_instructions(steps):
    """Decompose instruction steps into minimal units."""
    print("\n🔧 Decomposing instructions into minimal units...")
    decomposer = InstructionDecomposer()
    units = decomposer.decompose(steps)
    
    print(f"✓ Created {len(units)} instruction units")
    
    # Show unit distribution
    by_type = {}
    for unit in units:
        utype = unit.unit_type.value
        by_type[utype] = by_type.get(utype, 0) + 1
    
    print(f"  Unit types: {by_type}")
    return units


def personalize_instructions(units, skill_level, interests):
    """Personalize instructions based on user profile."""
    print("\n👤 Personalizing instructions for user profile...")
    
    # Create user profile
    profile = UserProfile(skill_level=skill_level)
    for interest in interests:
        profile.add_interest(interest)
    
    print(f"  Skill level: {skill_level.value}")
    print(f"  Interests: {[i.value for i in interests]}")
    
    # Personalize
    personalizer = InstructionPersonalizer(profile)
    personalized = personalizer.personalize(units)
    
    print(f"✓ Personalized to {len(personalized)} units")
    
    # Show stats
    difficulty_dist = personalizer.get_difficulty_distribution()
    estimated_time = personalizer.get_estimated_time()
    
    print(f"  Difficulty distribution: {difficulty_dist}")
    print(f"  Estimated time: {estimated_time // 60} minutes")
    
    return personalized


def add_interactions(units, frequency):
    """Add interactive elements to the instruction sequence."""
    print(f"\n💬 Adding interactions (frequency: {frequency})...")
    
    interaction_mgr = InteractionManager(frequency=frequency)
    interactions = interaction_mgr.generate_interactions(units)
    combined = interaction_mgr.insert_interactions(units, interactions)
    
    stats = interaction_mgr.get_interaction_stats()
    print(f"✓ Added {len(interactions)} interactions")
    print(f"  Interaction types: {stats}")
    
    return combined


def display_instructions(sequence):
    """Display the final personalized instruction sequence."""
    print("\n" + "=" * 60)
    print("   PERSONALIZED BUILDING INSTRUCTIONS")
    print("=" * 60)
    
    for idx, item in enumerate(sequence, 1):
        # Check if it's an interaction or instruction unit
        if hasattr(item, 'interaction_type'):
            # It's an interaction
            icon = {
                'question': '❓',
                'suggestion': '💡',
                'comment': '💬',
                'encouragement': '⭐',
                'tip': '🔍'
            }.get(item.interaction_type.value, '•')
            
            print(f"\n{icon} {item.interaction_type.value.upper()}: {item.content}")
        else:
            # It's an instruction unit
            difficulty_stars = "⭐" * item.difficulty
            print(f"\n[Unit {item.unit_id}] {difficulty_stars} ({item.unit_type.value})")
            print(f"  {item.content}")
            if item.tags:
                print(f"  Tags: {', '.join(item.tags)}")
    
    print("\n" + "=" * 60)


def export_to_json(sequence, output_path):
    """Export the personalized sequence to JSON."""
    print(f"\n💾 Exporting to: {output_path}")
    
    data = []
    for item in sequence:
        if hasattr(item, 'interaction_type'):
            data.append(item.to_dict())
        else:
            data.append(item.to_dict())
    
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"✓ Exported {len(data)} items to JSON")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Personalize Lego building instructions"
    )
    parser.add_argument(
        "--pdf",
        type=str,
        help="Path to PDF instruction file"
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run with sample demo data (no PDF required)"
    )
    parser.add_argument(
        "--skill-level",
        type=str,
        choices=["beginner", "intermediate", "advanced", "expert"],
        default="beginner",
        help="User skill level"
    )
    parser.add_argument(
        "--interests",
        type=str,
        nargs="+",
        choices=["vehicles", "buildings", "characters", "techniques", "speed_build", "detailed_build"],
        default=[],
        help="User interests"
    )
    parser.add_argument(
        "--interaction-frequency",
        type=str,
        choices=["low", "medium", "high"],
        default="medium",
        help="How often to insert interactions"
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Output JSON file path"
    )
    parser.add_argument(
        "--display",
        action="store_true",
        help="Display instructions in terminal"
    )
    
    args = parser.parse_args()
    
    print_banner()
    
    # Get instruction steps
    if args.demo or not args.pdf:
        print("🎮 Running in DEMO mode with sample instructions")
        steps = create_sample_instructions()
    else:
        steps = process_pdf(args.pdf)
        if not steps:
            sys.exit(1)
    
    # Decompose into units
    units = decompose_instructions(steps)
    
    if not units:
        print("❌ No units created")
        sys.exit(1)
    
    # Parse skill level and interests
    skill_level = SkillLevel(args.skill_level)
    interests = [InterestCategory(i) for i in args.interests]
    
    # Personalize
    personalized = personalize_instructions(units, skill_level, interests)
    
    # Add interactions
    final_sequence = add_interactions(personalized, args.interaction_frequency)
    
    # Display if requested
    if args.display or not args.output:
        display_instructions(final_sequence)
    
    # Export if requested
    if args.output:
        export_to_json(final_sequence, args.output)
    
    print("\n✅ Processing complete!")


if __name__ == "__main__":
    main()
