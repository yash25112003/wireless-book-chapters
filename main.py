# ==========================
# CONFIGURATION
# ==========================
BOOK_FOLDER_NAME = "Evolution_of_Wireless_Technology"
CHAPTER_TITLE = "The Evolution of Wireless Technology"
MAX_CHAPTERS = 22
CONTENT_POINTS = [
    # Foundation (Auto-generated)
    "1G: Analog cellular beginnings",
    "2G: Digital voice and SMS revolution",
    
    # User-specified points
    "3G inaugurates Mobile Broadband Service",
    "4G cements Mobile Internet Economy",
    "Multimedia apps popularity surge (2010s)",
    "New wave of apps creating millions of jobs",
    "Mobile Apps' critical COVID-19 role",
    "Mobile economy projected $4.8tn by 2023",
    "Employment: 14M direct, 17M indirect jobs",
    "50% global population as mobile subscribers",
    "5G enabling cross-industry services",
    "5G driving Industry 4.0 revolution",
    "Beyond 5G enabling Internet of Beings",
    "6G initiating Internet of Everything",
    "Spectrum allocation challenges",
    "Network slicing economics",
    "Edge computing business models",
    "Open RAN market disruption",
    "Satellite-terrestrial integration",
    "AI-driven network optimization",
    "Quantum-secure communications",
    "Sustainable wireless infrastructure"
]

# ==========================
# IMPORTS & SETUP
# ==========================
import os
import re
import base64
import requests
import traceback
import time
from github import Github, GithubException
from crewai import Agent, Task, Crew
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv() 

# ================
# LLM Setup
# ================
llm = ChatGroq(
    temperature=0,
    model_name="groq/gemma2-9b-it",
    api_key=os.getenv('GROQ_API_KEY'),
)

# ================
# GitHub Config
# ================
GITHUB_TOKEN = os.getenv('G_TOKEN')
GITHUB_USERNAME = "yash25112003"
REPO_OWNER = "yash25112003"
REPO_NAME = "wireless-book-chapters"
REPO_FULL_NAME = f"{REPO_OWNER}/{REPO_NAME}"
BRANCH = "main"
BASE_URL = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents"

# ==========================
# AGENT DEFINITIONS (OPTIMIZED)
# ==========================
planning_agent = Agent(
    llm=llm,
    role="Wireless Technology Historian & Strategist",
    goal="Develop a structured chapter outline tracing the evolution of wireless technology, emphasizing key historical breakthroughs, technical advancements, and societal impact.",
    backstory="Veteran researcher specializing in wireless communication history with extensive knowledge of ITU, 3GPP, and IEEE standards.",
    allow_delegation=False,
    verbose=True
)

writing_agent = Agent(
    llm=llm,
    role="Wireless Technology Analyst & Technical Writer",
    goal="Create engaging, well-researched chapters in continuous paragraph form (no bullet points/lists).",
    backstory="Telecom expert specializing in converting technical concepts into narrative prose.",
    allow_delegation=False,
    verbose=True
)

editing_agent = Agent(
    llm=llm,
    role="Paragraph Formatting Specialist",
    goal="Ensure seamless transitions between ideas and generations.",
    backstory="Technical editor trained in transforming outlines into publishable prose.",
    allow_delegation=False,
    verbose=True
)

fact_checking_agent = Agent(
    llm=llm,
    role="Wireless Technology & AI Validation Expert",
    goal="Validate claims against IEEE/3GPP/ITU standards.",
    backstory="Researcher specializing in network protocols and wireless infrastructure.",
    allow_delegation=False,
    verbose=True
)

publishing_agent = Agent(
    llm=llm,
    role="Publishing Specialist for Technical Literature",
    goal="Ensure professional formatting and citations.",
    backstory="Expert in technical publishing standards.",
    allow_delegation=False,
    verbose=True
)

# ============================
# TASK DEFINITIONS (OPTIMIZED)
# ============================
plan_book_task = Task(
    description="Develop comprehensive chapter outline from 1G to 6G+ technologies.",
    agent=planning_agent,
    expected_output="Structured outline with historical context and technical milestones."
)

chapter_task = Task(
    description="Write chapter content in continuous paragraphs about wireless evolution.",
    agent=writing_agent,
    expected_output="500-550 word narrative draft without bullet points."
)

edit_prose_task = Task(
    description="Convert any list-like structures into flowing paragraphs.",
    agent=editing_agent,
    expected_output="Fully paragraph-formatted text."
)

fact_check_task = Task(
    description="Verify technical claims against authoritative sources.",
    agent=fact_checking_agent,
    expected_output="Fact-checked chapter with citations."
)

format_markdown_task = Task(
    description="Apply publishing-grade formatting.",
    agent=publishing_agent,
    expected_output="Publication-ready Markdown."
)

