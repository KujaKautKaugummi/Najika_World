/**
 * Najika World Admin Dashboard
 * Complete admin panel for user, training, and system management
 */

class AdminDashboard {
    constructor() {
        // API Configuration
        this.apiBaseUrl = this.getApiBaseUrl();
        this.authToken = localStorage.getItem('admin_token') || '';

        // Data storage
        this.users = [];
        this.trainingJobs = [];
        this.logs = [];
        this.stats = {
            totalUsers: 0,
            activeUsers: 0,
            trainingJobs: 0,
            systemHealth: 'Unknown'
        };
        this.systemMetrics = {
            cpu: 0,
            memory: 0,
            disk: 0,
            uptime: 0
        };

        // Current section
        this.currentSection = 'overview';

        // Refresh intervals
        this.refreshIntervals = {
            stats: null,
            users: null,
            training: null,
            system: null,
            logs: null
        };

        // Initialize
        this.init();
    }

    /**
     * Get API base URL
     */
    getApiBaseUrl() {
        const protocol = window.location.protocol === 'https:' ? 'https:' : 'http:';
        const hostname = window.location.hostname;
        const port = hostname === 'localhost' ? '8000' : window.location.port;
        return `${protocol}//${hostname}:${port}/api`;
    }

    /**
     * Initialize dashboard
     */
    async init() {
        console.log('🎮 Initializing Admin Dashboard...');

        // Check authentication
        if (!this.authToken) {
            this.showLoginPrompt();
            return;
        }

        // Set up navigation
        this.setupNavigation();

        // Set up event listeners
        this.setupEventListeners();

        // Load initial data
        await this.loadAllData();

        // Start auto-refresh
        this.startAutoRefresh();

        // Display current user
        this.displayCurrentUser();

        console.log('✅ Dashboard initialized');
    }

    /**
     * Show login prompt
     */
    showLoginPrompt() {
        const username = prompt('Admin Username:');
        const password = prompt('Admin Password:');

        if (username && password) {
            this.login(username, password);
        } else {
            alert('Authentication required');
            window.location.href = '/login.html';
        }
    }

