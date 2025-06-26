"""
AI-powered code analysis that combines Perforce version control with OpenAI insights.
"""
import asyncio
from typing import Dict, Any, List, Optional
from homer.utils.logger import get_module_logger
from homer.modules.perforce.client import PerforceClient
from homer.modules.openai.client import OpenAIClient

log = get_module_logger("stack.perforce_openai.ai_code_analysis")

class AICodeAnalysis:
    """Provides AI-powered analysis of Perforce code changes and metadata."""
    
    def __init__(self):
        self.p4_client = PerforceClient()
        self.openai_client = OpenAIClient()
    
    async def analyze_changelist(self, changelist_id: str, include_files: bool = False) -> Dict[str, Any]:
        """Analyze a Perforce changelist using AI to extract insights."""
        try:
            # Get changelist details from Perforce
            log.info(f"Analyzing changelist {changelist_id}")
            changelist = await self.p4_client.get_changelist(changelist_id)
            
            if not changelist:
                raise ValueError(f"Changelist {changelist_id} not found")
            
            description = changelist.get('description', '')
            files = changelist.get('files', [])
            
            # Prepare analysis text
            analysis_text = f"Changelist {changelist_id}:\n"
            analysis_text += f"Description: {description}\n"
            analysis_text += f"Files changed: {len(files)}\n"
            
            if include_files and files:
                analysis_text += "Files:\n"
                for file_info in files[:20]:  # Limit to first 20 files
                    analysis_text += f"- {file_info.get('file', '')}\n"
            
            # Get AI analysis
            log.info("Generating AI insights")
            
            # Generate summary
            summary = await self.openai_client.summarize(
                text=analysis_text,
                max_length=150
            )
            
            # Generate tags for categorization
            tags = await self.openai_client.generate_tags(
                text=analysis_text,
                num_tags=5
            )
            
            # Analyze sentiment
            sentiment = await self.openai_client.analyze_sentiment(description)
            
            # Determine change type using AI
            change_type_prompt = f"Analyze this code change description and categorize it as one of: feature, bugfix, refactor, docs, test, style, chore. Description: {description}"
            change_type_response = await self.openai_client.generate_completion(
                prompt=change_type_prompt,
                max_tokens=50
            )
            
            change_type = change_type_response.strip().lower()
            
            result = {
                "changelist_id": changelist_id,
                "original_description": description,
                "files_count": len(files),
                "ai_analysis": {
                    "summary": summary,
                    "tags": tags,
                    "sentiment": sentiment,
                    "change_type": change_type,
                    "confidence": "high" if len(description) > 50 else "medium"
                },
                "recommendations": await self._generate_recommendations(changelist, summary, tags)
            }
            
            log.info(f"Completed AI analysis for changelist {changelist_id}")
            return result
            
        except Exception as e:
            log.error(f"Failed to analyze changelist {changelist_id}: {e}")
            raise

    async def generate_release_notes(self, changelists: List[str], target_audience: str = "technical") -> Dict[str, Any]:
        """Generate AI-powered release notes from multiple changelists."""
        try:
            log.info(f"Generating release notes for {len(changelists)} changelists")
            
            # Collect all changelist data
            all_changes = []
            for cl_id in changelists:
                try:
                    changelist = await self.p4_client.get_changelist(cl_id)
                    if changelist:
                        all_changes.append(changelist)
                except Exception as e:
                    log.warning(f"Skipping changelist {cl_id}: {e}")
            
            if not all_changes:
                raise ValueError("No valid changelists found")
            
            # Categorize changes by type
            features = []
            bugfixes = []
            other = []
            
            for change in all_changes:
                description = change.get('description', '').lower()
                if any(word in description for word in ['feature', 'add', 'new', 'implement']):
                    features.append(change)
                elif any(word in description for word in ['fix', 'bug', 'issue', 'resolve']):
                    bugfixes.append(change)
                else:
                    other.append(change)
            
            # Generate AI-powered release notes
            release_notes_prompt = f"""
            Generate professional release notes for a software release based on these changes:
            
            Features ({len(features)} changes):
            {self._format_changes_for_ai(features)}
            
            Bug Fixes ({len(bugfixes)} changes):
            {self._format_changes_for_ai(bugfixes)}
            
            Other Changes ({len(other)} changes):
            {self._format_changes_for_ai(other)}
            
            Target audience: {target_audience}
            Format: Professional release notes with clear categories and bullet points.
            """
            
            release_notes = await self.openai_client.generate_completion(
                prompt=release_notes_prompt,
                max_tokens=1000
            )
            
            # Generate version recommendation
            version_prompt = f"Based on these {len(all_changes)} changes, suggest a semantic version increment (major, minor, or patch) and briefly explain why."
            version_suggestion = await self.openai_client.generate_completion(
                prompt=version_prompt,
                max_tokens=100
            )
            
            result = {
                "changelists_analyzed": len(all_changes),
                "categorization": {
                    "features": len(features),
                    "bugfixes": len(bugfixes), 
                    "other": len(other)
                },
                "release_notes": release_notes,
                "version_suggestion": version_suggestion,
                "target_audience": target_audience
            }
            
            log.info("Successfully generated release notes")
            return result
            
        except Exception as e:
            log.error(f"Failed to generate release notes: {e}")
            raise

    async def code_review_assistant(self, changelist_id: str, focus_areas: List[str] = None) -> Dict[str, Any]:
        """AI-powered code review assistant for Perforce changes."""
        try:
            log.info(f"Running code review analysis for changelist {changelist_id}")
            
            # Get changelist with file details
            changelist = await self.p4_client.get_changelist(changelist_id)
            if not changelist:
                raise ValueError(f"Changelist {changelist_id} not found")
            
            # Get file diffs (simplified - in real implementation would get actual diffs)
            files = changelist.get('files', [])
            description = changelist.get('description', '')
            
            # Default focus areas if none provided
            if not focus_areas:
                focus_areas = ['security', 'performance', 'maintainability', 'best_practices']
            
            # Analyze description for potential issues
            review_prompt = f"""
            Perform a code review analysis on this changelist:
            
            Description: {description}
            Files modified: {len(files)}
            File paths: {', '.join([f.get('file', '')[:100] for f in files[:10]])}
            
            Focus areas: {', '.join(focus_areas)}
            
            Provide:
            1. Potential concerns or red flags
            2. Questions to ask in code review
            3. Areas that need extra attention
            4. Suggestions for improvement
            
            Be specific and actionable.
            """
            
            review_analysis = await self.openai_client.generate_completion(
                prompt=review_prompt,
                max_tokens=800
            )
            
            # Generate risk assessment
            risk_prompt = f"Rate the risk level (low/medium/high) of this code change and explain: {description}"
            risk_assessment = await self.openai_client.generate_completion(
                prompt=risk_prompt,
                max_tokens=100
            )
            
            # Check for common patterns
            security_check = await self._check_security_patterns(description, files)
            
            result = {
                "changelist_id": changelist_id,
                "review_analysis": review_analysis,
                "risk_assessment": risk_assessment,
                "security_check": security_check,
                "focus_areas": focus_areas,
                "files_count": len(files),
                "recommendations": {
                    "requires_security_review": security_check['has_security_concerns'],
                    "requires_performance_review": any('performance' in fa for fa in focus_areas),
                    "complexity_score": "medium" if len(files) > 5 else "low"
                }
            }
            
            log.info(f"Completed code review analysis for changelist {changelist_id}")
            return result
            
        except Exception as e:
            log.error(f"Failed to perform code review analysis: {e}")
            raise

    async def smart_commit_message(self, files: List[str], diff_summary: str = "") -> Dict[str, Any]:
        """Generate AI-powered commit messages based on file changes."""
        try:
            log.info(f"Generating smart commit message for {len(files)} files")
            
            # Analyze file patterns
            file_types = {}
            for file_path in files:
                ext = file_path.split('.')[-1] if '.' in file_path else 'unknown'
                file_types[ext] = file_types.get(ext, 0) + 1
            
            # Generate commit message
            commit_prompt = f"""
            Generate a concise, conventional commit message based on these file changes:
            
            Files changed ({len(files)}):
            {', '.join(files[:20])}
            
            File types: {', '.join([f'{k}({v})' for k, v in file_types.items()])}
            
            {f'Change summary: {diff_summary}' if diff_summary else ''}
            
            Follow conventional commit format: type(scope): description
            Keep it under 72 characters.
            """
            
            commit_message = await self.openai_client.generate_completion(
                prompt=commit_prompt,
                max_tokens=100
            )
            
            # Generate extended description
            extended_prompt = f"Generate a more detailed commit description (2-3 lines) for: {commit_message.strip()}"
            extended_description = await self.openai_client.generate_completion(
                prompt=extended_prompt,
                max_tokens=200
            )
            
            result = {
                "files_analyzed": len(files),
                "file_types": file_types,
                "commit_message": commit_message.strip(),
                "extended_description": extended_description.strip(),
                "confidence": "high" if len(files) <= 10 else "medium"
            }
            
            log.info("Generated smart commit message")
            return result
            
        except Exception as e:
            log.error(f"Failed to generate commit message: {e}")
            raise

    async def _generate_recommendations(self, changelist: Dict[str, Any], summary: str, tags: List[str]) -> List[str]:
        """Generate recommendations based on changelist analysis."""
        recommendations = []
        
        files_count = len(changelist.get('files', []))
        description = changelist.get('description', '')
        
        # Size-based recommendations
        if files_count > 20:
            recommendations.append("Consider breaking this large changelist into smaller, focused changes")
        
        # Tag-based recommendations
        if 'security' in tags:
            recommendations.append("This change may need security review")
        
        if 'database' in tags or 'schema' in tags:
            recommendations.append("Database changes detected - ensure migration scripts are included")
        
        # Description-based recommendations
        if len(description) < 20:
            recommendations.append("Consider adding more detail to the changelist description")
        
        return recommendations

    async def _check_security_patterns(self, description: str, files: List[Dict]) -> Dict[str, Any]:
        """Check for security-related patterns in changes."""
        security_keywords = ['password', 'token', 'secret', 'auth', 'login', 'security', 'crypto']
        sensitive_files = ['config', '.env', 'secrets', 'keys']
        
        has_security_keywords = any(keyword in description.lower() for keyword in security_keywords)
        has_sensitive_files = any(
            any(sensitive in file.get('file', '').lower() for sensitive in sensitive_files)
            for file in files
        )
        
        return {
            "has_security_concerns": has_security_keywords or has_sensitive_files,
            "security_keywords_found": has_security_keywords,
            "sensitive_files_detected": has_sensitive_files,
            "recommendation": "Security review recommended" if (has_security_keywords or has_sensitive_files) else "No security concerns detected"
        }

    def _format_changes_for_ai(self, changes: List[Dict]) -> str:
        """Format changelist data for AI prompts."""
        formatted = []
        for change in changes[:10]:  # Limit to prevent token overflow
            cl_id = change.get('changelist', 'unknown')
            desc = change.get('description', '')[:200]  # Truncate long descriptions
            formatted.append(f"- {cl_id}: {desc}")
        return '\n'.join(formatted)

    async def health_check(self) -> Dict[str, Any]:
        """Check connectivity to both Perforce and OpenAI."""
        results = {}
        
        try:
            p4_health = await self.p4_client.health_check()
            results["perforce"] = p4_health
        except Exception as e:
            results["perforce"] = {"status": "error", "error": str(e)}
        
        try:
            openai_health = await self.openai_client.health_check()
            results["openai"] = openai_health
        except Exception as e:
            results["openai"] = {"status": "error", "error": str(e)}
        
        # Overall status
        all_ok = all(r.get("status") == "ok" for r in results.values())
        results["overall"] = "ok" if all_ok else "degraded"
        
        return results


# Convenience functions for common workflows
async def analyze_changelist_quick(changelist_id: str) -> Dict[str, Any]:
    """Quick function to analyze a changelist."""
    analyzer = AICodeAnalysis()
    return await analyzer.analyze_changelist(changelist_id)

async def generate_smart_commit_message(files: List[str], diff_summary: str = "") -> str:
    """Quick function to generate a commit message."""
    analyzer = AICodeAnalysis()
    result = await analyzer.smart_commit_message(files, diff_summary)
    return result.get('commit_message', '')