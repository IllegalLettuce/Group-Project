package com.example.myapplication.database
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.firestore.FirebaseFirestore

fun registerUser(email: String, password: String, onComplete: (Boolean, String?) -> Unit) {
    val auth = FirebaseAuth.getInstance()
    auth.createUserWithEmailAndPassword(email, password)
        .addOnCompleteListener { task ->
            if (task.isSuccessful) {
                onComplete(true, null)
            } else {
                onComplete(false, task.exception?.message)
            }
        }
}

fun loginUser(email: String, password: String, onComplete: (Boolean, String?) -> Unit) {
    val auth = FirebaseAuth.getInstance()
    auth.signInWithEmailAndPassword(email, password)
        .addOnCompleteListener { task ->
            if (task.isSuccessful) {
                onComplete(true, null)
            } else {
                onComplete(false, task.exception?.message)
            }
        }
}

fun submitReview(rating: String, review: String, onComplete: (Boolean, String?) -> Unit) {
    val firestore = FirebaseFirestore.getInstance()
    val reviewData = hashMapOf(
        "rating" to rating,
        "review" to review
    )

    firestore.collection("reviews")
        .add(reviewData)
        .addOnSuccessListener { documentReference ->
            onComplete(true, null)
        }
        .addOnFailureListener { e ->
            onComplete(false, e.message)
        }
}