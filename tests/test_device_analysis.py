from datetime import datetime
from device_analysis.device_profile import DeviceProfile
from device_analysis.image_analyzer import ImageAnalyzer, ImageAnalysisResult
from device_analysis.analyzer import DeviceAnalyzer
from device_analysis.reuse_scorer import ReuseScorer
from reuse_passport.passport_status import PassportStatus
from reuse_passport.passport import DigitalReusePassport
from reuse_passport.passport_generator import PassportGenerator
from reuse_passport.passport_validator import PassportValidator

try:
    import pytest
except ImportError:
    pytest = None

# ==========================================
# 1. Device Profiles & Basic Analyses Tests
# ==========================================

def test_device_profile_validation():
    # Valid profile
    profile = DeviceProfile(
        item_id="RM-TEST-01",
        item_name="Test Phone",
        category="Smartphone",
        brand="Apple",
        model="iPhone X",
        estimated_age=4.5,
        working_status=True,
        power_status=True,
        physical_condition="GOOD",
        functional_condition="GOOD"
    )
    assert profile.item_id == "RM-TEST-01"
    assert profile.working_status is True
    assert len(profile.visible_damage) == 0

    # Invalid profile (negative age should fail Pydantic validation)
    if pytest:
        with pytest.raises(Exception):
            DeviceProfile(
                item_id="RM-TEST-01",
                item_name="Test Phone",
                category="Smartphone",
                brand="Apple",
                model="iPhone X",
                estimated_age=-1.0,
                working_status=True,
                power_status=True,
                physical_condition="GOOD",
                functional_condition="GOOD"
            )
    else:
        try:
            DeviceProfile(
                item_id="RM-TEST-01",
                item_name="Test Phone",
                category="Smartphone",
                brand="Apple",
                model="iPhone X",
                estimated_age=-1.0,
                working_status=True,
                power_status=True,
                physical_condition="GOOD",
                functional_condition="GOOD"
            )
            assert False, "Should have failed Pydantic validation on negative age"
        except Exception:
            pass


def test_image_analyzer_mock_integration():
    analyzer = ImageAnalyzer()
    
    # Test Laptop image mock
    laptop_res = analyzer.analyze_image("http://example.com/dell_laptop_image.jpg")
    assert laptop_res.detected_category == "Laptop"
    assert laptop_res.predicted_brand == "Dell"
    assert "scratched_casing" in laptop_res.visible_damage
    
    # Test Unknown image mock
    unknown_res = analyzer.analyze_image("http://example.com/random_device.png")
    assert unknown_res.detected_category == "Unknown"
    assert unknown_res.confidence_score == 0.50


def test_reuse_scorer_configurability():
    # Custom scoring weights summing to 1.0 (100%)
    custom_weights = {
        "functionality": 0.40,
        "physical_condition": 0.10,
        "repairability": 0.20,
        "component_recovery": 0.10,
        "remaining_life": 0.10,
        "recyclability": 0.10
    }
    
    # Init scorer with valid custom weights
    scorer = ReuseScorer(weights=custom_weights)
    assert scorer.weights["functionality"] == 0.40

    # Init scorer with invalid weights (sum is not 1.0)
    invalid_weights = {
        "functionality": 0.50,
        "physical_condition": 0.50,
        "repairability": 0.20
    }
    if pytest:
        with pytest.raises(ValueError):
            ReuseScorer(weights=invalid_weights)
    else:
        try:
            ReuseScorer(weights=invalid_weights)
            assert False, "Should have failed on invalid weights summing"
        except ValueError:
            pass


# ==========================================
# 2. Complete Device Scenario Integration Tests
# ==========================================

def test_scenario_1_direct_reuse_laptop():
    """
    Scenario 1: Working Dell laptop in excellent condition.
    Should yield DIRECT_REUSE and a high reuse score.
    """
    profile = DeviceProfile(
        item_id="RM-LAPTOP-01",
        item_name="Dell Latitude Notebook",
        category="Laptop",
        brand="Dell",
        model="Latitude 7420",
        estimated_age=1.5,
        working_status=True,
        power_status=True,
        physical_condition="EXCELLENT",
        functional_condition="EXCELLENT",
        visible_damage=[]
    )
    
    analyzer = DeviceAnalyzer()
    report = analyzer.analyze_device(profile)
    summary = report["analysis_summary"]
    
    assert summary["recommended_action"] == "DIRECT_REUSE"
    assert summary["reuse_score"] >= 80.0
    assert summary["reuse_level"] == "HIGH REUSE POTENTIAL"
    assert report["circular_economy_impact"]["landfill_diversion_status"] == "TOTAL_LANDFILL_AVOIDANCE"
    assert "redeployed immediately" in report["recommendation"]["explanation"].lower()


