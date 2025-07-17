#!/usr/bin/env python3
"""
Test script for the CodeAnalyzer module.

This script demonstrates how to use the CodeAnalyzer to analyze a codebase
and generate feature maps.
"""

import os
import sys
from code_analyzer import CodeAnalyzer


def test_analyzer_on_current_project():
    """Test the analyzer on the current project directory."""
    print("🧪 Testing CodeAnalyzer on current project...")
    
    # Get current directory (the project we're in)
    current_dir = os.getcwd()
    
    # Initialize analyzer
    analyzer = CodeAnalyzer(current_dir)
    
    # Run analysis
    try:
        feature_map = analyzer.analyze_project()
        
        # Print summary
        analyzer.print_summary()
        
        # Save feature map
        analyzer.save_feature_map("current_project_feature_map.json")
        
        print("\n✅ Test completed successfully!")
        
        # Print some specific insights
        print(f"\n🔍 Specific Insights:")
        print(f"   • React components found: {len([f for f in feature_map.files if f.file_path.endswith('.tsx')])}")
        print(f"   • Python modules found: {len([f for f in feature_map.files if f.file_path.endswith('.py')])}")
        print(f"   • Configuration files: {len([f for f in feature_map.files if 'config' in f.file_path.lower()])}")
        
        # Show some React-specific analysis
        react_files = [f for f in feature_map.files if f.file_path.endswith('.tsx')]
        if react_files:
            print(f"\n⚛️  React Components Analysis:")
            for react_file in react_files[:5]:  # Show first 5
                print(f"   • {react_file.file_path}: {len(react_file.functions)} functions, {react_file.lines_of_code} LOC")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


def create_sample_project():
    """Create a sample project structure for testing."""
    print("📁 Creating sample project structure...")
    
    sample_dir = "sample_project"
    os.makedirs(sample_dir, exist_ok=True)
    
    # Create sample Python files
    with open(f"{sample_dir}/main.py", "w") as f:
        f.write('''
"""Main application module."""

import os
import json
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class User:
    """User data model."""
    id: int
    name: str
    email: str
    is_active: bool = True

class UserService:
    """Service for managing users."""
    
    def __init__(self):
        self.users = []
    
    async def create_user(self, name: str, email: str) -> User:
        """Create a new user."""
        user = User(
            id=len(self.users) + 1,
            name=name,
            email=email
        )
        self.users.append(user)
        return user
    
    def get_user(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        for user in self.users:
            if user.id == user_id:
                return user
        return None

def main():
    """Main function."""
    service = UserService()
    print("Application started")

if __name__ == "__main__":
    main()
''')
    
    # Create sample JavaScript file
    with open(f"{sample_dir}/app.js", "w") as f:
        f.write('''
import React from 'react';
import axios from 'axios';

class UserComponent extends React.Component {
    constructor(props) {
        super(props);
        this.state = { users: [] };
    }
    
    async fetchUsers() {
        try {
            const response = await axios.get('/api/users');
            this.setState({ users: response.data });
        } catch (error) {
            console.error('Error fetching users:', error);
        }
    }
    
    render() {
        return (
            <div>
                <h1>Users</h1>
                {this.state.users.map(user => (
                    <div key={user.id}>{user.name}</div>
                ))}
            </div>
        );
    }
}

const UserList = ({ users }) => {
    return (
        <ul>
            {users.map(user => (
                <li key={user.id}>{user.name} - {user.email}</li>
            ))}
        </ul>
    );
};

export default UserComponent;
''')
    
    # Create sample TypeScript file
    with open(f"{sample_dir}/types.ts", "w") as f:
        f.write('''
interface User {
    id: number;
    name: string;
    email: string;
    isActive: boolean;
}

type UserStatus = 'active' | 'inactive' | 'pending';

interface ApiResponse<T> {
    data: T;
    status: number;
    message: string;
}

class ApiClient {
    private baseUrl: string;
    
    constructor(baseUrl: string) {
        this.baseUrl = baseUrl;
    }
    
    async get<T>(endpoint: string): Promise<ApiResponse<T>> {
        const response = await fetch(`${this.baseUrl}${endpoint}`);
        return response.json();
    }
    
    async post<T>(endpoint: string, data: any): Promise<ApiResponse<T>> {
        const response = await fetch(`${this.baseUrl}${endpoint}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        return response.json();
    }
}

export { User, UserStatus, ApiResponse, ApiClient };
''')
    
    print(f"✅ Sample project created in: {sample_dir}")
    return sample_dir


def test_analyzer_on_sample():
    """Test the analyzer on the sample project."""
    print("\n🧪 Testing CodeAnalyzer on sample project...")
    
    sample_dir = create_sample_project()
    
    # Initialize analyzer
    analyzer = CodeAnalyzer(sample_dir)
    
    # Run analysis
    try:
        feature_map = analyzer.analyze_project()
        
        # Print summary
        analyzer.print_summary()
        
        # Save feature map
        analyzer.save_feature_map("sample_project_feature_map.json")
        
        print("\n✅ Sample test completed successfully!")
        
        # Clean up
        import shutil
        shutil.rmtree(sample_dir)
        print(f"🧹 Cleaned up sample directory: {sample_dir}")
        
        return True
        
    except Exception as e:
        print(f"❌ Sample test failed: {e}")
        return False


def main():
    """Main test function."""
    print("🚀 Starting CodeAnalyzer Tests")
    print("=" * 50)
    
    # Test 1: Analyze current project
    success1 = test_analyzer_on_current_project()
    
    print("\n" + "=" * 50)
    
    # Test 2: Analyze sample project
    success2 = test_analyzer_on_sample()
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    print(f"   • Current project analysis: {'✅ PASSED' if success1 else '❌ FAILED'}")
    print(f"   • Sample project analysis: {'✅ PASSED' if success2 else '❌ FAILED'}")
    
    if success1 and success2:
        print("\n🎉 All tests passed! CodeAnalyzer is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")
        sys.exit(1)


if __name__ == "__main__":
    main()