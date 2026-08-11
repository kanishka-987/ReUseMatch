document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('submissionForm');
    const matchesList = document.getElementById('matchesList');
    const syncStatus = document.getElementById('syncStatus');
    
    // Timeline steps
    const steps = {
        object: document.getElementById('step-object'),
        condition: document.getElementById('step-condition'),
        need: document.getElementById('step-need'),
        logistics: document.getElementById('step-logistics')
    };

    // Attempt to test backend connectivity
    let backendActive = false;
    fetch('/health')
        .then(res => res.json())
        .then(data => {
            if (data.status === 'healthy') {
                backendActive = true;
                syncStatus.textContent = 'Connected to Backend (Active)';
                syncStatus.style.color = '#10b981';
            }
        })
        .catch(() => {
            syncStatus.textContent = 'API Offline (Running Simulation Mode)';
            syncStatus.style.color = '#f59e0b';
        });

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const itemName = document.getElementById('itemName').value;
        const itemDescription = document.getElementById('itemDescription').value;
        const itemLocation = document.getElementById('itemLocation').value;

        // Reset timeline statuses
        resetTimeline();
        matchesList.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">⚙️</div>
                <p>Orchestrator running agents sequence. Please look at the execution monitor...</p>
            </div>
        `;

        try {
            // Stage 1: Object Agent
            await runStep('object', 'Identifying...', 1000);
            
            // Stage 2: Condition Agent
            await runStep('condition', 'Grading...', 1000);
            
            // Stage 3: Need Agent
            await runStep('need', 'Matching...', 1000);
            
            // Stage 4: Logistics Agent
            await runStep('logistics', 'Routing...', 1000);

            // Fetch actual result or generate mock
            let finalResult;
            
            if (backendActive) {
                const response = await fetch('/api/matches/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        name: itemName,
                        description: itemDescription,
                        location: itemLocation
                    })
                });
                finalResult = await response.json();
            } else {
                // Generate high fidelity mock response mimicking backend orchestrator
                finalResult = generateMockMatches(itemName, itemDescription, itemLocation);
            }

            renderMatches(finalResult.matches);
            
        } catch (error) {
            console.error('Error during pipeline execution:', error);
            matchesList.innerHTML = `
                <div class="empty-state" style="color: #ef4444;">
                    <div class="empty-icon">⚠️</div>
                    <p>Error running matching pipeline. Check console logs.</p>
                </div>
            `;
        }
    });

    function resetTimeline() {
        Object.keys(steps).forEach(key => {
            steps[key].className = 'timeline-step pending';
            steps[key].querySelector('.status-pill').textContent = 'Idle';
        });
    }

    function runStep(key, statusText, duration) {
        return new Promise((resolve) => {
            steps[key].className = 'timeline-step active';
            steps[key].querySelector('.status-pill').textContent = statusText;
            
            setTimeout(() => {
                steps[key].className = 'timeline-step completed';
                steps[key].querySelector('.status-pill').textContent = 'Completed';
                resolve();
            }, duration);
        });
    }

    function generateMockMatches(name, desc, location) {
        // Standard mockup generation logic matching the orchestration rules
        const isFurniture = desc.toLowerCase().includes('table') || desc.toLowerCase().includes('chair');
        
        return {
            item_name: name,
            category: isFurniture ? 'Furniture' : 'General Goods',
            condition: desc.toLowerCase().includes('scratch') ? 'Good' : 'Like New',
            status: 'matched',
            matches: [
                {
                    recipient: {
                        organization_id: 'org_001',
                        organization_name: 'Community Housing Shelter',
                        priority: 'High'
                    },
                    logistics: {
                        origin: location,
                        destination: 'Community Housing Shelter Center, Downtown',
                        distance_km: 12.5,
                        estimated_cost_usd: 18.75,
                        recommended_mode: 'Local Pickup Courier'
                    },
                    score: 9.2
                },
                {
                    recipient: {
                        organization_id: 'org_002',
                        organization_name: 'Second Chance Goods',
                        priority: 'Medium'
                    },
                    logistics: {
                        origin: location,
                        destination: 'Second Chance Goods Warehouse, Northside',
                        distance_km: 24.1,
                        estimated_cost_usd: 36.15,
                        recommended_mode: 'Standard Shipping'
                    },
                    score: 8.5
                }
            ]
        };
    }

    function renderMatches(matches) {
        if (!matches || matches.length === 0) {
            matchesList.innerHTML = `
                <div class="empty-state">
                    <div class="empty-icon">🍃</div>
                    <p>No recipient match found for this category or condition grade.</p>
                </div>
            `;
            return;
        }

        matchesList.innerHTML = '';
        matches.forEach(match => {
            const card = document.createElement('div');
            card.className = 'match-card';
            card.innerHTML = `
                <div class="match-main-info">
                    <span class="match-title">${match.recipient.organization_name}</span>
                    <div class="match-meta-grid">
                        <div class="meta-item">📍 <span>${match.logistics.distance_km} km away</span></div>
                        <div class="meta-item">🚚 <span>${match.logistics.recommended_mode}</span></div>
                        <div class="meta-item">💵 <span>Est: $${match.logistics.estimated_cost_usd}</span></div>
                        <div class="meta-item">⚠️ <span>Priority: ${match.recipient.priority}</span></div>
                    </div>
                </div>
                <div class="match-score-badge">
                    <span class="score-num">${match.score.toFixed(1)}</span>
                    <span class="score-label">Reuse Score</span>
                </div>
            `;
            matchesList.appendChild(card);
        });
    }
});
