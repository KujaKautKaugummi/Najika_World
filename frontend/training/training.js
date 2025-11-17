/**
 * Najika World Training Dashboard
 * Real-time training job management and monitoring
 */

class TrainingDashboard {
    constructor() {
        // API Configuration
        this.apiBaseUrl = this.getApiBaseUrl();
        this.authToken = localStorage.getItem('admin_token') || '';

        // Data storage
        this.jobs = {
            running: [],
            queued: [],
            completed: [],
            failed: []
        };
        this.models = [];
        this.datasets = [];
        this.gpuMetrics = null;
        this.stats = {
            runningJobs: 0,
            queuedJobs: 0,
            completedToday: 0,
            totalModels: 0
        };

        // Current section
        this.currentSection = 'overview';

        // WebSocket for real-time updates
        this.ws = null;
        this.wsReconnectAttempts = 0;
        this.maxReconnectAttempts = 5;

        // Refresh intervals
        this.refreshIntervals = {
            overview: null,
            gpu: null,
            jobs: null
        };

        // Job filters
        this.historyFilters = {
            status: '',
            type: ''
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
        console.log('🤖 Initializing Training Dashboard...');

        // Check authentication
        if (!this.authToken) {
            alert('Please log in first');
            window.location.href = '/admin/';
            return;
        }

        // Set up navigation
        this.setupNavigation();

        // Set up event listeners
        this.setupEventListeners();

        // Load initial data
        await this.loadAllData();

        // Connect WebSocket for real-time updates
        this.connectWebSocket();

        // Start auto-refresh
        this.startAutoRefresh();

        console.log('✅ Training Dashboard initialized');
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
            const titles = {
                overview: 'Training Overview',
                active: 'Active Jobs',
                queue: 'Job Queue',
                history: 'Training History',
                models: 'Trained Models',
                datasets: 'Datasets',
                create: 'Create Training Job'
            };
            pageTitle.textContent = titles[sectionName] || sectionName;
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
                await this.loadOverview();
                break;
            case 'active':
                await this.loadActiveJobs();
                break;
            case 'queue':
                await this.loadQueuedJobs();
                break;
            case 'history':
                await this.loadHistory();
                break;
            case 'models':
                await this.loadModels();
                break;
            case 'datasets':
                await this.loadDatasets();
                break;
            case 'create':
                await this.loadDatasetsForForm();
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

        // Back button
        const backBtn = document.getElementById('back-btn');
        if (backBtn) {
            backBtn.addEventListener('click', () => {
                window.location.href = '/admin/';
            });
        }

        // Create job form
        const createJobForm = document.getElementById('create-job-form');
        if (createJobForm) {
            createJobForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.createTrainingJob();
            });
        }

        // Save draft button
        const saveDraftBtn = document.getElementById('save-draft-btn');
        if (saveDraftBtn) {
            saveDraftBtn.addEventListener('click', () => this.saveDraft());
        }

        // Upload model button
        const uploadModelBtn = document.getElementById('upload-model-btn');
        if (uploadModelBtn) {
            uploadModelBtn.addEventListener('click', () => this.uploadModel());
        }

        // Upload dataset button
        const uploadDatasetBtn = document.getElementById('upload-dataset-btn');
        if (uploadDatasetBtn) {
            uploadDatasetBtn.addEventListener('click', () => this.uploadDataset());
        }

        // History filters
        const historyFilterStatus = document.getElementById('history-filter-status');
        const historyFilterType = document.getElementById('history-filter-type');
        const historyClearFilters = document.getElementById('history-clear-filters');

        if (historyFilterStatus) {
            historyFilterStatus.addEventListener('change', (e) => {
                this.historyFilters.status = e.target.value;
                this.loadHistory();
            });
        }

        if (historyFilterType) {
            historyFilterType.addEventListener('change', (e) => {
                this.historyFilters.type = e.target.value;
                this.loadHistory();
            });
        }

