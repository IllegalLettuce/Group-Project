// https://www.youtube.com/watch?v=9kRgVxULbag



document.addEventListener("DOMContentLoaded", event =>{

    const app = firebase.app();

    document.getElementById("googleLoginButton").addEventListener("click", googleLogin, false);

    function googleLogin(){
        const provider = new firebase.auth.GoogleAuthProvider();
        firebase.auth().signInWithPopup(provider)
            .then(result =>{
                window.location.href="home.html"
            })
    }






})







