package com.example.myapplication

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.runtime.*
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.example.myapplication.navigation.Screen
import com.example.myapplication.screens.HelpSupportScreen
import com.example.myapplication.screens.HomeScreen
import com.example.myapplication.screens.LoginScreen
import com.example.myapplication.screens.PaymentScreen
import com.example.myapplication.screens.PriceAlertScreen
import com.example.myapplication.screens.PurchaseAssetsScreen
import com.example.myapplication.screens.RatingReviewScreen
import com.example.myapplication.screens.PurchasePremiumFunctionality
import com.example.myapplication.screens.RegisterScreen
import com.example.myapplication.ui.theme.MyApplicationTheme
import com.google.firebase.FirebaseApp

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
        composable(Screen.PurchasePremiumFunctionality.route) { PurchasePremiumFunctionality(navController) }
    }
}