        if (historyClearFilters) {
            historyClearFilters.addEventListener('click', () => {
                this.historyFilters = { status: '', type: '' };
                if (historyFilterStatus) historyFilterStatus.value = '';
                if (historyFilterType) historyFilterType.value = '';
                this.loadHistory();
            });
        }
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
                alert('Session expired. Please log in again.');
                window.location.href = '/admin/';
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
     * Load all initial data
     */
    async loadAllData() {
        await Promise.all([
            this.loadStats(),
            this.loadGPUMetrics(),
            this.loadActiveJobs(),
            this.loadDatasets()
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
     * Load overview data
     */
    async loadOverview() {
        await Promise.all([
            this.loadStats(),
            this.loadGPUMetrics(),
            this.loadRecentActivity()
        ]);

        this.updateStatsUI();
        this.updateGPUMetricsUI();
    }

    /**
     * Load stats
     */
    async loadStats() {
        try {
            const allJobs = await this.apiRequest('/training/jobs');

            this.stats.runningJobs = allJobs.filter(j => j.status === 'running').length;
            this.stats.queuedJobs = allJobs.filter(j => j.status === 'queued').length;

            // Count completed today
            const today = new Date();
            today.setHours(0, 0, 0, 0);
            this.stats.completedToday = allJobs.filter(j => {
                return j.status === 'completed' && new Date(j.completed_at) >= today;
            }).length;

            // Load models count
            try {
                const models = await this.apiRequest('/training/models');
                this.stats.totalModels = models.length;
            } catch {
                this.stats.totalModels = 0;
            }

            this.updateStatsUI();
        } catch (error) {
            console.error('Failed to load stats:', error);
        }
    }

    /**
     * Update stats UI
     */
    updateStatsUI() {
        const statRunningJobs = document.getElementById('stat-running-jobs');
        const statQueuedJobs = document.getElementById('stat-queued-jobs');
        const statCompletedToday = document.getElementById('stat-completed-today');
        const statTotalModels = document.getElementById('stat-total-models');

        if (statRunningJobs) statRunningJobs.textContent = this.stats.runningJobs;
        if (statQueuedJobs) statQueuedJobs.textContent = this.stats.queuedJobs;
        if (statCompletedToday) statCompletedToday.textContent = this.stats.completedToday;
        if (statTotalModels) statTotalModels.textContent = this.stats.totalModels;
    }

    /**
     * Load GPU metrics
     */
    async loadGPUMetrics() {
        try {
            this.gpuMetrics = await this.apiRequest('/system/gpu');
            this.updateGPUMetricsUI();
        } catch (error) {
            console.error('Failed to load GPU metrics:', error);
            this.gpuMetrics = null;
        }
    }

    /**
     * Update GPU metrics UI
     */
    updateGPUMetricsUI() {
        const gpuStatus = document.getElementById('gpu-status');

        if (!this.gpuMetrics || !this.gpuMetrics.available) {
            if (gpuStatus) {
                gpuStatus.textContent = 'GPU: Offline';
                gpuStatus.className = 'gpu-status offline';
            }
            return;
        }

        if (gpuStatus) {
            gpuStatus.textContent = `GPU: ${this.gpuMetrics.name || 'Available'}`;
            gpuStatus.className = 'gpu-status online';
        }

        // Update GPU 0 metrics
        const gpu = this.gpuMetrics.devices?.[0] || this.gpuMetrics;

        const gpu0Usage = document.getElementById('gpu-0-usage');
        const gpu0Percentage = document.getElementById('gpu-0-percentage');
        const gpu0Memory = document.getElementById('gpu-0-memory');
        const gpu0MemoryText = document.getElementById('gpu-0-memory-text');
        const gpu0Temp = document.getElementById('gpu-0-temp');

        if (gpu0Usage && gpu0Percentage) {
            const usage = gpu.utilization || 0;
            gpu0Usage.style.width = `${usage}%`;
            gpu0Percentage.textContent = `${usage}%`;
        }

        if (gpu0Memory && gpu0MemoryText) {
            const memoryUsed = gpu.memory_used || 0;
            const memoryTotal = gpu.memory_total || 1;
            const memoryPercent = (memoryUsed / memoryTotal) * 100;

            gpu0Memory.style.width = `${memoryPercent}%`;
            gpu0MemoryText.textContent = `${(memoryUsed / 1024).toFixed(1)} GB / ${(memoryTotal / 1024).toFixed(1)} GB`;
        }

        if (gpu0Temp) {
            const temp = gpu.temperature || 0;
            gpu0Temp.textContent = `${temp}°C`;

            // Color code temperature
            if (temp > 80) {
                gpu0Temp.style.color = 'var(--danger-color)';
            } else if (temp > 70) {
                gpu0Temp.style.color = 'var(--warning-color)';
            } else {
                gpu0Temp.style.color = 'var(--success-color)';
            }
        }
    }

    /**
     * Load recent activity
     */
    async loadRecentActivity() {
        try {
            const activity = await this.apiRequest('/training/activity');
            this.displayRecentActivity(activity);
        } catch (error) {
            console.error('Failed to load recent activity:', error);
        }
    }

    /**
     * Display recent activity
     */
    displayRecentActivity(activity) {
        const container = document.getElementById('recent-activity');
        if (!container) return;

        container.innerHTML = '';

        if (!activity || activity.length === 0) {
            container.innerHTML = '<div class="empty-state-text" style="padding: 20px;">No recent activity</div>';
            return;
        }

        activity.slice(0, 10).forEach(item => {
            const activityItem = document.createElement('div');
            activityItem.className = 'activity-item';
            activityItem.innerHTML = `
                <div class="time">${new Date(item.timestamp).toLocaleTimeString()}</div>
                <div class="message">${item.message}</div>
            `;
            container.appendChild(activityItem);
        });
    }

    /**
     * Load active jobs
     */
    async loadActiveJobs() {
        try {
            const allJobs = await this.apiRequest('/training/jobs');
            this.jobs.running = allJobs.filter(j => j.status === 'running');

            this.displayActiveJobs();
        } catch (error) {
            console.error('Failed to load active jobs:', error);
        }
    }

    /**
     * Display active jobs
     */
    displayActiveJobs() {
        const container = document.getElementById('active-jobs-container');
        if (!container) return;

        container.innerHTML = '';

        if (this.jobs.running.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <div class="empty-state-icon">🤖</div>
                    <div class="empty-state-text">No active training jobs</div>
                    <div class="empty-state-subtext">Start a new training job to see it here</div>
                </div>
            `;
            return;
        }

        this.jobs.running.forEach(job => {
            const jobCard = this.createJobCard(job);
            container.appendChild(jobCard);
        });
    }

    /**
     * Create job card element
     */
    createJobCard(job) {
        const card = document.createElement('div');
        card.className = 'job-card';

        const progress = job.progress || 0;
        const eta = this.calculateETA(job);

        card.innerHTML = `
            <div class="job-card-header">
                <div class="job-card-title">${job.job_name || 'Unnamed Job'}</div>
                <div class="job-card-status ${job.status}">${job.status}</div>
            </div>
            <div class="job-card-info">
                <p><strong>Type:</strong> ${job.training_type || 'Unknown'}</p>
                <p><strong>Started:</strong> ${new Date(job.started_at).toLocaleString()}</p>
                ${eta ? `<p><strong>ETA:</strong> ${eta}</p>` : ''}
            </div>
            <div class="job-card-progress">
                <label>Progress: ${progress.toFixed(1)}%</label>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: ${progress}%"></div>
                </div>
            </div>
            <div class="job-metrics">
                <div class="job-metric">
                    <span class="job-metric-label">Epoch</span>
                    <span class="job-metric-value">${job.current_epoch || 0} / ${job.total_epochs || 0}</span>
                </div>
                <div class="job-metric">
                    <span class="job-metric-label">Loss</span>
                    <span class="job-metric-value">${job.current_loss?.toFixed(4) || 'N/A'}</span>
                </div>
                <div class="job-metric">
                    <span class="job-metric-label">Accuracy</span>
                    <span class="job-metric-value">${job.accuracy ? (job.accuracy * 100).toFixed(2) + '%' : 'N/A'}</span>
                </div>
                <div class="job-metric">
                    <span class="job-metric-label">Learning Rate</span>
                    <span class="job-metric-value">${job.learning_rate?.toExponential(2) || 'N/A'}</span>
                </div>
            </div>
            <div class="job-card-actions">
                <button class="btn btn-secondary btn-sm" onclick="trainingDashboard.viewJobDetails(${job.id})">📊 Details</button>
                <button class="btn btn-warning btn-sm" onclick="trainingDashboard.pauseJob(${job.id})">⏸️ Pause</button>
                <button class="btn btn-danger btn-sm" onclick="trainingDashboard.cancelJob(${job.id})">❌ Cancel</button>
            </div>
        `;

        return card;
    }

    /**
     * Calculate ETA for job
     */
    calculateETA(job) {
        if (!job.started_at || !job.progress || job.progress === 0) {
            return null;
        }

        const elapsed = Date.now() - new Date(job.started_at).getTime();
        const totalTime = (elapsed / job.progress) * 100;
        const remaining = totalTime - elapsed;

        const hours = Math.floor(remaining / 3600000);
        const minutes = Math.floor((remaining % 3600000) / 60000);

        if (hours > 0) {
            return `${hours}h ${minutes}m`;
        } else {
            return `${minutes}m`;
        }
    }

    /**
     * Load queued jobs
     */
    async loadQueuedJobs() {
        try {
            const allJobs = await this.apiRequest('/training/jobs');
            this.jobs.queued = allJobs.filter(j => j.status === 'queued');

            this.displayQueuedJobs();
        } catch (error) {
            console.error('Failed to load queued jobs:', error);
        }
    }

    /**
     * Display queued jobs
     */
    displayQueuedJobs() {
        const tbody = document.getElementById('queue-tbody');
        if (!tbody) return;

        tbody.innerHTML = '';

        if (this.jobs.queued.length === 0) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="6" style="text-align: center; padding: 40px; color: var(--text-muted);">
                        No jobs in queue
                    </td>
                </tr>
            `;
            return;
        }

        this.jobs.queued.forEach(job => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${job.id}</td>
                <td>${job.job_name || 'Unnamed'}</td>
                <td>${job.training_type || 'N/A'}</td>
                <td>
                    <span class="badge badge-${this.getPriorityBadgeClass(job.priority)}">
                        ${job.priority || 'Normal'}
                    </span>
                </td>
                <td>${new Date(job.created_at).toLocaleString()}</td>
                <td>
                    <button class="btn btn-secondary btn-sm" onclick="trainingDashboard.viewJobDetails(${job.id})">View</button>
                    <button class="btn btn-danger btn-sm" onclick="trainingDashboard.cancelJob(${job.id})">Cancel</button>
                </td>
            `;
            tbody.appendChild(row);
        });
    }

    /**
     * Get priority badge class
     */
    getPriorityBadgeClass(priority) {
        const map = {
            low: 'info',
            normal: 'success',
            high: 'warning'
        };
        return map[priority] || 'success';
    }

    /**
     * Load history
     */
    async loadHistory() {
        try {
            let allJobs = await this.apiRequest('/training/jobs');

            // Filter completed/failed/cancelled
            allJobs = allJobs.filter(j => ['completed', 'failed', 'cancelled'].includes(j.status));

            // Apply filters
            if (this.historyFilters.status) {
                allJobs = allJobs.filter(j => j.status === this.historyFilters.status);
            }
            if (this.historyFilters.type) {
                allJobs = allJobs.filter(j => j.training_type === this.historyFilters.type);
            }

            this.jobs.completed = allJobs.filter(j => j.status === 'completed');
            this.jobs.failed = allJobs.filter(j => j.status === 'failed');

            this.displayHistory(allJobs);
        } catch (error) {
            console.error('Failed to load history:', error);
        }
    }

    /**
     * Display history
     */
    displayHistory(jobs) {
        const tbody = document.getElementById('history-tbody');
        if (!tbody) return;

        tbody.innerHTML = '';

        if (jobs.length === 0) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="7" style="text-align: center; padding: 40px; color: var(--text-muted);">
                        No training history
                    </td>
                </tr>
            `;
            return;
        }

        jobs.slice(0, 50).forEach(job => {
            const duration = this.calculateDuration(job);

            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${job.id}</td>
                <td>${job.job_name || 'Unnamed'}</td>
                <td>${job.training_type || 'N/A'}</td>
                <td>
                    <span class="badge badge-${this.getStatusBadgeClass(job.status)}">
                        ${job.status}
                    </span>
                </td>
                <td>${duration}</td>
                <td>${job.completed_at ? new Date(job.completed_at).toLocaleString() : 'N/A'}</td>
                <td>
                    <button class="btn btn-secondary btn-sm" onclick="trainingDashboard.viewJobDetails(${job.id})">View</button>
                    <button class="btn btn-danger btn-sm" onclick="trainingDashboard.deleteJob(${job.id})">Delete</button>
                </td>
            `;
            tbody.appendChild(row);
        });
    }

    /**
     * Get status badge class
     */
    getStatusBadgeClass(status) {
        const map = {
            completed: 'success',
            failed: 'danger',
            cancelled: 'warning'
        };
        return map[status] || 'info';
    }

    /**
     * Calculate duration
     */
    calculateDuration(job) {
        if (!job.started_at || !job.completed_at) {
            return 'N/A';
        }

        const duration = new Date(job.completed_at) - new Date(job.started_at);
        const hours = Math.floor(duration / 3600000);
        const minutes = Math.floor((duration % 3600000) / 60000);
        const seconds = Math.floor((duration % 60000) / 1000);

        if (hours > 0) {
            return `${hours}h ${minutes}m`;
        } else if (minutes > 0) {
            return `${minutes}m ${seconds}s`;
        } else {
            return `${seconds}s`;
        }
    }

    /**
     * Load models
     */
    async loadModels() {
        try {
            this.models = await this.apiRequest('/training/models');
            this.displayModels();
        } catch (error) {
            console.error('Failed to load models:', error);
        }
    }

    /**
     * Display models
     */
    displayModels() {
        const grid = document.getElementById('models-grid');
        if (!grid) return;

        grid.innerHTML = '';

        if (this.models.length === 0) {
            grid.innerHTML = `
                <div class="empty-state" style="grid-column: 1/-1;">
                    <div class="empty-state-icon">🧠</div>
                    <div class="empty-state-text">No trained models</div>
                    <div class="empty-state-subtext">Complete a training job to see models here</div>
                </div>
            `;
            return;
        }

        this.models.forEach(model => {
            const card = this.createModelCard(model);
            grid.appendChild(card);
        });
    }

    /**
     * Create model card
     */
    createModelCard(model) {
        const card = document.createElement('div');
        card.className = 'model-card';

        card.innerHTML = `
            <div class="model-card-header">
                <div class="model-card-title">${model.name || 'Unnamed Model'}</div>
                <div class="model-card-type">${model.type || 'Unknown'}</div>
            </div>
            <div class="model-card-info">
                <p><strong>Version:</strong> ${model.version || '1.0'}</p>
                <p><strong>Size:</strong> ${this.formatFileSize(model.size || 0)}</p>
                <p><strong>Created:</strong> ${new Date(model.created_at).toLocaleDateString()}</p>
                ${model.accuracy ? `<p><strong>Accuracy:</strong> ${(model.accuracy * 100).toFixed(2)}%</p>` : ''}
            </div>
            <div class="model-card-actions">
                <button class="btn btn-secondary btn-sm" onclick="trainingDashboard.downloadModel(${model.id})">⬇️ Download</button>
                <button class="btn btn-danger btn-sm" onclick="trainingDashboard.deleteModel(${model.id})">🗑️ Delete</button>
            </div>
        `;

        return card;
    }

    /**
     * Format file size
     */
    formatFileSize(bytes) {
        if (bytes < 1024) return bytes + ' B';
        if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + ' KB';
        if (bytes < 1024 * 1024 * 1024) return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
        return (bytes / (1024 * 1024 * 1024)).toFixed(2) + ' GB';
    }

    /**
     * Load datasets
     */
    async loadDatasets() {
        try {
            this.datasets = await this.apiRequest('/training/datasets');
            this.displayDatasets();
        } catch (error) {
            console.error('Failed to load datasets:', error);
        }
    }

    /**
     * Display datasets
     */
    displayDatasets() {
        const tbody = document.getElementById('datasets-tbody');
        if (!tbody) return;

        tbody.innerHTML = '';

        if (this.datasets.length === 0) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="7" style="text-align: center; padding: 40px; color: var(--text-muted);">
                        No datasets uploaded
                    </td>
                </tr>
            `;
            return;
        }

        this.datasets.forEach(dataset => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${dataset.id}</td>
                <td>${dataset.name || 'Unnamed'}</td>
                <td>${dataset.type || 'N/A'}</td>
                <td>${this.formatFileSize(dataset.size || 0)}</td>
                <td>${dataset.samples || 0}</td>
                <td>${new Date(dataset.created_at).toLocaleString()}</td>
                <td>
                    <button class="btn btn-secondary btn-sm" onclick="trainingDashboard.viewDataset(${dataset.id})">View</button>
                    <button class="btn btn-danger btn-sm" onclick="trainingDashboard.deleteDataset(${dataset.id})">Delete</button>
                </td>
            `;
            tbody.appendChild(row);
        });
    }

    /**
     * Load datasets for create form
     */
    async loadDatasetsForForm() {
        try {
            this.datasets = await this.apiRequest('/training/datasets');

            const datasetSelect = document.getElementById('dataset');
            if (datasetSelect) {
                datasetSelect.innerHTML = '<option value="">Select Dataset</option>';

                this.datasets.forEach(dataset => {
                    const option = document.createElement('option');
                    option.value = dataset.id;
                    option.textContent = `${dataset.name} (${dataset.type})`;
                    datasetSelect.appendChild(option);
                });
            }
        } catch (error) {
            console.error('Failed to load datasets for form:', error);
        }
    }

    /**
     * Create training job
     */
    async createTrainingJob() {
        const form = document.getElementById('create-job-form');
        const formData = new FormData(form);

        const jobData = {
            job_name: formData.get('job_name'),
            training_type: formData.get('training_type'),
            dataset_id: parseInt(formData.get('dataset_id')),
            base_model: formData.get('base_model') || null,
            config: {
                epochs: parseInt(formData.get('epochs')),
                batch_size: parseInt(formData.get('batch_size')),
                learning_rate: parseFloat(formData.get('learning_rate')),
                auto_save: formData.get('auto_save') === 'on',
                notify_complete: formData.get('notify_complete') === 'on'
            },
            priority: formData.get('priority'),
            description: formData.get('description') || null
        };

        try {
            await this.apiRequest('/training/jobs', {
                method: 'POST',
                body: JSON.stringify(jobData)
            });

            alert('✅ Training job created successfully!');
            form.reset();

            // Switch to active jobs section
            this.showSection('active');
        } catch (error) {
            alert(`❌ Failed to create training job: ${error.message}`);
        }
    }

    /**
     * View job details
     */
    async viewJobDetails(jobId) {
        try {
            const job = await this.apiRequest(`/training/jobs/${jobId}`);
            this.showJobDetailsModal(job);
        } catch (error) {
            alert(`Failed to load job details: ${error.message}`);
        }
    }

    /**
     * Show job details modal
     */
    showJobDetailsModal(job) {
        const modal = document.getElementById('job-details-modal');
        const body = document.getElementById('job-details-body');

        if (!modal || !body) return;

        body.innerHTML = `
            <div class="job-details">
                <div class="job-details-section">
                    <h3>General Information</h3>
                    <div class="job-details-grid">
                        <div class="job-detail-item">
                            <div class="job-detail-label">Job ID</div>
                            <div class="job-detail-value">${job.id}</div>
                        </div>
                        <div class="job-detail-item">
                            <div class="job-detail-label">Name</div>
                            <div class="job-detail-value">${job.job_name || 'Unnamed'}</div>
                        </div>
                        <div class="job-detail-item">
                            <div class="job-detail-label">Type</div>
                            <div class="job-detail-value">${job.training_type || 'N/A'}</div>
                        </div>
                        <div class="job-detail-item">
                            <div class="job-detail-label">Status</div>
                            <div class="job-detail-value">
                                <span class="badge badge-${this.getStatusBadgeClass(job.status)}">
                                    ${job.status}
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
                ${job.description ? `
                <div class="job-details-section">
                    <h3>Description</h3>
                    <p>${job.description}</p>
                </div>
                ` : ''}
                <div class="job-details-section">
                    <h3>Configuration</h3>
                    <div class="job-details-grid">
                        <div class="job-detail-item">
                            <div class="job-detail-label">Epochs</div>
                            <div class="job-detail-value">${job.config?.epochs || 'N/A'}</div>
                        </div>
                        <div class="job-detail-item">
                            <div class="job-detail-label">Batch Size</div>
                            <div class="job-detail-value">${job.config?.batch_size || 'N/A'}</div>
                        </div>
                        <div class="job-detail-item">
                            <div class="job-detail-label">Learning Rate</div>
                            <div class="job-detail-value">${job.config?.learning_rate || 'N/A'}</div>
                        </div>
                        <div class="job-detail-item">
                            <div class="job-detail-label">Priority</div>
                            <div class="job-detail-value">${job.priority || 'Normal'}</div>
                        </div>
                    </div>
                </div>
                ${job.logs ? `
                <div class="job-details-section">
                    <h3>Training Logs</h3>
                    <div class="log-container">
                        ${job.logs.split('\n').map(line => `<div class="log-entry">${line}</div>`).join('')}
                    </div>
                </div>
                ` : ''}
            </div>
        `;

        modal.classList.add('active');
    }

    /**
     * Close job details modal
     */
    closeJobDetailsModal() {
        const modal = document.getElementById('job-details-modal');
        if (modal) {
            modal.classList.remove('active');
        }
    }

    /**
     * Pause job
     */
    async pauseJob(jobId) {
        if (!confirm('Pause this training job?')) return;

        try {
            await this.apiRequest(`/training/jobs/${jobId}/pause`, {
                method: 'POST'
            });

            alert('Job paused');
            await this.loadActiveJobs();
        } catch (error) {
            alert(`Failed to pause job: ${error.message}`);
        }
    }

    /**
     * Cancel job
     */
    async cancelJob(jobId) {
        if (!confirm('Cancel this training job? This cannot be undone.')) return;

        try {
            await this.apiRequest(`/training/jobs/${jobId}/cancel`, {
                method: 'POST'
            });

            alert('Job cancelled');
            await this.refresh();
        } catch (error) {
            alert(`Failed to cancel job: ${error.message}`);
        }
    }

    /**
     * Delete job
     */
    async deleteJob(jobId) {
        if (!confirm('Delete this training job? This cannot be undone.')) return;

        try {
            await this.apiRequest(`/training/jobs/${jobId}`, {
                method: 'DELETE'
            });

            alert('Job deleted');
            await this.loadHistory();
        } catch (error) {
            alert(`Failed to delete job: ${error.message}`);
        }
    }

    /**
     * Download model
     */
    async downloadModel(modelId) {
        try {
            window.location.href = `${this.apiBaseUrl}/training/models/${modelId}/download`;
        } catch (error) {
            alert(`Failed to download model: ${error.message}`);
        }
    }

    /**
     * Delete model
     */
    async deleteModel(modelId) {
        if (!confirm('Delete this model? This cannot be undone.')) return;

        try {
            await this.apiRequest(`/training/models/${modelId}`, {
                method: 'DELETE'
            });

            alert('Model deleted');
            await this.loadModels();
        } catch (error) {
            alert(`Failed to delete model: ${error.message}`);
        }
    }

    /**
     * View dataset
     */
    async viewDataset(datasetId) {
        try {
            const dataset = await this.apiRequest(`/training/datasets/${datasetId}`);
            alert(`Dataset: ${dataset.name}\nType: ${dataset.type}\nSamples: ${dataset.samples}`);
        } catch (error) {
            alert(`Failed to load dataset: ${error.message}`);
        }
    }

    /**
     * Delete dataset
     */
    async deleteDataset(datasetId) {
        if (!confirm('Delete this dataset? This cannot be undone.')) return;

        try {
            await this.apiRequest(`/training/datasets/${datasetId}`, {
                method: 'DELETE'
            });

            alert('Dataset deleted');
            await this.loadDatasets();
        } catch (error) {
            alert(`Failed to delete dataset: ${error.message}`);
        }
    }

    /**
     * Upload model
     */
    uploadModel() {
        alert('Model upload feature coming soon!');
    }

    /**
     * Upload dataset
     */
    uploadDataset() {
        alert('Dataset upload feature coming soon!');
    }

    /**
     * Save draft
     */
    saveDraft() {
        const form = document.getElementById('create-job-form');
        const formData = new FormData(form);

        const draft = {};
        for (let [key, value] of formData.entries()) {
            draft[key] = value;
        }

        localStorage.setItem('training_job_draft', JSON.stringify(draft));
        alert('Draft saved!');
    }

    /**
     * Connect WebSocket for real-time updates
     */
    connectWebSocket() {
        try {
            const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
            const wsUrl = `${wsProtocol}//${window.location.hostname}:${window.location.port || '8000'}/api/training/ws`;

            this.ws = new WebSocket(wsUrl);

            this.ws.onopen = () => {
                console.log('✅ WebSocket connected for training updates');
                this.wsReconnectAttempts = 0;
            };

            this.ws.onmessage = (event) => {
                try {
                    const message = JSON.parse(event.data);
                    this.handleWebSocketMessage(message);
                } catch (error) {
                    console.error('Failed to parse WebSocket message:', error);
                }
            };

            this.ws.onclose = () => {
                console.log('WebSocket closed');
                this.reconnectWebSocket();
            };

            this.ws.onerror = (error) => {
                console.error('WebSocket error:', error);
            };
        } catch (error) {
            console.error('Failed to connect WebSocket:', error);
        }
    }

    /**
     * Reconnect WebSocket
     */
    reconnectWebSocket() {
        if (this.wsReconnectAttempts >= this.maxReconnectAttempts) {
            console.log('Max reconnect attempts reached');
            return;
        }

        this.wsReconnectAttempts++;
        const delay = Math.min(1000 * Math.pow(2, this.wsReconnectAttempts), 30000);

        console.log(`Reconnecting WebSocket in ${delay}ms...`);
        setTimeout(() => this.connectWebSocket(), delay);
    }

    /**
     * Handle WebSocket message
     */
    handleWebSocketMessage(message) {
        switch (message.type) {
            case 'job_update':
                this.handleJobUpdate(message.data);
                break;
            case 'job_completed':
                this.handleJobCompleted(message.data);
                break;
            case 'job_failed':
                this.handleJobFailed(message.data);
                break;
            case 'gpu_update':
                this.gpuMetrics = message.data;
                this.updateGPUMetricsUI();
                break;
        }
    }

    /**
     * Handle job update
     */
    handleJobUpdate(job) {
        // Find and update job in running list
        const index = this.jobs.running.findIndex(j => j.id === job.id);
        if (index >= 0) {
            this.jobs.running[index] = job;

            if (this.currentSection === 'active') {
                this.displayActiveJobs();
            }
        }
    }

    /**
     * Handle job completed
     */
    handleJobCompleted(job) {
        alert(`✅ Training job "${job.job_name}" completed successfully!`);
        this.refresh();
    }

    /**
     * Handle job failed
     */
    handleJobFailed(job) {
        alert(`❌ Training job "${job.job_name}" failed: ${job.error || 'Unknown error'}`);
        this.refresh();
    }

    /**
     * Start auto-refresh
     */
    startAutoRefresh() {
        // Refresh overview every 10 seconds
        this.refreshIntervals.overview = setInterval(() => {
            if (this.currentSection === 'overview') {
                this.loadOverview();
            }
        }, 10000);

        // Refresh GPU metrics every 5 seconds
        this.refreshIntervals.gpu = setInterval(() => {
            this.loadGPUMetrics();
        }, 5000);

        // Refresh jobs every 15 seconds
        this.refreshIntervals.jobs = setInterval(() => {
            if (['active', 'queue'].includes(this.currentSection)) {
                this.loadSectionData(this.currentSection);
            }
        }, 15000);
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

// Initialize training dashboard when DOM is loaded
let trainingDashboard;

document.addEventListener('DOMContentLoaded', () => {
    trainingDashboard = new TrainingDashboard();
});

// Export for onclick handlers
if (typeof window !== 'undefined') {
    window.trainingDashboard = trainingDashboard;
}