# ============================
# GITHUB HELPER FUNCTIONS
# ============================
def ensure_folder_exists(repo, folder_path):
    """Ensure a folder exists in the repo, create if not."""
    try:
        # Check if the folder path itself exists as content (this works for non-empty folders)
        repo.get_contents(folder_path, ref=BRANCH)
        print(f"Folder '{folder_path}' already exists.")
    except GithubException as e:
        if e.status == 404:
            # Folder doesn't exist, create a .gitkeep file to initialize it
            print(f"Folder '{folder_path}' not found. Creating...")
            repo.create_file(
                f"{folder_path}/.gitkeep",
                "Create folder",
                "", # Empty content for .gitkeep
                branch=BRANCH
            )
            print(f"Folder '{folder_path}' created successfully.")
        else:
            # Re-raise other GitHub related errors
            raise
    except Exception as e:
        # Re-raise other unexpected errors
        raise

def get_existing_chapters(repo, folder_path):
    """Get sorted chapter files using the provided repo object."""
    try:
        contents = repo.get_contents(folder_path, ref=BRANCH)
        # Filter out non-chapter files/folders like .gitkeep if present
        return sorted(
            [f.name for f in contents if f.type == 'file' and f.name.startswith("chapter") and f.name.endswith(".md")],
            key=lambda x: int(re.search(r"chapter(\d+).md", x).group(1))
        )
    except GithubException as e:
        if e.status == 404: # Folder might not exist yet or is empty
             print(f"No contents found in '{folder_path}', likely doesn't exist or is empty.")
             return []
        else:
            print(f"Error accessing folder contents in '{folder_path}': {e}")
            raise # Re-raise the exception to be caught higher up
    except Exception as e:
        print(f"Unexpected error listing chapters in '{folder_path}': {e}")
        raise # Re-raise

def get_chapter_context(repo, folder_path, chapter_files):
    """Get context using the provided repo object."""
    context = []
    # Get context from the last 3 chapters if they exist
    chapters_to_fetch = chapter_files[-3:]
    print(f"Fetching context from chapters: {chapters_to_fetch}")
    for fname in chapters_to_fetch:
        file_path = f"{folder_path}/{fname}"
        try:
            content_file = repo.get_contents(file_path, ref=BRANCH)
            # Limit context size per chapter if needed
            context.append(content_file.decoded_content.decode("utf-8")[:600])
            print(f"Successfully fetched context from {fname}")
        except GithubException as e:
            print(f"⚠️ Warning: Could not fetch context from {file_path}: {e.status} - {e.data}")
            continue # Skip this file if there's an error
        except Exception as e:
            print(f"⚠️ Warning: Unexpected error fetching context from {file_path}: {str(e)}")
            continue # Skip this file
            
    return "\n\nCONTEXT:\n" + "\n---\n".join(context) if context else ""

