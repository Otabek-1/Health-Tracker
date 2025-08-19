// Health Tracker Bot Dashboard JavaScript

class HealthTrackerDashboard {
    constructor() {
        this.activityChart = null;
        this.recordTypesChart = null;
        this.updateInterval = null;
        
        // Initialize dashboard
        this.init();
    }
    
    init() {
        console.log('Initializing Health Tracker Dashboard...');
        
        // Load initial data
        this.loadDashboardData();
        
        // Set up auto-refresh
        this.startAutoRefresh();
        
        // Update last updated timestamp
        this.updateTimestamp();
        
        console.log('Dashboard initialized successfully');
    }
    
    async loadDashboardData() {
        try {
            // Load health check data
            await this.loadHealthCheck();
            
            // Load statistics
            await this.loadStats();
            
            // Load activity chart
            await this.loadActivityChart();
            
        } catch (error) {
            console.error('Error loading dashboard data:', error);
            this.showError('Failed to load dashboard data');
        }
    }
    
    async loadHealthCheck() {
        try {
            const response = await fetch('/health');
            const data = await response.json();
            
            const statusElement = document.getElementById('bot-status');
            
            if (response.ok && data.status === 'healthy') {
                statusElement.innerHTML = '<i class="fas fa-check-circle text-success me-2"></i>Online';
                statusElement.className = 'card-text status-online';
            } else {
                statusElement.innerHTML = '<i class="fas fa-exclamation-triangle text-danger me-2"></i>Issues Detected';
                statusElement.className = 'card-text status-offline';
            }
            
        } catch (error) {
            console.error('Health check failed:', error);
            const statusElement = document.getElementById('bot-status');
            statusElement.innerHTML = '<i class="fas fa-times-circle text-danger me-2"></i>Offline';
            statusElement.className = 'card-text status-offline';
        }
    }
    
    async loadStats() {
        try {
            const response = await fetch('/stats');
            const data = await response.json();
            
            if (response.ok) {
                // Update stat cards
                document.getElementById('total-users').innerHTML = 
                    `<strong>${data.total_users.toLocaleString()}</strong>`;
                    
                document.getElementById('total-records').innerHTML = 
                    `<strong>${data.total_records.toLocaleString()}</strong>`;
                    
                document.getElementById('active-users').innerHTML = 
                    `<strong>${data.active_users_week.toLocaleString()}</strong> <small class="text-muted">this week</small>`;
                
                // Update record types chart
                this.updateRecordTypesChart(data.record_types);
                
            } else {
                throw new Error('Failed to load stats');
            }
            
        } catch (error) {
            console.error('Stats loading failed:', error);
            this.showStatsError();
        }
    }
    
    async loadActivityChart() {
        try {
            const response = await fetch('/api/recent-activity');
            const data = await response.json();
            
            if (response.ok) {
                this.updateActivityChart(data);
            } else {
                throw new Error('Failed to load activity data');
            }
            
        } catch (error) {
            console.error('Activity chart loading failed:', error);
            this.showChartError('activityChart');
        }
    }
    
    updateActivityChart(data) {
        const ctx = document.getElementById('activityChart').getContext('2d');
        
        // Prepare data for Chart.js
        const labels = data.map(item => {
            const date = new Date(item.date);
            return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
        }).reverse();
        
        const counts = data.map(item => item.count).reverse();
        
        // Destroy existing chart if it exists
        if (this.activityChart) {
            this.activityChart.destroy();
        }
        
        this.activityChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Daily Records',
                    data: counts,
                    borderColor: 'rgb(0, 123, 255)',
                    backgroundColor: 'rgba(0, 123, 255, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false,
                    }
                },
                scales: {
                    x: {
                        grid: {
                            display: false
                        }
                    },
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(0,0,0,0.1)'
                        }
                    }
                },
                interaction: {
                    mode: 'nearest',
                    axis: 'x',
                    intersect: false
                }
            }
        });
    }
    
    updateRecordTypesChart(recordTypes) {
        const ctx = document.getElementById('recordTypesChart').getContext('2d');
        
        // Prepare data
        const labels = Object.keys(recordTypes).map(type => 
            type.charAt(0).toUpperCase() + type.slice(1)
        );
        const data = Object.values(recordTypes);
        
        // Color scheme
        const colors = [
            '#007bff', // Blue
            '#28a745', // Green
            '#17a2b8', // Cyan
            '#ffc107', // Yellow
            '#dc3545', // Red
            '#6c757d', // Gray
            '#fd7e14', // Orange
            '#6f42c1'  // Purple
        ];
        
        // Destroy existing chart if it exists
        if (this.recordTypesChart) {
            this.recordTypesChart.destroy();
        }
        
        this.recordTypesChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: data,
                    backgroundColor: colors.slice(0, labels.length),
                    borderWidth: 2,
                    borderColor: '#fff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            padding: 20,
                            usePointStyle: true
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = ((context.raw / total) * 100).toFixed(1);
                                return `${context.label}: ${context.raw} (${percentage}%)`;
                            }
                        }
                    }
                },
                cutout: '60%'
            }
        });
    }
    
    showStatsError() {
        document.getElementById('total-users').innerHTML = '<span class="text-danger">Error</span>';
        document.getElementById('total-records').innerHTML = '<span class="text-danger">Error</span>';
        document.getElementById('active-users').innerHTML = '<span class="text-danger">Error</span>';
    }
    
    showChartError(chartId) {
        const canvas = document.getElementById(chartId);
        const ctx = canvas.getContext('2d');
        ctx.font = '16px Arial';
        ctx.fillStyle = '#dc3545';
        ctx.textAlign = 'center';
        ctx.fillText('Failed to load chart data', canvas.width / 2, canvas.height / 2);
    }
    
    showError(message) {
        console.error('Dashboard Error:', message);
        
        // You could show a toast notification or alert here
        const alertDiv = document.createElement('div');
        alertDiv.className = 'alert alert-danger alert-dismissible fade show position-fixed';
        alertDiv.style.top = '20px';
        alertDiv.style.right = '20px';
        alertDiv.style.zIndex = '9999';
        alertDiv.innerHTML = `
            <i class="fas fa-exclamation-triangle me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(alertDiv);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 5000);
    }
    
    startAutoRefresh() {
        // Refresh every 30 seconds
        this.updateInterval = setInterval(() => {
            this.loadDashboardData();
            this.updateTimestamp();
        }, 30000);
    }
    
    updateTimestamp() {
        const now = new Date();
        const timestamp = now.toLocaleString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        });
        
        const element = document.getElementById('last-updated');
        if (element) {
            element.textContent = timestamp;
        }
    }
    
    destroy() {
        // Clean up resources
        if (this.updateInterval) {
            clearInterval(this.updateInterval);
        }
        
        if (this.activityChart) {
            this.activityChart.destroy();
        }
        
        if (this.recordTypesChart) {
            this.recordTypesChart.destroy();
        }
    }
}

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.dashboard = new HealthTrackerDashboard();
});

// Clean up when page is unloaded
window.addEventListener('beforeunload', () => {
    if (window.dashboard) {
        window.dashboard.destroy();
    }
});

// Handle visibility change (pause updates when tab is not visible)
document.addEventListener('visibilitychange', () => {
    if (window.dashboard) {
        if (document.hidden) {
            clearInterval(window.dashboard.updateInterval);
        } else {
            window.dashboard.startAutoRefresh();
            window.dashboard.loadDashboardData();
        }
    }
});
