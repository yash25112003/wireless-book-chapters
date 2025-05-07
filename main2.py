# ==========================
# CONFIGURATION
# ==========================
BOOK_FOLDER_NAME = "FUTURE INTELLIGENT WIRELESS ECOSYSTEM"
CHAPTER_TITLE = "THE FUTURE INTELLIGENT WIRELESS ECOSYSTEM"
MAX_CHAPTERS = 22
CONTENT_POINTS = [
    # Foundation points from Chapter 2 (expanded with technical details)
    "AI-Native 6G Networks with Self-Optimizing capabilities",
    "Terahertz (THz) spectrum utilization (0.1-10 THz)",
    "Quantum-AI synergy for network optimization",
    "Unified terrestrial-satellite-aerial networks (LEO/MEO/GEO)",
    "Peak data rates of 1 Tbps with sub-0.1ms latency",
    "Edge Intelligence for decentralized real-time processing",
    "Fog Computing vs Pure Edge trade-offs (3.2ms vs 7.8ms latency)",
    "75% of enterprise data processed at edge by 2025",
    "Healthcare edge processing (4.3s diagnostic imaging)",
    "AI-Driven Network Automation & Zero-Touch Management",
    "Reinforcement Learning (73% better novel scenario adaptation)",
    "Rule-based systems (91% regulatory compliance)",
    "Dynamic Network Slicing for Industry 5.0",
    "URLLC for factories (99.99999% reliability)",
    "eMBB for video, mMTC for sensor networks",
    "35-40% operational cost reduction",
    "Massive IoT Ecosystems scaling to billions of devices",
    "Projected 75B+ IoT connections by 2025",
    "AI-optimized IoT power consumption (4x reduction)",
    "Digital Twins for cyber-physical synchronization",
    "High-fidelity physics models (92% accuracy)",
    "Statistical twins (85% accuracy, 4.5x less compute)",
    "78% reduction in network outages",
    "Advanced Spectrum Utilization with Cognitive Radio & THz",
    "Cognitive Radio Networks (200-300% spectrum efficiency)",
    "THz demonstrations: 100 Gbps lab, 47 Gbps urban",
    "AI beam steering (42% THz signal loss reduction)",
    "Enhanced Human-Machine Collaboration & Tactile Internet",
    "Tactile feedback for remote surgery (projected $12.6B market)",
    "Industry 5.0 cobots for human augmentation",
    "Proactive Cybersecurity & Federated Learning for Privacy",
    "Federated Learning (70-83% less data transfer)",
    "92% zero-day attack detection rate",
    "Quantum-Enhanced Security & Computation",
    "Quantum Key Distribution (10-20 Mbps metro rates)",
    "Quantum-secure AI protocols by 2035",
    "Sustainable & Energy-Efficient Wireless Ecosystems",
    "AI-optimized base stations (25-35% energy savings)",
    "RF energy harvesting (0.1 μW/cm² for IoT)",
    "Blockchain for e-waste tracking (53M metric tons)",
    "Ethical AI Governance & Bio-Inspired Network Resilience",
    "Explainable AI (XAI) for transparency",
    "Ant colony optimization (37% traffic reduction)",
    "Bio-inspired algorithms (63% attack resilience)"
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
    model_name="gemma2-9b-it",
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
    # Foundation chapters (expanded with technical sub-points)
    chapters = {
        1: {
            "title": "AI-Native 6G Networks", 
            "points": [
                CONTENT_POINTS[0],  # AI-Native 6G
                CONTENT_POINTS[1],  # THz spectrum
                CONTENT_POINTS[2],  # Quantum-AI
                CONTENT_POINTS[3],  # Unified networks
                CONTENT_POINTS[4]   # 1 Tbps
            ],
            "type": "foundation"
        },
        2: {
            "title": "Edge Intelligence", 
            "points": [
                CONTENT_POINTS[5],  # Edge processing
                CONTENT_POINTS[6],  # Fog vs Edge
                CONTENT_POINTS[7],  # 75% at edge
                CONTENT_POINTS[8]   # Healthcare example
            ],
            "type": "foundation"
        },
        3: {
            "title": "Network Automation & Management", 
            "points": [
                CONTENT_POINTS[9],  # ZSM
                CONTENT_POINTS[10], # RL
                CONTENT_POINTS[11]  # Rule-based
            ],
            "type": "foundation"
        },
        4: {
            "title": "Dynamic Network Slicing", 
            "points": [
                CONTENT_POINTS[12], # Slicing concept
                CONTENT_POINTS[13], # URLLC
                CONTENT_POINTS[14], # eMBB/mMTC
                CONTENT_POINTS[15]  # Cost reduction
            ],
            "type": "foundation"
        },
        5: {
            "title": "Massive IoT Ecosystems", 
            "points": [
                CONTENT_POINTS[16], # IoT scaling
                CONTENT_POINTS[17], # 75B+ devices
                CONTENT_POINTS[18]  # Power optimization
            ],
            "type": "foundation"
        },
        # Generation evolution chapters (unchanged)
        6: {"title": "3G: Mobile Broadband Revolution", "points": [], "type": "evolution"},
        7: {"title": "4G: The App Economy Era", "points": [], "type": "evolution"},
        8: {"title": "4G LTE: Digital Lifestyle", "points": [], "type": "evolution"},
        9: {"title": "5G: Industry Transformation", "points": [], "type": "evolution"},
        10: {"title": "5G Advanced: Network Slicing", "points": [], "type": "evolution"},
        11: {
            "title": "Beyond 5G: Internet of Beings", 
            "points": [
                CONTENT_POINTS[27],  # Enhanced Human-Machine Collaboration
                CONTENT_POINTS[28],  # Tactile feedback for remote surgery
                CONTENT_POINTS[29]   # Industry 5.0 cobots
            ], 
            "type": "evolution"
        },
        12: {"title": "6G: Internet of Everything", "points": [], "type": "evolution"},
        # Thematic chapters (now fully populated)
        13: {
            "title": "Spectrum Management Challenges",
            "points": [
                CONTENT_POINTS[23], # Cognitive Radio
                CONTENT_POINTS[24], # THz demonstrations
                CONTENT_POINTS[25]  # AI beam steering
            ],
            "type": "theme"
        },
        14: {"title": "Network Economics", "points": [], "type": "theme"},
        15: {
            "title": "Edge Computing Revolution",
            "points": [
                CONTENT_POINTS[19], # Digital Twins
                CONTENT_POINTS[20], # Physics models
                CONTENT_POINTS[21], # Statistical twins
                CONTENT_POINTS[22]  # Outage reduction
            ],
            "type": "theme"
        },
        16: {"title": "Open RAN Disruption", "points": [], "type": "theme"},
        17: {
            "title": "Satellite Integration",
            "points": [
                CONTENT_POINTS[3]   # Unified networks (reference only)
            ],
            "type": "theme"
        },
        18: {
            "title": "AI in Wireless Networks",
            "points": [
                CONTENT_POINTS[30],  # Proactive Cybersecurity
                CONTENT_POINTS[31],  # Federated Learning
                CONTENT_POINTS[32],  # 92% zero-day attack detection
                CONTENT_POINTS[39],  # Ethical AI Governance
                CONTENT_POINTS[40]   # XAI
            ],
            "type": "theme"
        },
        19: {
            "title": "Quantum-Secure Communications",
            "points": [
                CONTENT_POINTS[33], # Quantum-Enhanced Security
                CONTENT_POINTS[34], # QKD
                CONTENT_POINTS[35]  # Quantum-secure AI protocols
            ],
            "type": "theme"
        },
        20: {
            "title": "Sustainable Wireless Future",
            "points": [
                CONTENT_POINTS[36],  # Sustainable & Energy-Efficient
                CONTENT_POINTS[37],  # AI-optimized base stations
                CONTENT_POINTS[38],  # RF energy harvesting
                CONTENT_POINTS[39],  # Blockchain for e-waste
                CONTENT_POINTS[41],  # Ant colony optimization
                CONTENT_POINTS[42]   # Bio-inspired algorithms
            ],
            "type": "theme"
        },
        21: {"title": "Global Connectivity Impact", "points": [], "type": "theme"},
        22: {"title": "2080: The Wireless Horizon", "points": [], "type": "future"}
    }

    # No need for additional content mapping as all points are now directly assigned
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
