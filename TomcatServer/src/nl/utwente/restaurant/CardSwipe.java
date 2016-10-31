package nl.utwente.restaurant;

public class CardSwipe {

	private String	originName;
	private int		cardId;
	private String	cardData;

	public synchronized String getOriginName() {
		return originName;
	}

	public synchronized int getCardId() {
		return cardId;
	}

	public synchronized String getCardData() {
		return cardData;
	}

}
