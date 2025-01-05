const { defineConfig } = require('eslint-define-config');

module.exports = defineConfig({
    languageOptions: {
        globals: {
            browser: true,
        },
    },
    extends: [
        'eslint:recommended',
    ],
    parserOptions: {
        ecmaVersion: 12,
        sourceType: 'module',
    },
    rules: {
    },
});
