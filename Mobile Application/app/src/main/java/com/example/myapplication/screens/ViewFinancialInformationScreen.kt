package com.example.myapplication.screens
import Stock
import androidx.compose.foundation.Image
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.unit.dp
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.myapplication.R
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

@Composable
fun ViewFinancialInformationScreen(
    viewModel: FinancialInfoViewModel = viewModel(),
    query: String = "Amazon"
) {
    val financialInfo = viewModel.financialInfo.collectAsState()
    val isLoading = viewModel.isLoading.collectAsState()

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
            verticalArrangement = Arrangement.Center
        ) {
            Text(
                text = "Financial Information",
                style = MaterialTheme.typography.headlineSmall,
                modifier = Modifier.padding(bottom = 16.dp)
            )

            Button(
                onClick = { viewModel.fetchFinancialData(query) },
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 32.dp)
            ) {
                Text("get Data")
            }

            Spacer(modifier = Modifier.height(24.dp))

            if (isLoading.value) {
                CircularProgressIndicator()
            } else {
                financialInfo.value?.let { info ->
                    Card(
                        modifier = Modifier.fillMaxWidth(),
                        elevation = CardDefaults.cardElevation(defaultElevation = 8.dp),
                        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface)
                    ) {
                        Column(
                            modifier = Modifier.padding(16.dp),
                            horizontalAlignment = Alignment.Start,
                            verticalArrangement = Arrangement.spacedBy(8.dp)
                        ) {
                            Text(
                                text = "Company: ${info.blog}",
                                style = MaterialTheme.typography.bodyLarge,
                                color = MaterialTheme.colorScheme.onSurface
                            )
//                            Text(
//                                text = "Buy Percent: ${info.buy_percent}%",
//                                style = MaterialTheme.typography.bodyLarge,
//                                color = MaterialTheme.colorScheme.onSurface
//                            )
//                            Text(
//                                text = "Sell Percent: ${info.sell_percent}%",
//                                style = MaterialTheme.typography.bodyLarge,
//                                color = MaterialTheme.colorScheme.onSurface
//                            )
//                            Text(
//                                text = "Funds: \$${info.funds_dollar}",
//                                style = MaterialTheme.typography.bodyLarge,
//                                color = MaterialTheme.colorScheme.primary
//                            )
                            Button(
                                onClick = { viewModel.purchaseStock(info)
                                          },
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .padding(top = 8.dp)
                            ) {
                                Text("Purchase")
                            }
                        }
                    }
                }
            }
        }
    }
}

class FinancialInfoViewModel : ViewModel() {
    private val _financialInfo = MutableStateFlow<Stock?>(null)
    val financialInfo: StateFlow<Stock?> get() = _financialInfo

    private val _isLoading = MutableStateFlow(false)
    val isLoading: StateFlow<Boolean> get() = _isLoading

    fun fetchFinancialData(query: String) {
        _isLoading.value = true
        viewModelScope.launch {
            try {
                val response = RetrofitInstance.api.getStockInfo(query)
                _financialInfo.value = response
            } catch (e: Exception) {
                e.printStackTrace()
                _financialInfo.value = null
            } finally {
                _isLoading.value = false
            }
        }
    }
    fun purchaseStock(stock: Stock) {
        viewModelScope.launch {
            try {
                println("Purchased stock: ${stock.blog}")
//                println("Purchased stock: ${stock.buy_percent}")
//                println("Purchased stock: ${stock.sell_percent}")
//                println("Purchased stock: ${stock.funds_dollar}")
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
    }
}
