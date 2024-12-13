package com.example.myapplication.screens

import FinancialInfoViewModel
import android.util.Log
import androidx.compose.foundation.Image
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import com.example.myapplication.R
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.myapplication.database.getCurrentUserId


data class Stock(val name: String, val ticker: String)

@Composable
fun PurchaseAssetsScreen(viewModel: FinancialInfoViewModel = viewModel()) {

    val userId = getCurrentUserId()
    val stocks = listOf(
        Stock(name = "Lockheed Martin", ticker = "NYSE:LMT"),
        Stock(name = "General Dynamics", ticker = "NYSE:GD"),
        Stock(name = "Northrop Grumman", ticker = "NYSE:NOC"),
        Stock(name = "RTX", ticker = "NYSE:RTX"),
        Stock(name = "Boeing", ticker = "NYSE:BA"),
        Stock(name = "L3Harris", ticker = "NYSE:LHX"),
        Stock(name = "Rheinmetall", ticker = "ETR:RHM"),
        Stock(name = "SAAB", ticker = "STO:SAAB-B"),
        Stock(name = "Hensoldt", ticker = "ETR:HAG"),
        Stock(name = "Leonardo", ticker = "BIT:LDO")
    )

    var showInfoDialog by remember { mutableStateOf(false) }
    var showPurchaseDialog by remember { mutableStateOf(false) }
    var selectedStock by remember { mutableStateOf<Stock?>(null) }
    var showSellDialog by remember { mutableStateOf(false) }
    var showPriceDialog by remember { mutableStateOf(false)}

    Box(
        modifier = Modifier.fillMaxSize()
    ) {
        Image(
            painter = painterResource(id = R.drawable.background),
            contentDescription = null,
            modifier = Modifier.fillMaxSize(),
            contentScale = ContentScale.Crop
        )

        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(16.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Top
        ) {
            Text(
                text = "Purchase Assets",
                style = MaterialTheme.typography.headlineSmall
            )

            Spacer(modifier = Modifier.height(16.dp))

            LazyColumn(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(vertical = 8.dp),
                verticalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                items(stocks) { stock ->
                    StockCard(
                        stock = stock,
                        onInformationClick = {
                            selectedStock = stock
                            showInfoDialog = true
                        },
                        onPurchaseClick = {
                            selectedStock = stock
                            showPurchaseDialog = true
                        },
                        onSellClick = {
                            selectedStock = stock
                            showSellDialog = true
                        },
                        onPriceClick = {
                            selectedStock = stock
                            showPriceDialog = true
                        }
                    )
                }
            }
        }

        if (showInfoDialog) {
            FinancialInfoDialog(
                stock = selectedStock,
                viewModel = viewModel,
                onDismiss = { showInfoDialog = false }
            )
        }

        if (showPurchaseDialog) {
            selectedStock?.let {
                if (userId != null) {
                    PurchaseDialog(
                        stock = it,
                        userId = userId,
                        viewModel = viewModel,
                        onDismiss = { showPurchaseDialog = false }
                    )
                }
            }
        }
        if (showSellDialog) {
            selectedStock?.let {
                if (userId != null) {
                    SellDialogue(
                        stock = it,
                        userId = userId,
                        viewModel = viewModel,
                        onDismiss = { showSellDialog = false }
                    )
                }
            }
        }
        if (showPriceDialog) {
            selectedStock?.let {
                if (userId != null) {
                    PriceDialogue(
                        stock = it,
                        userId = userId,
                        viewModel = viewModel,
                        onDismiss = { showPriceDialog = false }
                    )
                }
            }
        }
    }
}


@Composable
fun StockCard(stock: Stock, onInformationClick: () -> Unit, onPurchaseClick: (Stock) -> Unit, onSellClick: (Stock) -> Unit,onPriceClick: (Stock) -> Unit ) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 8.dp),
        elevation = CardDefaults.cardElevation(8.dp)
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp)
        ) {
            Text(
                text = stock.name,
                style = MaterialTheme.typography.titleMedium
            )
            Text(
                text = "Ticker: ${stock.ticker}",
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )

            Spacer(modifier = Modifier.height(8.dp))
            Row {
                TextButton(
                    onClick = { onPurchaseClick(stock) },
                ) {
                    Text("Purchase")
                }
                TextButton(
                    onClick = onInformationClick,
                ) {
                    Text("Information")
                }
                TextButton(
                    onClick = {onSellClick(stock)},
                ) {
                    Text("Sell")
                }
                TextButton(
                    onClick = {onPriceClick(stock)},
                ) {
                    Text("Alert")
                }
            }
        }
    }
}

