package com.example.myapplication.database
import com.example.myapplication.navigation.Screen
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.firestore.FirebaseFirestore

data class PriceAlert(
    val ticker: String,
    val name: String,
    val change: String
)

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

fun getPriceAlerts(onComplete: (List<PriceAlert>) -> Unit) {
    val firestore = FirebaseFirestore.getInstance()
    firestore.collection("pricealerts")
        .get()
        .addOnSuccessListener { documents ->
            val alerts = documents.map { document ->
                PriceAlert(
                    ticker = document.getString("ticker") ?: "",
                    name = document.getString("name") ?: "",
                    change = document.getString("change") ?: ""
                )
            }
            onComplete(alerts)
        }
        .addOnFailureListener {
            onComplete(emptyList())
        }
}


fun getCurrentUserId(): String? {
    val user = FirebaseAuth.getInstance().currentUser
    return user?.uid
}