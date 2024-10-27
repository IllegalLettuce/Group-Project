package com.example.myapplication

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.Image
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.DropdownMenu
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.ExposedDropdownMenuBox
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.material3.TextField
import androidx.compose.material3.TextFieldDefaults
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.input.VisualTransformation
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.navigation.NavController
import androidx.navigation.NavHostController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.example.myapplication.ui.theme.MyApplicationTheme
import com.google.firebase.FirebaseApp
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.firestore.FirebaseFirestore

sealed class Screen(val route: String) {
    object Login : Screen("Login")
    object Register : Screen("Register")
    object Home : Screen("Home")
    object PurchaseAssets : Screen("PurchaseAssets")
    object Payment : Screen("Payment")
    object PriceAlert : Screen("PriceAlert")
    object HelpSupport : Screen("HelpSupport")
    object RatingReviewScreen : Screen("RatingReviewScreen")
}

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        FirebaseApp.initializeApp(this)
        enableEdgeToEdge()
        setContent {
            MyApplicationTheme {
                MainApp()
            }
        }
    }
}

@Composable
fun MainApp() {
    val navController = rememberNavController()
    NavHost(navController = navController, startDestination = Screen.Login.route) {
        composable(Screen.Login.route) {
            LoginScreen(navController)
        }
        composable(Screen.Register.route) {
            RegisterScreen(navController)
        }
        composable(Screen.Home.route) { HomeScreen(navController) }
        composable(Screen.Payment.route) { PaymentScreen() }
        composable(Screen.PriceAlert.route) { PriceAlertScreen() }
        composable(Screen.PurchaseAssets.route) { PurchaseAssetsScreen() }
        composable(Screen.HelpSupport.route) { HelpSupportScreen(navController) }
        composable(Screen.RatingReviewScreen.route) { RatingReviewScreen(navController) }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun LoginScreen(navController: NavHostController) {
    var email by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }
    var errorMessage by remember { mutableStateOf("") }

    Box(
        modifier = Modifier.fillMaxSize()
    ) {
        Image(
            painter = painterResource(id = R.drawable.background),
            contentDescription = null,
            contentScale = ContentScale.Crop,
            modifier = Modifier.fillMaxSize()
        )
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(16.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Top
        ) {
            Spacer(modifier = Modifier.height(40.dp))
            Text(
                text = "Login",
                style = MaterialTheme.typography.headlineMedium,
                modifier = Modifier.align(Alignment.CenterHorizontally)
            )

            Spacer(modifier = Modifier.height(40.dp))

            TextField(
                value = email,
                onValueChange = { email = it },
                label = { Text("Email") },
                modifier = Modifier
                    .padding(horizontal = 8.dp),
                keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Email),
                shape = MaterialTheme.shapes.medium,
                colors = TextFieldDefaults.textFieldColors(
                    containerColor = Color.Transparent,
                    focusedTextColor = Color.White
                )
            )

            Spacer(modifier = Modifier.height(16.dp))

            TextField(
                value = password,
                onValueChange = { password = it },
                label = { Text("Password") },
                modifier = Modifier
                    .padding(horizontal = 8.dp),
                keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Password),
                shape = MaterialTheme.shapes.medium,
                colors = TextFieldDefaults.textFieldColors(
                    containerColor = Color.Transparent,
                    focusedTextColor = Color.White
                )
            )

            Spacer(modifier = Modifier.height(32.dp))
            TextButton(
                onClick = {
                    loginUser(email, password) { success, error ->
                        if (success) {
                            navController.navigate(Screen.Home.route)
                        } else {
                            errorMessage = error ?: "Login failed"
                        }
                    }
                },
                modifier = Modifier.fillMaxWidth()
                    .padding(horizontal = 8.dp),
                colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.primary)
            ) {
                Text("Login")
            }

            Spacer(modifier = Modifier.height(16.dp))




            if (errorMessage.isNotEmpty()) {
                Text(text = errorMessage, color = Color.Red)
                Spacer(modifier = Modifier.height(16.dp))
            }
            TextButton(
                onClick = { navController.navigate(Screen.Register.route) },
                modifier = Modifier.fillMaxWidth()
                    .padding(horizontal = 8.dp),
                colors = ButtonDefaults.textButtonColors(contentColor = MaterialTheme.colorScheme.primary)
            ) {
                Text("Register")
            }
        }
    }
}


