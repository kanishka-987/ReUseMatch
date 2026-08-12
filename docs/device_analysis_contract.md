# Device Analysis & Digital Reuse Passport Data Contract

This document specifies the data schemas and contracts for **Member 2's** modules: Device Analysis and Digital Reuse Passport. These schemas are designed to be consumed by other members of the **ReUseMatch** engineering team:
* **Member 1 (Frontend UI)**: To render indicators, graphs, and condition logs.
* **Member 3 (AI Agents & Orchestrator)**: To sequence inputs and guide decisions.
* **Member 4 (Backend API & Database)**: To validate and save records to MySQL.

---

## 1. Input Schemas

To analyze a device, provide the following Pydantic-validated payload.

```json
{
  "item_id": "RM-001",
  "item_name": "Developer Dell Laptop",
  "category": "Laptop",
  "subcategory": "Developer Notebook",
  "brand": "Dell",
  "model": "Precision 5550",
  "serial_number": "MX-123456-ABC",
  "estimated_age": 2.5,
  "purchase_year": 2023,
  "working_status": true,
  "power_status": true,
  "physical_condition": "GOOD",
  "functional_condition": "EXCELLENT",
  "visible_damage": ["minor_scratches_bottom"],
  "damaged_components": [],
  "reusable_components": [],
  "missing_components": []
}
```

---

## 2. Standardized Output Schema (Core payload)

Calling `DeviceAnalyzer.analyze_device(...)` returns a comprehensive dictionary structured as follows.

### Example JSON Payload Output

```json
{
  "item_id": "RM-001",
  "device_profile": {
    "item_id": "RM-001",
    "item_name": "Developer Dell Laptop",
    "category": "Laptop",
    "subcategory": "Developer Notebook",
    "brand": "Dell",
    "model": "Precision 5550",
    "serial_number": "MX-123456-ABC",
    "estimated_age": 2.5,
    "purchase_year": 2023,
    "working_status": true,
    "power_status": true,
    "physical_condition": "GOOD",
    "functional_condition": "EXCELLENT",
    "visible_damage": [
      "minor_scratches_bottom"
    ],
    "damaged_components": [],
    "reusable_components": [],
    "missing_components": []
  },
  "condition_analysis": {
    "physical_grade": "GOOD",
    "physical_explanation": "The device is physically stable with minor cosmetic wear: minor_scratches_bottom.",
    "functional_grade": "EXCELLENT",
    "functional_explanation": "All core functionalities and interfaces passed functional testing.",
    "overall_grade": "GOOD",
    "overall_explanation": "Device is fully functional with minimal casing wear and no critical component failures."
  },
  "component_analysis": [
    {
      "component_name": "RAM",
      "condition": "EXCELLENT",
      "reusable": true,
      "repairable": false,
      "estimated_value": 15.75,
      "reuse_confidence": 0.95,
      "possible_reuse": "Extract for upgrading or repairing compatible machines",
      "explanation": "Component 'RAM' is functional, graded as 'EXCELLENT', and suitable for component extraction and reuse."
    },
    {
      "component_name": "SSD/HDD",
      "condition": "EXCELLENT",
      "reusable": true,
      "repairable": false,
      "estimated_value": 21.0,
      "reuse_confidence": 0.95,
      "possible_reuse": "Wipe and reuse as external secondary storage",
      "explanation": "Component 'SSD/HDD' is functional, graded as 'EXCELLENT', and suitable for component extraction and reuse."
    }
  ],
  "repairability": {
    "repairability_score": 100.0,
    "repairability_level": "HIGH",
    "repair_reason": "Device has zero to one minor faulty component with simple replacement requirements."
  },
  "reuse_score": {
    "total_score": 87.0,
    "reuse_level": "HIGH REUSE POTENTIAL",
    "factor_scores": {
      "functionality": 100.0,
      "physical_condition": 80.0,
      "repairability": 100.0,
      "component_recovery": 100.0,
      "remaining_life": 68.75,
      "recyclability": 90.0
    },
    "weights": {
      "functionality": 0.3,
      "physical_condition": 0.2,
      "repairability": 0.15,
      "component_recovery": 0.2,
      "remaining_life": 0.1,
      "recyclability": 0.05
    },
    "weighted_contributions": {
      "functionality": 30.0,
      "physical_condition": 16.0,
      "repairability": 15.0,
      "component_recovery": 20.0,
      "remaining_life": 6.88,
      "recyclability": 4.5
    },
    "explanation": "Overall Reuse Potential Score is 87.0/100 (HIGH REUSE POTENTIAL). Functionality score (100.0/100) contributes 30.0 points based on working state. Physical condition (80.0/100) contributes 16.0 points based on surface wear. Repairability index (100.0/100) contributes 15.0 points. Estimated remaining lifespan (5.5 years) contributes 6.88 points. Component recovery potential contributes 20.0 points based on parts harvestable."
  },
  "recommendation": {
    "recommended_action": "DIRECT_REUSE",
    "explanation": "The device functions perfectly with no major physical flaws. It can be redeployed immediately."
  },
  "circular_economy_impact": {
    "landfill_diversion_status": "TOTAL_LANDFILL_AVOIDANCE",
    "estimated_weight_diverted_kg": 2.2,
    "estimated_product_life_extension": "SIGNIFICANT (2-3 years)"
  },
  "analysis_summary": {
    "summary": "Dell Precision 5550 (Laptop) - Graded overall as GOOD. Suggested action: DIRECT_REUSE.",
    "condition": "GOOD",
    "reuse_score": 87.0,
    "reuse_level": "HIGH REUSE POTENTIAL",
    "repairability": 100.0,
    "reusable_component_count": 9,
    "recommended_action": "DIRECT_REUSE",
    "explanation": [
      "Overall Condition: GOOD - Device is fully functional with minimal casing wear and no critical component failures.",
      "Repairability: HIGH - Device has zero to one minor faulty component with simple replacement requirements.",
      "Recommendation: DIRECT_REUSE - The device functions perfectly with no major physical flaws. It can be redeployed immediately.",
      "Impact: TOTAL_LANDFILL_AVOIDANCE with 2.2 kg diverted."
    ]
  }
}
```

