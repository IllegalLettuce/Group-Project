package com.example.myapplication.screens

import FinancialInfoViewModel
import androidx.compose.foundation.Image
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
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
import androidx.compose.ui.unit.dp
import com.example.myapplication.R
import androidx.lifecycle.viewmodel.compose.viewModel


data class Stock(val name: String, val ticker: String)

@Composable
fun PurchaseAssetsScreen(viewModel: FinancialInfoViewModel = viewModel()) {
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

    var showDialog by remember { mutableStateOf(false) }
    var selectedStock by remember { mutableStateOf<Stock?>(null) }

    Box(
        modifier = Modifier
            .fillMaxSize()
    ) {
        // Background image
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
                            showDialog = true
                        }
                    )
                }
            }
        }

        // Show the dialog if triggered
        if (showDialog) {
            FinancialInfoDialog(
                stock = selectedStock,
                viewModel = viewModel,
                onDismiss = { showDialog = false }
            )
        }
    }
}

@Composable
fun StockCard(stock: Stock, onInformationClick: () -> Unit) {
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
            Row(){

            Button(
                onClick = {
                },
            ) {
                Text("Purchase")
            }
            Button(
                onClick = onInformationClick,
            ) {
                Text("Information")
            }
            Button(
                onClick = {
                },
            ) {
                Text("Sell")
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
                        // Add other financial details here
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

