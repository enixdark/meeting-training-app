function isSignedIn() {
  const user = JSON.parse(localStorage.getItem('user'));
  if (user) {
    return true;
  }
  return false;
}
function userData() {
  return JSON.parse(localStorage.getItem('user'));
}
function updateUserData(data) {
  localStorage.setItem('user', JSON.stringify(data));
}
function signOut() {
  localStorage.removeItem('user');
}
export default {
  isSignedIn,
  userData,
  updateUserData,
  signOut,
};
