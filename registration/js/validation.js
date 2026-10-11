/**
 * Student Admission Portal - Client-Side Form Validation & Handling
 * CO3: HTML, CSS, JavaScript Validation
 */

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('registrationForm');
    const nameInput = document.getElementById('studentName');
    const rollInput = document.getElementById('rollNumber');
    const emailInput = document.getElementById('email');
    const courseSelect = document.getElementById('course');
    const passwordInput = document.getElementById('password');
    const confirmPasswordInput = document.getElementById('confirmPassword');
    const profilePicInput = document.getElementById('profilePic');
    const previewThumb = document.getElementById('previewThumb');
    const fileInfoText = document.getElementById('fileInfoText');
    const submitBtn = document.getElementById('submitBtn');
    const btnSpinner = document.getElementById('btnSpinner');
    const btnText = document.getElementById('btnText');
    const formAlert = document.getElementById('formAlert');
    const successScreen = document.getElementById('successScreen');
    const formContainer = document.getElementById('formContainer');

    // Password strength meters
    const strengthFill = document.getElementById('strengthFill');
    const strengthLabel = document.getElementById('strengthLabel');
    const reqLength = document.getElementById('reqLength');
    const reqUpper = document.getElementById('reqUpper');
    const reqLower = document.getElementById('reqLower');
    const reqDigit = document.getElementById('reqDigit');
    const reqSpecial = document.getElementById('reqSpecial');

    // Validation State
    const state = {
        name: false,
        roll: false,
        email: false,
        course: false,
        password: false,
        confirmPassword: false,
        profilePic: true // Optional or valid when uploaded
    };

    // Helper: Show field error
    function setError(input, message) {
        const group = input.closest('.form-group');
        const errElem = group ? group.querySelector('.field-error') : null;
        input.classList.add('input-error');
        input.classList.remove('input-valid');
        if (errElem) {
            errElem.textContent = message;
            errElem.classList.add('active');
            input.setAttribute('aria-invalid', 'true');
        }
    }

    // Helper: Clear field error
    function setSuccess(input) {
        const group = input.closest('.form-group');
        const errElem = group ? group.querySelector('.field-error') : null;
        input.classList.remove('input-error');
        input.classList.add('input-valid');
        if (errElem) {
            errElem.textContent = '';
            errElem.classList.remove('active');
            input.removeAttribute('aria-invalid');
        }
    }

    // 1. Student Name Validation
    function validateName() {
        const val = nameInput.value.trim();
        if (!val) {
            setError(nameInput, 'Student name is required.');
            state.name = false;
        } else if (val.length < 3) {
            setError(nameInput, 'Name must be at least 3 characters long.');
            state.name = false;
        } else if (!/^[a-zA-Z\s.'-]+$/.test(val)) {
            setError(nameInput, 'Name can only contain letters, spaces, and hyphens.');
            state.name = false;
        } else {
            setSuccess(nameInput);
            state.name = true;
        }
        return state.name;
    }

    // 2. Roll Number Validation
    function validateRoll() {
        const val = rollInput.value.trim();
        if (!val) {
            setError(rollInput, 'Roll number is required.');
            state.roll = false;
        } else if (!/^[A-Za-z0-9-_]{3,20}$/.test(val)) {
            setError(rollInput, 'Roll number must be 3-20 alphanumeric characters (e.g. CS2026-001).');
            state.roll = false;
        } else {
            setSuccess(rollInput);
            state.roll = true;
        }
        return state.roll;
    }

    // 3. Email Validation
    function validateEmail() {
        const val = emailInput.value.trim();
        const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        if (!val) {
            setError(emailInput, 'Email address is required.');
            state.email = false;
        } else if (!emailRegex.test(val)) {
            setError(emailInput, 'Please provide a valid email address (e.g. name@domain.com).');
            state.email = false;
        } else {
            setSuccess(emailInput);
            state.email = true;
        }
        return state.email;
    }

    // 4. Course Selection Validation
    function validateCourse() {
        const val = courseSelect.value;
        if (!val) {
            setError(courseSelect, 'Please select a program or course.');
            state.course = false;
        } else {
            setSuccess(courseSelect);
            state.course = true;
        }
        return state.course;
    }

    // 5. Password Strength Validation
    function validatePassword() {
        const val = passwordInput.value;
        const hasLength = val.length >= 8;
        const hasUpper = /[A-Z]/.test(val);
        const hasLower = /[a-z]/.test(val);
        const hasDigit = /[0-9]/.test(val);
        const hasSpecial = /[^A-Za-z0-9]/.test(val);

        // Update requirement badges
        updateReq(reqLength, hasLength);
        updateReq(reqUpper, hasUpper);
        updateReq(reqLower, hasLower);
        updateReq(reqDigit, hasDigit);
        updateReq(reqSpecial, hasSpecial);

        let score = 0;
        if (hasLength) score++;
        if (hasUpper) score++;
        if (hasLower) score++;
        if (hasDigit) score++;
        if (hasSpecial) score++;

        // Visual Meter
        if (val.length === 0) {
            strengthFill.style.width = '0%';
            strengthFill.style.backgroundColor = '#e2e8f0';
            strengthLabel.textContent = 'Password strength: None';
            setError(passwordInput, 'Password is required.');
            state.password = false;
        } else if (score < 3) {
            strengthFill.style.width = '30%';
            strengthFill.style.backgroundColor = '#e63946';
            strengthLabel.textContent = 'Password strength: Weak';
            setError(passwordInput, 'Password does not meet all security criteria.');
            state.password = false;
        } else if (score < 5) {
            strengthFill.style.width = '65%';
            strengthFill.style.backgroundColor = '#f59e0b';
            strengthLabel.textContent = 'Password strength: Moderate';
            setError(passwordInput, 'Please fulfill all password requirements.');
            state.password = false;
        } else {
            strengthFill.style.width = '100%';
            strengthFill.style.backgroundColor = '#2a9d8f';
            strengthLabel.textContent = 'Password strength: Strong & Secure';
            setSuccess(passwordInput);
            state.password = true;
        }

        // Re-validate confirmation if populated
        if (confirmPasswordInput.value.length > 0) {
            validateConfirmPassword();
        }

        return state.password;
    }

    function updateReq(element, isMet) {
        if (!element) return;
        if (isMet) {
            element.classList.add('met');
            element.classList.remove('unmet');
            element.querySelector('.req-icon').textContent = '✓';
        } else {
            element.classList.remove('met');
            element.classList.add('unmet');
            element.querySelector('.req-icon').textContent = '○';
        }
    }

    // 6. Confirm Password Validation
    function validateConfirmPassword() {
        const pass = passwordInput.value;
        const confirm = confirmPasswordInput.value;

        if (!confirm) {
            setError(confirmPasswordInput, 'Please confirm your password.');
            state.confirmPassword = false;
        } else if (pass !== confirm) {
            setError(confirmPasswordInput, 'Passwords do not match.');
            state.confirmPassword = false;
        } else {
            setSuccess(confirmPasswordInput);
            state.confirmPassword = true;
        }
        return state.confirmPassword;
    }

    // 7. File Upload Validation (Image / File)
    function validateFile() {
        const file = profilePicInput.files[0];
        if (!file) {
            // Profile image is optional during admission or can be required
            previewThumb.style.display = 'none';
            fileInfoText.textContent = 'JPEG, PNG, or WebP up to 2MB (Optional)';
            state.profilePic = true;
            return true;
        }

        const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp'];
        const maxSize = 2 * 1024 * 1024; // 2MB

        if (!allowedTypes.includes(file.type.toLowerCase())) {
            setError(profilePicInput, 'Invalid file format. Only JPG, PNG, and WebP are accepted.');
            previewThumb.style.display = 'none';
            fileInfoText.textContent = 'Allowed: JPG, PNG, WebP (Max 2MB)';
            state.profilePic = false;
            return false;
        }

        if (file.size > maxSize) {
            setError(profilePicInput, 'File size exceeds 2MB limit (' + (file.size / 1024 / 1024).toFixed(2) + 'MB).');
            previewThumb.style.display = 'none';
            state.profilePic = false;
            return false;
        }

        // Generate live thumbnail preview
        const reader = new FileReader();
        reader.onload = (e) => {
            previewThumb.src = e.target.result;
            previewThumb.style.display = 'block';
        };
        reader.readAsDataURL(file);

        setSuccess(profilePicInput);
        fileInfoText.textContent = `${file.name} (${(file.size / 1024).toFixed(1)} KB)`;
        state.profilePic = true;
        return true;
    }

    // Event Listeners for Live Validation
    nameInput.addEventListener('input', validateName);
    nameInput.addEventListener('blur', validateName);

    rollInput.addEventListener('input', validateRoll);
    rollInput.addEventListener('blur', validateRoll);

    emailInput.addEventListener('input', validateEmail);
    emailInput.addEventListener('blur', validateEmail);

    courseSelect.addEventListener('change', validateCourse);
    courseSelect.addEventListener('blur', validateCourse);

    passwordInput.addEventListener('input', validatePassword);
    passwordInput.addEventListener('blur', validatePassword);

    confirmPasswordInput.addEventListener('input', validateConfirmPassword);
    confirmPasswordInput.addEventListener('blur', validateConfirmPassword);

    profilePicInput.addEventListener('change', validateFile);

    // Form Submission Handler
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Run full validation check
        const isNameOk = validateName();
        const isRollOk = validateRoll();
        const isEmailOk = validateEmail();
        const isCourseOk = validateCourse();
        const isPassOk = validatePassword();
        const isConfirmOk = validateConfirmPassword();
        const isFileOk = validateFile();

        if (!isNameOk || !isRollOk || !isEmailOk || !isCourseOk || !isPassOk || !isConfirmOk || !isFileOk) {
            formAlert.className = 'alert-banner alert-error';
            formAlert.textContent = 'Please correct the highlighted errors before submitting the application.';
            // Scroll to the first error
            const firstError = form.querySelector('.input-error');
            if (firstError) firstError.focus();
            return;
        }

        // Hide alert & set loading state
        formAlert.style.display = 'none';
        submitBtn.disabled = true;
        btnSpinner.style.display = 'inline-block';
        btnText.textContent = 'Submitting Application...';

        try {
            const formData = new FormData(form);
            const response = await fetch('register.php', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (data.status === 'success') {
                // Show rich success view
                formContainer.style.display = 'none';
                successScreen.style.display = 'block';

                document.getElementById('resRoll').textContent = data.student.roll_number;
                document.getElementById('resName').textContent = data.student.name;
                document.getElementById('resEmail').textContent = data.student.email;
                document.getElementById('resCourse').textContent = data.student.course;
                document.getElementById('resDate').textContent = data.student.registration_date || new Date().toLocaleString();
            } else {
                formAlert.className = 'alert-banner alert-error';
                formAlert.textContent = data.message || 'Registration failed. Please verify your details.';
                formAlert.style.display = 'block';
                formAlert.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        } catch (error) {
            console.error('Submission error:', error);
            formAlert.className = 'alert-banner alert-error';
            formAlert.textContent = 'Network or server error encountered. If using XAMPP, ensure Apache and MySQL are running.';
            formAlert.style.display = 'block';
        } finally {
            submitBtn.disabled = false;
            btnSpinner.style.display = 'none';
            btnText.textContent = 'Complete Registration';
        }
    });

    // Reset Form button in success screen
    const resetBtn = document.getElementById('registerAnotherBtn');
    if (resetBtn) {
        resetBtn.addEventListener('click', (e) => {
            e.preventDefault();
            form.reset();
            strengthFill.style.width = '0%';
            previewThumb.style.display = 'none';
            fileInfoText.textContent = 'JPEG, PNG, or WebP up to 2MB (Optional)';
            document.querySelectorAll('.req-item').forEach(el => updateReq(el, false));
            document.querySelectorAll('.form-control').forEach(el => {
                el.classList.remove('input-valid', 'input-error');
            });
            successScreen.style.display = 'none';
            formContainer.style.display = 'block';
        });
    }
});
