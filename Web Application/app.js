import firebase from "firebase/compat";

document.addEventListener("DOMContentLoaded",event =>{

    const app = firebase.app();

    const db = firebase.firestore();

    const post = db.collection('ProjectPosts').doc('firstpost');


    myPost.on(
        then(doc =>{
            const data = doc.data();
            document.write(data.title +`<br>`)
            document.write(data.created)
        })
    )
})






function googleLogin(){
    const provider = new firebase.auth.GoogleAuthProvider();
    firebase.auth().signInWithPopup(provider)
                .then(result =>{
                    const user = result.user;
                    document.write(`Hello, ${user.displayName}`);
                    console.log(user)
                })
                .catch(console.log)
                // Get user info from local storage
                const user = JSON.parse(localStorage.getItem("user"));
                console.log(user);
    document.getElementById('backButton').addEventListener('click', function() {
    window.history.back();
});


}


