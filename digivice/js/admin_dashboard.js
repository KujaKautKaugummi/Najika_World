/**
 * Admin Dashboard
 * Comprehensive administrative interface for Najika World
 */

import { API_BASE_URL } from './config.js';

export class AdminDashboard {
    constructor() {
        this.container = null;
        this.currentView = 'overview';
        this.refreshInterval = null;
        this.authToken = localStorage.getItem('auth_token');

        // Dashboard data
        this.dashboardData = null;
        this.users = [];
        this.characters = [];
        this.systemHealth = null;

        this.init();

        console.log('📊 Admin Dashboard initialized');
    }

    /**
     * Initialize dashboard
     */
    async init() {
        await this.loadDashboardData();
        this.render();
        this.startAutoRefresh();
    }

    /**
     * Load dashboard data
     */
    async loadDashboardData() {
        try {
            const response = await fetch(`${API_BASE_URL}/admin/dashboard`, {
                headers: {
                    'Authorization': `Bearer ${this.authToken}`
                }
            });

            if (response.ok) {
                const data = await response.json();
                this.dashboardData = data.dashboard;
            }
        } catch (error) {
            console.error('Failed to load dashboard data:', error);
        }
    }

    /**
     * Load system health
     */
    async loadSystemHealth() {
        try {
            const response = await fetch(`${API_BASE_URL}/admin/health`, {
                headers: {
                    'Authorization': `Bearer ${this.authToken}`
                }
            });

            if (response.ok) {
                const data = await response.json();
                this.systemHealth = data.health;
            }
        } catch (error) {
            console.error('Failed to load system health:', error);
        }
    }

    /**
     * Load users list
     */
    async loadUsers(page = 1, search = '') {
        try {
            const params = new URLSearchParams({
                page: page,
                limit: 50,
                search: search
            });

            const response = await fetch(`${API_BASE_URL}/admin/users?${params}`, {
                headers: {
                    'Authorization': `Bearer ${this.authToken}`
                }
            });

            if (response.ok) {
                const data = await response.json();
                this.users = data.users;
                return data;
            }
        } catch (error) {
            console.error('Failed to load users:', error);
        }
    }

    /**
     * Render dashboard
     */
    render() {
        // Create or get container
        this.container = document.getElementById('admin-dashboard');

        if (!this.container) {
            this.container = document.createElement('div');
            this.container.id = 'admin-dashboard';
            this.container.className = 'admin-dashboard';
            document.body.appendChild(this.container);
        }

        this.container.innerHTML = `
            <div class="admin-dashboard-wrapper">
                <!-- Sidebar -->
                <div class="admin-sidebar">
                    <div class="admin-sidebar-header">
                        <h2>🎮 Najika World Admin</h2>
                    </div>

                    <nav class="admin-nav">
                        <button class="admin-nav-item ${this.currentView === 'overview' ? 'active' : ''}"
                                data-view="overview">
                            <span>📊</span> Overview
                        </button>
                        <button class="admin-nav-item ${this.currentView === 'users' ? 'active' : ''}"
                                data-view="users">
                            <span>👥</span> Users
                        </button>
                        <button class="admin-nav-item ${this.currentView === 'characters' ? 'active' : ''}"
                                data-view="characters">
                            <span>⚔️</span> Characters
                        </button>
                        <button class="admin-nav-item ${this.currentView === 'digimon' ? 'active' : ''}"
                                data-view="digimon">
                            <span>🦖</span> Digimon
                        </button>
                        <button class="admin-nav-item ${this.currentView === 'arena' ? 'active' : ''}"
                                data-view="arena">
                            <span>🏟️</span> Arena
                        </button>
                        <button class="admin-nav-item ${this.currentView === 'system' ? 'active' : ''}"
                                data-view="system">
                            <span>⚙️</span> System
                        </button>
                        <button class="admin-nav-item ${this.currentView === 'analytics' ? 'active' : ''}"
                                data-view="analytics">
                            <span>📈</span> Analytics
                        </button>
                    </nav>

                    <div class="admin-sidebar-footer">
                        <button class="admin-logout-btn" id="admin-logout">
                            <span>🚪</span> Logout
                        </button>
                    </div>
                </div>

                <!-- Main Content -->
                <div class="admin-content">
                    <div class="admin-content-header">
                        <h1>${this.getViewTitle()}</h1>
                        <div class="admin-actions">
                            <button class="admin-refresh-btn" id="admin-refresh">
                                🔄 Refresh
                            </button>
                        </div>
                    </div>

                    <div class="admin-content-body" id="admin-content-body">
                        ${this.renderCurrentView()}
                    </div>
                </div>
            </div>
        `;

        this.attachEventListeners();
    }

