package com.example.myapplication

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
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
import androidx.compose.runtime.*
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.ui.Modifier
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.example.myapplication.navigation.NavItem
import com.example.myapplication.navigation.Screen
import com.example.myapplication.screens.HelpSupportScreen
import com.example.myapplication.screens.HomeScreen
import com.example.myapplication.screens.LoginScreen
import com.example.myapplication.screens.PriceAlertScreen
import com.example.myapplication.screens.PurchaseAssetsScreen
import com.example.myapplication.screens.RatingReviewScreen
import com.example.myapplication.screens.PurchasePremiumFunctionality
import com.example.myapplication.screens.RegisterScreen
import com.example.myapplication.ui.theme.MyApplicationTheme
import com.google.firebase.FirebaseApp
import android.content.Context



class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        FirebaseApp.initializeApp(this)
        setUserLoggedIn(this, false)


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
    val startDestination = if (isUserLoggedIn(navController.context)) Screen.Home.route else Screen.Login.route
    var selectedIndex by rememberSaveable { mutableStateOf(0) }
    val userId = getUserId(navController.context)
    val currentRoute = navController.currentBackStackEntryFlow.collectAsState(initial = navController.currentBackStackEntry).value?.destination?.route
    val navItemList = listOf(
        NavItem(label = "Home", icon = Icons.Default.Home, screen = Screen.Home),
        NavItem(label = "Help", icon = Icons.Default.Person, screen = Screen.HelpSupport),
        NavItem(label = "Stocks", icon = Icons.Default.ShoppingCart, screen = Screen.PurchaseAssets)
    )

    Scaffold(
        modifier = Modifier.fillMaxSize(),
        bottomBar = {
            if (currentRoute != Screen.Login.route && currentRoute != Screen.Register.route) {
                BottomAppBar {
                    NavigationBar {
                        navItemList.forEachIndexed { index, item ->
                            NavigationBarItem(
                                selected = selectedIndex == index,
                                onClick = {
                                    selectedIndex = index
                                    if (navController.currentDestination?.route != item.screen.route) {
                                        navController.navigate(item.screen.route) {
                                            launchSingleTop = true
                                            restoreState = true
                                        }
                                    }
                                },
                                icon = { Icon(imageVector = item.icon, contentDescription = item.label) },
                                label = { Text(text = item.label) }
                            )
                        }
                    }
                }
            }
        }
    ) { innerPadding ->

        NavHost(
            navController = navController,
            startDestination = startDestination,
            modifier = Modifier.padding(innerPadding)
        ) {
            composable(Screen.Login.route) { LoginScreen(navController) }
            composable(Screen.Register.route) { RegisterScreen(navController) }
            composable(Screen.Home.route) { HomeScreen(navController) }
            composable(Screen.PriceAlert.route) { PriceAlertScreen() }
            composable(Screen.PurchaseAssets.route) { PurchaseAssetsScreen() }
            composable(Screen.HelpSupport.route) { HelpSupportScreen(navController) }
            composable(Screen.RatingReviewScreen.route) { RatingReviewScreen(navController) }
            composable(Screen.PurchasePremiumFunctionality.route) { PurchasePremiumFunctionality(navController) }
        }
    }
}

fun getUserId(context: Context): String? {
    val sharedPref = context.getSharedPreferences("user_prefs", Context.MODE_PRIVATE)
    return sharedPref.getString("user_id", null)
}


fun isUserLoggedIn(context: Context): Boolean {
    val sharedPref = context.getSharedPreferences("user_prefs", Context.MODE_PRIVATE)
    return sharedPref.getBoolean("is_logged_in", false)
}

fun setUserLoggedIn(context: Context, isLoggedIn: Boolean) {
    val sharedPref = context.getSharedPreferences("user_prefs", Context.MODE_PRIVATE)
    with(sharedPref.edit()) {
        putBoolean("is_logged_in", isLoggedIn)
        apply()
    }
}
