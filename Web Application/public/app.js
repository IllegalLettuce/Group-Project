// https://www.youtube.com/watch?v=9kRgVxULbag



document.addEventListener("DOMContentLoaded", event =>{

    const app = firebase.app();

    document.getElementById("googleLoginButton").addEventListener("click", googleLogin, false);

    function googleLogin(){
        const provider = new firebase.auth.GoogleAuthProvider();
        firebase.auth().signInWithRedirect(provider)
            .then(result =>{
                const user = result.user;
                document.write(`Hello, ${user.displayName}`);
                console.log(user)
            })
            .catch(console.log)
        const user = JSON.parse(localStorage.getItem("user"));
        console.log(user);
        document.getElementById('backButton').addEventListener('click', function() {
            window.history.back();
        });
    }






})







