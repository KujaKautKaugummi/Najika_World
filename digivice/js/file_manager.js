/**
 * NAJIKA FILE MANAGER - Matrix-Style File Browser
 * Full-featured file explorer with drag-drop, context menus
 */

const FileManager = {
    isOpen: false,
    overlay: null,
    currentPath: '.',
    selectedFiles: [],
    clipboard: null, // {type: 'copy'|'cut', files: [...]}

    open() {
        if (this.isOpen) return;
        this.isOpen = true;

        this.overlay = document.createElement('div');
        this.overlay.id = 'fileManagerOverlay';
        this.overlay.innerHTML = `
            <div class="file-manager-container">
                <!-- Header -->
                <div class="file-manager-header">
                    <div class="header-left">
                        <span class="terminal-icon">⬢</span>
                        <span class="title">FILE MANAGER</span>
                        <span class="status-indicator">●</span>
                    </div>
                    <div class="header-actions">
                        <button class="header-btn" onclick="FileManager.goBack()" title="Zurück">◄</button>
                        <button class="header-btn" onclick="FileManager.goHome()" title="Home">🏠</button>
                        <button class="header-btn" onclick="FileManager.refresh()" title="Aktualisieren">🔄</button>
                        <button class="header-btn" onclick="FileManager.createFolder()" title="Neuer Ordner">📁+</button>
                        <button class="header-btn" onclick="FileManager.createFile()" title="Neue Datei">📄+</button>
                    </div>
                    <button class="close-btn" onclick="FileManager.close()">✕</button>
                </div>

                <!-- Path Bar -->
                <div class="path-bar">
                    <span class="path-label">PATH:</span>
                    <input type="text" id="filePathInput" value="." readonly />
                    <button onclick="FileManager.navigateTo()">GO</button>
                </div>

                <!-- Main Area -->
                <div class="file-manager-main">
                    <!-- File List (Left/Main) -->
                    <div class="file-list-container">
                        <div class="file-list-header">
                            <div class="col-name">NAME</div>
                            <div class="col-type">TYPE</div>
                            <div class="col-size">SIZE</div>
                            <div class="col-actions">ACTIONS</div>
                        </div>
                        <div class="file-list" id="fileList">
                            <div class="loading-indicator">🔄 Lädt Dateien...</div>
                        </div>
                    </div>

                    <!-- File Preview (Right) -->
                    <div class="file-preview-panel">
                        <div class="preview-header">PREVIEW</div>
                        <div class="preview-content" id="filePreview">
                            <div class="preview-empty">Keine Datei ausgewählt</div>
                        </div>
                    </div>
                </div>

                <!-- Bottom Actions -->
                <div class="file-manager-footer">
                    <div class="selection-info">
                        <span id="fileCountDisplay">0 Dateien</span>
                        <span id="selectedCountDisplay"></span>
                    </div>
                    <div class="clipboard-info" id="clipboardInfo"></div>
                </div>
            </div>
        `;

        document.body.appendChild(this.overlay);

        // Load initial directory
        this.loadDirectory(this.currentPath);

        // Setup keyboard shortcuts
        this.setupKeyboardShortcuts();
    },

    close() {
        if (!this.isOpen) return;
        this.isOpen = false;
        if (this.overlay) {
            this.overlay.remove();
            this.overlay = null;
        }
    },

    async loadDirectory(path) {
        const fileList = document.getElementById('fileList');
        if (!fileList) return;

        fileList.innerHTML = '<div class="loading-indicator">🔄 Lädt Dateien...</div>';

        try {
            const response = await fetch('/api/file/list', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({path})
            });
            const data = await response.json();

            if (data.success) {
                this.currentPath = path;
                this.renderFileList(data.files);
                this.updatePathBar();
                this.updateFooter(data.files.length);
            } else {
                fileList.innerHTML = `<div class="error-message">❌ Fehler: ${data.error}</div>`;
            }
        } catch (error) {
            fileList.innerHTML = `<div class="error-message">❌ Netzwerkfehler: ${error.message}</div>`;
        }
    },

    renderFileList(files) {
        const fileList = document.getElementById('fileList');
        if (!fileList) return;

        if (files.length === 0) {
            fileList.innerHTML = '<div class="empty-folder">📂 Leerer Ordner</div>';
            return;
        }

        // Sort: folders first, then files
        files.sort((a, b) => {
            if (a.type === b.type) return a.name.localeCompare(b.name);
            return a.type === 'folder' ? -1 : 1;
        });

        fileList.innerHTML = '';
        files.forEach(file => {
            const row = this.createFileRow(file);
            fileList.appendChild(row);
        });
    },

    createFileRow(file) {
        const row = document.createElement('div');
        row.className = `file-row ${file.type}`;
        row.dataset.filename = file.name;
        row.dataset.type = file.type;

        const icon = this.getFileIcon(file);
        const size = file.type === 'file' ? this.formatSize(file.size) : '-';

        row.innerHTML = `
            <div class="col-name">
                <span class="file-icon">${icon}</span>
                <span class="file-name">${file.name}</span>
            </div>
            <div class="col-type">${file.type.toUpperCase()}</div>
            <div class="col-size">${size}</div>
            <div class="col-actions">
                <button class="action-btn" onclick="FileManager.openFile('${file.name}', '${file.type}')" title="Öffnen">📂</button>
                <button class="action-btn" onclick="FileManager.renameFile('${file.name}')" title="Umbenennen">✏️</button>
                <button class="action-btn" onclick="FileManager.deleteFile('${file.name}')" title="Löschen">🗑️</button>
            </div>
        `;

        // Click: select/deselect
        row.addEventListener('click', (e) => {
            if (!e.target.closest('.action-btn')) {
                this.toggleSelection(row);
            }
        });

        // Double-click: open
        row.addEventListener('dblclick', () => {
            this.openFile(file.name, file.type);
        });

        // Right-click: context menu
        row.addEventListener('contextmenu', (e) => {
            e.preventDefault();
            this.showContextMenu(e, file);
        });

        return row;
    },

    getFileIcon(file) {
        if (file.type === 'folder') return '📁';

        const ext = file.name.split('.').pop().toLowerCase();
        const iconMap = {
            'py': '🐍',
            'js': '📜',
            'html': '🌐',
            'css': '🎨',
            'json': '📋',
            'txt': '📄',
            'md': '📝',
            'png': '🖼️',
            'jpg': '🖼️',
            'jpeg': '🖼️',
            'gif': '🖼️',
            'mp3': '🎵',
            'mp4': '🎬',
            'zip': '📦',
            'pdf': '📕'
        };

        return iconMap[ext] || '📄';
    },

    formatSize(bytes) {
        if (bytes === 0) return '0 B';
        const k = 1024;
        const sizes = ['B', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
    },

    toggleSelection(row) {
        row.classList.toggle('selected');

        const filename = row.dataset.filename;
        const index = this.selectedFiles.indexOf(filename);

        if (index > -1) {
            this.selectedFiles.splice(index, 1);
        } else {
            this.selectedFiles.push(filename);
        }

        this.updateSelectionDisplay();
    },

    updateSelectionDisplay() {
        const display = document.getElementById('selectedCountDisplay');
        if (display) {
            if (this.selectedFiles.length > 0) {
                display.textContent = `| ${this.selectedFiles.length} ausgewählt`;
            } else {
                display.textContent = '';
            }
        }
    },

    async openFile(filename, type) {
        if (type === 'folder') {
            const newPath = this.currentPath === '.' ? filename : `${this.currentPath}/${filename}`;
            this.loadDirectory(newPath);
        } else {
            // Load file preview
            await this.loadFilePreview(filename);
        }
    },

    async loadFilePreview(filename) {
        const preview = document.getElementById('filePreview');
        if (!preview) return;

        preview.innerHTML = '<div class="loading-indicator">🔄 Lädt...</div>';

        const filePath = this.currentPath === '.' ? filename : `${this.currentPath}/${filename}`;

        try {
            const response = await fetch('/api/file/read', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({path: filePath})
            });
            const data = await response.json();

            if (data.success) {
                // Show preview
                const ext = filename.split('.').pop().toLowerCase();
                const textFormats = ['py', 'js', 'html', 'css', 'json', 'txt', 'md'];

                if (textFormats.includes(ext)) {
                    preview.innerHTML = `
                        <div class="preview-header-info">
                            <strong>${filename}</strong>
                            <button onclick="FileManager.editFile('${filename}')">✏️ Edit</button>
                        </div>
                        <pre class="preview-text">${this.escapeHtml(data.content)}</pre>
                    `;
                } else {
                    preview.innerHTML = `
                        <div class="preview-header-info">
                            <strong>${filename}</strong>
                        </div>
                        <div class="preview-binary">
                            📦 Binärdatei (${ext.toUpperCase()})
                            <br><br>
                            <button onclick="FileManager.downloadFile('${filename}')">⬇️ Download</button>
                        </div>
                    `;
                }
            } else {
                preview.innerHTML = `<div class="error-message">❌ ${data.error}</div>`;
            }
        } catch (error) {
            preview.innerHTML = `<div class="error-message">❌ ${error.message}</div>`;
        }
    },

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    },

    async createFolder() {
        const name = prompt('Ordnername:');
        if (!name) return;

        const path = this.currentPath === '.' ? name : `${this.currentPath}/${name}`;

        try {
            const response = await fetch('/api/file/write', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    path: `${path}/.keep`,
                    content: ''
                })
            });
            const data = await response.json();

            if (data.success) {
                notify(`✓ Ordner erstellt: ${name}`, 'success');
                this.refresh();
            } else {
                notify(`Fehler: ${data.error}`, 'error');
            }
        } catch (error) {
            notify('Ordner konnte nicht erstellt werden', 'error');
        }
    },

    async createFile() {
        const name = prompt('Dateiname:');
        if (!name) return;

        const path = this.currentPath === '.' ? name : `${this.currentPath}/${name}`;

        try {
            const response = await fetch('/api/file/write', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    path,
                    content: ''
                })
            });
            const data = await response.json();

            if (data.success) {
                notify(`✓ Datei erstellt: ${name}`, 'success');
                this.refresh();
            } else {
                notify(`Fehler: ${data.error}`, 'error');
            }
        } catch (error) {
            notify('Datei konnte nicht erstellt werden', 'error');
        }
    },

    async deleteFile(filename) {
        if (!confirm(`Wirklich löschen: ${filename}?`)) return;

        // TODO: Backend needs /api/file/delete endpoint
        notify('⚠️ Delete-Funktion noch nicht im Backend implementiert', 'warning');
    },

    async renameFile(filename) {
        const newName = prompt('Neuer Name:', filename);
        if (!newName || newName === filename) return;

        // TODO: Backend needs /api/file/rename endpoint
        notify('⚠️ Rename-Funktion noch nicht im Backend implementiert', 'warning');
    },

    goBack() {
        if (this.currentPath === '.') return;

        const parts = this.currentPath.split('/');
        parts.pop();
        const newPath = parts.length > 0 ? parts.join('/') : '.';
        this.loadDirectory(newPath);
    },

    goHome() {
        this.loadDirectory('.');
    },

    refresh() {
        this.loadDirectory(this.currentPath);
    },

    updatePathBar() {
        const input = document.getElementById('filePathInput');
        if (input) {
            input.value = this.currentPath;
        }
    },

    updateFooter(fileCount) {
        const display = document.getElementById('fileCountDisplay');
        if (display) {
            display.textContent = `${fileCount} Dateien`;
        }
    },

    showContextMenu(event, file) {
        // TODO: Implement context menu
        console.log('Context menu for:', file);
    },

    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            if (!this.isOpen) return;

            // F5: Refresh
            if (e.key === 'F5') {
                e.preventDefault();
                this.refresh();
            }
            // Backspace: Go back
            if (e.key === 'Backspace') {
                e.preventDefault();
                this.goBack();
            }
            // Ctrl+A: Select all
            if (e.ctrlKey && e.key === 'a') {
                e.preventDefault();
                this.selectAll();
            }
            // Delete: Delete selected
            if (e.key === 'Delete' && this.selectedFiles.length > 0) {
                e.preventDefault();
                this.deleteSelected();
            }
        });
    },

    selectAll() {
        const rows = document.querySelectorAll('.file-row');
        this.selectedFiles = [];
        rows.forEach(row => {
            row.classList.add('selected');
            this.selectedFiles.push(row.dataset.filename);
        });
        this.updateSelectionDisplay();
    },

    deleteSelected() {
        if (this.selectedFiles.length === 0) return;
        const files = this.selectedFiles.join(', ');
        if (confirm(`${this.selectedFiles.length} Dateien löschen: ${files}?`)) {
            // TODO: Batch delete
            notify('⚠️ Batch-Delete noch nicht implementiert', 'warning');
        }
    },

    editFile(filename) {
        // Open in Code Editor
        if (window.CodeEditor) {
            this.close();
            CodeEditor.open();
            setTimeout(() => {
                const filePath = this.currentPath === '.' ? filename : `${this.currentPath}/${filename}`;
                CodeEditor.loadFile(filePath);
            }, 300);
        }
    }
};

// Global verfügbar machen
window.FileManager = FileManager;