def test_scenario_2_repair_laptop():
    """
    Scenario 2: Damaged laptop with minor, repairable component faults.
    Should yield REPAIR recommendation.
    """
    profile = DeviceProfile(
        item_id="RM-LAPTOP-02",
        item_name="Lenovo ThinkPad",
        category="Laptop",
        brand="Lenovo",
        model="T490",
        estimated_age=3.5,
        working_status=False,
        power_status=True,
        physical_condition="GOOD",
        functional_condition="GOOD",
        damaged_components=["Battery"],
        visible_damage=["scratched casing"]
    )
    
    analyzer = DeviceAnalyzer()
    report = analyzer.analyze_device(profile)
    summary = report["analysis_summary"]
    
    assert summary["recommended_action"] == "REPAIR"
    assert report["repairability"]["repairability_level"] == "MODERATE"
    assert "replacing the faulty components" in report["recommendation"]["explanation"].lower()


def test_scenario_3_refurbishment_monitor():
    """
    Scenario 3: Good-condition monitor requiring minor cosmetic/cleaning attention.
    Should yield REFURBISHMENT recommendation.
    """
    profile = DeviceProfile(
        item_id="RM-MONITOR-01",
        item_name="HP Display Monitor",
        category="Monitor",
        brand="HP",
        model="EliteDisplay",
        estimated_age=4.0,
        working_status=True,
        power_status=True,
        physical_condition="FAIR",
        functional_condition="GOOD"
    )
    
    analyzer = DeviceAnalyzer()
    report = analyzer.analyze_device(profile)
    summary = report["analysis_summary"]
    
    assert summary["recommended_action"] == "REFURBISHMENT"
    assert "requires software wiping, os installation, or deep cleaning" in report["recommendation"]["explanation"].lower()


def test_scenario_4_component_reuse_desktop():
    """
    Scenario 4: Broken desktop with multiple salvageable parts.
    Should yield COMPONENT_REUSE.
    """
    profile = DeviceProfile(
        item_id="RM-DESKTOP-01",
        item_name="Gaming Desktop PC",
        category="Desktop",
        brand="Custom",
        model="Intel Build",
        estimated_age=5.0,
        working_status=False,
        power_status=False,
        physical_condition="GOOD",
        functional_condition="NON_FUNCTIONAL",
        damaged_components=["Power supply", "Motherboard"],
        reusable_components=["RAM", "CPU", "GPU", "Storage"]
    )
    
    analyzer = DeviceAnalyzer()
    report = analyzer.analyze_device(profile)
    summary = report["analysis_summary"]
    
    assert summary["recommended_action"] == "COMPONENT_REUSE"
    ram_entry = next(c for c in report["component_analysis"] if c["component_name"] == "RAM")
    assert ram_entry["reusable"] is True
    assert ram_entry["estimated_value"] > 0
    assert report["circular_economy_impact"]["landfill_diversion_status"] == "PARTIAL_RECOVERY"


def test_scenario_5_recycling_smartphone():
    """
    Scenario 5: Obsolete, non-functional smartphone.
    Should yield RECYCLING recommendation.
    """
    profile = DeviceProfile(
        item_id="RM-PHONE-01",
        item_name="Old Shattered Smartphone",
        category="Smartphone",
        brand="Samsung",
        model="Galaxy S6",
        estimated_age=9.0,
        working_status=False,
        power_status=False,
        physical_condition="NON_FUNCTIONAL",
        functional_condition="NON_FUNCTIONAL",
        damaged_components=["Display screen", "Battery", "Logic board"],
        visible_damage=["shattered screen", "missing back cover"]
    )
    
    analyzer = DeviceAnalyzer()
    report = analyzer.analyze_device(profile)
    summary = report["analysis_summary"]
    
    assert summary["recommended_action"] == "RECYCLING"
    assert summary["reuse_level"] == "RECYCLING / RESPONSIBLE DISPOSAL"
    assert report["circular_economy_impact"]["estimated_weight_diverted_kg"] == 0.0


# ==========================================
# 3. Digital Reuse Passport & Lifecycle Tests
# ==========================================

def test_passport_generation_and_validation():
    profile = DeviceProfile(
        item_id="RM-LAPTOP-100",
        item_name="MacBook Pro",
        category="Laptop",
        brand="Apple",
        model="M1 Air",
        estimated_age=2.0,
        working_status=True,
        power_status=True,
        physical_condition="EXCELLENT",
        functional_condition="EXCELLENT"
    )
    
    analyzer = DeviceAnalyzer()
    report = analyzer.analyze_device(profile)
    
    generator = PassportGenerator()
    passport = generator.generate_passport(report)
    
    assert passport.passport_id.startswith("RM-PASS-")
    assert passport.current_status == PassportStatus.ANALYZED
    assert len(passport.status_history) == 1
    assert passport.status_history[0].status == PassportStatus.ANALYZED
    
    validator = PassportValidator()
    assert validator.validate_structure(passport) is True


