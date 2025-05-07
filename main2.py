# ==========================
# CONFIGURATION
# ==========================
BOOK_FOLDER_NAME = "FUTURE INTELLIGENT WIRELESS ECOSYSTEM"
CHAPTER_TITLE = "THE FUTURE INTELLIGENT WIRELESS ECOSYSTEM"
MAX_CHAPTERS = 22
CONTENT_POINTS = [
    # Points from "CHAPTER 2: FUTURE INTELLIGENT WIRELESS ECOSYSTEM"
    "AI-Native 6G Networks with Self-Optimizing capabilities",  # 0
    "Terahertz (THz) spectrum utilization (0.1-10 THz)",  # 1
    "Quantum-AI synergy for network optimization",  # 2
    "Unified terrestrial-satellite-aerial networks (LEO/MEO/GEO)",  # 3
    "Peak data rates of 1 Tbps with sub-0.1ms latency",  # 4
    "Edge Intelligence for decentralized real-time processing",  # 5
    "Fog Computing vs Pure Edge trade-offs (3.2ms vs 7.8ms latency)",  # 6
    "75% of enterprise data processed at edge by 2025",  # 7
    "Healthcare edge processing (4.3s diagnostic imaging)",  # 8
    "AI-Driven Network Automation & Zero-Touch Management",  # 9
    "Reinforcement Learning (73% better novel scenario adaptation)",  # 10
    "Rule-based systems (91% regulatory compliance)",  # 11
    "Dynamic Network Slicing for Industry 5.0",  # 12
    "URLLC for factories (99.99999% reliability)",  # 13
    "eMBB for video, mMTC for sensor networks",  # 14
    "35-40% operational cost reduction",  # 15
    "Massive IoT Ecosystems scaling to billions of devices",  # 16
    "Projected 75B+ IoT connections by 2025",  # 17
    "AI-optimized IoT power consumption (4x reduction)",  # 18
    "Digital Twins for cyber-physical synchronization",  # 19
    "High-fidelity physics models (92% accuracy)",  # 20
    "Statistical twins (85% accuracy, 4.5x less compute)",  # 21
    "78% reduction in network outages",  # 22
    "Advanced Spectrum Utilization with Cognitive Radio & THz",  # 23 (General heading for spectrum)
    "Cognitive Radio Networks (200-300% spectrum efficiency)",  # 24
    "THz demonstrations: 100 Gbps lab, 47 Gbps urban",  # 25
    "AI beam steering (42% THz signal loss reduction)",  # 26
    "Enhanced Human-Machine Collaboration & Tactile Internet",  # 27
    "Tactile feedback for remote surgery (projected $12.6B market)",  # 28
    "Industry 5.0 cobots for human augmentation",  # 29
    "Proactive Cybersecurity & Federated Learning for Privacy",  # 30 (General heading for security aspects)
    "Federated Learning (70-83% less data transfer)",  # 31
    "92% zero-day attack detection rate",  # 32
    "Quantum-Enhanced Security & Computation",  # 33 (General heading for quantum)
    "Quantum Key Distribution (10-20 Mbps metro rates)",  # 34
    "Quantum-secure AI protocols by 2035",  # 35
    "Sustainable & Energy-Efficient Wireless Ecosystems",  # 36 (General heading for sustainability)
    "AI-optimized base stations (25-35% energy savings)",  # 37
    "RF energy harvesting (0.1 μW/cm² for IoT)",  # 38
    "Blockchain for e-waste tracking (53M metric tons)",  # 39
    "Ethical AI Governance & Bio-Inspired Network Resilience",  # 40 (General heading for ethics/bio-inspired)
    "Explainable AI (XAI) for transparency",  # 41
    "Ant colony optimization (37% traffic reduction)",  # 42
    "Bio-inspired algorithms (63% attack resilience)" # 43 (Added as per reasoning in thought block)
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
    chapters = {
        # Part 1: Foundational Technologies (Type: foundation)
        1: {
            "title": "AI-Native 6G: Core Principles and Performance Targets",
            "points": [CONTENT_POINTS[0], CONTENT_POINTS[4]],
            "type": "foundation"
        },
        2: {
            "title": "Next-Generation Spectrum: Terahertz (THz) Potentials and Challenges",
            "points": [CONTENT_POINTS[1], CONTENT_POINTS[25], CONTENT_POINTS[26]],
            "type": "foundation"
        },
        3: {
            "title": "Edge Intelligence: Decentralized Processing for Real-Time Applications",
            "points": [CONTENT_POINTS[5], CONTENT_POINTS[7], CONTENT_POINTS[8]],
            "type": "foundation"
        },
        4: {
            "title": "Automating the Future: AI-Driven Network Management and Zero-Touch Operations",
            "points": [CONTENT_POINTS[9], CONTENT_POINTS[10], CONTENT_POINTS[11]],
            "type": "foundation"
        },
        5: {
            "title": "Connecting Billions: Scaling Massive IoT Ecosystems with AI",
            "points": [CONTENT_POINTS[16], CONTENT_POINTS[17], CONTENT_POINTS[18]],
            "type": "foundation"
        },
        # Part 2: Architectural Innovations and Service Evolution (Type: evolution)
        6: {
            "title": "Unified Connectivity: Integrating Terrestrial, Satellite, and Aerial Networks",
            "points": [CONTENT_POINTS[3]],
            "type": "evolution"
        },
        7: {
            "title": "Architectural Choices: Fog Computing versus Pure Edge Intelligence",
            "points": [CONTENT_POINTS[6]],
            "type": "evolution"
        },
        8: {
            "title": "Dynamic Network Slicing: Customizing Services for Industry 5.0 and Beyond",
            "points": [CONTENT_POINTS[12], CONTENT_POINTS[13], CONTENT_POINTS[14], CONTENT_POINTS[15]],
            "type": "evolution"
        },
        9: {
            "title": "Digital Twins: Bridging Physical and Virtual Worlds for Network Optimization",
            "points": [CONTENT_POINTS[19], CONTENT_POINTS[20], CONTENT_POINTS[21], CONTENT_POINTS[22]],
            "type": "evolution"
        },
        10: {
            "title": "The Tactile Internet: Enabling Enhanced Human-Machine Collaboration",
            "points": [CONTENT_POINTS[27], CONTENT_POINTS[28]],
            "type": "evolution"
        },
        11: {
            "title": "Industry 5.0 Realized: Human Augmentation with Collaborative Robots (Cobots)",
            "points": [CONTENT_POINTS[29]], # Focus on cobots aspect of HMC
            "type": "evolution"
        },
        # Part 3: Advanced Concepts and Societal Impact (Type: theme)
        12: {
            "title": "Cognitive Radio Networks: Intelligent Dynamic Spectrum Access",
            "points": [[CONTENT_POINTS[23], CONTENT_POINTS[24]], # CONTENT_POINTS[23] is a general heading for spectrum
            "type": "theme"
        },
        13: {
            "title": "The Quantum-AI Synergy: Optimizing Future Network Performance and Design",
            "points": [CONTENT_POINTS[2]],
            "type": "theme"
        },
        14: {
            "title": "Securing the Quantum Age: Principles of Quantum Key Distribution (QKD)",
            "points": [CONTENT_POINTS[33], CONTENT_POINTS[34]], # CP33 for context
            "type": "theme"
        },
        15: {
            "title": "Privacy-Preserving AI: The Role of Federated Learning in Wireless Networks",
            "points": [CONTENT_POINTS[30], CONTENT_POINTS[31]], # CP30 for context
            "type": "theme"
        },
        16: {
            "title": "AI for Proactive Cybersecurity: Strategies for Detecting Zero-Day Attacks",
            "points": [CONTENT_POINTS[32]], # CP30 context is covered by previous chapter
            "type": "theme"
        },
        17: {
            "title": "Building Sustainable Wireless Ecosystems: AI for Energy Efficiency",
            "points": [CONTENT_POINTS[36], CONTENT_POINTS[37]], # CP36 for context
            "type": "theme"
        },
        18: {
            "title": "Innovations in Wireless Energy: RF Harvesting for Self-Sustaining IoT Devices",
            "points": [CONTENT_POINTS[38]],
            "type": "theme"
        },
        19: {
            "title": "Towards a Circular Economy in Tech: Blockchain for E-Waste Tracking and Management",
            "points": [CONTENT_POINTS[39]],
            "type": "theme"
        },
        20: {
            "title": "Governing Intelligent Systems: Ethical AI and the Imperative of Explainable AI (XAI)",
            "points": [CONTENT_POINTS[40], CONTENT_POINTS[41]], # CP40 for context
            "type": "theme"
        },
        21: {
            "title": "Bio-Inspired Networking: Enhancing Resilience and Efficiency Through Nature's Designs",
            "points": [CONTENT_POINTS[42], CONTENT_POINTS[43]], # CP40 context covered by previous chapter
            "type": "theme"
        },
        # Part 4: Future Outlook (Type: future)
        22: {
            "title": "The Path to 2035 and Beyond: Realizing Quantum-Secure AI Protocols and the Future Wireless Horizon",
            "points": [CONTENT_POINTS[35]],
            "type": "future"
        }
    }
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
