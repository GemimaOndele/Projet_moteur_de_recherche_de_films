/* js/script.js
   - Onglets Login / Register (un seul formulaire visible à la fois)
   - Mock d'authentification (localStorage) + redirection vers profil
*/

// ----- Sélecteurs -----
const loginTab = document.getElementById("loginTab");
const registerTab = document.getElementById("registerTab");
const loginForm = document.getElementById("loginForm");
const registerForm = document.getElementById("registerForm");

// Champs login
const loginEmail = document.getElementById("loginEmail");
const loginPassword = document.getElementById("loginPassword");

// Champs register
const regName = document.getElementById("regName");
const regEmail = document.getElementById("regEmail");
const regPassword = document.getElementById("regPassword");
const regConfirm = document.getElementById("regConfirm");

// ----- Helper: activer un onglet -----
function setActiveTab(which) {
  const showLogin = which === "login";

  // classes
  loginTab?.classList.toggle("active", showLogin);
  registerTab?.classList.toggle("active", !showLogin);
  loginForm?.classList.toggle("active", showLogin);
  registerForm?.classList.toggle("active", !showLogin);

  // accessibilité (facultatif mais propre)
  loginTab?.setAttribute("aria-selected", String(showLogin));
  registerTab?.setAttribute("aria-selected", String(!showLogin));

  // focus premier champ
  if (showLogin) {
    loginEmail?.focus();
  } else {
    regName?.focus();
  }
}

// ----- Événements onglets -----
if (loginTab && registerTab && loginForm && registerForm) {
  loginTab.addEventListener("click", () => setActiveTab("login"));
  registerTab.addEventListener("click", () => setActiveTab("register"));

  // État initial : si URL contient #register on affiche inscription
  if (location.hash.replace("#", "") === "register") {
    setActiveTab("register");
  } else {
    setActiveTab("login");
  }
}

// ----- Petits plus: empêcher les boutons sociaux de soumettre le formulaire -----
document.querySelectorAll(".social").forEach(btn => {
  btn.addEventListener("click", (e) => e.preventDefault());
});