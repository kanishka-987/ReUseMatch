export const INITIAL_DEVICES = [
  {
    id: "DEV-1092",
    title: "Apple MacBook Pro 16\" (2021 M1 Pro)",
    category: "Laptops",
    brand: "Apple",
    model: "MacBook Pro A2442",
    serialNumber: "C02G4589MD6R",
    condition: "Like New",
    status: "Matched",
    usabilityScore: 94,
    repairabilityScore: 78,
    circularScore: 92,
    location: "742 Evergreen Terrace, Springfield, IL",
    specs: {
      processor: "Apple M1 Pro (10-Core)",
      ram: "16 GB Unified",
      storage: "512 GB SSD",
      batteryHealth: "91% (142 cycles)",
      display: "16.2-inch Liquid Retina XDR"
    },
    images: [
      "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=crop&w=800&q=80",
      "https://images.unsplash.com/photo-1611186871348-b1ce696e52c9?auto=format&fit=crop&w=800&q=80"
    ],
    environmentalSavings: {
      co2Kg: 285,
      waterLiters: 1420,
      eWasteKg: 2.1
    },
    createdAt: "2026-08-01T10:30:00Z",
    owner: "Alex Morgan",
    matchedRecipient: "Springfield STEM Academy",
    passportHash: "0x8f93a2b1c4e5d6f7a8b9c0d1e2f3a4b5c6d7e8f9"
  },
  {
    id: "DEV-2041",
    title: "Dell XPS 15 9520 OLED",
    category: "Laptops",
    brand: "Dell",
    model: "XPS 15 9520",
    serialNumber: "57B9X23",
    condition: "Good",
    status: "Diagnosed",
    usabilityScore: 82,
    repairabilityScore: 88,
    circularScore: 85,
    location: "100 Michigan Ave, Chicago, IL",
    specs: {
      processor: "Intel Core i7-12700H",
      ram: "32 GB DDR5",
      storage: "1 TB NVMe SSD",
      batteryHealth: "78%",
      display: "15.6\" 3.5K OLED Touch"
    },
    images: [
      "https://images.unsplash.com/photo-1593642632823-8f785ba67e45?auto=format&fit=crop&w=800&q=80"
    ],
    environmentalSavings: {
      co2Kg: 240,
      waterLiters: 1100,
      eWasteKg: 1.9
    },
    createdAt: "2026-08-05T14:15:00Z",
    owner: "Jordan Taylor",
    matchedRecipient: null,
    passportHash: "0x1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b"
  },
  {
    id: "DEV-3058",
    title: "Apple iPhone 12 Pro 128GB",
    category: "Smartphones",
    brand: "Apple",
    model: "iPhone 12 Pro",
    serialNumber: "DNQF89320D1",
    condition: "Fair",
    status: "Evaluating",
    usabilityScore: 71,
    repairabilityScore: 65,
    circularScore: 74,
    location: "450 Sutter St, San Francisco, CA",
    specs: {
      processor: "A14 Bionic",
      ram: "6 GB",
      storage: "128 GB",
      batteryHealth: "76% (Replace recommended)",
      display: "6.1\" Super Retina XDR"
    },
    images: [
      "https://images.unsplash.com/photo-1605236453806-6ff36851218e?auto=format&fit=crop&w=800&q=80"
    ],
    environmentalSavings: {
      co2Kg: 70,
      waterLiters: 450,
      eWasteKg: 0.2
    },
    createdAt: "2026-08-09T09:00:00Z",
    owner: "Samantha Reed",
    matchedRecipient: null,
    passportHash: "0x9a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b"
  },
  {
    id: "DEV-4019",
    title: "Apple iPad Air (4th Gen) 64GB Wi-Fi",
    category: "Tablets",
    brand: "Apple",
    model: "iPad Air 4",
    serialNumber: "GG7F92031K",
    condition: "Like New",
    status: "Approved",
    usabilityScore: 96,
    repairabilityScore: 72,
    circularScore: 94,
    location: "1200 Market St, Philadelphia, PA",
    specs: {
      processor: "A14 Bionic",
      ram: "4 GB",
      storage: "64 GB",
      batteryHealth: "94%",
      display: "10.9\" Liquid Retina"
    },
    images: [
      "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?auto=format&fit=crop&w=800&q=80"
    ],
    environmentalSavings: {
      co2Kg: 120,
      waterLiters: 680,
      eWasteKg: 0.5
    },
    createdAt: "2026-08-10T11:20:00Z",
    owner: "Marcus Vance",
    matchedRecipient: "City Youth Community Center",
    passportHash: "0x3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d"
  },
  {
    id: "DEV-5099",
    title: "Sony WH-1000XM4 Headphones",
    category: "Audio",
    brand: "Sony",
    model: "WH-1000XM4",
    serialNumber: "SN8849201",
    condition: "Good",
    status: "In Transit",
    usabilityScore: 89,
    repairabilityScore: 82,
    circularScore: 90,
    location: "88 University Ave, Austin, TX",
    specs: {
      processor: "QN1 HD Noise Canceling",
      batteryHealth: "88%",
      connectivity: "Bluetooth 5.0 / LDAC"
    },
    images: [
      "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=800&q=80"
    ],
    environmentalSavings: {
      co2Kg: 45,
      waterLiters: 310,
      eWasteKg: 0.3
    },
    createdAt: "2026-08-08T16:45:00Z",
    owner: "Elena Rostova",
    matchedRecipient: "Austin Public Library Digital Lab",
    passportHash: "0x7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b"
  }
];

