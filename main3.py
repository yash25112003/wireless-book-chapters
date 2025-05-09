# ==========================
# CONFIGURATION
# ==========================
BOOK_FOLDER_NAME = "BEYOND 5G REVOLUTIONARY TECHNOLOGIES"
CHAPTER_TITLE = "BEYOND 5G REVOLUTIONARY TECHNOLOGIES"
MAX_CHAPTERS = 22

REFERENCE_FOLDER = "FUTURE INTELLIGENT WIRELESS ECOSYSTEM"

CONTENT_POINTS_CH3 = [
    # 1. Terahertz (THz) Communications
    "Operates in 0.1–10 THz, offering 100+ GHz contiguous bandwidth (vs. 5G’s fragmented mmWave)",  # 0
    "Challenges: Severe path loss (~10–30 dB worse than mmWave), molecular absorption (H₂O/O₂ resonance peaks), and blockages",  # 1
    "Requires ultra-massive MIMO (1024+ elements) and photonic-plasmonic hybrid transceivers for THz",  # 2
    "Lab Results: THz achieving 1 Tbps over 1–10 m (NTT DoCoMo, 2024); 150 Gbps at 20m using adaptive beamforming",  # 3
    "Favorable THz Transmission Windows: 275–300 GHz and 500–600 GHz bands show 37–45% lower attenuation",  # 4
    "THz semiconductor market projected to hit $41B by 2032 (51.7% patents from Asia)",  # 5
    "THz Vision: Instant holographic communications, wireless data centers, and nanoscale IoT (sub-1mm devices)",  # 6
    # 2. AI-Native 6G
    "AI/ML is native to PHY/MAC layers in 6G, not just an add-on to the network",  # 7
    "AI-driven approaches replace traditional DSP blocks (e.g., AI channel coding, AI beam prediction)",  # 8
    "Explainable AI (XAI) ensures trust and reliability for critical 6G services (e.g., remote surgery, autonomous vehicles)",  # 9
    "AI-native 6G demonstrates 35–50% spectral efficiency gain (Chen et al., 2022) via real-time waveform adaptation",  # 10
    "AI-native 6G achieves 40% latency reduction in control loops (e.g., for factory robots)",  # 11
    "AI-Native Vision: Self-evolving networks that autonomously discover new protocols beyond human design",  # 12
    # 3. Reconfigurable Intelligent Surfaces (RIS)
    "RIS are passive meta-surfaces with 1000+ elements that manipulate EM waves (phase/amplitude)",  # 13
    "RIS creates virtual Line-of-Sight (LOS) paths; contrasts with active relays (achieving 85% energy savings)",  # 14
    "RIS provides 300–400% signal boost in Non-Line-of-Sight (NLOS) scenarios (Basar et al., 2021)",  # 15
    "RIS cost at $5–7/cm² (down 73% since 2020); deployable as 'smart walls' or integrated into urban infrastructure",  # 16
    "RIS Vision: Creating 'energy bubbles' for targeted wireless charging and anti-eavesdropping beams",  # 17
    # 4. Integrated Sensing & Communication (ISAC)
    "ISAC utilizes a single waveform for dual-functionality (e.g., OFDM for data + FMCW for radar)",  # 18
    "ISAC employs joint mutual information maximization to balance comms throughput vs. sensing resolution",  # 19
    "ISAC trials: Achieved 10 Gbps data + 0.7cm positioning simultaneously (at 28 GHz)",  # 20
    "ISAC offers 70–85% spectrum efficiency gain compared to separate communication and sensing systems",  # 21
    "ISAC Vision: Autonomous cars with real-time environmental mapping via V2X ISAC signals",  # 22
    # 5. Quantum-Secured Wireless
    "Quantum Key Distribution (QKD) uses quantum entanglement (no-cloning theorem) for eavesdrop-proof key exchange",  # 23
    "Post-Quantum Cryptography (PQC) provides software-based protection against quantum attacks",  # 24
    "QKD demonstrated at 20 Mbps over metro fiber; intercontinental satellite QKD achieved (China’s Micius satellite)",  # 25
    "Quantum security achieving 99.9999% security compliance in Singaporean financial institutions (MAS Report, 2024)",  # 26
    "Quantum Vision: A future quantum internet with entanglement-distributed sensors and communications",  # 27
    # 6. Cell-Free Massive MIMO
    "Cell-Free Massive MIMO uses user-centric distributed Access Points (APs) replacing traditional cellular towers",  # 28
    "Coherent joint transmission in Cell-Free MIMO converts interference into useful signal, enhancing performance",  # 29
    "Cell-Free MIMO shows 470% throughput gain for edge users and 95% fewer outages",  # 30
    "O(K²N) complexity in Cell-Free MIMO can be mitigated using federated learning approaches",  # 31
    "Cell-Free MIMO Vision: Seamless user mobility and development of wireless power transfer grids",  # 32
    # 7. Non-Terrestrial Networks (NTN)
    "NTNs involve LEO satellites (e.g., Starlink), HAPS, and drones integrating with terrestrial 6G (as per 3GPP Rel. 17+)",  # 33
    "Current LEO NTN offerings provide 150–300 Mbps speeds with 20–50ms latency",  # 34
    "NTN market projected to be $20B by 2028; ideal for maritime, aviation, and disaster recovery scenarios",  # 35
    "NTN Vision: Direct-to-smartphone satellite links for ubiquitous connectivity (e.g., Apple/Globalstar tests)",  # 36
    # 8. Semantic Communications
    "Semantic communications are task-driven, not bit-accurate, with AI extracting/encoding only relevant semantics",  # 37
    "Semantic communications can achieve 90% bandwidth reduction for IoT control commands and similar applications",  # 38
    "Semantic Comms Vision: Ultra-low-latency Machine-to-Machine (M2M) interactions (e.g., factory robots negotiating collision avoidance)",  # 39
    # 9. Zero-Energy IoT
    "Zero-Energy IoT devices use ambient RF, solar, or kinetic energy harvesting and backscatter communications (1–10 μW power)",  # 40
    "Zero-Energy IoT nodes have a projected cost of $0.42/node at scale and a 20-year lifespan",  # 41
    "Zero-Energy IoT Vision: 17.5B battery-free devices by 2030, potentially eliminating 230K tons of battery waste",  # 42
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

# Modified get_chapter_context function to also fetch content from a reference folder
def get_chapter_context(repo, folder_path, chapter_files, reference_folder=None):
    """
    Get context using the provided repo object.

    Args:
        repo: GitHub repository object
        folder_path: Path to the book folder
        chapter_files: List of existing chapter files
        reference_folder: Optional folder name to fetch additional reference content

    Returns:
        String containing context from previous chapters and reference folder
    """
    context = []

    # Get context from the last 3 chapters if they exist
    chapters_to_fetch = chapter_files[-3:] if chapter_files else []
    print(f"Fetching context from chapters: {chapters_to_fetch}")
    for fname in chapters_to_fetch:
        file_path = f"{folder_path}/{fname}"
        try:
            content_file = repo.get_contents(file_path, ref=BRANCH)
            # Limit context size per chapter if needed
            context.append(f"FROM PREVIOUS CHAPTER ({fname}):\n{content_file.decoded_content.decode('utf-8')[:600]}")
            print(f"Successfully fetched context from {fname}")
        except GithubException as e:
            print(f"⚠️ Warning: Could not fetch context from {file_path}: {e.status} - {e.data}")
            continue
        except Exception as e:
            print(f"⚠️ Warning: Unexpected error fetching context from {file_path}: {str(e)}")
            continue

    # Only try to fetch reference content if a folder was specified and it's not empty
    if reference_folder and reference_folder.strip():
        try:
            # Verify the reference folder exists before trying to access it
            repo.get_contents(reference_folder, ref=BRANCH)
            print(f"Fetching additional context from reference folder: {reference_folder}")

            reference_files = repo.get_contents(reference_folder, ref=BRANCH)
            for file in reference_files:
                if file.type == 'file' and file.name.endswith(('.md', '.txt', '.rst')):
                    try:
                        file_content = file.decoded_content.decode('utf-8')
                        context.append(f"FROM REFERENCE ({file.name}):\n{file_content[2800]}")
                        print(f"Successfully fetched reference from {file.name}")
                    except Exception as e:
                        print(f"⚠️ Warning: Error processing reference file {file.name}: {str(e)}")
        except GithubException as e:
            if e.status == 404:
                print(f"⚠️ Reference folder '{reference_folder}' not found - skipping reference content")
            else:
                print(f"⚠️ Error accessing reference folder '{reference_folder}': {e.status} - {e.data}")
        except Exception as e:
            print(f"⚠️ Unexpected error with reference folder '{reference_folder}': {str(e)}")

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
        1: {
            "title": "Terahertz (THz) Communications: The High-Frequency Frontier Beyond 5G",
            "points": [
                CONTENT_POINTS_CH3[0], CONTENT_POINTS_CH3[1], CONTENT_POINTS_CH3[2],
                CONTENT_POINTS_CH3[3], CONTENT_POINTS_CH3[4], CONTENT_POINTS_CH3[5],
                CONTENT_POINTS_CH3[6]
            ],
            "type": "core_technology"
        },
        2: {
            "title": "AI-Native Air Interface: Embedding Intelligence Deeply in 6G",
            "points": [
                CONTENT_POINTS_CH3[7], CONTENT_POINTS_CH3[8], CONTENT_POINTS_CH3[10],
                CONTENT_POINTS_CH3[11]
            ],
            "type": "core_technology"
        },
        3: {
            "title": "The Role of Explainable AI (XAI) in Critical 6G Services",
            "points": [CONTENT_POINTS_CH3[9]],
            "type": "implementation_aspect"
        },
        4: {
            "title": "Vision for AI-Native Networks: Towards Self-Evolving Wireless Systems",
            "points": [CONTENT_POINTS_CH3[12]],
            "type": "future_outlook"
        },
        5: {
            "title": "Reconfigurable Intelligent Surfaces (RIS): Engineering Smart Radio Environments",
            "points": [
                CONTENT_POINTS_CH3[13], CONTENT_POINTS_CH3[14], CONTENT_POINTS_CH3[15],
                CONTENT_POINTS_CH3[16], CONTENT_POINTS_CH3[17]
            ],
            "type": "core_technology"
        },
        6: {
            "title": "Integrated Sensing and Communication (ISAC): Unifying Network Dual Functions",
            "points": [
                CONTENT_POINTS_CH3[18], CONTENT_POINTS_CH3[19], CONTENT_POINTS_CH3[20],
                CONTENT_POINTS_CH3[21], CONTENT_POINTS_CH3[22]
            ],
            "type": "core_technology"
        },
        7: {
            "title": "Quantum Key Distribution (QKD): Hardware-Based Unhackable Wireless Security",
            "points": [
                CONTENT_POINTS_CH3[23], CONTENT_POINTS_CH3[25], CONTENT_POINTS_CH3[26],
                CONTENT_POINTS_CH3[27] # Includes vision for Quantum Internet
            ],
            "type": "security_paradigm"
        },
        8: {
            "title": "Post-Quantum Cryptography (PQC): Software Armor for Future-Proofing Networks",
            "points": [CONTENT_POINTS_CH3[24]],
            "type": "security_paradigm"
        },
        9: {
            "title": "Cell-Free Massive MIMO: User-Centric, Edge-Less Networking Paradigm",
            "points": [
                CONTENT_POINTS_CH3[28], CONTENT_POINTS_CH3[29], CONTENT_POINTS_CH3[30],
                CONTENT_POINTS_CH3[31], CONTENT_POINTS_CH3[32]
            ],
            "type": "network_architecture"
        },
        10: {
            "title": "Non-Terrestrial Networks (NTN): Extending Connectivity Globally from Above",
            "points": [
                CONTENT_POINTS_CH3[33], CONTENT_POINTS_CH3[34], CONTENT_POINTS_CH3[35],
                CONTENT_POINTS_CH3[36]
            ],
            "type": "network_architecture"
        },
        11: {
            "title": "Semantic Communications: Transmitting Meaning and Intent, Not Just Bits",
            "points": [CONTENT_POINTS_CH3[37], CONTENT_POINTS_CH3[38], CONTENT_POINTS_CH3[39]],
            "type": "communication_paradigm"
        },
        12: {
            "title": "Zero-Energy IoT: Powering a Sustainable, Battery-Free Connected Future",
            "points": [CONTENT_POINTS_CH3[40], CONTENT_POINTS_CH3[41], CONTENT_POINTS_CH3[42]],
            "type": "sustainability_focus"
        }
    }
    return chapters