@Composable
fun RegisterScreen(navController: NavHostController) {
    var email by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }
    var errorMessage by remember { mutableStateOf("") }

    Box(
        modifier = Modifier.fillMaxSize()
    ) {
        Image(
            painter = painterResource(id = R.drawable.background),
            contentDescription = null,
            contentScale = ContentScale.Crop,
            modifier = Modifier.fillMaxSize()
        )

        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(16.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center
        ) {
            Text(text = "Register", style = MaterialTheme.typography.headlineSmall)

            TextField(value = email, onValueChange = { email = it }, label = { Text("Email") })
            Spacer(modifier = Modifier.height(8.dp))

            TextField(
                value = password,
                onValueChange = { password = it },
                label = { Text("Password") })
            Spacer(modifier = Modifier.height(16.dp))

            TextButton(
                colors = ButtonDefaults.textButtonColors(contentColor = MaterialTheme.colorScheme.primary),
                onClick = {
                    registerUser(email, password) { success, error ->
                        if (success) {
                            navController.navigate(Screen.Login.route)
                        } else {
                            errorMessage = error ?: "Registration failed"
                        }
                    }
                }
            ) {
                Text("Register")
            }

            Spacer(modifier = Modifier.height(8.dp))

            if (errorMessage.isNotEmpty()) {
                Text(text = errorMessage, color = Color.Red)
            }

            TextButton(
                colors = ButtonDefaults.textButtonColors(contentColor = MaterialTheme.colorScheme.primary),
                onClick = { navController.navigate(Screen.Login.route) }) {
                Text("Login")
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun HomeScreen(navController: NavHostController) {
    var expanded by remember { mutableStateOf(false) }
    var selectedOption by remember { mutableStateOf("Options") }
    val menuOptions = listOf("Help/Support", "Rating/Review")

    Box(
        modifier = Modifier.fillMaxSize()
    ) {
        Image(
            painter = painterResource(id = R.drawable.background),
            contentDescription = null,
            contentScale = ContentScale.Crop,
            modifier = Modifier.fillMaxSize()
        )

        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(16.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.SpaceBetween
        ) {

            Spacer(modifier = Modifier.height(40.dp))
            ExposedDropdownMenuBox(
                expanded = expanded,
                onExpandedChange = { expanded = !expanded }
            ) {
                OutlinedTextField(
                    value = selectedOption,
                    onValueChange = { },
                    readOnly = true,
                    label = { Text("Menu", color = Color.White) },
                    modifier = Modifier
                        .menuAnchor(),
                    colors = TextFieldDefaults.outlinedTextFieldColors(
                        containerColor = Color.Transparent,
                        focusedTextColor = Color.White,
                        unfocusedLabelColor = Color.White,
                    )
                )

                DropdownMenu(
                    expanded = expanded,
                    onDismissRequest = { expanded = false }
                ) {
                    menuOptions.forEach { option ->
                        androidx.compose.material3.DropdownMenuItem(
                            text = { Text(option) },
                            onClick = {
                                selectedOption = option
                                expanded = false
                                when (option) {
                                    "Help/Support" -> { navController.navigate(Screen.HelpSupport.route) }
                                    "Rating/Review" -> { navController.navigate(Screen.RatingReviewScreen.route)}
                                    "Logout" -> { /* Logout Logic here maybe? */ }
                                }
                            }
                        )
                    }
                }
            }

            Spacer(modifier = Modifier.height(16.dp))

            Text(text = "Welcome to the Home Page!", style = MaterialTheme.typography.headlineSmall)

            Spacer(modifier = Modifier.height(16.dp))

            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceEvenly
            ) {
                TextButton(onClick = { navController.navigate(Screen.PriceAlert.route) },
                    colors = ButtonDefaults.textButtonColors(contentColor = Color.White)) {
                    Text("Price Alert")
                }

                TextButton(onClick = { navController.navigate(Screen.Payment.route) },
                    colors = ButtonDefaults.textButtonColors(contentColor = Color.White)) {
                    Text("Payment")
                }

                TextButton(onClick = { navController.navigate(Screen.PurchaseAssets.route) },
                    colors = ButtonDefaults.textButtonColors(contentColor = Color.White)) {
                    Text("Purchase")
                }
            }
        }
    }
}



@Composable
fun PaymentScreen() {
    Box(
        modifier = Modifier.fillMaxSize()
    ) {
        Image(
            painter = painterResource(id = R.drawable.background),
            contentDescription = null,
            contentScale = ContentScale.Crop,
            modifier = Modifier.fillMaxSize()
        )


        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(16.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Bottom
        ) {
            Text(
                text = "This is the Payment screen",
                style = MaterialTheme.typography.headlineSmall,
            )

            Spacer(modifier = Modifier.height(32.dp))

            TextButton(onClick = { /* Pop Up Screen with Payement*/  }) {
                Text("Proceed to Payment")
            }
        }
    }
}


@Composable
fun RatingReviewScreen(navController: NavController) {
    var rating by remember { mutableStateOf("") }
    var review by remember { mutableStateOf("") }
    var submittedMessage by remember { mutableStateOf("") }
    var errorMessage by remember { mutableStateOf("") }

    Box(modifier = Modifier.fillMaxSize()) {
        Image(
            painter = painterResource(id = R.drawable.background),
            contentDescription = null,
            contentScale = ContentScale.Crop,
            modifier = Modifier.fillMaxSize()
        )
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(16.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center
        ) {
            Text("Rating & Review", style = MaterialTheme.typography.headlineSmall)

            Spacer(modifier = Modifier.height(16.dp))
            OutlinedTextField(
                value = rating,
                onValueChange = { rating = it },
                label = { Text("Rating (1-5)") },
                modifier = Modifier.fillMaxWidth()
            )

            Spacer(modifier = Modifier.height(8.dp))
            OutlinedTextField(
                value = review,
                onValueChange = { review = it },
                label = { Text("Review") },
                modifier = Modifier
                    .fillMaxWidth()
                    .height(100.dp)
            )
            Spacer(modifier = Modifier.height(16.dp))
            TextButton(onClick = {
                submitReview(rating, review) { success, message ->
                    if (success) {
                        submittedMessage = "Rating: $rating\nReview: $review"
                        errorMessage = ""
                    } else {
                        errorMessage = message ?: "Failed to submit review"
                    }
                }
            }) {
                Text("Submit")
            }

            Spacer(modifier = Modifier.height(16.dp))
            if (submittedMessage.isNotEmpty()) {
                Text(submittedMessage)
                Spacer(modifier = Modifier.height(8.dp))
                Button(onClick = { navController.navigate(Screen.Home.route) }) {
                    Text("Back to Home")
                }
            }
            if (errorMessage.isNotEmpty()) {
                Text(errorMessage, color = Color.Red)
            }
        }
    }
}


@Composable
fun PriceAlertScreen() {

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Bottom
    ) {
        Text(text = "Price Alert Settings", style = MaterialTheme.typography.headlineSmall)

        Spacer(modifier = Modifier.height(32.dp))

        TextButton(onClick = { /* Price Alert Logic, take it to a different Screen */ }) {
            Text("Set Price Alerts")
        }
    }
}

@Composable
fun PurchaseAssetsScreen() {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Bottom
    ) {
        Text(text = "Purchase Assets", style = MaterialTheme.typography.headlineSmall)

        Spacer(modifier = Modifier.height(32.dp))

        Button(onClick = { /* maybe different options for payement here like cards and then enter maypement info sned it to firebase but make it secure?*/ }) {
            Text("Purchase Now")
        }
    }
}

