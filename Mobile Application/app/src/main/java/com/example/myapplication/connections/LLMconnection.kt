import android.content.Context
import com.android.volley.Request
import com.android.volley.RequestQueue
import com.android.volley.toolbox.StringRequest
import com.android.volley.toolbox.Volley

fun connection(context: Context) {
    val apiSample = "https://quiet-yak-presently.ngrok-free.app/"

    val myRequestQueue: RequestQueue = Volley.newRequestQueue(context)

    val myStringRequest = object : StringRequest(Request.Method.POST, apiSample,
        { response ->
            println("Response: $response")
        },
        { error ->
            error.printStackTrace()
            println("Error: ${error.message}")
        }) {
        override fun getBody(): ByteArray {
            val jsonBody = """
                {
                    "company":
                }
            """.trimIndent()
            return jsonBody.toByteArray(Charsets.UTF_8)
        }

        override fun getBodyContentType(): String {
            return "application/json; charset=utf-8"
        }
    }
    myRequestQueue.add(myStringRequest)
}


fun fetchData() {
    //TO DO

}