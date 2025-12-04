from datetime import datetime, timedelta
from typing import List, Dict, Optional
from dataclasses import dataclass, field
from enum import Enum
import json

class PhaseStatus(Enum):
    NOT_STARTED = "Not Started"
    IN_PROGRESS = "In Progress"
    REVIEW_PENDING = "Review Pending"
    COMPLETED = "Completed"
    REQUIRES_FEEDBACK = "Requires Feedback"

class RiskLevel(Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"

@dataclass
class QualityGate:
    """Represents a quality gate between phases"""
    name: str
    criteria: List[str]
    passed: bool = False
    reviewer: Optional[str] = None
    review_date: Optional[datetime] = None
    comments: str = ""

@dataclass
class FeedbackItem:
    """Represents feedback from later phases to earlier phases"""
    from_phase: str
    to_phase: str
    issue_description: str
    recommended_action: str
    priority: RiskLevel
    created_date: datetime = field(default_factory=datetime.now)
    resolved: bool = False

@dataclass
class ValidationActivity:
    """Represents activities in the continuous validation layer"""
    activity_name: str
    description: str
    responsible_person: str
    frequency: str  # e.g., "Daily", "Weekly", "Per Phase"
    status: PhaseStatus = PhaseStatus.NOT_STARTED

@dataclass
class Phase:
    """Represents a phase in the GeytonModel"""
    name: str
    description: str
    deliverables: List[str]
    activities: List[str]
    responsible_team: str
    estimated_duration: int  # in days
    status: PhaseStatus = PhaseStatus.NOT_STARTED
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    completion_percentage: int = 0
    feedback_received: List[FeedbackItem] = field(default_factory=list)
    quality_gate: Optional[QualityGate] = None

class GeytonModel:
    """
    Implementation of the GeytonModel - Enhanced Waterfall with Feedback Loops & Quality Gates
    """
    
    def __init__(self, project_name: str = ""):
        self.project_name = project_name
        self.created_date = datetime.now()
        self.phases: Dict[str, Phase] = {}
        self.validation_activities: List[ValidationActivity] = []
        self.project_risks: List[Dict] = []
        self.stakeholders: List[str] = []
        
        # Initialize default phases
        self._initialize_default_phases()
    
    def _initialize_default_phases(self):
        """Initialize the five core phases of the GeytonModel"""
        
        # Communication Phase
        self.phases["Communication"] = Phase(
            name="Communication",
            description="Project initiation and requirements gathering",
            deliverables=["Requirements Document", "Stakeholder Matrix", "Project Charter"],
            activities=["Stakeholder interviews", "Requirements analysis", "Project scope definition"],
            responsible_team="Business Analysts",
            estimated_duration=14
        )
        
        # Planning Phase
        self.phases["Planning"] = Phase(
            name="Planning",
            description="Project planning and risk assessment",
            deliverables=["Project Plan", "Risk Register", "Resource Plan"],
            activities=["Schedule creation", "Resource allocation", "Risk assessment"],
            responsible_team="Project Management",
            estimated_duration=10
        )
        
        # Modeling Phase
        self.phases["Modeling"] = Phase(
            name="Modeling",
            description="System analysis and architecture design",
            deliverables=["System Architecture", "Design Documents", "Prototypes"],
            activities=["System design", "Architecture modeling", "Prototype development"],
            responsible_team="System Architects",
            estimated_duration=21
        )
        
        # Construction Phase
        self.phases["Construction"] = Phase(
            name="Construction",
            description="Code development and testing",
            deliverables=["Source Code", "Unit Tests", "Integration Tests"],
            activities=["Code development", "Unit testing", "Code reviews"],
            responsible_team="Development Team",
            estimated_duration=45
        )
        
        # Deployment Phase
        self.phases["Deployment"] = Phase(
            name="Deployment",
            description="System delivery and user acceptance",
            deliverables=["Deployed System", "User Documentation", "Support Plan"],
            activities=["System deployment", "User training", "Go-live support"],
            responsible_team="DevOps & Support",
            estimated_duration=14
        )
        
        # Initialize Quality Gates
        self._initialize_quality_gates()
        
        # Initialize Validation Activities
        self._initialize_validation_activities()
    
    def _initialize_quality_gates(self):
        """Initialize quality gates between phases"""
        
        self.phases["Communication"].quality_gate = QualityGate(
            name="Requirements Review",
            criteria=[
                "All stakeholders have approved requirements",
                "Requirements are complete and unambiguous",
                "Acceptance criteria are defined"
            ]
        )
        
        self.phases["Planning"].quality_gate = QualityGate(
            name="Design Review",
            criteria=[
                "Project plan is realistic and approved",
                "Resources are allocated and available",
                "Risks are identified and mitigation plans exist"
            ]
        )
        
        self.phases["Modeling"].quality_gate = QualityGate(
            name="Architecture Review",
            criteria=[
                "Architecture meets requirements",
                "Design is technically feasible",
                "Prototypes validate key concepts"
            ]
        )
        
        self.phases["Construction"].quality_gate = QualityGate(
            name="Testing Review",
            criteria=[
                "Code coverage meets standards",
                "All unit tests pass",
                "Integration testing completed"
            ]
        )
    
    def _initialize_validation_activities(self):
        """Initialize continuous validation activities"""
        
        self.validation_activities = [
            ValidationActivity(
                "Stakeholder Reviews",
                "Regular stakeholder feedback sessions",
                "Business Analyst",
                "Weekly"
            ),
            ValidationActivity(
                "Quality Assurance",
                "Continuous quality monitoring",
                "QA Team",
                "Daily"
            ),
            ValidationActivity(
                "Risk Monitoring",
                "Track and assess project risks",
                "Project Manager",
                "Weekly"
            ),
            ValidationActivity(
                "Early Testing",
                "Progressive testing of components",
                "Test Team",
                "Per Phase"
            )
        ]
    
    def setup_project_interactively(self):
        """Interactive setup of the GeytonModel project"""
        
        print("=" * 60)
        print("🚀 GEYTONMODEL PROJECT SETUP")
        print("=" * 60)
        
        # Project basics
        if not self.project_name:
            self.project_name = input("\n📋 Enter project name: ").strip()
        
        print(f"\n🎯 Setting up project: {self.project_name}")
        
        # Stakeholders
        self._setup_stakeholders()
        
        # Phase customization
        self._customize_phases()
        
        # Validation activities
        self._customize_validation_activities()
        
        # Initial risks
        self._setup_initial_risks()
        
        print("\n✅ Project setup completed successfully!")
        return self
    
    def _setup_stakeholders(self):
        """Setup project stakeholders"""
        print("\n" + "=" * 40)
        print("👥 STAKEHOLDER SETUP")
        print("=" * 40)
        
        while True:
            stakeholder = input("\nEnter stakeholder name (or 'done' to finish): ").strip()
            if stakeholder.lower() == 'done':
                break
            if stakeholder:
                self.stakeholders.append(stakeholder)
                print(f"✓ Added stakeholder: {stakeholder}")
    
    def _customize_phases(self):
        """Allow customization of phases"""
        print("\n" + "=" * 40)
        print("🔧 PHASE CUSTOMIZATION")
        print("=" * 40)
        
        for phase_name, phase in self.phases.items():
            print(f"\n📋 Customizing {phase_name} Phase")
            print(f"Current team: {phase.responsible_team}")
            print(f"Current duration: {phase.estimated_duration} days")
            
            # Update responsible team
            new_team = input(f"New responsible team (press Enter to keep '{phase.responsible_team}'): ").strip()
            if new_team:
                phase.responsible_team = new_team
            
            # Update duration
            new_duration = input(f"New duration in days (press Enter to keep {phase.estimated_duration}): ").strip()
            if new_duration.isdigit():
                phase.estimated_duration = int(new_duration)
            
            # Add custom deliverables
            print(f"Current deliverables: {', '.join(phase.deliverables)}")
            custom_deliverable = input("Add custom deliverable (press Enter to skip): ").strip()
            if custom_deliverable:
                phase.deliverables.append(custom_deliverable)
                print(f"✓ Added deliverable: {custom_deliverable}")
    
    def _customize_validation_activities(self):
        """Customize validation activities"""
        print("\n" + "=" * 40)
        print("✅ VALIDATION ACTIVITIES")
        print("=" * 40)
        
        print("Current validation activities:")
        for i, activity in enumerate(self.validation_activities, 1):
            print(f"{i}. {activity.activity_name} - {activity.responsible_person}")
        
        custom_activity = input("\nAdd custom validation activity (press Enter to skip): ").strip()
        if custom_activity:
            responsible = input("Who is responsible for this activity? ").strip()
            frequency = input("How often? (Daily/Weekly/Per Phase): ").strip()
            
            self.validation_activities.append(
                ValidationActivity(custom_activity, custom_activity, responsible, frequency)
            )
            print(f"✓ Added validation activity: {custom_activity}")
    
    def _setup_initial_risks(self):
        """Setup initial project risks"""
        print("\n" + "=" * 40)
        print("⚠️  INITIAL RISK ASSESSMENT")
        print("=" * 40)
        
        while True:
            risk_desc = input("\nEnter a project risk (or 'done' to finish): ").strip()
            if risk_desc.lower() == 'done':
                break
            
            if risk_desc:
                print("Risk levels: 1=Low, 2=Medium, 3=High, 4=Critical")
                level_input = input("Risk level (1-4): ").strip()
                
                level_map = {'1': RiskLevel.LOW, '2': RiskLevel.MEDIUM, 
                           '3': RiskLevel.HIGH, '4': RiskLevel.CRITICAL}
                
                risk_level = level_map.get(level_input, RiskLevel.MEDIUM)
                
                mitigation = input("Mitigation strategy: ").strip()
                
                self.project_risks.append({
                    'description': risk_desc,
                    'level': risk_level,
                    'mitigation': mitigation,
                    'identified_date': datetime.now()
                })
                print(f"✓ Added risk: {risk_desc}")
    
    def add_feedback(self, from_phase: str, to_phase: str, issue: str, action: str, priority: RiskLevel):
        """Add feedback from one phase to another"""
        
        if to_phase not in self.phases:
            raise ValueError(f"Phase '{to_phase}' does not exist")
        
        feedback = FeedbackItem(from_phase, to_phase, issue, action, priority)
        self.phases[to_phase].feedback_received.append(feedback)
        
        # Update phase status to indicate feedback is required
        if self.phases[to_phase].status == PhaseStatus.COMPLETED:
            self.phases[to_phase].status = PhaseStatus.REQUIRES_FEEDBACK
        
        return feedback
    
    def complete_quality_gate(self, phase_name: str, reviewer: str, passed: bool, comments: str = ""):
        """Complete a quality gate review"""
        
        if phase_name not in self.phases:
            raise ValueError(f"Phase '{phase_name}' does not exist")
        
        gate = self.phases[phase_name].quality_gate
        if gate:
            gate.passed = passed
            gate.reviewer = reviewer
            gate.review_date = datetime.now()
            gate.comments = comments
            
            if passed:
                print(f"✅ Quality gate '{gate.name}' passed for {phase_name} phase")
            else:
                print(f"❌ Quality gate '{gate.name}' failed for {phase_name} phase")
        
        return gate
    
    def update_phase_status(self, phase_name: str, status: PhaseStatus, completion: int = 0):
        """Update phase status and completion percentage"""
        
        if phase_name not in self.phases:
            raise ValueError(f"Phase '{phase_name}' does not exist")
        
        phase = self.phases[phase_name]
        phase.status = status
        phase.completion_percentage = max(0, min(100, completion))
        
        if status == PhaseStatus.IN_PROGRESS and not phase.start_date:
            phase.start_date = datetime.now()
        elif status == PhaseStatus.COMPLETED:
            phase.end_date = datetime.now()
            phase.completion_percentage = 100
    
    def get_project_summary(self) -> str:
        """Generate a comprehensive project summary"""
        
        summary = []
        summary.append("=" * 80)
        summary.append(f"📊 GEYTONMODEL PROJECT SUMMARY: {self.project_name}")
        summary.append("=" * 80)
        summary.append(f"Created: {self.created_date.strftime('%Y-%m-%d %H:%M:%S')}")
        summary.append(f"Stakeholders: {len(self.stakeholders)}")
        summary.append(f"Total Estimated Duration: {sum(p.estimated_duration for p in self.phases.values())} days")
        
        # Phase overview
        summary.append("\n📋 PHASE OVERVIEW")
        summary.append("-" * 50)
        for phase_name, phase in self.phases.items():
            status_icon = {
                PhaseStatus.NOT_STARTED: "⭕",
                PhaseStatus.IN_PROGRESS: "🔄",
                PhaseStatus.REVIEW_PENDING: "⏳",
                PhaseStatus.COMPLETED: "✅",
                PhaseStatus.REQUIRES_FEEDBACK: "🔄"
            }.get(phase.status, "❓")
            
            summary.append(f"{status_icon} {phase_name:15} | {phase.status.value:15} | {phase.completion_percentage:3}% | {phase.responsible_team}")
        
        # Quality Gates Status
        summary.append("\n🚪 QUALITY GATES STATUS")
        summary.append("-" * 50)
        for phase_name, phase in self.phases.items():
            if phase.quality_gate:
                gate = phase.quality_gate
                status = "✅ PASSED" if gate.passed else "❌ PENDING"
                reviewer = gate.reviewer or "Not assigned"
                summary.append(f"{gate.name:20} | {status} | Reviewer: {reviewer}")
        
        # Validation Activities
        summary.append("\n✅ VALIDATION ACTIVITIES")
        summary.append("-" * 50)
        for activity in self.validation_activities:
            status_icon = "✅" if activity.status == PhaseStatus.COMPLETED else "⭕"
            summary.append(f"{status_icon} {activity.activity_name:25} | {activity.responsible_person:15} | {activity.frequency}")
        
        # Feedback Summary
        total_feedback = sum(len(phase.feedback_received) for phase in self.phases.values())
        if total_feedback > 0:
            summary.append(f"\n🔄 FEEDBACK ITEMS: {total_feedback}")
            summary.append("-" * 50)
            for phase_name, phase in self.phases.items():
                for feedback in phase.feedback_received:
                    status = "✅ Resolved" if feedback.resolved else "⭕ Open"
                    summary.append(f"{feedback.from_phase} → {feedback.to_phase} | {feedback.priority.value} | {status}")
        
        # Risk Summary
        if self.project_risks:
            summary.append(f"\n⚠️  PROJECT RISKS: {len(self.project_risks)}")
            summary.append("-" * 50)
            for risk in self.project_risks:
                level_icon = {"Low": "🟢", "Medium": "🟡", "High": "🟠", "Critical": "🔴"}.get(risk['level'].value, "❓")
                summary.append(f"{level_icon} {risk['level'].value:8} | {risk['description']}")
        
        # Stakeholders
        if self.stakeholders:
            summary.append(f"\n👥 STAKEHOLDERS: {len(self.stakeholders)}")
            summary.append("-" * 50)
            summary.append(", ".join(self.stakeholders))
        
        summary.append("\n" + "=" * 80)
        
        return "\n".join(summary)
    
    def export_to_json(self) -> str:
        """Export the project to JSON format"""
        
        def serialize_datetime(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            elif isinstance(obj, (PhaseStatus, RiskLevel)):
                return obj.value
            raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
        
        project_data = {
            'project_name': self.project_name,
            'created_date': self.created_date,
            'phases': {name: phase.__dict__ for name, phase in self.phases.items()},
            'validation_activities': [activity.__dict__ for activity in self.validation_activities],
            'project_risks': self.project_risks,
            'stakeholders': self.stakeholders
        }
        
        return json.dumps(project_data, default=serialize_datetime, indent=2)

# Example usage and demonstration
def demo_geytonmodel():
    """Demonstration of the GeytonModel class"""
    
    print("🎯 GeytonModel Demo - Creating a sample project")
    
    # Create a sample project
    model = GeytonModel("RimWorld Mod Development")
    
    # Add some sample stakeholders
    model.stakeholders = ["Mod Users", "RimWorld Community", "Steam Workshop", "Development Team"]
    
    # Update some phases
    model.update_phase_status("Communication", PhaseStatus.COMPLETED, 100)
    model.update_phase_status("Planning", PhaseStatus.IN_PROGRESS, 75)
    
    # Complete a quality gate
    model.complete_quality_gate("Communication", "Lead BA", True, "All requirements gathered and approved")
    
    # Add some feedback
    model.add_feedback(
        "Construction", 
        "Modeling", 
        "Architecture doesn't support mod compatibility requirements",
        "Revise architecture to include mod API integration patterns",
        RiskLevel.HIGH
    )
    
    # Add a project risk
    model.project_risks.append({
        'description': 'RimWorld game updates may break mod compatibility',
        'level': RiskLevel.MEDIUM,
        'mitigation': 'Design mod with version checking and graceful degradation',
        'identified_date': datetime.now()
    })
    
    # Display the summary
    print(model.get_project_summary())
    
    return model

if __name__ == "__main__":
    # Run interactive setup
    interactive_setup = input("Would you like to run interactive setup? (y/n): ").lower().strip()
    
    if interactive_setup == 'y':
        model = GeytonModel().setup_project_interactively()
        print("\n" + model.get_project_summary())
    else:
        # Run demo
        demo_model = demo_geytonmodel()
        
        print("\n🔄 Would you like to see the JSON export? (y/n): ", end="")
        if input().lower().strip() == 'y':
            print("\n📄 JSON EXPORT:")
            print("-" * 40)
            print(demo_model.export_to_json())