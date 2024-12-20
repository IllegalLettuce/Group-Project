package com.example.myapplication.screens

import androidx.compose.foundation.Image
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.Card
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.unit.dp
import com.example.myapplication.R
import com.example.myapplication.database.PriceAlert
import com.example.myapplication.database.getPriceAlerts


@Composable
fun PriceAlertScreen() {
    var priceAlerts by remember { mutableStateOf<List<PriceAlert>>(emptyList()) }
    LaunchedEffect(Unit) {
        getPriceAlerts { alerts ->
            priceAlerts = alerts
        }
    }
    Box(
        modifier = Modifier.fillMaxSize()
    ) {
        Image(
            painter = painterResource(id = R.drawable.background),
            contentDescription = null,
            contentScale = ContentScale.Crop,
            modifier = Modifier.fillMaxSize()
        )

        LazyColumn(
            modifier = Modifier.fillMaxSize().padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            items(priceAlerts) { alert ->
                PriceAlertCard(alert)
            }
        }
    }
}

@Composable
fun PriceAlertCard(alert: PriceAlert) {
    Card(
        modifier = Modifier.fillMaxWidth(),
    ) {
        Column(
            modifier = Modifier.padding(16.dp)
        ) {
            Text(
                text = "Ticker: ${alert.ticker}",
                style = MaterialTheme.typography.bodyLarge
            )
            Text(
                text = "Name: ${alert.name}",
                style = MaterialTheme.typography.bodyMedium
            )
            Text(
                text = "Change: ${alert.change}",
                style = MaterialTheme.typography.bodySmall
            )
        }
    }
}
