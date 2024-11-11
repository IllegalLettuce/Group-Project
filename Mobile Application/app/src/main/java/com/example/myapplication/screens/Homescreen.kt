package com.example.myapplication.screens

import androidx.compose.foundation.Image
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.DropdownMenu
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.ExposedDropdownMenuBox
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.material3.TextFieldDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.unit.dp
import androidx.navigation.NavHostController
import com.example.myapplication.R
import com.example.myapplication.navigation.Screen

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun HomeScreen(navController: NavHostController) {
    var expanded by remember { mutableStateOf(false) }
    var selectedOption by remember { mutableStateOf("Options") }
    val menuOptions = listOf("Help/Support", "Rating/Review","PurchasePremium")

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
                                    "PurchasePremium" -> { navController.navigate(Screen.PurchasePremiumFunctionality.route)}
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