---

## 3. Component Recovery Estimation Schema (For non-functional/dead devices)

When a device is marked `power_status: false` or `working_status: false`, it cannot be confirmed as fully functional. Sub-components are assessed under the `component_recovery` list.

### Component Recovery Payload Structure

Each entry in `component_recovery` contains:
* `component` (str): Name of the hardware component (e.g. `RAM`, `SSD`).
* `potential_score` (float): Recovery potential grade from `0` to `100`.
* `potential_level` (str): Rating label (`HIGH`, `MEDIUM`, `LOW`, `VERY LOW / UNKNOWN`).
* `confidence_score` (float): Calculation confidence grade from `0` to `100` (reduced by `20` points if the device does not boot).
* `confidence_level` (str): Confidence rating label (`HIGH`, `MEDIUM`, `LOW`).
* `assessment_status` (str): Grading status (`VERIFIED` if physically tested, `ESTIMATED` if calculated, `UNKNOWN` if missing).
* `reason` (str): Human-readable explainability string for UI rendering.

### Example Non-Functional Device Response

```json
{
  "item_id": "RM-002",
  "device_profile": {
    "item_id": "RM-002",
    "item_name": "Non-Functional Laptop",
    "category": "Laptop",
    "brand": "Dell",
    "model": "Precision 5550",
    "estimated_age": 4.0,
    "working_status": false,
    "power_status": false,
    "physical_condition": "FAIR",
    "functional_condition": "NON_FUNCTIONAL",
    "visible_damage": ["minor_scratches"],
    "damaged_components": [],
    "reusable_components": [],
    "missing_components": [],
    "known_components": {
      "RAM": "8GB",
      "SSD": "512GB"
    },
    "verified_components": []
  },
  "condition_analysis": {
    "physical_grade": "FAIR",
    "physical_explanation": "The device displays noticeable cosmetic wear or moderate damage: minor_scratches.",
    "functional_grade": "NON_FUNCTIONAL",
    "functional_explanation": "The device does not boot or draw power.",
    "overall_grade": "NON_FUNCTIONAL",
    "overall_explanation": "Device is non-functional due to power/operational test failures."
  },
  "component_recovery": [
    {
      "component": "RAM",
      "potential_score": 75.0,
      "potential_level": "HIGH",
      "confidence_score": 75.0,
      "confidence_level": "HIGH",
      "assessment_status": "ESTIMATED",
      "reason": "RAM (8GB) has high recovery potential based on device category and specs, but functionality cannot be confirmed because the device does not power on."
    },
    {
      "component": "SSD",
      "potential_score": 75.0,
      "potential_level": "HIGH",
      "confidence_score": 75.0,
      "confidence_level": "HIGH",
      "assessment_status": "ESTIMATED",
      "reason": "SSD (512GB) has high recovery potential based on device category and specs, but functionality cannot be confirmed because the device does not power on."
    }
  ],
  "recommendation": {
    "recommended_action": "COMPONENT_REUSE",
    "explanation": "The complete device is not currently suitable for direct reuse because it does not power on. However, several components have high estimated recovery potential and may be suitable for component reuse."
  }
}
```

---

## 4. UI and Frontend Integration (analysis_summary)

The `analysis_summary` object inside the output payload is designed for fast rendering of frontend cards:
1. **Reuse Score Meter**: Bind `reuse_score` (e.g. `87.0`) and `reuse_level` (e.g. `HIGH REUSE POTENTIAL`) to a circular gauge.
2. **Condition Badge**: Draw a badge using `condition` (e.g., `GOOD` or `POOR`) with context-aware CSS colors.
3. **Component Recovery list**: For non-functional devices, iterate over `component_recovery` to display component cards containing estimated potential levels, confidence scores, and description tooltips.
4. **Lifecycle Timeline**: Render `status_history` in sequence to display the device custody tracking trail.
