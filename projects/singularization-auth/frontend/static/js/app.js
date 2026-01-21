/**
 * SPS Auth Workflow - Main JavaScript
 * 
 * Handles password strength meter, password confirmation, 
 * and singularization toggle functionality.
 */

/**
 * Initialize the password strength meter.
 * Updates the visual indicator as the user types.
 * 
 * The bar grows progressively:
 * - 0-5 chars: Red zone (0% to ~16% of bar, progressing within weak)
 * - 6-11 chars: Yellow zone (~16% to ~37% of bar, progressing within moderate)  
 * - 12-32 chars: Green zone (~37% to 100% of bar, progressing within strong)
 */
function initPasswordStrengthMeter() {
    const passwordInput = document.getElementById('password');
    const strengthBar = document.getElementById('password-strength-bar');
    const passwordHint = document.getElementById('password-hint');
    
    if (!passwordInput || !strengthBar) return;
    
    const MAX_LENGTH = 32;
    
    passwordInput.addEventListener('input', function() {
        const password = this.value;
        const length = password.length;
        
        // Remove existing classes
        strengthBar.classList.remove('weak', 'moderate', 'strong');
        
        if (length === 0) {
            strengthBar.style.width = '0%';
            strengthBar.style.backgroundColor = '';
            if (passwordHint) {
                passwordHint.textContent = '12-32 characters, include uppercase, digit, and special character';
                passwordHint.style.color = '';
            }
            return;
        }
        
        // Calculate progressive width based on character count
        // Map length to percentage: 0 chars = 0%, 32 chars = 100%
        const widthPercent = Math.min((length / MAX_LENGTH) * 100, 100);
        strengthBar.style.width = widthPercent + '%';
        
        // Determine color based on length thresholds
        if (length < 6) {
            // Weak: Red
            strengthBar.style.backgroundColor = '#ef4444';
            strengthBar.classList.add('weak');
            if (passwordHint) {
                passwordHint.textContent = 'Weak - keep typing';
                passwordHint.style.color = '#ef4444';
            }
        } else if (length < 12) {
            // Moderate: Yellow
            strengthBar.style.backgroundColor = '#eab308';
            strengthBar.classList.add('moderate');
            if (passwordHint) {
                passwordHint.textContent = 'Moderate - add more characters';
                passwordHint.style.color = '#eab308';
            }
        } else {
            // Strong: Green
            strengthBar.style.backgroundColor = '#22c55e';
            strengthBar.classList.add('strong');
            if (passwordHint) {
                passwordHint.textContent = 'Strong - looking good!';
                passwordHint.style.color = '#22c55e';
            }
        }
    });
}

/**
 * Initialize password confirmation validation.
 * Shows visual feedback when passwords match or differ.
 */
function initPasswordConfirmation() {
    const passwordInput = document.getElementById('password');
    const confirmInput = document.getElementById('confirm_password');
    const confirmHint = document.getElementById('confirm-hint');
    
    if (!passwordInput || !confirmInput) return;
    
    function checkMatch() {
        const password = passwordInput.value;
        const confirm = confirmInput.value;
        
        if (!confirmHint) return;
        
        if (confirm.length === 0) {
            confirmHint.textContent = '';
            confirmHint.style.color = '';
            return;
        }
        
        if (password === confirm) {
            confirmHint.textContent = 'Passwords match';
            confirmHint.style.color = '#22c55e';
        } else {
            confirmHint.textContent = 'Passwords do not match';
            confirmHint.style.color = '#ef4444';
        }
    }
    
    confirmInput.addEventListener('input', checkMatch);
    passwordInput.addEventListener('input', function() {
        if (confirmInput.value.length > 0) {
            checkMatch();
        }
    });
}

/**
 * Initialize the singularization toggle.
 * Shows a notice when enabled and logs the action to the server.
 * 
 * @param {string} pageName - The name of the current page (e.g., 'login', 'signup')
 */
function initSingularizationToggle(pageName) {
    const toggle = document.getElementById('singularization-toggle');
    const notice = document.getElementById('singularization-notice');
    
    if (!toggle || !notice) return;
    
    toggle.addEventListener('change', function() {
        if (this.checked) {
            notice.classList.remove('hidden');
            
            // Log to server
            fetch('/api/singularization-log', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ page: pageName })
            }).catch(function(error) {
                console.error('Failed to log singularization activation:', error);
            });
        } else {
            notice.classList.add('hidden');
        }
    });
}

/**
 * Update the current time display.
 * Called periodically to keep the time current.
 */
function updateCurrentTime() {
    const timeElement = document.getElementById('current-time');
    if (!timeElement) return;
    
    const now = new Date();
    const options = { 
        weekday: 'long', 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    };
    timeElement.textContent = now.toLocaleDateString('en-US', options);
}
