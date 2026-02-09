/**
 * Jest Configuration for Frontend Tests
 */

module.exports = {
    // Test environment
    testEnvironment: 'jsdom',

    // Test file patterns
    testMatch: [
        '**/tests/**/*.test.js',
        '**/tests/**/*.spec.js'
    ],

    // Coverage configuration
    collectCoverageFrom: [
        'digivice/js/**/*.js',
        '!digivice/js/**/*.min.js',
        '!digivice/js/vendor/**',
        '!**/node_modules/**'
    ],

    coverageDirectory: 'coverage',

    coverageReporters: [
        'html',
        'text',
        'lcov'
    ],

    coverageThreshold: {
        global: {
            branches: 40,
            functions: 40,
            lines: 40,
            statements: 40
        }
    },

    // Module paths
    modulePaths: [
        '<rootDir>/digivice/js'
    ],

    // Setup files
    setupFilesAfterEnv: [
        '<rootDir>/tests/setup.js'
    ],

    // Transform files
    transform: {
        '^.+\\.js$': 'babel-jest'
    },

    // Module name mapper for imports
    moduleNameMapper: {
        '\\.(css|less|scss|sass)$': 'identity-obj-proxy',
        '\\.(jpg|jpeg|png|gif|svg)$': '<rootDir>/tests/__mocks__/fileMock.js'
    },

    // Ignore patterns
    testPathIgnorePatterns: [
        '/node_modules/',
        '/dist/',
        '/build/'
    ],

    // Verbose output
    verbose: true,

    // Timeout
    testTimeout: 10000,

    // Clear mocks between tests
    clearMocks: true,

    // Restore mocks between tests
    restoreMocks: true,

    // Reset mocks between tests
    resetMocks: true
};
