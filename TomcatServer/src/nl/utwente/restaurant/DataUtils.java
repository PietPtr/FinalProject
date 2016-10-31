package nl.utwente.restaurant;

import com.google.gson.Gson;

public class DataUtils {

	public static CardSwipe parseCardSwipe(String data) {
		return new Gson().fromJson(data, CardSwipe.class);
	}
}
