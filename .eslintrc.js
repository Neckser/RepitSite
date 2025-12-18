module.exports = {
    root: true,
    env: {
        browser: true,
        es2021: true,
        node: true,
    },
    extends: ['eslint:recommended', 'plugin:prettier/recommended'],
    parserOptions: {
        ecmaVersion: 'latest',
        sourceType: 'module',
    },
    plugins: ['prettier'],
    rules: {
        'no-console': 'off',
        'no-unused-vars': 'warn',
        'no-undef': 'off',
        'prettier/prettier': 'warn',
    },
    ignorePatterns: ['node_modules/', 'build/'],
};