    /**
     * Login
     */
    async login(username, password) {
        try {
            const response = await fetch(`${this.apiBaseUrl}/auth/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, password })
            });

            if (response.ok) {
                const data = await response.json();
                this.authToken = data.access_token;
                localStorage.setItem('admin_token', this.authToken);

                // Reload page to initialize dashboard
                window.location.reload();
            } else {
                alert('Login failed');
                this.showLoginPrompt();
            }
        } catch (error) {
            console.error('Login error:', error);
            alert('Login error. Check console for details.');
        }
    }

    /**
     * Logout
     */
    logout() {
        localStorage.removeItem('admin_token');
        this.authToken = '';
        window.location.href = '/login.html';
    }

    /**
     * Setup navigation
     */
    setupNavigation() {
        const navItems = document.querySelectorAll('.nav-item');

        navItems.forEach(item => {
            item.addEventListener('click', (e) => {
                e.preventDefault();

                // Remove active class from all items
                navItems.forEach(nav => nav.classList.remove('active'));

                // Add active to clicked item
                item.classList.add('active');

                // Get section from data attribute
                const section = item.getAttribute('data-section');
                this.showSection(section);
            });
        });
    }

    /**
     * Show section
     */
    showSection(sectionName) {
        // Hide all sections
        const sections = document.querySelectorAll('.content-section');
        sections.forEach(section => section.classList.remove('active'));

        // Show target section
        const targetSection = document.getElementById(`${sectionName}-section`);
        if (targetSection) {
            targetSection.classList.add('active');
        }

        // Update page title
        const pageTitle = document.getElementById('page-title');
        if (pageTitle) {
            pageTitle.textContent = sectionName.charAt(0).toUpperCase() + sectionName.slice(1);
        }

        // Update current section
        this.currentSection = sectionName;

        // Load section-specific data
        this.loadSectionData(sectionName);
    }

    /**
     * Load section-specific data
     */
    async loadSectionData(section) {
        switch (section) {
            case 'overview':
                await this.loadStats();
                break;
            case 'users':
                await this.loadUsers();
                break;
            case 'training':
                await this.loadTrainingJobs();
                break;
            case 'system':
                await this.loadSystemHealth();
                break;
            case 'logs':
                await this.loadLogs();
                break;
            case 'settings':
                await this.loadSettings();
                break;
        }
    }

    /**
     * Setup event listeners
     */
    setupEventListeners() {
        // Refresh button
        const refreshBtn = document.getElementById('refresh-btn');
        if (refreshBtn) {
            refreshBtn.addEventListener('click', () => this.refresh());
        }

        // Logout button
        const logoutBtn = document.getElementById('logout-btn');
        if (logoutBtn) {
            logoutBtn.addEventListener('click', () => this.logout());
        }

        // Add user button
        const addUserBtn = document.getElementById('add-user-btn');
        if (addUserBtn) {
            addUserBtn.addEventListener('click', () => this.showAddUserDialog());
        }

        // Create training button
        const createTrainingBtn = document.getElementById('create-training-btn');
        if (createTrainingBtn) {
            createTrainingBtn.addEventListener('click', () => this.showCreateTrainingDialog());
        }

        // Log level filter
        const logLevelFilter = document.getElementById('log-level-filter');
        if (logLevelFilter) {
            logLevelFilter.addEventListener('change', (e) => {
                this.filterLogs(e.target.value);
            });
        }

        // Settings form
        const settingsForm = document.getElementById('settings-form');
        if (settingsForm) {
            settingsForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.saveSettings();
            });
        }
    }

    /**
     * Load all initial data
     */
    async loadAllData() {
        await Promise.all([
            this.loadStats(),
            this.loadUsers(),
            this.loadTrainingJobs(),
            this.loadSystemHealth(),
            this.loadLogs()
        ]);
    }

    /**
     * Refresh current section
     */
    async refresh() {
        console.log('🔄 Refreshing...');
        await this.loadSectionData(this.currentSection);
    }

    /**
     * Make API request
     */
    async apiRequest(endpoint, options = {}) {
        const url = `${this.apiBaseUrl}${endpoint}`;

        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.authToken}`
            }
        };

        const finalOptions = {
            ...defaultOptions,
            ...options,
            headers: {
                ...defaultOptions.headers,
                ...(options.headers || {})
            }
        };

        try {
            const response = await fetch(url, finalOptions);

            if (response.status === 401) {
                this.logout();
                throw new Error('Unauthorized');
            }

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            return await response.json();
        } catch (error) {
            console.error(`API Request failed: ${endpoint}`, error);
            throw error;
        }
    }

    /**
     * Load stats for overview
     */
    async loadStats() {
        try {
            // Load user stats
            const usersData = await this.apiRequest('/users');
            this.stats.totalUsers = usersData.length || 0;
            this.stats.activeUsers = usersData.filter(u => u.is_active).length || 0;

            // Load training stats
            const trainingData = await this.apiRequest('/training/jobs');
            this.stats.trainingJobs = trainingData.filter(j => j.status === 'running').length || 0;

            // Load system health
            const systemData = await this.apiRequest('/system/health');
            this.stats.systemHealth = systemData.status || 'Unknown';

            // Update UI
            this.updateStatsUI();
        } catch (error) {
            console.error('Failed to load stats:', error);
        }
    }

