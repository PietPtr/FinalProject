package nl.utwente.restaurant;

import java.io.BufferedReader;
import java.io.IOException;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

/**
 * Servlet implementation class PythonReceiver
 */
@WebServlet("/PythonReceiver")
public class PythonReceiver extends HttpServlet {

	private static final long serialVersionUID = 1L;

	/**
	 * @see HttpServlet#HttpServlet()
	 */
	public PythonReceiver() {
		super();
		// TODO Auto-generated constructor stub
	}

	/**
	 * @see HttpServlet#doPost(HttpServletRequest request, HttpServletResponse
	 *      response)
	 */
	protected void doPost(	HttpServletRequest request,
							HttpServletResponse response) throws ServletException, IOException {
		System.out.println("Got POST!");
		BufferedReader br = request.getReader();
		if (br.ready()) {
			CardSwipe swipe = null;
			try {
				swipe = DataUtils.parseCardSwipe(br.readLine());
			} catch (Exception e) {
				e.printStackTrace();
			}
			System.out.println(swipe.getCardId());
		}
	}

	protected void doGet(	HttpServletRequest request,
							HttpServletResponse response) throws ServletException, IOException {
		System.out.println("Got GET!");
	}

}