def github_commit(repo, file_content, filename, commit_message):
    """
    Commit a file to GitHub using the provided repo object.
    
    Args:
        repo: Authenticated GitHub repository object
        file_content: Content to commit (str or bytes)
        filename: Path to file in repository
        commit_message: Commit message
        
    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        # Ensure content is properly encoded as string
        if isinstance(file_content, bytes):
            try:
                file_content = file_content.decode('utf-8')
            except UnicodeDecodeError:
                return False, "Content could not be decoded as UTF-8"
        elif not isinstance(file_content, str):
            file_content = str(file_content)

        # Verify filename is valid
        if not filename or any(c in filename for c in '\0\\:'):
            return False, f"Invalid filename: {filename}"

        try:
            # Try to get existing file
            contents = repo.get_contents(filename, ref=BRANCH)
            # Update existing file
            repo.update_file(
                path=contents.path,
                message=commit_message,
                content=file_content,
                sha=contents.sha,
                branch=BRANCH
            )
            return True, f"Updated '{filename}' successfully"

        except GithubException as e:
            if e.status == 404:
                # File doesn't exist - create new
                try:
                    repo.create_file(
                        path=filename,
                        message=commit_message,
                        content=file_content,
                        branch=BRANCH
                    )
                    return True, f"Created '{filename}' successfully"
                except GithubException as create_e:
                    return False, f"Create failed: {create_e.status} - {create_e.data}"
            else:
                return False, f"GitHub error: {e.status} - {e.data}"

    except Exception as e:
        error_msg = f"Unexpected error committing '{filename}': {str(e)}"
        import traceback
        traceback.print_exc()
        return False, error_msg

# ============================
# CONTENT DISTRIBUTION SYSTEM
# ============================
def build_chapter_plan():
    # Foundation chapters (first 5 chapters)
    chapters = {
        1: {"title": "The Analog Foundation: 1G Systems", "points": [CONTENT_POINTS[0]], "type": "foundation"},
        2: {"title": "Digital Revolution: 2G and GSM", "points": [CONTENT_POINTS[1]], "type": "foundation"},
        3: {"title": "Transition to Data: 2.5G-3G", "points": [], "type": "foundation"},
        4: {"title": "Standardization and Regulation", "points": [], "type": "foundation"},
        5: {"title": "The Business of Wireless", "points": [], "type": "foundation"}
    }

    # Generation-specific chapters
    generation_chapters = {
        6: {"title": "3G: Mobile Broadband Revolution", "points": [], "type": "evolution"},
        7: {"title": "4G: The App Economy Era", "points": [], "type": "evolution"},
        8: {"title": "4G LTE: Digital Lifestyle", "points": [], "type": "evolution"},
        9: {"title": "5G: Industry Transformation", "points": [], "type": "evolution"},
        10: {"title": "5G Advanced: Network Slicing", "points": [], "type": "evolution"},
        11: {"title": "Beyond 5G: Internet of Beings", "points": [], "type": "evolution"},
        12: {"title": "6G: Internet of Everything", "points": [], "type": "evolution"}
    }
    chapters.update(generation_chapters)

    # Thematic chapters
    thematic_chapters = {
        13: {"title": "Spectrum Management Challenges", "points": [], "type": "theme"},
        14: {"title": "Network Economics", "points": [], "type": "theme"},
        15: {"title": "Edge Computing Revolution", "points": [], "type": "theme"},
        16: {"title": "Open RAN Disruption", "points": [], "type": "theme"},
        17: {"title": "Satellite Integration", "points": [], "type": "theme"},
        18: {"title": "AI in Wireless Networks", "points": [], "type": "theme"},
        19: {"title": "Quantum-Secure Communications", "points": [], "type": "theme"},
        20: {"title": "Sustainable Wireless Future", "points": [], "type": "theme"},
        21: {"title": "Global Connectivity Impact", "points": [], "type": "theme"},
        22: {"title": "2080: The Wireless Horizon", "points": [], "type": "future"}
    }
    chapters.update(thematic_chapters)

    # Content point mapping - explicit assignments
    content_mapping = {
        "3G inaugurates Mobile Broadband Service": [6],
        "4G cements Mobile Internet Economy": [7],
        "Multimedia apps popularity surge (2010s)": [7,8],
        "New wave of apps creating millions of jobs": [7],
        "Mobile Apps' critical COVID-19 role": [7],
        "Mobile economy projected $4.8tn by 2023": [21],
        "Employment: 14M direct, 17M indirect jobs": [21],
        "50% global population as mobile subscribers": [21],
        "5G enabling cross-industry services": [9],
        "5G driving Industry 4.0 revolution": [9],
        "Beyond 5G enabling Internet of Beings": [11],
        "6G initiating Internet of Everything": [12],
        "Spectrum allocation challenges": [13],
        "Network slicing economics": [10,14],
        "Edge computing business models": [15],
        "Open RAN market disruption": [16],
        "Satellite-terrestrial integration": [17],
        "AI-driven network optimization": [18],
        "Quantum-secure communications": [19],
        "Sustainable wireless infrastructure": [20]
    }

    # Assign points based on mapping
    for point, chapter_ids in content_mapping.items():
        for chap_id in chapter_ids:
            if chap_id in chapters:
                chapters[chap_id]["points"].append(point)

    return chapters

def validate_chapter_plan(plan):
    distributed_points = sum(len(ch['points']) for ch in plan.values())
    if distributed_points < len(CONTENT_POINTS):
        missing = set(CONTENT_POINTS) - set(p for ch in plan.values() for p in ch['points'])
        raise ValueError(f"Missing content points: {missing}")

# ============================
# EXECUTION WORKFLOW (OPTIMIZED)
# ============================
def main():
    """Generate one new chapter per execution, resuming from last created chapter."""
    g = None
    repo = None
    try:
        # Initialize GitHub connection
        try:
            g = Github(GITHUB_TOKEN)
            user = g.get_user() # Test authentication
            print(f"✅ GitHub authenticated as: {user.login}")
        except GithubException as e:
            print(f"❌ GitHub authentication error: {e.status} - {e.data}")
            print("💡 Tip: Check your GitHub token and ensure it has appropriate permissions (repo scope).")
            return
        except Exception as e:
            print(f"❌ GitHub connection error: {str(e)}")
            print("💡 Tip: Check your network connection and GitHub API status.")
            return

        # Get repository
        try:
            repo = g.get_repo(REPO_FULL_NAME)
            print(f"✅ Successfully connected to repository: {REPO_FULL_NAME}")
        except GithubException as e:
            print(f"❌ Repository access error: {e.status} - {e.data}")
            print(f"💡 Tip: Ensure the repository '{REPO_FULL_NAME}' exists and your token has access.")
            return
        except Exception as e:
            print(f"❌ Repository connection error: {str(e)}")
            return

        # Ensure book folder exists
        try:
            # Pass the fetched repo object to the function
            ensure_folder_exists(repo, BOOK_FOLDER_NAME)
            print(f"✅ Book folder '{BOOK_FOLDER_NAME}' verified/created.")
        except GithubException as e:
            print(f"❌ Folder creation/verification error: {e.status} - {e.data}")
            print(f"💡 Tip: Check if token has write permissions to '{REPO_FULL_NAME}'.")
            return
        except Exception as e:
            print(f"❌ Folder handling error: {str(e)}")
            return

        # Get existing chapters and determine next chapter number
        try:
            # Pass the fetched repo object to the function
            existing_chapters = get_existing_chapters(repo, BOOK_FOLDER_NAME)
            next_chapter_num = len(existing_chapters) + 1
            print(f"✅ Found {len(existing_chapters)} existing chapters: {existing_chapters}")
        except GithubException as e:
            print(f"❌ Chapter listing error: {e.status} - {e.data}")
            return
        except Exception as e:
            print(f"❌ Chapter listing failed: {str(e)}")
            return

        # Check if book is complete
        if next_chapter_num > MAX_CHAPTERS:
            print(f"📘 Book complete! All {MAX_CHAPTERS} chapters exist in '{BOOK_FOLDER_NAME}'.")
            return

        print(f"▶️ Preparing to generate Chapter {next_chapter_num}")

        # Build and validate chapter plan
        try:
            chapter_plan = build_chapter_plan()
            validate_chapter_plan(chapter_plan)
            print("✅ Chapter plan validated")
        except ValueError as e:
            print(f"❌ Chapter plan validation failed: {str(e)}")
            return
        except Exception as e:
            print(f"❌ Chapter planning error: {str(e)}")
            return

        # Get current chapter details
        try:
            current_chapter = chapter_plan[next_chapter_num]
            print(f"✅ Current chapter details loaded: '{current_chapter['title']}'")
        except KeyError:
            print(f"❌ Chapter {next_chapter_num} not found in plan")
            return
        except Exception as e:
            print(f"❌ Chapter detail error: {str(e)}")
            return

        # Get context from previous chapters
        context = ""
        try:
            # Get context from last 3 chapters
            context = get_chapter_context(repo, BOOK_FOLDER_NAME, existing_chapters[-3:])
            if context:
                print("✅ Previous chapter context loaded.")
            else:
                print("ℹ️ No previous chapters found or context is empty.")
        except Exception as e:
            # Non-critical error, proceed without context
            print(f"⚠️ Context loading error: {str(e)}. Proceeding without context.")
            context = "" # Ensure context is empty string on error

        print(f"⏳ Generating Chapter {next_chapter_num}: {current_chapter['title']}")

        # Configure the writing task dynamically
        chapter_task.description = f"""Compose Chapter {next_chapter_num}: {current_chapter['title']}