    /**
     * Update stats UI
     */
    updateStatsUI() {
        const statTotalUsers = document.getElementById('stat-total-users');
        const statActiveUsers = document.getElementById('stat-active-users');
        const statTrainingJobs = document.getElementById('stat-training-jobs');
        const statSystemHealth = document.getElementById('stat-system-health');

        if (statTotalUsers) statTotalUsers.textContent = this.stats.totalUsers;
        if (statActiveUsers) statActiveUsers.textContent = this.stats.activeUsers;
        if (statTrainingJobs) statTrainingJobs.textContent = this.stats.trainingJobs;
        if (statSystemHealth) {
            statSystemHealth.textContent = this.stats.systemHealth;
            statSystemHealth.className = 'stat-value';

            if (this.stats.systemHealth === 'healthy') {
                statSystemHealth.style.color = 'var(--success-color)';
            } else if (this.stats.systemHealth === 'degraded') {
                statSystemHealth.style.color = 'var(--warning-color)';
            } else {
                statSystemHealth.style.color = 'var(--danger-color)';
            }
        }
    }

    /**
     * Load users
     */
    async loadUsers() {
        try {
            this.users = await this.apiRequest('/users');
            this.updateUsersTable();
        } catch (error) {
            console.error('Failed to load users:', error);
        }
    }