@Composable
fun FinancialInfoDialog(
    stock: Stock?,
    viewModel: FinancialInfoViewModel,
    onDismiss: () -> Unit
) {
    val financialInfo = viewModel.financialInfo.collectAsState()
    val isLoading = viewModel.isLoading.collectAsState()

    LaunchedEffect(stock) {
        stock?.let {
            viewModel.fetchFinancialData(it.name)
        }
    }

    AlertDialog(
        onDismissRequest = onDismiss,
        title = {
            Text(text = "Financial Information")
        },
        text = {
            if (isLoading.value) {
                CircularProgressIndicator()
            } else {
                financialInfo.value?.let { info ->
                    Column {
                        Text(text = "Company: ${info.blog}")
                    }
                } ?: Text(text = "Unable to fetch financial data.")
            }
        },
        confirmButton = {
            TextButton(onClick = onDismiss) {
                Text("Close")
            }
        }
    )
}

@Composable
fun PurchaseDialog(
    stock: Stock,
    userId: String,
    viewModel: FinancialInfoViewModel,
    onDismiss: () -> Unit
) {
    var amount by remember { mutableStateOf("") }
    val isAmountValid = amount.toIntOrNull() != null && amount.toInt() > 0

    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text(text = "Purchase ${stock.name}") },
        text = {
            Column {
                Text("Enter the amount of shares:")
                OutlinedTextField(
                    value = amount,
                    onValueChange = { amount = it },
                    label = { Text("Amount") },
                    isError = !isAmountValid && amount.isNotEmpty(),
                    modifier = Modifier.fillMaxWidth(),
                    keyboardOptions = KeyboardOptions.Default.copy(keyboardType = KeyboardType.Number)
                )
                if (!isAmountValid && amount.isNotEmpty()) {
                    Text(
                        text = "Please enter a valid positive number.",
                        color = MaterialTheme.colorScheme.error
                    )
                }
            }
        },
        confirmButton = {
            TextButton(
                onClick = {
                    if (isAmountValid) {
                        viewModel.manageStock(
                            ticker = stock.ticker,
                            userId = userId,
                            amount = amount.toInt(),
                            action = "buy"
                        )
                        onDismiss()

                    }
                },
                enabled = isAmountValid
            ) {
                Text("Confirm")
            }
        },
        dismissButton = {
            TextButton(onClick = onDismiss) {
                Text("Cancel")
            }
        }
    )
}

@Composable
fun SellDialogue(
    stock: Stock,
    userId: String,
    viewModel: FinancialInfoViewModel,
    onDismiss: () -> Unit
) {
    var amount by remember { mutableStateOf("") }
    val isAmountValid = amount.toIntOrNull() != null && amount.toInt() > 0

    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text(text = "Sell ${stock.name}") },
        text = {
            Column {
                Text("Enter the amount of shares:")
                OutlinedTextField(
                    value = amount,
                    onValueChange = { amount = it },
                    label = { Text("Amount") },
                    isError = !isAmountValid && amount.isNotEmpty(),
                    modifier = Modifier.fillMaxWidth(),
                    keyboardOptions = KeyboardOptions.Default.copy(keyboardType = KeyboardType.Number)
                )
                if (!isAmountValid && amount.isNotEmpty()) {
                    Text(
                        text = "Please enter a valid positive number.",
                        color = MaterialTheme.colorScheme.error
                    )
                }
            }
        },
        confirmButton = {
            TextButton(
                onClick = {
                    if (isAmountValid) {
                        viewModel.manageStock(
                            ticker = stock.ticker,
                            userId = userId,
                            amount = amount.toInt(),
                            action = "sell",
                        )
                        onDismiss()
                    }
                },
                enabled = isAmountValid
            ) {
                Text("Confirm")
            }
        },
        dismissButton = {
            TextButton(onClick = onDismiss) {
                Text("Cancel")
            }
        }
    )
}

@Composable
fun PriceDialogue(
    stock: Stock,
    userId: String,
    viewModel: FinancialInfoViewModel,
    onDismiss: () -> Unit
) {
    var price by remember { mutableStateOf("") }
    val isPriceValid = price.toIntOrNull() != null && price.toInt() > 0

    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text(text = "Sell ${stock.name}") },
        text = {
            Column {
                Text("Enter the amount of shares:")
                OutlinedTextField(
                    value = price,
                    onValueChange = { price = it },
                    label = { Text("Price") },
                    isError = !isPriceValid && price.isNotEmpty(),
                    modifier = Modifier.fillMaxWidth(),
                    keyboardOptions = KeyboardOptions.Default.copy(keyboardType = KeyboardType.Number)
                )
                if (!isPriceValid && price.isNotEmpty()) {
                    Text(
                        text = "Please enter a valid positive number.",
                        color = MaterialTheme.colorScheme.error
                    )
                }
            }
        },
        confirmButton = {
            TextButton(
                onClick = {
                    if (isPriceValid) {
                        viewModel.manageStock(
                            ticker = stock.ticker,
                            userId = userId,
                            action = "Alert",
                            amount = null
                        )
                        onDismiss()
                    }
                },
                enabled = isPriceValid
            ) {
                Text("Confirm")
            }
        },
        dismissButton = {
            TextButton(onClick = onDismiss) {
                Text("Cancel")
            }
        }
    )
}





