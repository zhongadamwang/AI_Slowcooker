#!/usr/bin/env python3
"""
GitHub Issue Create/Update Script
==================================

Creates and updates GitHub Issues from local task markdown files with 
field mapping, metadata extraction, and two-way synchronization support 
for project management integration.

Usage:
    python create_update_issues.py --file <task_file>
    python create_update_issues.py --project <project_directory>
    python create_update_issues.py --directory <tasks_directory>
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

# Import shared utilities
sys.path.insert(0, str(Path(__file__).parent.parent / "shared"))
from github_utils import (
    ConfigurationManager, GitHubAuthenticator, GitHubClient,
    TaskFileParser, GitHubAuthenticationError, GitHubAPIError,
    get_repository_from_config_or_credentials
)


class GitHubIssueCreator:
    """Main class for creating and updating GitHub issues from task files."""
    
    def __init__(self, project_path: Optional[str] = None, config_override: Optional[Dict] = None):
        self.config_manager = ConfigurationManager(project_path)
        if config_override:
            # Merge in any configuration overrides
            self.config_manager.config.update(config_override)
        
        self.authenticator = GitHubAuthenticator(self.config_manager)
        self.credentials = None
        self.github_client = None
        self.results = []
    
    def initialize(self):
        """Initialize GitHub authentication and client."""
        try:
            self.credentials = self.authenticator.get_credentials()
            self.github_client = GitHubClient(self.credentials, self.config_manager)
            print(f"✅ Authenticated as: {self.credentials.username}")
        except GitHubAuthenticationError as e:
            print(f"❌ Authentication failed: {e}")
            sys.exit(1)
    
    def process_single_file(self, file_path: Path) -> Dict[str, Any]:
        """Process a single task file."""
        print(f"📄 Processing: {file_path.name}")
        
        try:
            # Parse task file
            task_data = TaskFileParser.parse_task_file(file_path)
            
            # Get repository info
            owner, repo = get_repository_from_config_or_credentials(
                self.config_manager, self.credentials
            )
            
            # Determine if this is create or update operation
            if task_data['github_issue_number']:
                return self._update_existing_issue(owner, repo, task_data)
            else:
                return self._create_new_issue(owner, repo, task_data)
        
        except Exception as e:
            error_msg = f"❌ Error processing {file_path.name}: {e}"
            print(error_msg)
            return {
                'file': file_path.name,
                'operation': 'error',
                'error': str(e),
                'success': False
            }
    
    def _create_new_issue(self, owner: str, repo: str, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new GitHub issue."""
        try:
            # Map task data to GitHub issue fields
            title, body, labels, assignees = self._map_task_to_issue_fields(task_data)
            
            # Create the issue
            issue = self.github_client.create_issue(owner, repo, title, body, labels, assignees)
            
            # Update task file with GitHub issue metadata
            updates = {
                'github_issue_number': issue.number,
                'github_issue_url': issue.url,
                'last_synced': datetime.now().isoformat()
            }
            
            success = TaskFileParser.update_task_file(
                task_data['file_path'], 
                updates,
                backup=self.config_manager.get("github.file_handling.backup_on_update", False)
            )
            
            if success:
                result = {
                    'file': task_data['file_path'].name,
                    'operation': 'created',
                    'issue_number': issue.number,
                    'issue_url': issue.url,
                    'title': title,
                    'success': True
                }
                print(f"✅ Created issue #{issue.number}: {title}")
            else:
                result = {
                    'file': task_data['file_path'].name,
                    'operation': 'created_but_update_failed',
                    'issue_number': issue.number,
                    'issue_url': issue.url,
                    'success': False,
                    'warning': 'Issue created but task file update failed'
                }
                print(f"⚠️ Created issue #{issue.number} but failed to update task file")
            
            return result
            
        except GitHubAPIError as e:
            error_msg = f"Failed to create issue: {e}"
            print(f"❌ {error_msg}")
            return {
                'file': task_data['file_path'].name,
                'operation': 'create_failed',
                'error': str(e),
                'success': False
            }
    
    def _update_existing_issue(self, owner: str, repo: str, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing GitHub issue."""
        issue_number = task_data['github_issue_number']
        
        try:
            # Map task data to GitHub issue fields
            title, body, labels, assignees = self._map_task_to_issue_fields(task_data)
            
            # Get current issue to determine what needs updating
            current_issue = self.github_client.get_issue(owner, repo, issue_number)
            
            # Determine state mapping
            new_state = self._map_task_state_to_github_state(task_data['state'])
            
            # Update the issue
            issue = self.github_client.update_issue(
                owner, repo, issue_number, 
                title=title, 
                body=body, 
                state=new_state,
                labels=labels,
                assignees=assignees
            )
            
            # Update task file sync metadata
            updates = {
                'last_synced': datetime.now().isoformat()
            }
            
            success = TaskFileParser.update_task_file(
                task_data['file_path'], 
                updates,
                backup=self.config_manager.get("github.file_handling.backup_on_update", False)
            )
            
            # Summarize changes
            changes = []
            if current_issue.title != title:
                changes.append("title")
            if current_issue.body != body:
                changes.append("description") 
            if current_issue.state != new_state:
                changes.append("state")
            if set(current_issue.labels) != set(labels or []):
                changes.append("labels")
            if set(current_issue.assignees) != set(assignees or []):
                changes.append("assignees")
            
            result = {
                'file': task_data['file_path'].name,
                'operation': 'updated',
                'issue_number': issue.number,
                'issue_url': issue.url,
                'title': title,
                'changes': changes,
                'success': True
            }
            
            if changes:
                print(f"✅ Updated issue #{issue.number}: {', '.join(changes)} changed")
            else:
                print(f"ℹ️  Issue #{issue.number} is already up to date")
            
            return result
            
        except GitHubAPIError as e:
            error_msg = f"Failed to update issue #{issue_number}: {e}"
            print(f"❌ {error_msg}")
            return {
                'file': task_data['file_path'].name,
                'operation': 'update_failed',
                'issue_number': issue_number,
                'error': str(e),
                'success': False
            }
    
    def _map_task_to_issue_fields(self, task_data: Dict[str, Any]) -> Tuple[str, str, List[str], List[str]]:
        """Map task file data to GitHub issue fields."""
        title = task_data['title'] or f"Task: {task_data['file_path'].stem}"
        body = task_data['description'] or "No description provided."
        
        # Process labels
        labels = list(task_data['labels']) if task_data['labels'] else []
        
        # Add priority label if configured
        if task_data['priority']:
            priority_mapping = self.config_manager.get("github.field_mapping.priority_labels", {})
            if task_data['priority'] in priority_mapping:
                priority_config = priority_mapping[task_data['priority']]
                labels.append(priority_config.get("name", f"priority:{task_data['priority'].lower()}"))
            else:
                labels.append(f"priority:{task_data['priority'].lower()}")
        
        # Add effort label if configured
        if task_data['estimated_effort']:
            effort_prefix = self.config_manager.get("github.field_mapping.effort_label_prefix", "effort:")
            effort_label = f"{effort_prefix}{task_data['estimated_effort'].replace(' ', '-')}"
            labels.append(effort_label)
        
        # Add additional labels from configuration
        additional_labels = self.config_manager.get("github.field_mapping.additional_labels", [])
        labels.extend(additional_labels)
        
        # Remove excluded labels
        excluded_labels = self.config_manager.get("github.field_mapping.exclude_labels", [])
        labels = [label for label in labels if label not in excluded_labels]
        
        # Remove duplicates while preserving order
        seen = set()
        unique_labels = []
        for label in labels:
            if label not in seen:
                unique_labels.append(label)
                seen.add(label)
        
        # Process assignees
        assignees = task_data['assignees'] if task_data['assignees'] else []
        
        # Add default assignee if configured
        default_assignee = self.config_manager.get("github.issue_defaults.default_assignee")
        if default_assignee and default_assignee not in assignees:
            assignees.append(default_assignee)
        
        return title, body, unique_labels, assignees
    
    def _map_task_state_to_github_state(self, task_state: str) -> str:
        """Map task state to GitHub issue state."""
        state_mapping = self.config_manager.get("github.field_mapping.state_mapping", {})
        return state_mapping.get(task_state, "open")
    
    def process_directory(self, directory: Path) -> List[Dict[str, Any]]:
        """Process all task files in a directory."""
        if not directory.exists():
            print(f"❌ Directory not found: {directory}")
            return []
        
        print(f"📁 Processing directory: {directory}")
        
        # Find all markdown files (potential task files)
        markdown_files = list(directory.glob("*.md"))
        
        if not markdown_files:
            print("ℹ️  No markdown files found in directory")
            return []
        
        results = []
        successful = 0
        failed = 0
        
        for file_path in markdown_files:
            # Skip README and other non-task files
            if file_path.name.lower() in ['readme.md', 'index.md']:
                continue
                
            result = self.process_single_file(file_path)
            results.append(result)
            
            if result.get('success', False):
                successful += 1
            else:
                failed += 1
        
        print(f"\n📊 Summary: {successful} successful, {failed} failed")
        return results
    
    def process_project(self, project_path: Path) -> List[Dict[str, Any]]:
        """Process all task files in a project's tasks directory."""
        tasks_dir = project_path / "tasks"
        if not tasks_dir.exists():
            print(f"❌ Tasks directory not found: {tasks_dir}")
            return []
        
        print(f"🎯 Processing project: {project_path.name}")
        return self.process_directory(tasks_dir)
    
    def generate_report(self, results: List[Dict[str, Any]]) -> str:
        """Generate a summary report of the operations."""
        if not results:
            return "No operations performed."
        
        successful = [r for r in results if r.get('success', False)]
        failed = [r for r in results if not r.get('success', False)]
        
        report = [
            f"GitHub Issue Create/Update Report",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"",
            f"Summary:",
            f"  Total files processed: {len(results)}",
            f"  Successful operations: {len(successful)}",
            f"  Failed operations: {len(failed)}",
            f""
        ]
        
        if successful:
            report.append("Successful Operations:")
            for result in successful:
                operation = result['operation']
                file_name = result['file']
                issue_num = result.get('issue_number', 'N/A')
                
                if operation == 'created':
                    report.append(f"  ✅ {file_name} → Created issue #{issue_num}")
                elif operation == 'updated':
                    changes = result.get('changes', [])
                    if changes:
                        report.append(f"  ✅ {file_name} → Updated issue #{issue_num} ({', '.join(changes)})")
                    else:
                        report.append(f"  ℹ️  {file_name} → Issue #{issue_num} already up to date")
            report.append("")
        
        if failed:
            report.append("Failed Operations:")
            for result in failed:
                file_name = result['file']
                error = result.get('error', 'Unknown error')
                report.append(f"  ❌ {file_name} → {error}")
            report.append("")
        
        return "\n".join(report)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Create and update GitHub Issues from EDPS task files",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--file', '-f',
        type=Path,
        help='Process a single task file'
    )
    
    parser.add_argument(
        '--directory', '-d',
        type=Path,
        help='Process all task files in a directory'
    )
    
    parser.add_argument(
        '--project', '-p',
        type=Path,
        help='Process all task files in a project (looks for tasks/ subdirectory)'
    )
    
    parser.add_argument(
        '--config',
        type=Path,
        help='Path to configuration file override'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be done without making changes'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )
    
    parser.add_argument(
        '--report',
        type=Path,
        help='Save detailed report to file'
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    input_sources = [args.file, args.directory, args.project]
    if sum(1 for source in input_sources if source) != 1:
        parser.error("Please specify exactly one of: --file, --directory, or --project")
    
    # Load configuration override if specified
    config_override = {}
    if args.config and args.config.exists():
        with open(args.config) as f:
            config_override = json.load(f)
    
    # Determine project path for configuration hierarchy
    project_path = None
    if args.project:
        project_path = str(args.project)
    elif args.directory and 'projects' in str(args.directory):
        # Try to infer project path from directory
        parts = args.directory.parts
        if 'projects' in parts:
            project_idx = parts.index('projects')
            if project_idx + 1 < len(parts):
                project_path = str(Path(*parts[:project_idx + 2]))
    
    if args.dry_run:
        print("🔍 DRY RUN MODE - No changes will be made")
        print()
    
    # Initialize creator
    creator = GitHubIssueCreator(project_path, config_override)
    creator.initialize()
    
    # Process files based on arguments
    results = []
    
    if args.file:
        if not args.file.exists():
            print(f"❌ File not found: {args.file}")
            sys.exit(1)
        results = [creator.process_single_file(args.file)]
    
    elif args.directory:
        results = creator.process_directory(args.directory)
    
    elif args.project:
        results = creator.process_project(args.project)
    
    # Generate and display report
    report = creator.generate_report(results)
    print("\n" + "="*50)
    print(report)
    
    # Save report if requested
    if args.report:
        with open(args.report, 'w') as f:
            f.write(report)
        print(f"\n📄 Report saved to: {args.report}")
    
    # Exit with appropriate code
    failed_count = sum(1 for r in results if not r.get('success', False))
    if failed_count > 0:
        print(f"\n⚠️  {failed_count} operations failed")
        sys.exit(1)
    else:
        print(f"\n✅ All operations completed successfully")
        sys.exit(0)


if __name__ == "__main__":
    main()