def test_passport_lifecycle_status_transitions():
    profile = DeviceProfile(
        item_id="RM-MONITOR-50",
        item_name="Dell Screen",
        category="Monitor",
        brand="Dell",
        model="P2419H",
        estimated_age=3.0,
        working_status=True,
        power_status=True,
        physical_condition="GOOD",
        functional_condition="GOOD"
    )
    analyzer = DeviceAnalyzer()
    report = analyzer.analyze_device(profile)
    generator = PassportGenerator()
    passport = generator.generate_passport(report)
    
    validator = PassportValidator()
    
    assert passport.current_status == PassportStatus.ANALYZED
    
    validator.update_status(passport, PassportStatus.AVAILABLE, "Listed on exchange portal")
    assert passport.current_status == PassportStatus.AVAILABLE
    
    validator.update_status(passport, PassportStatus.MATCHED, "Recipient matched")
    assert passport.current_status == PassportStatus.MATCHED
    
    validator.update_status(passport, PassportStatus.RESERVED, "Held for collection")
    assert passport.current_status == PassportStatus.RESERVED
    
    validator.update_status(passport, PassportStatus.TRANSFERRED, "Dispatched via courier")
    assert passport.current_status == PassportStatus.TRANSFERRED
    
    validator.update_status(passport, PassportStatus.REUSED, "Recipient confirmed delivery and use")
    assert passport.current_status == PassportStatus.REUSED
    assert len(passport.status_history) == 6
    
    # Attempting to go back from REUSED directly to AVAILABLE (invalid)
    if pytest:
        with pytest.raises(ValueError):
            validator.update_status(passport, PassportStatus.AVAILABLE, "Invalid backward state jump")
    else:
        try:
            validator.update_status(passport, PassportStatus.AVAILABLE, "Invalid backward state jump")
            assert False, "Should have thrown ValueError"
        except ValueError:
            pass


def test_passport_alternative_lifecycle_paths():
    profile = DeviceProfile(
        item_id="RM-MONITOR-51",
        item_name="Dell Screen",
        category="Monitor",
        brand="Dell",
        model="P2419H",
        estimated_age=3.0,
        working_status=True,
        power_status=True,
        physical_condition="GOOD",
        functional_condition="GOOD"
    )
    analyzer = DeviceAnalyzer()
    report = analyzer.analyze_device(profile)
    generator = PassportGenerator()
    passport = generator.generate_passport(report)
    
    validator = PassportValidator()
    
    # Path 2: ANALYZED -> REFURBISHMENT_REQUIRED -> AVAILABLE
    validator.update_status(passport, PassportStatus.REFURBISHMENT_REQUIRED, "Requires wiping")
    assert passport.current_status == PassportStatus.REFURBISHMENT_REQUIRED
    
    validator.update_status(passport, PassportStatus.AVAILABLE, "Refurbishment complete, listed")
    assert passport.current_status == PassportStatus.AVAILABLE

    # Path 3: ANALYZED -> RECYCLING
    passport_2 = generator.generate_passport(report)
    validator.update_status(passport_2, PassportStatus.RECYCLING, "Sent directly to recycling center")
    assert passport_2.current_status == PassportStatus.RECYCLING


def test_scenario_6_non_functional_component_recovery():
    """
    Scenario 6: Non-functional laptop where components are estimated or unknown,
    but not verified working unless explicitly passed.
    """
    profile = DeviceProfile(
        item_id="RM-LAPTOP-06",
        item_name="Non-Functional Dell Laptop",
        category="Laptop",
        brand="Dell",
        model="Latitude 5420",
        estimated_age=4.0,
        working_status=False,
        power_status=False,
        physical_condition="FAIR",
        functional_condition="NON_FUNCTIONAL",
        visible_damage=["Minor scratches"],
        missing_components=["Charger/adapter"],
        known_components={
            "RAM": "8GB RAM",
            "SSD": "512GB SSD"
        }
    )
    
    analyzer = DeviceAnalyzer()
    report = analyzer.analyze_device(profile)
    summary = report["analysis_summary"]
    
    # 1. Recommended action must be COMPONENT_REUSE
    assert summary["recommended_action"] == "COMPONENT_REUSE"
    assert "component reuse" in report["recommendation"]["explanation"].lower()
    
    # 2. Check component recovery details list exists
    recovery = report["component_recovery"]
    assert len(recovery) > 0
    
    # 3. Charger/adapter must be UNKNOWN status
    charger_entry = next(c for c in recovery if c["component"] == "Charger/adapter")
    assert charger_entry["assessment_status"] == "UNKNOWN"
    assert charger_entry["potential_score"] == 0.0
    assert "missing" in charger_entry["reason"].lower()

    # 4. RAM must be ESTIMATED (not verified!) and have HIGH potential
    ram_entry = next(c for c in recovery if c["component"] == "RAM")
    assert ram_entry["assessment_status"] == "ESTIMATED"
    assert ram_entry["potential_level"] == "HIGH"
    assert "8gb ram" in ram_entry["reason"].lower()
    # Confidence score: 85 - 20 (power issue) + 10 (known specs) = 75
    assert ram_entry["confidence_score"] == 75.0
    assert "does not power on" in ram_entry["reason"].lower()
    assert "verified" not in ram_entry["reason"].lower()

    # 5. Check passport mapping
    generator = PassportGenerator()
    passport = generator.generate_passport(report)
    assert len(passport.component_recovery) > 0
    
    validator = PassportValidator()
    assert validator.validate_structure(passport) is True

