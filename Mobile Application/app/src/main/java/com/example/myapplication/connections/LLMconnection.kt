
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.jakewharton.retrofit2.converter.kotlinx.serialization.asConverterFactory
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.launch
import kotlinx.serialization.Serializable
import kotlinx.serialization.json.Json
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import retrofit2.Retrofit
import retrofit2.http.GET
import retrofit2.http.POST
import retrofit2.http.Query
import retrofit2.http.Body
import java.util.concurrent.TimeUnit


@Serializable
data class Stock(
    val blog: String,
    //val buy_percent: Int,
    //val sell_percent: Int,
    //val funds_dollar: Int
)


object RetrofitInstance {
    private const val BASE_URL = "https://d-yak-presently.ngrok-free.app/"
    private val json = Json { ignoreUnknownKeys = true }

    private val okHttpClient = OkHttpClient.Builder()
        .connectTimeout(1, TimeUnit.MINUTES)  // Connection timeout
        .readTimeout(1, TimeUnit.MINUTES)     // Read timeout
        .writeTimeout(1, TimeUnit.MINUTES)    // Write timeout
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


