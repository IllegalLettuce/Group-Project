package com.example.myapplication.screens

import android.util.Log
import androidx.compose.foundation.Image
import androidx.compose.foundation.layout.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Notifications
import androidx.compose.material.icons.filled.Star
import androidx.compose.material3.DropdownMenu
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.ExposedDropdownMenuBox
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.runtime.*
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
fun HomeScreen(navController: NavHostController, modifier: Modifier = Modifier) {
    var expanded by remember { mutableStateOf(false) }
    var selectedOption by remember { mutableStateOf("Options") }
    val menuOptions = listOf("Rating", "Premium")

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
            ExposedDropdownMenuBox(
                expanded = expanded,
                onExpandedChange = { expanded = !expanded },
            ) {
                OutlinedTextField(
                    value = selectedOption,
                    onValueChange = { },
                    readOnly = true,
                    label = { Text("Menu", color = Color.White) },
                    modifier = Modifier.menuAnchor(),
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
                                    "Rating" -> {
                                        navController.navigate(Screen.RatingReviewScreen.route)
                                    }

                                    "Premium" -> {
                                        navController.navigate(Screen.PurchasePremiumFunctionality.route)
                                    }
                                }
                            }
                        )
                    }
                }
            }

            Spacer(modifier = Modifier.height(16.dp))

            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceEvenly
            ) {

            }

            Spacer(modifier = Modifier.height(16.dp))

            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceEvenly
            ) {
                Column(
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    IconButton(onClick = { navController.navigate(Screen.PriceAlert.route) }) {
                        Icon(
                            imageVector = Icons.Filled.Notifications,
                            contentDescription = "Alert",
                            tint = Color.White,
                            modifier = Modifier.size(48.dp)
                        )
                    }
                    Text(
                        text = "Alert",
                        color = Color.White,
                        modifier = Modifier.padding(top = 8.dp)
                    )
                }
            }
        }
    }
}