// Experimental Features are used, maybe remove later incase it provides an "error"??
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun HelpSupportScreen(navController: NavHostController) {
    var firstName by remember { mutableStateOf("") }
    var lastName by remember { mutableStateOf("") }
    var subject by remember { mutableStateOf("") }
    var message by remember { mutableStateOf("") }

    Box(
        modifier = Modifier.fillMaxSize()
    ) {
        Image(
            painter = painterResource(id = R.drawable.background),
            contentDescription = null,
            contentScale = ContentScale.Crop,
            modifier = Modifier.fillMaxSize()
        )
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(16.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Top
        ) {
            Text(
                text = "Help & Support",
                style = MaterialTheme.typography.headlineSmall.copy(color = Color.White)
            )

            Spacer(modifier = Modifier.height(24.dp))

            OutlinedTextField(
                value = firstName,
                onValueChange = { firstName = it },
                label = { Text("First Name") },
                modifier = Modifier.fillMaxWidth(),
                colors = TextFieldDefaults.outlinedTextFieldColors(
                    focusedTextColor = Color.White,
                    unfocusedTextColor = Color.White,
                )
            )

            Spacer(modifier = Modifier.height(16.dp))

            OutlinedTextField(
                value = lastName,
                onValueChange = { lastName = it },
                label = { Text("Last Name") },
                modifier = Modifier.fillMaxWidth(),
                colors = TextFieldDefaults.outlinedTextFieldColors(
                    focusedTextColor = Color.White,
                    unfocusedTextColor = Color.White,
                )
            )

            Spacer(modifier = Modifier.height(16.dp))

            OutlinedTextField(
                value = subject,
                onValueChange = { subject = it },
                label = { Text("Subject") },
                modifier = Modifier.fillMaxWidth(),
                colors = TextFieldDefaults.outlinedTextFieldColors(
                    focusedTextColor = Color.White,
                    unfocusedTextColor = Color.White,
                )
            )

            Spacer(modifier = Modifier.height(16.dp))

            OutlinedTextField(
                value = message,
                onValueChange = { message = it },
                label = { Text("Message") },
                modifier = Modifier
                    .fillMaxWidth()
                    .height(150.dp),
                colors = TextFieldDefaults.outlinedTextFieldColors(
                    focusedTextColor = Color.White,
                    unfocusedTextColor = Color.White,
                ),
                maxLines = 5,
                visualTransformation = VisualTransformation.None
            )

            Spacer(modifier = Modifier.height(32.dp))

            Button(
                onClick = {
                    ///Handle Ticket here, send to firebase?
                },
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("Send Ticket")
            }

            Spacer(modifier = Modifier.height(16.dp))

            Text(
                text = "For assistance, please contact support at:",
                style = MaterialTheme.typography.bodyLarge.copy(color = Color.White)
            )

            Spacer(modifier = Modifier.height(16.dp))

            Text(
                text = "fixemaillater@gmail.com",
                style = MaterialTheme.typography.bodyMedium.copy(color = MaterialTheme.colorScheme.primary) // Keep this as primary color for visibility
            )

            Spacer(modifier = Modifier.height(32.dp))
            Text(
                text = "Alternatively, you can visit our help center for FAQs and troubleshooting tips.",
                style = MaterialTheme.typography.bodyMedium.copy(color = Color.White)
            )

            Spacer(modifier = Modifier.height(16.dp))

            Text(
                text = "Our support team is available 24/7 to assist you with any issues you may encounter.",
                style = MaterialTheme.typography.bodyMedium.copy(color = Color.White)
            )

            Spacer(modifier = Modifier.height(32.dp))

            Button(onClick = { navController.navigate(Screen.Home.route) }) {
                Text("Back to Home")
            }
        }
    }
}


