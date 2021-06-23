const profilePixBtn = document.getElementById("picture");
const profilePix = document.getElementById("profile");

profilePixBtn.addEventListener("change", (event) => {
  setTimeout(() => {
    profilePix.src = profilePixBtn.value;
  }, 1000);
});
