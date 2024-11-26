package com.example.myapplication.screens

import androidx.compose.foundation.Image
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.Button
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.unit.dp
import com.example.myapplication.R

data class Stock(val name: String, val ticker: String)

@Composable
fun PurchaseAssetsScreen() {
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

    Box(
        modifier = Modifier
            .fillMaxSize()
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
                modifier = Modifier.fillMaxWidth(),
                verticalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                items(stocks) { stock ->
                    StockItem(stock = stock)
                }
            }
        }
    }
}

@Composable
fun StockItem(stock: Stock) {
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text(
            text = "${stock.name} (${stock.ticker})",
            style = MaterialTheme.typography.bodyLarge
        )
        Spacer(modifier = Modifier.height(8.dp))
        Button(
            onClick = {
                // Implement purchase logic here
            }
        ) {
            Text("Purchase ${stock.name}")
        }
    }
}
