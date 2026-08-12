import {
  INITIAL_DEVICES,
  MOCK_AGENTS,
  MOCK_MATCHES,
  MOCK_LOGISTICS_TIMELINE,
  MOCK_PASSPORT,
  MOCK_STATS
} from '../data/mockData';

const STORAGE_KEY = 'reusematch_devices';

// Helper to load devices from localStorage or initialize with mock data
const loadStoredDevices = () => {
  const stored = localStorage.getItem(STORAGE_KEY);
  if (!stored) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(INITIAL_DEVICES));
    return INITIAL_DEVICES;
  }
  try {
    return JSON.parse(stored);
  } catch (e) {
    console.error("Failed to parse stored devices", e);
    return INITIAL_DEVICES;
  }
};

const saveDevices = (devices) => {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(devices));
};

const delay = (ms = 400) => new Promise(resolve => setTimeout(resolve, ms));

export const api = {
  // Execute complete 5-Agent pipeline
  async runPipeline(description, location = "123 Main St", imageUrl = null) {
    await delay(600);
    const descLower = description.lower ? description.lower() : String(description).toLowerCase();

    // 1. Evidence Agent
    let identifiedName = "Generic Unused Item";
    let category = "General";
    let attrs = ["general"];

    if (descLower.includes("laptop") || descLower.includes("dell") || descLower.includes("macbook")) {
      identifiedName = descLower.includes("dell") ? "Dell Laptop" : "MacBook Pro";
      category = "Electronics";
      attrs = ["electronics", "laptop", "portable"];
    } else if (descLower.includes("table") || descLower.includes("desk") || descLower.includes("chair")) {
      identifiedName = "Generic Wooden Table";
      category = "Furniture";
      attrs = ["wood", "furniture"];
    }

    const observedEvidence = [];
    if (descLower.includes("scratch") || descLower.includes("scratches")) {
      observedEvidence.append ? observedEvidence.append("Visible surface scratches on chassis") : observedEvidence.push("Visible surface scratches on chassis");
    }
    if (descLower.includes("turns on") || descLower.includes("working")) {
      observedEvidence.push("Device powers on successfully");
    }
    if (descLower.includes("broken") || descLower.includes("damaged")) {
      observedEvidence.push("Structural component damage observed");
    }
    if (observedEvidence.length === 0) {
      observedEvidence.push("Item submitted in baseline state");
    }

    const evidence = {
      status: "Success",
      source: "mock_fallback",
      observed_evidence: observedEvidence,
      functional_claims: ["User claims item is in functional condition"],
      missing_information: ["Purchase receipt", "Inner diagnostic log"],
      confidence: 0.88,
      item_details: {
        identified_name: identifiedName,
        category: category,
        detected_attributes: attrs
      }
    };

    // 2. Diagnosis Agent
    let conditionGrade = "Good";
    let conditionScore = 7.0;

    if (descLower.includes("destroy") || descLower.includes("beyond repair") || descLower.includes("recycl")) {
      conditionGrade = "Poor";
      conditionScore = 2.0;
    } else if (descLower.includes("damaged") || descLower.includes("broken")) {
      conditionGrade = "Fair";
      conditionScore = 4.0;
    } else if (descLower.includes("scratch") || descLower.includes("wear")) {
      conditionGrade = "Good";
      conditionScore = 7.0;
    } else {
      conditionGrade = "Like New";
      conditionScore = 9.0;
    }

    const diagnosis = {
      status: "Success",
      condition_score: conditionScore,
      condition_grade: conditionGrade,
      repairability: conditionGrade === "Poor" ? "Low" : (conditionGrade === "Fair" ? "Medium" : "High"),
      reuse_potential: conditionGrade === "Poor" ? "Low (Salvage)" : "High",
      likely_repairs: conditionGrade === "Poor" ? ["Full disassembly for recycling"] : ["Cosmetic cleaning & inspection"],
      risks: conditionGrade === "Poor" ? ["Unviable repair cost exceeding device value"] : ["Minor cosmetic blemish"],
      confidence_score: 0.85,
      condition_notes: "Assessed via condition heuristics."
    };

    // 3. Decision Agent
    let bestAction = "REUSE";
    let reasoning = "Item is in good working order suitable for direct community reuse.";
    let alternatives = ["DONATE", "REPAIR"];

    if (descLower.includes("recycle") || descLower.includes("beyond repair") || conditionGrade === "Poor") {
      bestAction = "RECYCLE";
      reasoning = "Device is severely degraded or explicitly flagged for component breakdown and material recycling.";
      alternatives = ["SALVAGE_PARTS"];
    } else if (descLower.includes("repair")) {
      bestAction = "REPAIR";
      reasoning = "Device retains high core functional value but requires component repair before redistribution.";
      alternatives = ["REUSE", "DONATE"];
    } else if (conditionScore >= 8.0) {
      bestAction = "DONATE";
      reasoning = "High usability score makes device ideal for direct donation to educational or non-profit recipients.";
      alternatives = ["REUSE", "RESELL"];
    }

    const decision = {
      status: "Success",
      best_lifecycle_action: bestAction,
      reasoning: reasoning,
      alternatives: alternatives,
      confidence_score: 0.90
    };

    // 4. Need Agent
    let needRes = {
      status: "Success",
      matching_organizations_count: 0,
      matches: [],
      skip_reason: null
    };

    if (bestAction === "RECYCLE") {
      needRes = {
        status: "Skipped",
        matching_organizations_count: 0,
        matches: [],
        skip_reason: "Recipient matching was bypassed because the lifecycle decision is RECYCLE."
      };
    } else {
      // Standard matching logic
      const orgList = [
        { organization_name: "Community Housing Shelter", organization_id: "org_001", priority: "Medium", match_score: 85, reason: "Needs furniture and tech for shelter", location: "Community Housing Shelter Center, Downtown", missing_information: "None" },
        { organization_name: "Kids Club Foundation", organization_id: "org_003", priority: "High", match_score: 92, reason: "Youth learning center expansion", location: "Kids Club Center, Northside", missing_information: "None" }
      ];

      // Check if user specifically requested an un-matchable item category
      if (descLower.includes("unmatchable") || descLower.includes("no match")) {
        needRes = {
          status: "Success",
          matching_organizations_count: 0,
          matches: [],
          skip_reason: null
        };
      } else {
        needRes = {
          status: "Success",
          matching_organizations_count: orgList.length,
          matches: orgList,
          skip_reason: null
        };
      }
    }

    // 5. Logistics Agent
    let logisticsRes = [];
    if (bestAction === "RECYCLE") {
      logisticsRes = [];
    } else if (needRes.matches.length > 0) {
      logisticsRes = needRes.matches.map(m => ({
        origin: location,
        destination: m.location,
        distance_km: 12.5,
        estimated_cost_usd: 18.75,
        recommended_mode: "Local Pickup Courier",
        route_status: "optimal"
      }));
    }

    const finalRecommendation = {
      item_name: identifiedName,
      category: category,
      condition: conditionGrade,
      recommended_lifecycle_action: bestAction,
      recipient_organizations: needRes.matches.length > 0 ? needRes.matches.map(m => m.organization_name) : ["N/A (Recycled/No match)"],
      estimated_logistics: logisticsRes.length > 0 ? `${logisticsRes[0].recommended_mode} ($${logisticsRes[0].estimated_cost_usd}, ${logisticsRes[0].distance_km} km)` : (bestAction === "RECYCLE" ? "Skipped (Direct Recycling)" : "Skipped (No match found)")
    };

    return {
      status: bestAction === "RECYCLE" ? "recycled" : (needRes.matches.length > 0 ? "matched" : "no_match_found"),
      item_details: {
        name: identifiedName,
        category: category,
        condition: conditionGrade
      },
      evidence,
      diagnosis,
      decision,
      need: needRes,
      logistics: logisticsRes,
      matches: needRes.matches.map(m => ({
        recipient: { organization_id: m.organization_id, organization_name: m.organization_name, priority: m.priority },
        logistics: { origin: location, destination: m.location, distance_km: 12.5, estimated_cost_usd: 18.75, recommended_mode: "Local Pickup Courier" },
        score: conditionScore
      })),
      final_recommendation: finalRecommendation
    };
  },

  // Fetch all devices
  async getDevices() {
    await delay(300);
    return loadStoredDevices();
  },

  // Fetch a single device by ID
  async getDeviceById(id) {
    await delay(200);
    const devices = loadStoredDevices();
    const found = devices.find(d => d.id === id);
    return found || devices[0];
  },

  // Register new device
  async createDevice(deviceData) {
    await delay(600);
    const devices = loadStoredDevices();
    const newId = `DEV-${Math.floor(1000 + Math.random() * 9000)}`;
    const newDevice = {
      id: newId,
      title: `${deviceData.brand || 'Generic'} ${deviceData.model || 'Device'}`,
      category: deviceData.category || 'Electronics',
      brand: deviceData.brand || 'Unknown',
      model: deviceData.model || 'Custom',
      serialNumber: deviceData.serialNumber || `SN${Math.floor(100000 + Math.random() * 900000)}`,
      condition: deviceData.condition || 'Good',
      status: 'Evaluating',
      usabilityScore: Math.floor(75 + Math.random() * 20),
      repairabilityScore: Math.floor(65 + Math.random() * 30),
      circularScore: Math.floor(80 + Math.random() * 18),
      location: deviceData.location || 'Local Donor Address',
      specs: {
        processor: deviceData.processor || 'Standard Chipset',
        ram: deviceData.ram || '8 GB',
        storage: deviceData.storage || '256 GB',
        batteryHealth: deviceData.batteryHealth || '85%'
      },
      images: deviceData.images && deviceData.images.length > 0 ? deviceData.images : [
        'https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?auto=format&fit=crop&w=800&q=80'
      ],
      environmentalSavings: {
        co2Kg: Math.floor(80 + Math.random() * 150),
        waterLiters: Math.floor(400 + Math.random() * 800),
        eWasteKg: parseFloat((0.3 + Math.random() * 1.5).toFixed(1))
      },
      createdAt: new Date().toISOString(),
      owner: 'Current User',
      matchedRecipient: null,
      passportHash: `0x${Array.from({length: 40}, () => Math.floor(Math.random()*16).toString(16)).join('')}`
    };
    
    devices.unshift(newDevice);
    saveDevices(devices);
    return newDevice;
  },

  // Update device status
  async updateDeviceStatus(id, newStatus, recipient = null) {
    await delay(300);
    const devices = loadStoredDevices();
    const index = devices.findIndex(d => d.id === id);
    if (index !== -1) {
      devices[index].status = newStatus;
      if (recipient) devices[index].matchedRecipient = recipient;
      saveDevices(devices);
      return devices[index];
    }
    return null;
  },

  // Simulated AI Diagnosis execution
  async runDiagnosis(id) {
    await delay(800);
    const device = await this.getDeviceById(id);
    return {
      deviceId: id,
      deviceTitle: device.title,
      usabilityScore: device.usabilityScore,
      repairabilityScore: device.repairabilityScore,
      circularScore: device.circularScore,
      diagnosisSummary: "Item verified by Object & Condition Agents. Functional hardware components in good health.",
      recommendedPath: "Direct Education Donation / Secondary Refurbishment",
      estimatedValuationUsd: Math.floor(device.usabilityScore * 8.5)
    };
  },

  // Get Agent execution breakdown & logs
  async getAgentLogs(id) {
    await delay(300);
    return {
      deviceId: id,
      agents: MOCK_AGENTS,
      executionSteps: [
        { agent: "Evidence Agent", time: "10:00:02 AM", status: "Success", log: "Analyzed visual parameters & user claims. Matched category: Electronics." },
        { agent: "Diagnosis Agent", time: "10:00:04 AM", status: "Success", log: "Evaluated hardware condition & structural wear index." },
        { agent: "Decision Agent", time: "10:00:05 AM", status: "Success", log: "Classified optimal lifecycle action: REUSE." },
        { agent: "Need Agent", time: "10:00:06 AM", status: "Success", log: "Scanned recipient database. Identified priority matches." },
        { agent: "Logistics Agent", time: "10:00:08 AM", status: "Success", log: "Calculated eco-courier route & distance." }
      ]
    };
  },

  // Get recipient matches
  async getMatches(id) {
    await delay(400);
    return MOCK_MATCHES;
  },

  // Get orchestrator recommendation
  async getRecommendation(id) {
    await delay(350);
    const device = await this.getDeviceById(id);
    return {
      deviceId: id,
      primaryMatch: MOCK_MATCHES[0],
      alternativeMatches: MOCK_MATCHES.slice(1),
      reasoning: "Springfield STEM Academy exhibits the highest alignment due to zero digital access among students.",
      circularImpact: {
        co2AvoidedKg: device.environmentalSavings?.co2Kg || 285,
        socialBenefitIndex: "98/100",
        economicValuationUsd: `$${Math.floor(device.usabilityScore * 8.5)}`
      }
    };
  },

  // Approve recommendation
  async approveRecommendation(id, matchId) {
    await delay(500);
    const match = MOCK_MATCHES.find(m => m.id === matchId) || MOCK_MATCHES[0];
    await this.updateDeviceStatus(id, "Approved", match.recipientName);
    return { success: true, status: "Approved", recipient: match.recipientName };
  },

  // Get logistics route & timeline
  async getLogistics(id) {
    await delay(300);
    const device = await this.getDeviceById(id);
    return {
      deviceId: id,
      origin: device.location,
      destination: device.matchedRecipient || "Springfield STEM Academy",
      carrier: "GreenCycle Eco-Courier",
      mode: "Electric Cargo Bike",
      estimatedCarbonSavedKg: device.environmentalSavings?.co2Kg || 285,
      timeline: MOCK_LOGISTICS_TIMELINE
    };
  },

  // Get ReUse Passport lifecycle data
  async getPassport(id) {
    await delay(300);
    const device = await this.getDeviceById(id);
    return {
      ...MOCK_PASSPORT,
      deviceId: device.id,
      title: device.title,
      serialNumber: device.serialNumber,
      passportHash: device.passportHash,
      carbonSavedTotalKg: device.environmentalSavings?.co2Kg || 285
    };
  },

  // Global platform impact statistics
  async getStats() {
    await delay(200);
    return MOCK_STATS;
  }
};
