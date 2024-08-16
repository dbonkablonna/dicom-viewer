const emailInput = document.getElementById('email');
const passwordInput = document.getElementById('password');
const svgContainer = document.querySelector('.svgContainer');
const body = document.querySelector('.body');
const earL = document.querySelector('.earL');
const earR = document.querySelector('.earR');

function onInputFocus(input) {
    svgContainer.classList.add('focused');
    if (input.id === 'email') {
        body.classList.add('emailFocus');
        earL.classList.add('emailFocus');
        earR.classList.add('emailFocus');
    } else {
        body.classList.add('passwordFocus');
        earL.classList.add('passwordFocus');
        earR.classList.add('passwordFocus');
    }
}

function onInputBlur(input) {
    svgContainer.classList.remove('focused');
    body.classList.remove('emailFocus', 'passwordFocus');
    earL.classList.remove('emailFocus', 'passwordFocus');
    earR.classList.remove('emailFocus', 'passwordFocus');
}

emailInput.addEventListener('focus', () => onInputFocus(emailInput));
passwordInput.addEventListener('focus', () => onInputFocus(passwordInput));

emailInput.addEventListener('blur', () => onInputBlur(emailInput));
passwordInput.addEventListener('blur', () => onInputBlur(passwordInput));