@Preview(showBackground = true)
@Composable
fun LoginScreenPreview() {
    MyApplicationTheme {
        LoginScreen(navController = rememberNavController())
    }
}

@Preview(showBackground = true)
@Composable
fun RegisterScreenPreview() {
    MyApplicationTheme {
        RegisterScreen(navController = rememberNavController())
    }
}

@Preview(showBackground = true)
@Composable
fun HomeScreenPreview() {
    MyApplicationTheme {
        HomeScreen(navController = rememberNavController())
    }
}

@Preview(showBackground = true)
@Composable
fun PaymentScreenPreview() {
    MyApplicationTheme {
        PaymentScreen()
    }
}

@Preview(showBackground = true)
@Composable
fun PriceAlertScreenPreview() {
    MyApplicationTheme {
        PriceAlertScreen()
    }
}

@Preview(showBackground = true)
@Composable
fun PurchaseAssetsScreenPreview() {
    MyApplicationTheme {
        PurchaseAssetsScreen()
    }
}

@Preview(showBackground = true)
@Composable
fun HelpSupportPreview() {
    MyApplicationTheme {
        HelpSupportScreen(navController = rememberNavController())
    }
}


private fun registerUser(email: String, password: String, onComplete: (Boolean, String?) -> Unit) {
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

private fun loginUser(email: String, password: String, onComplete: (Boolean, String?) -> Unit) {
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

private fun submitReview(rating: String, review: String, onComplete: (Boolean, String?) -> Unit) {
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
