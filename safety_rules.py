"""
Safety pattern definitions for terminal command analysis.
"""

DANGEROUS_PATTERNS = {
    'file_system_destruction': [
        'rm -rf /',
        'rm -rf ~',
        'rm -rf *',
        'rm -rf .*',
        '> /dev/sda',
        'dd if=/dev/zero',
        'mkfs.',
        ':(){:|:&};:',  # Fork bomb
    ],
    'privilege_escalation': [
        'sudo rm',
        'sudo dd',
        'sudo chmod 777',
        'sudo chown',
        'chmod -R 777',
    ],
    'data_exposure': [
        'cat /etc/passwd',
        'cat /etc/shadow',
        'history | grep password',
        'env | grep',
    ],
    'network_attacks': [
        'curl | sh',
        'wget | bash',
        'curl | sudo',
        '| bash',
        '| sh',
    ],
    'git_destructive': [
        'git push --force',
        'git push -f',
        'git reset --hard HEAD~',
        'git clean -fd',
        'git branch -D',
    ],
    'database_destructive': [
        'DROP DATABASE',
        'DROP TABLE',
        'DELETE FROM',
        'TRUNCATE',
        'ALTER TABLE DROP',
    ],
}

SAFE_ALTERNATIVES = {
    'rm -rf /': 'Specify the exact directory you want to remove, e.g., rm -rf /path/to/specific/dir',
    'rm -rf *': 'Use rm -i * for interactive deletion, or specify exact files',
    'sudo chmod 777': 'Use more restrictive permissions like 755 or 644',
    'git push --force': 'Use git push --force-with-lease to prevent overwriting others\' work',
    'curl | sh': 'Download the script first, inspect it, then run: curl -o script.sh URL && bash script.sh',
    'DROP DATABASE': 'Create a backup first: mysqldump database > backup.sql',
    'DELETE FROM': 'Use WHERE clause to limit scope: DELETE FROM table WHERE condition',
}

SEVERITY_LEVELS = {
    'CRITICAL': ['file_system_destruction', 'privilege_escalation'],
    'HIGH': ['data_exposure', 'network_attacks'],
    'MEDIUM': ['git_destructive', 'database_destructive'],
}

def get_severity(category):
    """Get severity level for a pattern category."""
    for level, categories in SEVERITY_LEVELS.items():
        if category in categories:
            return level
    return 'LOW'