Key Points: {current_chapter.get('points', 'Wireless technology evolution')}
Historical Context: {context if context else 'First chapter of the book'}"""

        # Execute the crew
        result = None
        try:
            crew = Crew(
                agents=[writing_agent, fact_checking_agent, editing_agent, publishing_agent],
                tasks=[chapter_task, fact_check_task, edit_prose_task, format_markdown_task],
                verbose=True
            )
            result = crew.kickoff()
            if not result:
                raise ValueError("Content generation returned empty result.")
            print("✅ Chapter content generated successfully")
        except Exception as e:
            print(f"❌ Content generation error: {str(e)}")
            return # Stop if generation fails

        # Commit to GitHub with verification
        commit_success = False
        try:
            commit_filename = f"{BOOK_FOLDER_NAME}/chapter{next_chapter_num}.md"
            commit_message = f"Added Chapter {next_chapter_num}: {current_chapter['title']}"
            # Pass the repo object to the corrected github_commit function
            commit_success = github_commit(repo, result, commit_filename, commit_message)

            if commit_success:
                print(f"✅ Successfully committed Chapter {next_chapter_num} to GitHub.")
                print(f"📊 Progress: {next_chapter_num}/{MAX_CHAPTERS} chapters completed.")
            else:
                # The github_commit function now returns False on failure and prints details
                print(f"⚠️ Chapter {next_chapter_num} generated but GitHub commit failed. Check logs above for details.")

        except Exception as e:
            # Catch unexpected errors during the commit call itself (less likely now)
            print(f"❌ Unexpected error during commit process: {str(e)}")
            traceback.print_exc()
            print("💡 Generated content was not saved to GitHub.")

    except Exception as e:
        # Catch-all for critical failures in main setup
        print(f"❌ Critical failure in main execution: {str(e)}")
        print("💡 Tip: Check global configurations (token, repo name), network, and traceback.")
        traceback.print_exc()

if __name__ == "__main__":
    main()
