const themeToggle = document.getElementById('themeToggle');
const html = document.documentElement;
const savedTheme = localStorage.getItem('cardioscan-theme');

if (savedTheme) {
  html.setAttribute('data-theme', savedTheme);
  updateButtonLabel(savedTheme);
}

themeToggle.addEventListener('click', () => {
  const currentTheme = html.getAttribute('data-theme') === 'light' ? 'dark' : 'light';
  html.setAttribute('data-theme', currentTheme);
  localStorage.setItem('cardioscan-theme', currentTheme);
  updateButtonLabel(currentTheme);
});

function updateButtonLabel(theme) {
  themeToggle.textContent = theme === 'light' ? '🌙 Dark Mode' : '☀️ Light Mode';
}

const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
    }
  });
}, { threshold: 0.15 });

document.querySelectorAll('.reveal').forEach((section) => observer.observe(section));

const form = document.getElementById('riskForm');
const resultLabel = document.querySelector('.result-label');
const riskBar = document.getElementById('riskBar');
const riskMessage = document.getElementById('riskMessage');
const riskAdvice = document.getElementById('riskAdvice');

form.addEventListener('submit', function (event) {
  event.preventDefault();

  const age = Number(document.getElementById('age').value);
  const gender = document.getElementById('gender').value;
  const chestPain = document.getElementById('chestPain').value;
  const bp = Number(document.getElementById('bp').value);
  const cholesterol = Number(document.getElementById('cholesterol').value);
  const fbs = document.getElementById('fbs').value;
  const heartRate = Number(document.getElementById('heartRate').value);
  const angina = document.getElementById('angina').value;

  let score = 0;

  if (age >= 60) score += 25;
  else if (age >= 45) score += 15;
  else if (age >= 35) score += 8;

  if (gender === 'male') score += 5;
  if (chestPain === 'asymptomatic') score += 18;
  else if (chestPain === 'non-anginal') score += 10;
  else if (chestPain === 'atypical') score += 5;

  if (bp >= 160) score += 12;
  else if (bp >= 140) score += 8;
  if (cholesterol >= 240) score += 10;
  else if (cholesterol >= 200) score += 5;
  if (fbs === 'yes') score += 6;
  if (heartRate <= 120) score += 8;
  else if (heartRate <= 140) score += 4;
  if (angina === 'yes') score += 12;

  score = Math.min(score, 100);

  let level = 'Low';
  let advice = 'Keep a healthy lifestyle and schedule regular checkups.';

  if (score >= 76) {
    level = 'Very High';
    advice = 'Please consult a medical professional for a full assessment as soon as possible.';
  } else if (score >= 51) {
    level = 'High';
    advice = 'Consider medical guidance and health monitoring soon.';
  } else if (score >= 26) {
    level = 'Moderate';
    advice = 'Monitor your health closely and discuss your risk factors with a doctor.';
  }

  resultLabel.textContent = `Estimated Risk Score: ${score}%`;
  riskBar.style.width = `${score}%`;
  riskMessage.textContent = `Risk Level: ${level}`;
  riskAdvice.textContent = advice;
});