    /**
     * Update users table
     */
    updateUsersTable() {
        const tbody = document.getElementById('users-tbody');
        if (!tbody) return;

        tbody.innerHTML = '';

        this.users.forEach(user => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${user.id}</td>
                <td>${user.username}</td>
                <td>${user.email || 'N/A'}</td>
                <td>
                    <span class="badge ${user.is_active ? 'badge-success' : 'badge-danger'}">
                        ${user.is_active ? 'Active' : 'Inactive'}
                    </span>
                </td>
                <td>
                    <span class="badge ${user.is_admin ? 'badge-warning' : 'badge-secondary'}">
                        ${user.is_admin ? 'Yes' : 'No'}
                    </span>
                </td>
                <td>${new Date(user.created_at).toLocaleDateString()}</td>
                <td>
                    <button class="btn btn-secondary btn-sm" onclick="dashboard.editUser(${user.id})">Edit</button>
                    <button class="btn btn-danger btn-sm" onclick="dashboard.deleteUser(${user.id})">Delete</button>
                    ${!user.is_active ?
                        `<button class="btn btn-success btn-sm" onclick="dashboard.activateUser(${user.id})">Activate</button>` :
                        `<button class="btn btn-warning btn-sm" onclick="dashboard.deactivateUser(${user.id})">Deactivate</button>`
                    }
                </td>
            `;
            tbody.appendChild(row);
        });
    }

    /**
     * Show add user dialog
     */
    showAddUserDialog() {
        const username = prompt('Username:');
        const email = prompt('Email:');
        const password = prompt('Password:');

        if (username && password) {
            this.addUser(username, email, password);
        }
    }

    /**
     * Add user
     */
    async addUser(username, email, password) {
        try {
            await this.apiRequest('/users', {
                method: 'POST',
                body: JSON.stringify({
                    username,
                    email,
                    password
                })
            });

            alert('User created successfully');
            await this.loadUsers();
        } catch (error) {
            alert(`Failed to create user: ${error.message}`);
        }
    }

    /**
     * Edit user
     */
    async editUser(userId) {
        const user = this.users.find(u => u.id === userId);
        if (!user) return;

        const newEmail = prompt('New Email:', user.email);

        if (newEmail !== null) {
            try {
                await this.apiRequest(`/users/${userId}`, {
                    method: 'PATCH',
                    body: JSON.stringify({
                        email: newEmail
                    })
                });

                alert('User updated successfully');
                await this.loadUsers();
            } catch (error) {
                alert(`Failed to update user: ${error.message}`);
            }
        }
    }

    /**
     * Delete user
     */
    async deleteUser(userId) {
        if (!confirm('Are you sure you want to delete this user?')) {
            return;
        }

        try {
            await this.apiRequest(`/users/${userId}`, {
                method: 'DELETE'
            });

            alert('User deleted successfully');
            await this.loadUsers();
        } catch (error) {
            alert(`Failed to delete user: ${error.message}`);
        }
    }

    /**
     * Activate user
     */
    async activateUser(userId) {
        try {
            await this.apiRequest(`/users/${userId}/activate`, {
                method: 'POST'
            });

            alert('User activated');
            await this.loadUsers();
        } catch (error) {
            alert(`Failed to activate user: ${error.message}`);
        }
    }

    /**
     * Deactivate user
     */
    async deactivateUser(userId) {
        try {
            await this.apiRequest(`/users/${userId}/deactivate`, {
                method: 'POST'
            });

            alert('User deactivated');
            await this.loadUsers();
        } catch (error) {
            alert(`Failed to deactivate user: ${error.message}`);
        }
    }

    /**
     * Load training jobs
     */
    async loadTrainingJobs() {
        try {
            this.trainingJobs = await this.apiRequest('/training/jobs');
            this.updateTrainingTable();
        } catch (error) {
            console.error('Failed to load training jobs:', error);
        }
    }

    /**
     * Update training table
     */
    updateTrainingTable() {
        const tbody = document.getElementById('training-tbody');
        if (!tbody) return;

        tbody.innerHTML = '';

        this.trainingJobs.forEach(job => {
            const row = document.createElement('tr');

            let statusBadge = 'badge-secondary';
            if (job.status === 'running') statusBadge = 'badge-warning';
            else if (job.status === 'completed') statusBadge = 'badge-success';
            else if (job.status === 'failed') statusBadge = 'badge-danger';

            row.innerHTML = `
                <td>${job.id}</td>
                <td>${job.job_name || 'Unnamed'}</td>
                <td>${job.training_type || 'N/A'}</td>
                <td>
                    <span class="badge ${statusBadge}">
                        ${job.status}
                    </span>
                </td>
                <td>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: ${job.progress || 0}%"></div>
                    </div>
                    <span>${job.progress || 0}%</span>
                </td>
                <td>${new Date(job.created_at).toLocaleDateString()}</td>
                <td>
                    <button class="btn btn-secondary btn-sm" onclick="dashboard.viewTrainingJob(${job.id})">View</button>
                    ${job.status === 'running' ?
                        `<button class="btn btn-danger btn-sm" onclick="dashboard.cancelTrainingJob(${job.id})">Cancel</button>` :
                        `<button class="btn btn-danger btn-sm" onclick="dashboard.deleteTrainingJob(${job.id})">Delete</button>`
                    }
                </td>
            `;
            tbody.appendChild(row);
        });
    }

    /**
     * Show create training dialog
     */
    showCreateTrainingDialog() {
        const jobName = prompt('Job Name:');
        const trainingType = prompt('Training Type (text/image/voice):');

        if (jobName && trainingType) {
            this.createTrainingJob(jobName, trainingType);
        }
    }

    /**
     * Create training job
     */
    async createTrainingJob(jobName, trainingType) {
        try {
            await this.apiRequest('/training/jobs', {
                method: 'POST',
                body: JSON.stringify({
                    job_name: jobName,
                    training_type: trainingType,
                    config: {}
                })
            });

            alert('Training job created successfully');
            await this.loadTrainingJobs();
        } catch (error) {
            alert(`Failed to create training job: ${error.message}`);
        }
    }

    /**
     * View training job
     */
    async viewTrainingJob(jobId) {
        try {
            const job = await this.apiRequest(`/training/jobs/${jobId}`);

            const details = `
Job ID: ${job.id}
Name: ${job.job_name}
Type: ${job.training_type}
Status: ${job.status}
Progress: ${job.progress}%
Created: ${new Date(job.created_at).toLocaleString()}
            `;

            alert(details);
        } catch (error) {
            alert(`Failed to load job details: ${error.message}`);
        }
    }

    /**
     * Cancel training job
     */
    async cancelTrainingJob(jobId) {
        if (!confirm('Are you sure you want to cancel this job?')) {
            return;
        }

        try {
            await this.apiRequest(`/training/jobs/${jobId}/cancel`, {
                method: 'POST'
            });

            alert('Training job cancelled');
            await this.loadTrainingJobs();
        } catch (error) {
            alert(`Failed to cancel job: ${error.message}`);
        }
    }

    /**
     * Delete training job
     */
    async deleteTrainingJob(jobId) {
        if (!confirm('Are you sure you want to delete this job?')) {
            return;
        }

        try {
            await this.apiRequest(`/training/jobs/${jobId}`, {
                method: 'DELETE'
            });

            alert('Training job deleted');
            await this.loadTrainingJobs();
        } catch (error) {
            alert(`Failed to delete job: ${error.message}`);
        }
    }

    /**
     * Load system health
     */
    async loadSystemHealth() {
        try {
            const data = await this.apiRequest('/system/health');

            this.systemMetrics = {
                cpu: data.cpu_usage || 0,
                memory: data.memory_usage || 0,
                disk: data.disk_usage || 0,
                uptime: data.uptime || 0
            };

            this.updateSystemHealthUI(data);
        } catch (error) {
            console.error('Failed to load system health:', error);
        }
    }

    /**
     * Update system health UI
     */
    updateSystemHealthUI(data) {
        // CPU
        const cpuUsage = document.getElementById('cpu-usage');
        const cpuPercentage = document.getElementById('cpu-percentage');
        if (cpuUsage && cpuPercentage) {
            const cpu = this.systemMetrics.cpu;
            cpuUsage.style.width = `${cpu}%`;
            cpuPercentage.textContent = `${cpu.toFixed(1)}%`;
        }

        // Memory
        const memoryUsage = document.getElementById('memory-usage');
        const memoryPercentage = document.getElementById('memory-percentage');
        if (memoryUsage && memoryPercentage) {
            const memory = this.systemMetrics.memory;
            memoryUsage.style.width = `${memory}%`;
            memoryPercentage.textContent = `${memory.toFixed(1)}%`;
        }

        // Disk
        const diskUsage = document.getElementById('disk-usage');
        const diskPercentage = document.getElementById('disk-percentage');
        if (diskUsage && diskPercentage) {
            const disk = this.systemMetrics.disk;
            diskUsage.style.width = `${disk}%`;
            diskPercentage.textContent = `${disk.toFixed(1)}%`;
        }

        // System info
        const apiVersion = document.getElementById('api-version');
        const databaseStatus = document.getElementById('database-status');
        const uptime = document.getElementById('uptime');

        if (apiVersion) apiVersion.textContent = data.version || 'Unknown';
        if (databaseStatus) {
            databaseStatus.textContent = data.database_connected ? 'Connected' : 'Disconnected';
            databaseStatus.style.color = data.database_connected ? 'var(--success-color)' : 'var(--danger-color)';
        }
        if (uptime) {
            const hours = Math.floor(this.systemMetrics.uptime / 3600);
            const minutes = Math.floor((this.systemMetrics.uptime % 3600) / 60);
            uptime.textContent = `${hours}h ${minutes}m`;
        }
    }

    /**
     * Load logs
     */
    async loadLogs() {
        try {
            this.logs = await this.apiRequest('/system/logs');
            this.displayLogs();
        } catch (error) {
            console.error('Failed to load logs:', error);
        }
    }

    /**
     * Display logs
     */
    displayLogs(filter = '') {
        const logsContainer = document.getElementById('logs-container');
        if (!logsContainer) return;

        logsContainer.innerHTML = '';

        let filteredLogs = this.logs;
        if (filter) {
            filteredLogs = this.logs.filter(log => log.level === filter);
        }

        filteredLogs.slice(-100).reverse().forEach(log => {
            const logEntry = document.createElement('div');
            logEntry.className = `log-entry ${log.level}`;
            logEntry.textContent = `[${new Date(log.timestamp).toLocaleTimeString()}] [${log.level}] ${log.message}`;
            logsContainer.appendChild(logEntry);
        });

        // Auto-scroll to bottom
        logsContainer.scrollTop = logsContainer.scrollHeight;
    }

    /**
     * Filter logs
     */
    filterLogs(level) {
        this.displayLogs(level);
    }

    /**
     * Load settings
     */
    async loadSettings() {
        try {
            const settings = await this.apiRequest('/system/settings');

            // Update form
            const enableRegistration = document.getElementById('enable-registration');
            const enableVoice = document.getElementById('enable-voice');
            const enableTraining = document.getElementById('enable-training');
            const maxTrainingJobs = document.getElementById('max-training-jobs');

            if (enableRegistration) enableRegistration.checked = settings.enable_registration || false;
            if (enableVoice) enableVoice.checked = settings.enable_voice || false;
            if (enableTraining) enableTraining.checked = settings.enable_training || false;
            if (maxTrainingJobs) maxTrainingJobs.value = settings.max_training_jobs || 5;
        } catch (error) {
            console.error('Failed to load settings:', error);
        }
    }

    /**
     * Save settings
     */
    async saveSettings() {
        const enableRegistration = document.getElementById('enable-registration').checked;
        const enableVoice = document.getElementById('enable-voice').checked;
        const enableTraining = document.getElementById('enable-training').checked;
        const maxTrainingJobs = parseInt(document.getElementById('max-training-jobs').value);

        try {
            await this.apiRequest('/system/settings', {
                method: 'PUT',
                body: JSON.stringify({
                    enable_registration: enableRegistration,
                    enable_voice: enableVoice,
                    enable_training: enableTraining,
                    max_training_jobs: maxTrainingJobs
                })
            });

            alert('Settings saved successfully');
        } catch (error) {
            alert(`Failed to save settings: ${error.message}`);
        }
    }

    /**
     * Display current user
     */
    displayCurrentUser() {
        const currentUserSpan = document.getElementById('current-user');
        if (currentUserSpan) {
            // Try to extract username from token (simple JWT decode)
            try {
                const payload = JSON.parse(atob(this.authToken.split('.')[1]));
                currentUserSpan.textContent = payload.sub || 'Admin';
            } catch {
                currentUserSpan.textContent = 'Admin';
            }
        }
    }

    /**
     * Start auto-refresh
     */
    startAutoRefresh() {
        // Refresh stats every 5 seconds
        this.refreshIntervals.stats = setInterval(() => {
            if (this.currentSection === 'overview') {
                this.loadStats();
            }
        }, 5000);

        // Refresh system health every 3 seconds
        this.refreshIntervals.system = setInterval(() => {
            if (this.currentSection === 'system') {
                this.loadSystemHealth();
            }
        }, 3000);

        // Refresh logs every 2 seconds
        this.refreshIntervals.logs = setInterval(() => {
            if (this.currentSection === 'logs') {
                this.loadLogs();
            }
        }, 2000);

        // Refresh users every 10 seconds
        this.refreshIntervals.users = setInterval(() => {
            if (this.currentSection === 'users') {
                this.loadUsers();
            }
        }, 10000);

        // Refresh training every 5 seconds
        this.refreshIntervals.training = setInterval(() => {
            if (this.currentSection === 'training') {
                this.loadTrainingJobs();
            }
        }, 5000);
    }

    /**
     * Stop auto-refresh
     */
    stopAutoRefresh() {
        Object.values(this.refreshIntervals).forEach(interval => {
            if (interval) clearInterval(interval);
        });
    }
}

// Initialize dashboard when DOM is loaded
let dashboard;

document.addEventListener('DOMContentLoaded', () => {
    dashboard = new AdminDashboard();
});

// Export for use in onclick handlers
if (typeof window !== 'undefined') {
    window.dashboard = dashboard;
}
