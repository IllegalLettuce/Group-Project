
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.jakewharton.retrofit2.converter.kotlinx.serialization.asConverterFactory
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.launch
import kotlinx.serialization.Serializable
import kotlinx.serialization.json.Json
import okhttp3.MediaType.Companion.toMediaType
import retrofit2.Retrofit
import retrofit2.http.GET
import retrofit2.http.Query


@Serializable
data class Stock(
    val company: String,
    val buy_percent: Int,
    val sell_percent: Int,
    val funds_dollar: Int
)


object RetrofitInstance {
    private const val BASE_URL = "https://d-yak-presently.ngrok-free.app/"
    private val json = Json { ignoreUnknownKeys = true }

    val api: StockApiService by lazy {
        Retrofit.Builder()
            .baseUrl(BASE_URL)
            .addConverterFactory(json.asConverterFactory("application/json".toMediaType()))
            .build()
            .create(StockApiService::class.java)
    }
}


interface StockApiService {
    @GET("https://quiet-yak-presently.ngrok-free.app/manages")
    suspend fun getStockInfo(
        @Query("q") query: String
    ): Stock
}


class StockViewModel : ViewModel() {
    private val _stock = MutableStateFlow<Stock?>(null)
    val stock = _stock

    fun fetchStock(query: String) {
        viewModelScope.launch {
            try {
                val response = RetrofitInstance.api.getStockInfo(query)
                println("Response: $response")
                _stock.value = response
            } catch (e: Exception) {
                e.printStackTrace()
                _stock.value = null
            }
        }
    }
}