export const MOCK_AGENTS = {
  object_agent: {
    id: "agent_obj",
    name: "Object Identification Agent",
    version: "v2.4.1",
    type: "Computer Vision & Taxonomy",
    status: "Completed",
    confidence: 0.98,
    details: "Identified hardware model, manufacturer specs, release year, and original MSRP.",
    lastExecutionMs: 420
  },
  condition_agent: {
    id: "agent_cond",
    name: "Condition Assessment Agent",
    version: "v3.1.0",
    type: "Quality & Wear Scoring",
    status: "Completed",
    confidence: 0.94,
    details: "Calculated battery decay index, chassis wear, display integrity, and repair feasibility.",
    lastExecutionMs: 650
  },
  need_agent: {
    id: "agent_need",
    name: "Need Matching Agent",
    version: "v1.9.3",
    type: "Social Impact & Recipient Ranking",
    status: "Completed",
    confidence: 0.96,
    details: "Cross-referenced 48 local schools, non-profits, and refurbishers for urgent digital access needs.",
    lastExecutionMs: 810
  },
  logistics_agent: {
    id: "agent_log",
    name: "Logistics Optimization Agent",
    version: "v2.0.5",
    type: "Transit & Carbon Minimization",
    status: "Completed",
    confidence: 0.92,
    details: "Calculated optimal local courier pickup, zero-emission route, and total shipping cost.",
    lastExecutionMs: 540
  },
  coordinator_agent: {
    id: "agent_coord",
    name: "Orchestrator Agent",
    version: "v4.0.0",
    type: "Decision Matrix Engine",
    status: "Completed",
    confidence: 0.97,
    details: "Aggregated agent outputs to compute final circular economy match recommendation.",
    lastExecutionMs: 310
  }
};

export const MOCK_MATCHES = [
  {
    id: "MATCH-801",
    recipientName: "Springfield STEM Academy",
    type: "School / Non-Profit",
    matchScore: 97,
    distanceKm: 4.2,
    estimatedImpact: "Provides laptop access for 1 high school student for 3 years",
    logisticsCost: "$12.50 (Local Eco-Courier)",
    urgentNeed: "High - 45 students without personal devices",
    recommendedAction: "Direct Donation"
  },
  {
    id: "MATCH-802",
    recipientName: "Community Tech Refurbishers",
    type: "Refurbishment Hub",
    matchScore: 89,
    distanceKm: 8.7,
    estimatedImpact: "Battery upgrade & redistribution to local job seekers",
    logisticsCost: "$18.00 (Standard Transit)",
    urgentNeed: "Medium - Hardware queue open",
    recommendedAction: "Refurbish & Re-sell at subsidized cost"
  },
  {
    id: "MATCH-803",
    recipientName: "EcoRecycle E-Waste Solutions",
    type: "Certified Recycler",
    matchScore: 62,
    distanceKm: 14.1,
    estimatedImpact: "Precious metal extraction (Gold, Copper, Lithium recovery)",
    logisticsCost: "$22.00 (Bulk Freight)",
    urgentNeed: "Low - Component salvage",
    recommendedAction: "Component Recycling"
  }
];

export const MOCK_LOGISTICS_TIMELINE = [
  {
    step: "Match Confirmed",
    date: "Aug 10, 2026 - 10:00 AM",
    status: "Completed",
    description: "Donor and recipient approved the match recommendation."
  },
  {
    step: "Courier Assigned",
    date: "Aug 10, 2026 - 02:30 PM",
    status: "Completed",
    description: "GreenCycle Electric Cargo Bike #41 assigned for pickup."
  },
  {
    step: "Item Picked Up",
    date: "Aug 11, 2026 - 09:15 AM",
    status: "Completed",
    description: "Verified package code at donor address (742 Evergreen Terrace)."
  },
  {
    step: "In Transit",
    date: "Aug 11, 2026 - Current",
    status: "Active",
    description: "En route to Springfield STEM Academy (Eta: 45 minutes)."
  },
  {
    step: "Delivery & Verification",
    date: "Pending",
    status: "Upcoming",
    description: "Digital proof of delivery & product passport update."
  }
];

export const MOCK_PASSPORT = {
  deviceId: "DEV-1092",
  serialNumber: "C02G4589MD6R",
  manufactureYear: 2021,
  firstPurchase: "Nov 2021 (Retail)",
  lifecycleEvents: [
    { date: "Nov 15, 2021", event: "Manufactured by Apple Inc. (China)", type: "Origin" },
    { date: "Dec 02, 2021", event: "Purchased by Alex Morgan", type: "Ownership" },
    { date: "Jun 14, 2024", event: "Battery Health Inspection (91% capacity)", type: "Maintenance" },
    { date: "Aug 01, 2026", event: "Submitted to ReUseMatch Circular Platform", type: "Platform Entry" },
    { date: "Aug 10, 2026", event: "AI Match Approved for Springfield STEM Academy", type: "Reuse Match" }
  ],
  carbonSavedTotalKg: 285,
  circularValuationUsd: 850
};

export const MOCK_STATS = {
  totalDevicesSaved: 1428,
  eWasteDivertedKg: 3840,
  co2PreventedKg: 41250,
  activeMatches: 84,
  partnerOrganizations: 156
};
