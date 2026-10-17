/**
 * SPS Auth Workflow - Main JavaScript
 * 
 * Handles password strength meter, password confirmation, 
 * and singularization toggle functionality.
 */

/**
 * Global flag: whether singularization mode is currently active.
 * Toggled by initSingularizationToggle(). Affects the password
 * strength meter thresholds.
 */
var singularizationEnabled = false;

/**
 * Initialize the password strength meter.
 * Updates the visual indicator as the user types.
 * 
 * Standard mode (singularization OFF):
 * - 0-5 chars: Red zone, progressing within weak
 * - 6-11 chars: Yellow zone, progressing within moderate
 * - 12-32 chars: Green zone, progressing within strong
 * 
 * Singularization mode (singularization ON):
 * - 0 chars: 0%
 * - 1 char: ~20%, red
 * - 2 chars: ~50%, yellow
 * - 3 chars: ~75%, green
 * - 4 chars: ~90%, green
 * - 5+ chars: 100%, green
 * Because a 64-hex-char nonce is concatenated server-side, even
 * a 3-character password becomes extremely strong.
 */
function initPasswordStrengthMeter() {
    var passwordInput = document.getElementById('password');
    var strengthBar = document.getElementById('password-strength-bar');
    var passwordHint = document.getElementById('password-hint');
    
    if (!passwordInput || !strengthBar) return;
    
    passwordInput.addEventListener('input', function() {
        updatePasswordStrengthBar(this.value, strengthBar, passwordHint);
    });
}

/**
 * Compute and apply the password strength bar state.
 * Extracted so it can be re-triggered when the singularization
 * toggle changes.
 */
function updatePasswordStrengthBar(password, strengthBar, passwordHint) {
    var length = password.length;
    
    // Remove existing classes
    strengthBar.classList.remove('weak', 'moderate', 'strong');
    
    if (length === 0) {
        strengthBar.style.width = '0%';
        strengthBar.style.backgroundColor = '';
        if (passwordHint) {
            if (singularizationEnabled) {
                passwordHint.textContent = 'Minimum 3 characters (singularization provides additional security)';
            } else {
                passwordHint.textContent = '12-32 characters, include uppercase, digit, and special character';
            }
            passwordHint.style.color = '';
        }
        return;
    }
    
    if (singularizationEnabled) {
        // Singularization mode: strength ramps up very fast
        // Green threshold is 3 chars. At 3 chars, show progressive width.
        // At 4+ chars, snap to 100% and stay there.
        var widthPercent;
        if (length >= 4) {
            widthPercent = 100;
        } else {
            widthPercent = Math.min((length / 5) * 100, 100);
        }
        strengthBar.style.width = widthPercent + '%';
        
        if (length < 2) {
            strengthBar.style.backgroundColor = '#ef4444';
            strengthBar.classList.add('weak');
            if (passwordHint) {
                passwordHint.textContent = 'Weak - keep typing';
                passwordHint.style.color = '#ef4444';
            }
        } else if (length < 3) {
            strengthBar.style.backgroundColor = '#eab308';
            strengthBar.classList.add('moderate');
            if (passwordHint) {
                passwordHint.textContent = 'Moderate - almost there';
                passwordHint.style.color = '#eab308';
            }
        } else {
            strengthBar.style.backgroundColor = '#22c55e';
            strengthBar.classList.add('strong');
            if (passwordHint) {
                passwordHint.textContent = 'Strong - singularization secures your password!';
                passwordHint.style.color = '#22c55e';
            }
        }
    } else {
        // Standard mode: green threshold is 12 chars.
        // At 12 chars, show progressive width. At 13+ chars, snap to 100%.
        var MAX_LENGTH = 32;
        var widthPercent;
        if (length >= 13) {
            widthPercent = 100;
        } else {
            widthPercent = Math.min((length / MAX_LENGTH) * 100, 100);
        }
        strengthBar.style.width = widthPercent + '%';
        
        if (length < 6) {
            strengthBar.style.backgroundColor = '#ef4444';
            strengthBar.classList.add('weak');
            if (passwordHint) {
                passwordHint.textContent = 'Weak - keep typing';
                passwordHint.style.color = '#ef4444';
            }
        } else if (length < 12) {
            strengthBar.style.backgroundColor = '#eab308';
            strengthBar.classList.add('moderate');
            if (passwordHint) {
                passwordHint.textContent = 'Moderate - add more characters';
                passwordHint.style.color = '#eab308';
            }
        } else {
            strengthBar.style.backgroundColor = '#22c55e';
            strengthBar.classList.add('strong');
            if (passwordHint) {
                passwordHint.textContent = 'Strong - looking good!';
                passwordHint.style.color = '#22c55e';
            }
        }
    }
}

/**
 * Initialize password confirmation validation.
 * Shows visual feedback when passwords match or differ.
 */
function initPasswordConfirmation() {
    var passwordInput = document.getElementById('password');
    var confirmInput = document.getElementById('confirm_password');
    var confirmHint = document.getElementById('confirm-hint');
    
    if (!passwordInput || !confirmInput) return;
    
    function checkMatch() {
        var password = passwordInput.value;
        var confirm = confirmInput.value;
        
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
 * 
 * When toggled ON:
 * - Updates the hidden form input to "on" so the backend receives it
 * - Shows a contextual notice (different text for signup vs login)
 * - Sets the global singularizationEnabled flag
 * - Re-triggers the password strength meter (signup page only)
 * - Logs the action to the server
 * 
 * When toggled OFF:
 * - Reverses all of the above
 * 
 * @param {string} pageName - 'login' or 'signup'
 */
function initSingularizationToggle(pageName) {
    var toggle = document.getElementById('singularization-toggle');
    var notice = document.getElementById('singularization-notice');
    var hiddenInput = document.getElementById('singularization-value');
    
    if (!toggle || !notice) return;
    
    toggle.addEventListener('change', function() {
        singularizationEnabled = this.checked;
        
        // Sync hidden form input
        if (hiddenInput) {
            hiddenInput.value = this.checked ? 'on' : 'off';
        }
        
        if (this.checked) {
            notice.classList.remove('hidden');
        } else {
            notice.classList.add('hidden');
        }
        
        // Re-trigger password strength meter on signup page
        if (pageName === 'signup') {
            var passwordInput = document.getElementById('password');
            var strengthBar = document.getElementById('password-strength-bar');
            var passwordHint = document.getElementById('password-hint');
            if (passwordInput && strengthBar) {
                updatePasswordStrengthBar(passwordInput.value, strengthBar, passwordHint);
            }
        }
        
        // Log to server
        fetch('/api/singularization-log', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ page: pageName, enabled: this.checked })
        }).catch(function(error) {
            console.error('Failed to log singularization toggle:', error);
        });
    });
}

/**
 * Update the current time display.
 * Called periodically to keep the time current.
 */
function updateCurrentTime() {
    var timeElement = document.getElementById('current-time');
    if (!timeElement) return;
    
    var now = new Date();
    var options = { 
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
