#!/usr/bin/env python3
"""
Test script for the PromptRefiner module
Demonstrates usage with various example prompts
"""

from prompt_refiner import PromptRefiner
import json

def test_ecommerce_prompt():
    """Test with an e-commerce app prompt"""
    print("=== Testing E-commerce App Prompt ===")
    
    prompt = """
    Create a simple e-commerce app where users can buy and sell products. 
    It should be secure and fast, with a modern design. Users should be able to 
    create accounts, browse products, add items to cart, and checkout with payment.
    Admin users should be able to manage products and orders.
    """
    
    refiner = PromptRefiner()
    enhanced_spec = refiner.refine_prompt(prompt, "ecommerce_spec.json")
    
    print(f"✅ Generated spec for: {enhanced_spec.app_name}")
    print(f"📱 App Type: {enhanced_spec.app_type}")
    print(f"🎯 Target Audience: {enhanced_spec.target_audience}")
    print(f"⚡ Features: {len(enhanced_spec.features)}")
    print(f"👥 User Roles: {len(enhanced_spec.user_roles)}")
    print(f"🔧 Ambiguities Resolved: {len(enhanced_spec.ambiguities_resolved)}")
    
    return enhanced_spec

def test_social_app_prompt():
    """Test with a social app prompt"""
    print("\n=== Testing Social App Prompt ===")
    
    prompt = """
    Build a social platform where people can share posts, message each other,
    and follow friends. It needs to be user-friendly and support real-time chat.
    """
    
    refiner = PromptRefiner()
    enhanced_spec = refiner.refine_prompt(prompt, "social_spec.json")
    
    print(f"✅ Generated spec for: {enhanced_spec.app_name}")
    print(f"📱 App Type: {enhanced_spec.app_type}")
    print(f"🎯 Target Audience: {enhanced_spec.target_audience}")
    print(f"⚡ Features: {len(enhanced_spec.features)}")
    print(f"👥 User Roles: {len(enhanced_spec.user_roles)}")
    print(f"🔧 Ambiguities Resolved: {len(enhanced_spec.ambiguities_resolved)}")
    
    return enhanced_spec

def test_productivity_app_prompt():
    """Test with a productivity app prompt"""
    print("\n=== Testing Productivity App Prompt ===")
    
    prompt = """
    Create a task management application for teams. Users should be able to 
    create projects, assign tasks, set deadlines, and track progress. 
    It should have notifications and be scalable for large teams.
    """
    
    refiner = PromptRefiner()
    enhanced_spec = refiner.refine_prompt(prompt, "productivity_spec.json")
    
    print(f"✅ Generated spec for: {enhanced_spec.app_name}")
    print(f"📱 App Type: {enhanced_spec.app_type}")
    print(f"🎯 Target Audience: {enhanced_spec.target_audience}")
    print(f"⚡ Features: {len(enhanced_spec.features)}")
    print(f"👥 User Roles: {len(enhanced_spec.user_roles)}")
    print(f"🔧 Ambiguities Resolved: {len(enhanced_spec.ambiguities_resolved)}")
    
    return enhanced_spec

def test_vague_prompt():
    """Test with a very vague prompt to show ambiguity resolution"""
    print("\n=== Testing Vague Prompt ===")
    
    prompt = """
    Make a simple app that's easy to use and modern. It should be fast and secure.
    Users can do stuff and it should work well.
    """
    
    refiner = PromptRefiner()
    enhanced_spec = refiner.refine_prompt(prompt, "vague_spec.json")
    
    print(f"✅ Generated spec for: {enhanced_spec.app_name}")
    print(f"📱 App Type: {enhanced_spec.app_type}")
    print(f"🎯 Target Audience: {enhanced_spec.target_audience}")
    print(f"⚡ Features: {len(enhanced_spec.features)}")
    print(f"👥 User Roles: {len(enhanced_spec.user_roles)}")
    print(f"🔧 Ambiguities Resolved: {len(enhanced_spec.ambiguities_resolved)}")
    
    # Show resolved ambiguities for vague prompt
    print("\n🔍 Ambiguities Resolved:")
    for ambiguity in enhanced_spec.ambiguities_resolved:
        print(f"  • {ambiguity['original_ambiguity']}")
        print(f"    → {ambiguity['resolution']}")
    
    return enhanced_spec

def compare_specs(specs):
    """Compare different generated specs"""
    print("\n=== Specification Comparison ===")
    
    for i, spec in enumerate(specs, 1):
        print(f"\n{i}. {spec.app_name} ({spec.app_type})")
        print(f"   Features: {len(spec.features)}")
        print(f"   Integrations: {len(spec.integration_requirements)}")
        print(f"   Security Requirements: {len(spec.security_requirements)}")
        print(f"   Ambiguities Resolved: {len(spec.ambiguities_resolved)}")

def main():
    """Run all tests"""
    print("🚀 PromptRefiner Module Test Suite")
    print("=" * 50)
    
    specs = []
    
    try:
        # Test different types of prompts
        specs.append(test_ecommerce_prompt())
        specs.append(test_social_app_prompt())
        specs.append(test_productivity_app_prompt())
        specs.append(test_vague_prompt())
        
        # Compare results
        compare_specs(specs)
        
        print("\n✅ All tests completed successfully!")
        print("📁 Generated specification files:")
        print("   • ecommerce_spec.json")
        print("   • social_spec.json") 
        print("   • productivity_spec.json")
        print("   • vague_spec.json")
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        raise

if __name__ == "__main__":
    main()