    /**
     * Get view title
     */
    getViewTitle() {
        const titles = {
            'overview': 'Dashboard Overview',
            'users': 'User Management',
            'characters': 'Character Management',
            'digimon': 'Digimon Statistics',
            'arena': 'Arena Management',
            'system': 'System Health',
            'analytics': 'Analytics'
        };

        return titles[this.currentView] || 'Admin Dashboard';
    }

    /**
     * Render current view
     */
    renderCurrentView() {
        switch (this.currentView) {
            case 'overview':
                return this.renderOverview();
            case 'users':
                return this.renderUsers();
            case 'characters':
                return this.renderCharacters();
            case 'digimon':
                return this.renderDigimon();
            case 'arena':
                return this.renderArena();
            case 'system':
                return this.renderSystem();
            case 'analytics':
                return this.renderAnalytics();
            default:
                return this.renderOverview();
        }
    }

    /**
     * Render overview
     */
    renderOverview() {
        if (!this.dashboardData) {
            return '<div class="loading">Loading dashboard data...</div>';
        }

        const { users, characters, digimon, top_players } = this.dashboardData;

        return `
            <div class="dashboard-overview">
                <!-- Stats Grid -->
                <div class="stats-grid">
                    <div class="stat-card stat-users">
                        <div class="stat-icon">👥</div>
                        <div class="stat-info">
                            <div class="stat-label">Total Users</div>
                            <div class="stat-value">${users.total.toLocaleString()}</div>
                            <div class="stat-sub">
                                ${users.active_24h} active (24h) ·
                                ${users.active_7d} active (7d)
                            </div>
                        </div>
                    </div>

                    <div class="stat-card stat-characters">
                        <div class="stat-icon">⚔️</div>
                        <div class="stat-info">
                            <div class="stat-label">Characters</div>
                            <div class="stat-value">${characters.total.toLocaleString()}</div>
                            <div class="stat-sub">
                                Avg Level: ${characters.avg_level} ·
                                Max: ${characters.max_level}
                            </div>
                        </div>
                    </div>

                    <div class="stat-card stat-digimon">
                        <div class="stat-icon">🦖</div>
                        <div class="stat-info">
                            <div class="stat-label">Digimon</div>
                            <div class="stat-value">${digimon.total.toLocaleString()}</div>
                            <div class="stat-sub">
                                ${Object.keys(digimon.by_stage || {}).length} stages
                            </div>
                        </div>
                    </div>

                    <div class="stat-card stat-growth">
                        <div class="stat-icon">📈</div>
                        <div class="stat-info">
                            <div class="stat-label">New Users Today</div>
                            <div class="stat-value">${users.new_today}</div>
                            <div class="stat-sub">
                                ${users.growth_rate.toFixed(2)}% growth rate
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Top Players -->
                <div class="dashboard-section">
                    <h2>🏆 Top Players</h2>
                    <div class="top-players-list">
                        ${top_players.map((player, index) => `
                            <div class="top-player-item">
                                <div class="player-rank">#${index + 1}</div>
                                <div class="player-name">${player.username}</div>
                                <div class="player-stats">
                                    <span>Lvl ${player.level}</span>
                                    <span>${player.experience.toLocaleString()} XP</span>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>

                <!-- Digimon Distribution -->
                <div class="dashboard-section">
                    <h2>🦖 Digimon by Stage</h2>
                    <div class="digimon-distribution">
                        ${Object.entries(digimon.by_stage || {}).map(([stage, count]) => `
                            <div class="distribution-item">
                                <div class="distribution-label">${stage}</div>
                                <div class="distribution-bar">
                                    <div class="distribution-fill"
                                         style="width: ${(count / digimon.total) * 100}%">
                                    </div>
                                </div>
                                <div class="distribution-value">${count}</div>
                            </div>
                        `).join('')}
                    </div>
                </div>
            </div>
        `;
    }

    /**
     * Render users view
     */
    renderUsers() {
        return `
            <div class="users-management">
                <div class="users-controls">
                    <input type="text"
                           id="user-search"
                           class="admin-search-input"
                           placeholder="Search users...">
                    <button class="admin-btn admin-btn-primary" id="create-user-btn">
                        ➕ Create User
                    </button>
                </div>

                <div class="users-table-container">
                    <table class="admin-table" id="users-table">
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Username</th>
                                <th>Email</th>
                                <th>Status</th>
                                <th>Admin</th>
                                <th>Created</th>
                                <th>Last Login</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody id="users-table-body">
                            <tr>
                                <td colspan="8" class="loading">Loading users...</td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <div class="admin-pagination" id="users-pagination">
                    <!-- Pagination controls will be inserted here -->
                </div>
            </div>
        `;
    }

    /**
     * Render characters view
     */
    renderCharacters() {
        return `
            <div class="characters-management">
                <div class="characters-controls">
                    <input type="number"
                           id="char-min-level"
                           class="admin-input-small"
                           placeholder="Min Level">
                    <input type="number"
                           id="char-max-level"
                           class="admin-input-small"
                           placeholder="Max Level">
                    <button class="admin-btn admin-btn-primary" id="filter-characters-btn">
                        🔍 Filter
                    </button>
                </div>

                <div class="characters-grid" id="characters-grid">
                    <div class="loading">Loading characters...</div>
                </div>
            </div>
        `;
    }

    /**
     * Render Digimon view
     */
    renderDigimon() {
        return `
            <div class="digimon-stats">
                <h2>📊 Digimon Statistics</h2>
                <div id="digimon-stats-content">
                    <div class="loading">Loading Digimon statistics...</div>
                </div>
            </div>
        `;
    }

    /**
     * Render Arena view
     */
    renderArena() {
        return `
            <div class="arena-management">
                <h2>🏟️ Arena Management</h2>
                <div class="arena-controls">
                    <button class="admin-btn admin-btn-primary" id="view-arena-hierarchy">
                        👑 View Hierarchy
                    </button>
                    <button class="admin-btn admin-btn-secondary" id="view-finishers">
                        💀 View Finishers
                    </button>
                    <button class="admin-btn admin-btn-success" id="create-monster">
                        ➕ Create Monster
                    </button>
                </div>

                <div id="arena-content">
                    <p>Select an option above to view arena data.</p>
                </div>
            </div>
        `;
    }

    /**
     * Render System view
     */
    renderSystem() {
        return `
            <div class="system-health">
                <h2>⚙️ System Health</h2>
                <div id="system-health-content">
                    <div class="loading">Loading system health...</div>
                </div>

                <div class="system-logs">
                    <h3>📜 Recent Logs</h3>
                    <div class="logs-container" id="logs-container">
                        <div class="loading">Loading logs...</div>
                    </div>
                </div>
            </div>
        `;
    }

    /**
     * Render Analytics view
     */
    renderAnalytics() {
        return `
            <div class="analytics-view">
                <h2>📈 Analytics</h2>

                <div class="analytics-controls">
                    <select id="analytics-period" class="admin-select">
                        <option value="7">Last 7 Days</option>
                        <option value="30" selected>Last 30 Days</option>
                        <option value="90">Last 90 Days</option>
                    </select>
                    <button class="admin-btn admin-btn-primary" id="load-analytics">
                        📊 Load Analytics
                    </button>
                </div>

                <div class="analytics-charts">
                    <div class="chart-container">
                        <h3>User Growth</h3>
                        <canvas id="user-growth-chart"></canvas>
                    </div>

                    <div class="chart-container">
                        <h3>Activity Rate</h3>
                        <canvas id="activity-chart"></canvas>
                    </div>
                </div>
            </div>
        `;
    }

    /**
     * Attach event listeners
     */
    attachEventListeners() {
        // Navigation
        document.querySelectorAll('.admin-nav-item').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const view = e.currentTarget.dataset.view;
                this.switchView(view);
            });
        });

        // Refresh button
        const refreshBtn = document.getElementById('admin-refresh');
        if (refreshBtn) {
            refreshBtn.addEventListener('click', () => {
                this.refresh();
            });
        }

        // Logout button
        const logoutBtn = document.getElementById('admin-logout');
        if (logoutBtn) {
            logoutBtn.addEventListener('click', () => {
                this.logout();
            });
        }

        // Load view-specific data
        if (this.currentView === 'users') {
            this.loadUsersTable();
        } else if (this.currentView === 'system') {
            this.loadSystemHealthView();
        }
    }

    /**
     * Switch view
     */
    switchView(view) {
        this.currentView = view;
        this.render();
    }

    /**
     * Refresh current view
     */
    async refresh() {
        await this.loadDashboardData();

        if (this.currentView === 'system') {
            await this.loadSystemHealth();
        }

        this.render();
    }

    /**
     * Load users table
     */
    async loadUsersTable(page = 1, search = '') {
        const data = await this.loadUsers(page, search);

        if (!data) return;

        const tbody = document.getElementById('users-table-body');
        if (!tbody) return;

        tbody.innerHTML = data.users.map(user => `
            <tr>
                <td>${user.id}</td>
                <td>${user.username}</td>
                <td>${user.email || 'N/A'}</td>
                <td>
                    <span class="status-badge ${user.is_active ? 'status-active' : 'status-inactive'}">
                        ${user.is_active ? 'Active' : 'Inactive'}
                    </span>
                </td>
                <td>${user.is_admin ? '✅' : '❌'}</td>
                <td>${user.created_at ? new Date(user.created_at).toLocaleDateString() : 'N/A'}</td>
                <td>${user.last_login ? new Date(user.last_login).toLocaleDateString() : 'Never'}</td>
                <td>
                    <button class="admin-btn-small" onclick="adminDashboard.viewUser(${user.id})">
                        👁️ View
                    </button>
                    <button class="admin-btn-small admin-btn-danger" onclick="adminDashboard.deleteUser(${user.id})">
                        🗑️ Delete
                    </button>
                </td>
            </tr>
        `).join('');
    }

    /**
     * Load system health view
     */
    async loadSystemHealthView() {
        await this.loadSystemHealth();

        const container = document.getElementById('system-health-content');
        if (!container || !this.systemHealth) return;

        container.innerHTML = `
            <div class="health-status">
                <div class="health-item">
                    <span class="health-label">Database:</span>
                    <span class="health-value ${this.systemHealth.database === 'healthy' ? 'health-good' : 'health-bad'}">
                        ${this.systemHealth.database}
                    </span>
                </div>

                ${this.systemHealth.system ? `
                    <div class="health-section">
                        <h3>System Resources</h3>
                        <div class="health-item">
                            <span class="health-label">CPU Usage:</span>
                            <span class="health-value">${this.systemHealth.system.cpu_usage}</span>
                        </div>
                        <div class="health-item">
                            <span class="health-label">Memory:</span>
                            <span class="health-value">
                                ${this.systemHealth.system.memory.used} /
                                ${this.systemHealth.system.memory.total}
                                (${this.systemHealth.system.memory.percent})
                            </span>
                        </div>
                        <div class="health-item">
                            <span class="health-label">Disk:</span>
                            <span class="health-value">
                                ${this.systemHealth.system.disk.used} /
                                ${this.systemHealth.system.disk.total}
                                (${this.systemHealth.system.disk.percent})
                            </span>
                        </div>
                    </div>
                ` : ''}
            </div>
        `;
    }

    /**
     * View user details
     */
    async viewUser(userId) {
        if (typeof notify === 'function') notify(`👤 User ${userId} anzeigen (in Arbeit)`, 'info');
    }

    /**
     * Delete user
     */
    async deleteUser(userId) {
        if (!this._deleteConfirmId || this._deleteConfirmId !== userId) {
            this._deleteConfirmId = userId;
            if (typeof notify === 'function') notify(`⚠️ Nochmal klicken um User ${userId} zu löschen!`, 'warning');
            setTimeout(() => { this._deleteConfirmId = null; }, 3000);
            return;
        }
        this._deleteConfirmId = null;

        try {
            const response = await fetch(`${API_BASE_URL}/admin/users/${userId}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${this.authToken}`
                }
            });

            if (response.ok) {
                if (typeof notify === 'function') notify('✅ User gelöscht', 'success');
                this.loadUsersTable();
            } else {
                if (typeof notify === 'function') notify('❌ User löschen fehlgeschlagen', 'error');
            }
        } catch (error) {
            console.error('Failed to delete user:', error);
            if (typeof notify === 'function') notify('❌ Fehler beim Löschen', 'error');
        }
    }

    /**
     * Logout
     */
    logout() {
        localStorage.removeItem('auth_token');
        window.location.href = '/login.html';
    }

    /**
     * Start auto-refresh
     */
    startAutoRefresh() {
        // Refresh dashboard every 60 seconds
        this.refreshInterval = setInterval(() => {
            if (this.currentView === 'overview') {
                this.loadDashboardData();
            }
        }, 60000);
    }

    /**
     * Stop auto-refresh
     */
    stopAutoRefresh() {
        if (this.refreshInterval) {
            clearInterval(this.refreshInterval);
            this.refreshInterval = null;
        }
    }

    /**
     * Dispose
     */
    dispose() {
        this.stopAutoRefresh();

        if (this.container) {
            this.container.remove();
        }
    }
}

// Make globally available
window.AdminDashboard = AdminDashboard;

// Auto-initialize if on admin page
if (window.location.pathname.includes('admin')) {
    window.adminDashboard = new AdminDashboard();
}
