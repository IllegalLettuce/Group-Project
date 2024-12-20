package com.example.myapplication.navigation
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.example.myapplication.screens.HelpSupportScreen
import com.example.myapplication.screens.HomeScreen
import com.example.myapplication.screens.LoginScreen
import com.example.myapplication.screens.PriceAlertScreen
import com.example.myapplication.screens.PurchaseAssetsScreen
import com.example.myapplication.screens.PurchasePremiumFunctionality
import com.example.myapplication.screens.RegisterScreen
import com.example.myapplication.screens.RatingReviewScreen

sealed class Screen(val route: String) {
    object Login : Screen("login")
    object Register : Screen("register")
    object Home : Screen("home")
    object PurchaseAssets : Screen("purchase_assets")
    object PriceAlert : Screen("price_alert")
    object HelpSupport : Screen("help_support")
    object RatingReviewScreen : Screen("rating_review")
    object PurchasePremiumFunctionality : Screen("purchase_premium")
}

data class NavItem(
    var label: String, val icon: ImageVector, val screen: Screen
)


@Composable
fun NavGraph() {
    val navController = rememberNavController()

    NavHost(navController = navController, startDestination = Screen.Login.route) {
        composable(Screen.Login.route) { LoginScreen(navController) }
        composable(Screen.Register.route) { RegisterScreen(navController) }
        composable(Screen.Home.route) { HomeScreen(navController) }
        composable(Screen.PurchaseAssets.route) { PurchaseAssetsScreen() }
        composable(Screen.PriceAlert.route) { PriceAlertScreen() }
        composable(Screen.HelpSupport.route) { HelpSupportScreen(navController) }
        composable(Screen.RatingReviewScreen.route) { RatingReviewScreen(navController) }
        composable(Screen.PurchasePremiumFunctionality.route) {
            PurchasePremiumFunctionality(navController = navController)
        }

    }
}