def validate_chapter_plan(plan):
    distributed_points = sum(len(ch['points']) for ch in plan.values())
    if distributed_points < len(CONTENT_POINTS_CH3):  # Changed from CONTENT_POINTS to CONTENT_POINTS_CH3
        missing = set(CONTENT_POINTS_CH3) - set(p for ch in plan.values() for p in ch['points'])
        raise ValueError(f"Missing content points: {missing}")

# ============================
# EXECUTION WORKFLOW (OPTIMIZED)
# ============================
# Update the main function to accept and use a reference folder parameter
def main(reference_folder=None):
    """
    Generate one new chapter per execution, resuming from last created chapter.

    Args:
        reference_folder: Optional folder path in the repository to use as reference
    """
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

        # Get context from previous chapters and reference folder
        context = ""
        try:
            # Pass reference_folder to get_chapter_context
            context = get_chapter_context(repo, BOOK_FOLDER_NAME, existing_chapters[-3:], reference_folder)
            if context:
                print("✅ Context loaded from previous chapters and reference folder.")
            else:
                print("ℹ️ No previous chapters or reference content found.")
        except Exception as e:
            # Non-critical error, proceed without context
            print(f"⚠️ Context loading error: {str(e)}. Proceeding without context.")
            context = "" # Ensure context is empty string on error

        print(f"⏳ Generating Chapter {next_chapter_num}: {current_chapter['title']}")

        # Configure the writing task dynamically
        chapter_task.description = f"""Compose Chapter {next_chapter_num}: {current_chapter['title']}
Key Points: {current_chapter.get('points', 'Wireless technology evolution')}
Historical Context: {context if context else 'First chapter of the book'}
Reference Folder: {reference_folder if reference_folder else 'None provided'}"""

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
            success, message = github_commit(repo, result, commit_filename, commit_message)

            if success:
                print(f"✅ Successfully committed Chapter {next_chapter_num} to GitHub: {message}")
                print(f"📊 Progress: {next_chapter_num}/{MAX_CHAPTERS} chapters completed.")
            else:
                print(f"⚠️ Chapter {next_chapter_num} generated but GitHub commit failed: {message}")

        except Exception as e:
            # Catch unexpected errors during the commit call itself
            print(f"❌ Unexpected error during commit process: {str(e)}")
            import traceback
            traceback.print_exc()
            print("💡 Generated content was not saved to GitHub.")

    except Exception as e:
        # Catch-all for critical failures in main setup
        print(f"❌ Critical failure in main execution: {str(e)}")
        print("💡 Tip: Check global configurations (token, repo name), network, and traceback.")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Only use reference folder if it exists in the config and isn't empty
    reference_folder = REFERENCE_FOLDER if REFERENCE_FOLDER and REFERENCE_FOLDER.strip() else None
    main(reference_folder)
