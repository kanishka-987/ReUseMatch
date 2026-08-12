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
    if (!found) {
      // Fallback to first device if ID not found for demo resilience
      return devices[0];
    }
    return found;
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
      diagnosisSummary: "Item verified by Object & Condition Agents. Functional hardware components in good health. Minor battery capacity degradation detected.",
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
        { agent: "Object Agent", time: "10:00:02 AM", status: "Success", log: "Analyzed visual parameters. Matched category: Electronics." },
        { agent: "Condition Agent", time: "10:00:04 AM", status: "Success", log: "Evaluated hardware condition. Computed wear index: 14%." },
        { agent: "Need Agent", time: "10:00:06 AM", status: "Success", log: "Scanned recipient database. Identified 3 priority matches." },
        { agent: "Logistics Agent", time: "10:00:08 AM", status: "Success", log: "Calculated eco-courier route. Distance: 4.2 km." },
        { agent: "Orchestrator Agent", time: "10:00:09 AM", status: "Success", log: "Aggregated agent outputs into final recommendation." }
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
      reasoning: "Springfield STEM Academy exhibits the highest alignment due to zero digital access among 45 students, combined with optimal proximity (4.2 km) minimizing transit emissions.",
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
