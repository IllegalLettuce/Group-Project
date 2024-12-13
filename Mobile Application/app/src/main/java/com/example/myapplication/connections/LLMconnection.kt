
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.jakewharton.retrofit2.converter.kotlinx.serialization.asConverterFactory
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch
import kotlinx.serialization.Serializable
import kotlinx.serialization.json.Json
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import retrofit2.Retrofit
import retrofit2.http.POST
import retrofit2.http.Body
import java.util.concurrent.TimeUnit

@Serializable
data class ManageStockRequest(
    val ticker: String,
    val userId: String,
    val amount: Int,
    val action: String,
)

@Serializable
data class ManageStockResponse(
    val success: Boolean,
    val message: String
)


@Serializable
data class Stock(
    val blog: String,
)


object RetrofitInstance {
    private const val BASE_URL = "https://d-yak-presently.ngrok-free.app/"
    private val json = Json { ignoreUnknownKeys = true }

    private val okHttpClient = OkHttpClient.Builder()
        .connectTimeout(1, TimeUnit.MINUTES)
        .readTimeout(1, TimeUnit.MINUTES)
        .writeTimeout(1, TimeUnit.MINUTES)
        .build()


    val api: StockApiService by lazy {
        Retrofit.Builder()
            .baseUrl(BASE_URL)
            .client(okHttpClient)
            .addConverterFactory(json.asConverterFactory("application/json".toMediaType()))
            .build()
            .create(StockApiService::class.java)
    }
}


interface StockApiService {
    @POST("https://quiet-yak-presently.ngrok-free.app/report")
    suspend fun getStockInfo(
        @Body blog: String
    ): Stock

    @POST("https://quiet-yak-presently.ngrok-free.app/managestock")
    suspend fun manageStock(
        @Body request: ManageStockRequest?
    ): ManageStockResponse
}


class StockViewModel : ViewModel() {
    private val _stock = MutableStateFlow<Stock?>(null)
    val stock = _stock

    fun fetchStock(blog: String) {
        viewModelScope.launch {
            try {
                val response = RetrofitInstance.api.getStockInfo(blog)
                println("Response: $response")
                _stock.value = response
            } catch (e: Exception) {
                e.printStackTrace()
                _stock.value = null
            }
        }
    }
}



class FinancialInfoViewModel : ViewModel() {
    private val _financialInfo = MutableStateFlow<Stock?>(null)
    val financialInfo: StateFlow<Stock?> get() = _financialInfo

    private val _actionStatus = MutableStateFlow<String?>(null)
    val actionStatus: StateFlow<String?> get() = _actionStatus

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

    fun manageStock(ticker: String, userId: String, amount: Int?, action: String,) {
        viewModelScope.launch {
            try {
                val request = amount?.let {
                    ManageStockRequest(
                            ticker = ticker,
                            userId = userId,
                            amount = it,
                            action = action,
                        )
                    }
                val response = RetrofitInstance.api.manageStock(request)
                if (response.success) {
                    println("Stock action successful: ${response.message}")
                } else {
                    println("Stock action failed: ${response.message}")
                }
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
    }
}

