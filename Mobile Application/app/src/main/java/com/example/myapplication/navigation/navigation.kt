package com.example.myapplication.navigation

import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.filled.Person
import androidx.compose.material.icons.filled.ShoppingCart
import androidx.compose.material3.BottomAppBar
import androidx.compose.material3.Icon
import androidx.compose.material3.NavigationBar
import androidx.compose.material3.NavigationBarItem
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.example.myapplication.screens.HelpSupportScreen
import com.example.myapplication.screens.HomeScreen
import com.example.myapplication.screens.LLMPredictionScreen
import com.example.myapplication.screens.LoginScreen
import com.example.myapplication.screens.PaymentScreen
import com.example.myapplication.screens.PriceAlertScreen
import com.example.myapplication.screens.PurchaseAssetsScreen
import com.example.myapplication.screens.PurchasePremiumFunctionality
import com.example.myapplication.screens.RegisterScreen
import com.example.myapplication.screens.RatingReviewScreen
import com.example.myapplication.screens.ViewFinancialInformationScreen

sealed class Screen(val route: String) {
    object Login : Screen("login")
    object Register : Screen("register")
    object Home : Screen("home")
    object PurchaseAssets : Screen("purchase_assets")
    object Payment : Screen("payment")
    object PriceAlert : Screen("price_alert")
    object HelpSupport : Screen("help_support")
    object RatingReviewScreen : Screen("rating_review")
    object PurchasePremiumFunctionality : Screen("purchase_premium")
    object LLMPredictionScreen : Screen("prediction_screen")
    object ViewFinancialInformationScreen : Screen("financial_information")
}

data class NavItem(
    var label: String,
    val icon: ImageVector,
    val screen: Screen
)


@Composable
fun NavGraph() {
    val navController = rememberNavController()

    NavHost(navController = navController, startDestination = Screen.Login.route) {
        composable(Screen.Login.route) { LoginScreen(navController) }
        composable(Screen.Register.route) { RegisterScreen(navController) }
        composable(Screen.Home.route) { HomeScreen(navController) }
        composable(Screen.PurchaseAssets.route) { PurchaseAssetsScreen() }
        composable(Screen.Payment.route) { PaymentScreen() }
        composable(Screen.PriceAlert.route) { PriceAlertScreen() }
        composable(Screen.HelpSupport.route) { HelpSupportScreen(navController) }
        composable(Screen.RatingReviewScreen.route) { RatingReviewScreen(navController) }
        composable(Screen.PurchasePremiumFunctionality.route) {
            PurchasePremiumFunctionality(navController = navController)
        }
        composable(Screen.LLMPredictionScreen.route) { LLMPredictionScreen() }
        composable(Screen.ViewFinancialInformationScreen.route) { ViewFinancialInformationScreen() }

    }
}
